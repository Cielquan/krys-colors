# VSCode color theme "krys-colors"

This theme's colors are originally based on the original Monokai.

Following _languages_ have been tested:

- Bash / Shell (*.{bash,sh})
- CSS
- Dockerfile
- Gettext (*.{po,pot})
- GDScript
- HTML
- Ignore (.gitignore)
- INI
- JavaScript
- Jinja2
- JSON
- Markdown
- Python
- React (*.{jsx,tsx})
- RegEx
- ReStructuredText
- Rust
- SQL
- TOML
- TypeScript
- XML
- YAML

## Installation

The extension is available from the following marketplaces:

- [VSCode Marketplace](https://marketplace.visualstudio.com/items?itemName=cielquan.krys-colors)
- [Open VSX Marketplace](https://open-vsx.org/extension/cielquan/krys-colors)

## Development (in VSCode)

To build the theme JSON artifact from the JSONC file run `pre-commit run remove-comments-from-jsonc --all-files`.
To automatically rebuild the artifact run: `watchexec -w themes pre-commit run remove-comments-from-jsonc --all-files`.

In VSCode press `F5` to launch a development window, where you can open the example files to see the theme in action.

`pre-commit` is a python package and can be installed via `pip install pre-commit`.
`watchexec` is a rust crate and can be installed via `cargo install --locked watchexec-cli`.

### Release / VSIX Builds

Install `vsce` util
`npm install -g @vscode/vsce`

Run `pre-commit` for linting, formatting and output generation
`pre-commit run --all-files`

Run `vsce` to generate `vsix` file
`vsce package`

See also: https://code.visualstudio.com/api/working-with-extensions/publishing-extension
