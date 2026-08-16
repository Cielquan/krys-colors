#!/usr/bin/env node
/* eslint-disable no-await-in-loop */
import fs from "fs/promises";

import yaml from "yaml";

/**
 * Run the script and pass paths to one or more JSON files.
 *
 * The script will convert JSON to YAML.
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
  const filenames = process.argv.slice(2);

  // eslint-disable-next-line no-restricted-syntax
  for (const filename of filenames) {
    console.log(`File: ${filename}`);
    if (!filename) throw new Error("No file given.");
    if (!(await exists(filename))) throw new Error(`File not found: ${filename}`);

    const jsonSource = await fs.readFile(filename, "utf8");

    console.log("Parsing JSON source");
    const grammarObj = JSON.parse(jsonSource);

    console.log("Creating YAML source");
    const yamlSource = yaml.stringify(grammarObj);

    const outputFile = filename.replace(/\.json$/, ".yaml");

    console.log("Writing output file");
    await fs.writeFile(outputFile, yamlSource);

    console.log(`Converted '${filename}' to '${outputFile}'`);
  }
};

await main();
