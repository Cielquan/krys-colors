## VSCode color theme "krys-colors"

This theme's colors are based on the original Monokai.

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

Following extensions are needed for the corresponding file type:

- Dockerfile: jeff-hykin.better-dockerfile-syntax
- Jinja2: samuelcolvin.jinjahtml
- ReStructuredText: lextudio.restructuredtext + trond-snekvik.simple-rst
- Rust: rust-lang.rust-analyzer
- TOML: tamasfe.even-better-toml or bungcip.better-toml

## Install the extension

To start using this extension with Visual Studio Code copy it into the
`<user home>/.vscode/extensions` folder and restart Code.

Run: `git clone https://github.com/Cielquan/krys-colors ~/.vscode/extensions/krys-colors`

## Development (in VSCode)

In VSCode press `F5` to launch a development window where you can open a file to see the theme in action.

Code changes are ment to be made in the JSONC file, which supports comments. With `pre-commit run remove-comments-from-jsonc --all-files` the comments are striped and the JSON file gets overridden.

`pre-commit` is a python package and can be installed via `pip install pre-commit`.
