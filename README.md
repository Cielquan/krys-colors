# Monorepo for `Krys Colors` theme and language extentions for VSCode

See the respective READMEs of the extentions for extention specifics:

- `krys-colors`: [README.md](./extensions/krys-colors/README.md)
- `gitignore-syntax-vsx`: [README.md](./extensions/gitignore-syntax-vsx/README.md)

## Development (in VSCode)

### Builds

To build the theme JSON artifact from the JSONC file run the `build` npm script via
`pnpm --filter krys-colors build`.

You can also run the `watch` npm script via `pnpm watch` which uses
[`watchexec`](https://github.com/watchexec/watchexec) to automatically rebuild the JSON artifact.
You can install `watchexec` with `cargo install --locked watchexec-cli`.

### Testing

In VSCode press `F5` to launch a development window. The windows will run off the local versions
of all extentions from this repo. The `code_examples/` directory is available for testing.

### Tooling

Linter and Formatter are managed via the `pre-commit` framework. You can use `pre-commit` or `prek`
to run them.

- `pre-commit`: `pip install pre-commit`
- `prek`: `cargo install --locked prek`

### Release / VSIX Builds

To create the VISX artifacts run the `package` npm script via `pnpm package`. This runs a custom
build script which builds and packages all extentions into the `dist/` directory.

The VISX artifacts can then be uploaded to the marketplaces.

See also: https://code.visualstudio.com/api/working-with-extensions/publishing-extension
