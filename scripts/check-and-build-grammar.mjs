#!/usr/bin/env node
import fs from "fs/promises";
import { fileURLToPath } from "node:url";
import path from "path";

import oniguruma from "vscode-oniguruma";
import textmate from "vscode-textmate";
import yaml from "yaml";

/**
 * Run the script and pass the path to grammar YAML file
 *
 * Additional arguments will be ignored.
 *
 * The script will
 * - parse YAML source
 * - build JSON artifact from YAML source
 * - compile grammar
 * - validate all RegExes compile
 */

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * @param {string} file
 */
const exists = async (file) => {
  try {
    await fs.access(file);
    return true;
  } catch {
    return false;
  }
};

const REGEX_KEYS = new Set(["match", "begin", "end", "while"]);

/**
 *
 * @param {object} obj
 * @param {string} path_
 * @param {{
 *    regex: string,
 *    location: string,
 * }[]} result
 * @returns
 */
const extractRegexesFromGrammarObj = (obj, path_ = "", result = []) => {
  if (!obj || typeof obj !== "object") {
    return result;
  }

  // eslint-disable-next-line no-restricted-syntax
  for (const [key, value] of Object.entries(obj)) {
    const currentPath = path_ !== "" ? `${path_}.${key}` : key;

    if (REGEX_KEYS.has(key) && typeof value === "string") {
      result.push({
        regex: value,
        location: currentPath,
      });
    }

    if (value && typeof value === "object") {
      extractRegexesFromGrammarObj(value, currentPath, result);
    }
  }

  return result;
};

/**
 * @param {string} grammarJsonStr
 * @param {Record<string, unknown>} grammarObj
 */
const checkGrammar = async (grammarJsonStr, grammarObj) => {
  console.log("Starting grammar checks...");

  const wasmBinFile = path.join(__dirname, "../node_modules/vscode-oniguruma/release/onig.wasm");
  if (!(await exists(wasmBinFile))) throw new Error("onig.wasm not found.");

  await oniguruma.loadWASM((await fs.readFile(wasmBinFile)).buffer);

  const vscodeOnigurumaLib = {
    /**
     * @param {string[]} patterns
     */
    createOnigScanner(patterns) {
      return new oniguruma.OnigScanner(patterns);
    },

    /**
     * @param {string} str
     */
    createOnigString(str) {
      return new oniguruma.OnigString(str);
    },
  };

  console.log("Loading grammar");
  const registry = new textmate.Registry({
    onigLib: Promise.resolve(vscodeOnigurumaLib),
    loadGrammar: async () => {
      console.log("Parsing grammar");
      return textmate.parseRawGrammar(grammarJsonStr, ".json");
    },
  });
  const { scopeName } = grammarObj;
  if (typeof scopeName !== "string") throw new Error("Missing grammar scope");
  const grammar = await registry.loadGrammar(scopeName);
  if (!grammar) throw new Error("Missing grammar");

  console.log("Collecting RegExes");
  const regexes = extractRegexesFromGrammarObj(grammarObj);
  console.log(`Found ${regexes.length} RegEx(es)`);

  console.log("Compiling RegExes");
  const errors = regexes
    .map(({ location, regex }) => {
      try {
        vscodeOnigurumaLib.createOnigScanner([regex]);
      } catch (error) {
        const err = error instanceof Error ? error.message : String(error);
        return { regex, location, err };
      }
      return null;
    })
    .filter((v) => v !== null);

  if (errors.length) {
    console.error(`Found ${errors.length} erroneous RegEx(es):`);
    errors.forEach((err) => {
      console.error("---");
      console.error(`Invalid RegEx: ${err.regex}`);
      console.error(`Path: ${err.location}`);
      console.error(`Error: ${err.err}`);
    });
    console.error("--- --- ---");
  }

  console.log("...Finished grammar checks");
};

const main = async () => {
  const filename = process.argv[2];
  if (!filename) throw new Error("No file given.");
  if (!(await exists(filename))) throw new Error(`File not found: ${filename}`);

  const yamlSource = await fs.readFile(filename, "utf8");

  console.log("Parsing YAML source");
  const grammarObj = yaml.parse(yamlSource);

  console.log("Creating JSON source");
  const jsonSource = `${JSON.stringify(grammarObj, null, 2)}\n`;

  const outputFile = filename.replace(/\.yaml$/, ".json");

  console.log("Writing output file");
  await fs.writeFile(outputFile, jsonSource);

  await checkGrammar(jsonSource, grammarObj);

  console.log(`Converted '${filename}' to '${outputFile}'`);
};

await main();
