#!/usr/bin/env node
import fs from "fs/promises";
import childProcess from "node:child_process";
import util from "node:util";
import path from "path";

/**
 * Run the script and
 * - first pass the `ReleaseType` (see below) and
 * - second pass the path to extension directory, e.g. extensions/krys-colors
 *
 * The script will
 * - finalize the Changelog
 * - bump the version in package.json
 * - commit the changes
 * - create a tag
 */

const execFileAsync = util.promisify(childProcess.execFile);

/**
 * @typedef {"patch" | "bugfix" | "minor" | "feature" | "major" | "breaking"} ReleaseType
 */

/**
 * @typedef {{
 *   name: string;
 *   version: string;
 *   repository: { url: string }
 * }} PackageJson
 */

const RELEASE_TYPES = {
  patch: "patch",
  bugfix: "patch",
  minor: "minor",
  feature: "minor",
  major: "major",
  breaking: "major",
};

/**
 * @param {string[]} args
 * @returns {{
 *   releaseType: ReleaseType;
 *   extensionDir: string;
 * }}
 */
const parseArgs = (args) => {
  const [releaseType, extensionDir] = args;

  /**
   * @param {string} value
   * @returns {value is ReleaseType}
   */
  const isReleaseType = (value) => value in RELEASE_TYPES;

  if (!releaseType || !isReleaseType(releaseType)) {
    throw new Error(
      "Usage: release.mjs <patch|bugfix|minor|feature|major|breaking> <extension-dir>",
    );
  }

  if (!extensionDir) {
    throw new Error(
      "Usage: release.mjs <patch|bugfix|minor|feature|major|breaking> <extension-dir>",
    );
  }

  const resolvedExtensionDir = path.resolve(extensionDir);

  return {
    releaseType,
    extensionDir: resolvedExtensionDir,
  };
};

/**
 * @param {string} currentVersion
 * @param {ReleaseType} releaseType
 * @returns {string}
 */
const bumpVersion = (currentVersion, releaseType) => {
  const match = /^v?(\d+)\.(\d+)\.(\d+)$/.exec(currentVersion);

  if (!match) {
    throw new Error(`Unparsable version: ${currentVersion}`);
  }

  const major = Number(match[1]);
  const minor = Number(match[2]);
  const patch = Number(match[3]);
  const bump = RELEASE_TYPES[releaseType];

  switch (bump) {
    case "major":
      return `${major + 1}.0.0`;

    case "minor":
      return `${major}.${minor + 1}.0`;

    case "patch":
      return `${major}.${minor}.${patch + 1}`;

    default:
      throw new Error(`Invalid release type: ${releaseType}`);
  }
};

/**
 * @param {string} changelogPath
 * @param {string} currentVersion
 * @param {string} newVersion
 * @param {string} repositoryUrl
 */
const updateChangelog = async (changelogPath, currentVersion, newVersion, repositoryUrl) => {
  const changelog = await fs.readFile(changelogPath, "utf8");

  const unreleasedIdx = changelog.search(/^## \[Unreleased\]$/m);
  const afterHeadingIdx = changelog.indexOf("\n", unreleasedIdx);

  const contentAfterHeading = changelog.slice(afterHeadingIdx);
  const unreleasedDiff = /^\[diff.*?main\)/m.exec(contentAfterHeading);
  if (unreleasedDiff === null) {
    throw new Error("Diff link after '## Unreleased' header not found.");
  }
  const diffEndIdx = afterHeadingIdx + unreleasedDiff.index + unreleasedDiff[0].length;

  const beforeUnreleased = changelog.slice(0, unreleasedIdx);
  const afterUnreleasedDiff = changelog.slice(diffEndIdx);

  const today = new Date().toISOString().slice(0, 10);
  const replacement = [
    "## [Unreleased]",
    "",
    `[diff ${newVersion}...main](${repositoryUrl}/compare/${newVersion}...main)`,
    "",
    `## ${newVersion} (${today})`,
    "",
    `[diff ${currentVersion}...${newVersion}](${repositoryUrl}/compare/${currentVersion}...${newVersion})`,
  ].join("\n");

  await fs.writeFile(
    changelogPath,
    `${beforeUnreleased}${replacement}${afterUnreleasedDiff}`,
    "utf8",
  );
};

const main = async () => {
  const { releaseType, extensionDir } = parseArgs(process.argv.slice(2));
  const packagePath = path.resolve(extensionDir, "package.json");
  const changelogPath = path.resolve(extensionDir, "CHANGELOG.md");

  const contents = await fs.readFile(packagePath, "utf8");
  /** @type {PackageJson} */
  const packageJson = JSON.parse(contents);

  const {
    version: currentVersion,
    name: extensionName,
    repository: { url: repositoryUrl },
  } = packageJson;

  const newVersion = bumpVersion(currentVersion, releaseType);

  console.log(`Releasing ${extensionName}: ${currentVersion} -> ${newVersion}`);

  const updatedPackageJson = {
    ...packageJson,
    version: newVersion,
  };
  await fs.writeFile(packagePath, `${JSON.stringify(updatedPackageJson, null, 2)}\n`, "utf8");

  const tagCurrentVersion = `${extensionName}/v${currentVersion}`;
  const tagNewVersion = `${extensionName}/v${newVersion}`;

  await updateChangelog(changelogPath, tagCurrentVersion, tagNewVersion, repositoryUrl);

  await execFileAsync("git", [
    "commit",
    "--no-verify",
    "--message",
    `Release: ${tagNewVersion}`,
    "--include",
    packagePath,
    changelogPath,
  ]);

  await execFileAsync("git", ["tag", "--annotate", "--message", tagNewVersion, tagNewVersion]);

  console.log(`Created release ${extensionName}/${newVersion}`);
};

await main();
