#!/usr/bin/env node
import fs from "fs/promises";

import { parse } from "jsonc-parser";

/**
 * @param {string[]} filenames
 */
const main = async (filenames) => {
  Promise.all(
    filenames.map(async (filename) => {
      const input = await fs.readFile(filename, "utf8");
      const output = `${JSON.stringify(parse(input), null, 2)}\n`;

      const newFilename = filename.replace(/(\.jsonc)$/, ".json");
      await fs.writeFile(newFilename, output);

      console.log(`Converted ${filename} to ${newFilename}`);
    }),
  );
};

await main(process.argv.slice(2));
