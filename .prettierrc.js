const config = {
  "printWidth": 88,
  "endOfLine": "auto",
  "overrides": [
    // Revert JSONC parsing:
    // https://github.com/prettier/prettier/issues/15553
    {
      "files": ["**/*.jsonc"],
      "options": {
        "parser": "json"
      }
    }
  ]
}

module.exports = config;
