# Monorepo for `Krys Colors` theme and language extentions for VSCode

See the respective extentions for specifics:

- Krys Colors: [`krys-colors`](./extensions/krys-colors)
- Better GDScript Syntax: [`better-gdscript-syntax`](./extensions/better-gdscript-syntax)
- GitIgnore Syntax: [`gitignore-syntax-vsx`](./extensions/gitignore-syntax-vsx)
- YAML RegEx Highlighting: [`yaml-regex-highlighting`](./extensions/yaml-regex-highlighting)

## Development (in VSCode)

Most npm scripts listed below also have a shorthand, see the root `package.json` for details.

### Builds

All extensions have a npm `build` script which can be called via `pnpm --filter <EXT> build`.

You can also run the `watch` npm script via `pnpm --filter <EXT> watch` which uses
[`watchexec`](https://github.com/watchexec/watchexec) to automatically rebuild the artifacts.
You can install `watchexec` with `cargo install --locked watchexec-cli`.

### Testing (manual)

In VSCode press `F5` to launch a development window. The windows will run off the local versions
of all extentions from this repo. The `code_examples/` directory is available for testing.

### Validation

The `better-gdscript-syntax` extension also has a `validate` npm script callable via
`pnpm --filter better-gdscript-syntax validate`.

### Tooling

Linter and Formatter are managed via the `pre-commit` framework. You can use `pre-commit` or `prek`
to run them.

- `pre-commit`: `pip install pre-commit`
- `prek`: `cargo install --locked prek`

### Release / VSIX Builds

1. Run the `pnpm release <VERSION_TYPE> <EXT_DIR_PATH>` npm script to create a release for a given
  extension.
1. To create the VISX artifacts run the `package` npm script via `pnpm package`. This runs a custom
  build script which builds and packages all extentions into the `dist/` directory.
1. The VISX artifacts can then be uploaded to the marketplaces.
  See also: https://code.visualstudio.com/api/working-with-extensions/publishing-extension
