# VSCode color theme "krys-colors"

This theme's colors are originally based on the original Monokai.

Following _languages_ I have tested and partially additionally configured:

- CSS
- Dockerfile
- HTML
- INI
- JavaScript
- Jinja2
- JSON
- Markdown
- Python
- RegEx
- ReStructuredText
- Rust
- TOML
- TypeScript
- YAML

Planned to be also tested:

- SQL
- React
- po translation files (mrorz.language-gettext)
- XML
- PS1
- Makefile
- Nix
- VimScript


Following extensions are needed for the corresponding file type:

- Dockerfile: jeff-hykin.better-dockerfile-syntax
- Jinja2: samuelcolvin.jinjahtml
- ReStructuredText: lextudio.restructuredtext + trond-snekvik.simple-rst
- Rust: rust-lang.rust-analyzer
- TOML: tamasfe.even-better-toml or bungcip.better-toml

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
