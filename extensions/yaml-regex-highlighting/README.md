# VSCode extension for YAML RegEx syntax highlighting

**DISCLAIMER:** This extension is intended for internal use, due to lack of reliably recognizing
RegEx strings in YAML source.

Only unquoted block strings (Scope: `string.unquoted.block.yaml`) starting with a flag, which at
least contains `x` (extended), and ending with the terminator comment `# regex-end` will be
highlighted.

## Installation

The extension is available from the following marketplaces:

- [VSCode Marketplace](https://marketplace.visualstudio.com/items?itemName=cielquan.yaml-regex-highlighting)
- [Open VSX Marketplace](https://open-vsx.org/extension/cielquan/yaml-regex-highlighting)

## Issues

If you face issues or have improvment ideas please create an issue on the
[Github repository](https://github.com/Cielquan/krys-colors).
