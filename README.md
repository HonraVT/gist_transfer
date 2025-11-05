# Gist Transfer CLI

A simple command-line interface (CLI) tool for transferring files using GitHub Gists via the GitHub API. It supports uploading files (with automatic base64 encoding for binary files), listing existing Gists, and downloading Gists (with automatic decoding for base64-encoded files). This tool is ideal for sharing files up to GitHub's Gist size limit (typically around 25MB for practical use).

Modified from the original [gistup](https://github.com/tuladhar/gistup) by Puru Tuladhar.

## Features

- **Upload Files**: Upload any text or binary file to a new Gist. Binary files are automatically encoded in base64 and appended with a `.base64` extension in the Gist.
- **List Gists**: Retrieve and display a list of your existing Gists with their URLs and descriptions.
- **Download Gists**: Download files from a specified Gist by URL or ID. Automatically decodes base64-encoded files and restores the original filename.
- **Secure Token Handling**: If the GitHub token is not provided via the command line, it prompts for input securely (without echoing to the terminal or logs).
- **Public/Private Control**: Option to make uploaded Gists public.
- **File Size Limit**: Supports files up to GitHub's API limits (e.g., 25MB for base64-encoded content).

## Requirements

- Python 3.x (tested on Python 3.12+)
- No external dependencies—uses only standard Python libraries (`os`, `sys`, `json`, `urllib.request`, `argparse`, `base64`, `re`, `getpass`).

## Installation

Run it directly with Python:
   ```
   python gist_transfer.py --help
   ```

## Usage

The tool provides a built-in help message with examples. Run `python gist_transfer.py --help` for details.

### Key Commands

- **Upload a File**:
  ```
  python gist_transfer.py -u -f path/to/file.zip -t YOUR_TOKEN
  ```
  - Add a description: `-D "My custom description"`
  - Make public: `--public`
  - If `-t` is omitted, it will prompt for the token securely.

- **List Existing Gists**:
  ```
  python gist_transfer.py -l -t YOUR_TOKEN
  ```
  - Outputs a list like: `https://gist.github.com/abcdef1234567890 - My description`

- **Download a Gist**:
  ```
  python gist_transfer.py -d -g https://gist.github.com/someuser/abcdef1234567890 -t YOUR_TOKEN
  ```
  - Alternatively, use just the Gist ID: `-g abcdef1234567890`
  - Downloads files to the current directory, decoding base64 if applicable.

### Notes on Binary Files
- Binary files (e.g., ZIP, images) are encoded in base64 during upload to comply with GitHub's API (which requires string content in JSON).
- On download, if a file ends with `.base64`, it is decoded back to binary and the extension is removed.

## Getting a GitHub Personal Access Token

1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens).
2. Generate a new token with the `gist` scope.
3. Copy the token and use it with the `-t` flag (or enter it when prompted).

**Important**: Treat your token like a password—do not hardcode it or expose it in logs. Using the prompt feature helps avoid this.

## Limitations

- GitHub Gist API limits apply (e.g., file size, rate limits).
- Only supports single-file Gists (multi-file support can be added if needed).
- Public Gists are visible to everyone; use private for sensitive data (default behavior).

## Credits

- Based on the original [gistup](https://github.com/tuladhar/gistup) by Puru Tuladhar.
- Extended with list/download features, base64 handling, and secure token input.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. (If no LICENSE file exists, add one with standard MIT terms.)
