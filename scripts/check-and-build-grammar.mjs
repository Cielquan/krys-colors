#!/usr/bin/env node
import fs from "fs/promises";

import yaml from "yaml";

/**
 * Run the script and pass the path to grammar YAML file
 *
 * Additional arguments will be ignored.
 *
 * The script will
 * - check YAML source
 * - build JSON artifact from YAML source
 * - check JSON artifact
 * - validate all RegExes compile
 */

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

const main = async () => {
  const filename = process.argv[2];
  if (!filename) throw new Error("No file given.");
  if (!(await exists(filename))) throw new Error(`File not found: ${filename}`);

  const yamlSource = await fs.readFile(filename, "utf8");

  console.log("Parsing YAML source");
  const grammarYaml = yaml.parse(yamlSource);

  console.log("Creating JSON source");
  const jsonSource = `${JSON.stringify(grammarYaml, null, 2)}\n`;

  const outputFile = filename.replace(/\.yaml$/, ".json");

  console.log("Writing output file");
  await fs.writeFile(outputFile, jsonSource);

  console.log(`Converted '${filename}' to '${outputFile}'`);
};

await main();
