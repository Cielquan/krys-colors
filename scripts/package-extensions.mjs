#!/usr/bin/env node
import fs from "fs/promises";
import childProcess from "node:child_process";
import { fileURLToPath } from "node:url";
import util from "node:util";
import path from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const root = path.resolve(__dirname, "..");
const extensionsDir = path.join(root, "extensions");
const distDir = path.join(root, "dist");
const license = path.join(root, "LICENSE");

const execFileAsync = util.promisify(childProcess.execFile);

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
 * @param {string} extensionDir
 */
const buildAndPackageExtension = async (extensionDir) => {
  const extensionName = path.basename(extensionDir);
  const extensionLicense = path.join(extensionDir, "LICENSE");

  console.log(`\nPackaging ${extensionName}...`);

  const packageJson = JSON.parse(
    await fs.readFile(path.join(extensionDir, "package.json"), "utf8"),
  );

  try {
    await fs.copyFile(license, extensionLicense);

    if (packageJson?.scripts?.build) {
      console.log(`Building ${extensionName}...`);

      await execFileAsync("pnpm", ["run", "build"], { cwd: extensionDir });
    }

    await execFileAsync("pnpx", ["vsce", "package", "--out", distDir], { cwd: extensionDir });

    console.log(`✓ ${extensionName} packaged successfully`);
  } catch {
    throw new Error(`✗ Failed to package ${extensionName}`);
  } finally {
    await fs.rm(extensionLicense, { force: true });
  }
};

const main = async () => {
  if (!(await exists(license))) throw new Error(`LICENSE not found: ${license}`);

  if (!(await exists(extensionsDir)))
    throw new Error(`Extensions directory not found: ${extensionsDir}`);

  const entries = await fs.readdir(extensionsDir, { withFileTypes: true });
  const extensions = (
    await Promise.all(
      entries.map(async (entry) => {
        const extensionDir = path.join(extensionsDir, entry.name);
        const packageJson = path.join(extensionDir, "package.json");
        return (await exists(packageJson)) ? extensionDir : null;
      }),
    )
  ).filter((v) => v !== null);

  if (extensions.length === 0) throw new Error("ERROR: No extensions found.");

  console.log(`Found ${extensions.length} extension(s).`);

  await fs.mkdir(distDir, { recursive: true });

  // eslint-disable-next-line no-restricted-syntax
  for (const extensionDir of extensions) {
    // eslint-disable-next-line no-await-in-loop
    await buildAndPackageExtension(extensionDir);
  }

  console.log("\n✓ All extensions packaged successfully.");
  console.log(`  Output: ${distDir}`);
};

await main();
