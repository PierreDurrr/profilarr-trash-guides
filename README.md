# Unofficial TRaSH-Guides Database for Profilarr

This repository hosts [TRaSH-Guides's](https://trash-guides.info/) unofficial database for Profilarr containing:

- Regex Patterns
- Custom Formats
- Quality Profiles
- Media Management

The goal of this repository is to generate a Profilarr database based on TRaSH-Guides configuration without any changes. If you want anything custom you can commit it yourself within the Profilarr UI.

The repo will be automatically kept in sync with the TRaSH-Guides repository. A Github Action will run every day pulling the latest version of TRaSH-Guides and running the scripts committing and pushing any changes.

## Scripts

The repository a script to generate the specification based on the TRaSH-Guide data.

### Requirements

The scripts utilize UV for easy package management, ensure it's installed by following the [official instructions](https://github.com/astral-sh/uv?tab=readme-ov-file#installation).

Additionally it's expected that you have a local folder with a TRaSH-Guides clone containing the JSON data ([docs/json within the TRaSH-Guides repository](https://github.com/TRaSH-Guides/Guides/tree/master/docs/json)). The script does not pull any data.

### Running the script

Assuming you're in the root directory of the repository you can now run:

```
uv run scripts/generate.py /path/to/trash-guides/docs/json .
```

It will clear any potentially pre-existing output and generate new output based on the provided TRaSH-Guides folder.
