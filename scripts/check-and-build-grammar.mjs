#!/usr/bin/env node
/* eslint-disable no-await-in-loop */
import fs from "fs/promises";
import { fileURLToPath } from "node:url";
import path from "path";

import oniguruma from "vscode-oniguruma";
import textmate from "vscode-textmate";
import yaml from "yaml";

/**
 * Run the script and pass paths to one or more grammar YAML files or directories.
 *
 * If a directory is passed, all *.tmLanguage.yaml files in that directory
 * and its subdirectories will be processed.
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

/**
 * @param {string} file
 */
const isDirectory = async (file) => {
  try {
    return (await fs.stat(file)).isDirectory();
  } catch {
    return false;
  }
};

/**
 * Recursively find all *.tmLanguage.yaml files in a directory.
 *
 * @param {string} directory
 * @returns {Promise<string[]>}
 */
const findGrammarFiles = async (directory) => {
  const entries = await fs.readdir(directory, { withFileTypes: true });

  const foundFiles = await Promise.all(
    entries.map(async (entry) => {
      const filename = path.join(directory, entry.name);

      if (entry.isDirectory()) {
        return await findGrammarFiles(filename);
      }
      if (entry.isFile() && entry.name.endsWith(".tmLanguage.yaml")) {
        return [filename];
      }
      return [null];
    }),
  );

  return foundFiles.flat().filter((v) => v !== null);
};

const REGEX_KEYS = new Set(["match", "begin", "end", "while"]);

/**
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

  if (!(await exists(wasmBinFile))) {
    throw new Error("onig.wasm not found.");
  }

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

/**
 * @param {string} filename
 */
const processFile = async (filename) => {
  console.log(`\nFile: ${filename}`);

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

const main = async () => {
  const paths = process.argv.slice(2);

  if (paths.length === 0) {
    throw new Error("No files or directories given.");
  }

  const filenames = [];

  // eslint-disable-next-line no-restricted-syntax
  for (const inputPath of paths) {
    if (!(await exists(inputPath))) {
      throw new Error(`File or directory not found: ${inputPath}`);
    }

    if (await isDirectory(inputPath)) {
      filenames.push(...(await findGrammarFiles(inputPath)));
    } else {
      filenames.push(inputPath);
    }
  }

  if (filenames.length === 0) {
    console.log("No *.tmLanguage.yaml files found.");
    return;
  }

  const sortedUniqueFilenames = [...new Set(filenames)].sort();

  console.log(`Found ${sortedUniqueFilenames.length} grammar file(s)`);

  // eslint-disable-next-line no-restricted-syntax
  for (const filename of sortedUniqueFilenames) {
    await processFile(filename);
  }
};

await main();
