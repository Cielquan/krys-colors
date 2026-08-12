#!/usr/bin/env node
import fs from "fs/promises";

import { parse } from "jsonc-parser";

/**
 * Run the script and pass as many file-paths as you want.
 * No validation logic is build in.
 */

const main = async () => {
  const filenames = process.argv.slice(2);

  Promise.all(
    filenames.map(async (filename) => {
      const input = await fs.readFile(filename, "utf8");
      const output = `${JSON.stringify(parse(input), null, 2)}\n`;

      const newFilename = filename.replace(/(\.jsonc)$/, ".json");
      await fs.writeFile(newFilename, output);

      console.log(`Converted '${filename}' to '${newFilename}'`);
    }),
  );
};

await main();
