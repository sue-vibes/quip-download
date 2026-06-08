# Quip Download

A Python script to download all your Quip documents and convert them to Markdown or HTML format.

## Features

- Downloads documents from your Quip desktop, private, archive, and shared folders
- Supports Markdown and HTML export formats
- Sanitizes filenames to prevent OS compatibility issues
- Handles nested subfolders recursively

## Requirements

- Python 3.6+
- `requests` library
- `markdownify` library

Install dependencies:

```bash
pip install -r requirements.txt
```

## Setup

1. Create a `.env` file (copy from `.env.example`)
2. Get your Quip Personal Access Token from https://quip.com/settings/access_tokens
3. Add your token to the `.env` file

## Usage

```bash
python quip_download.py
```

Documents will be saved to `./quip_all_exports` by default.

## Configuration

Configure via environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `QUIP_TOKEN` | Your Quip Personal Access Token | (required) |
| `EXPORT_FORMAT` | Export format: `markdown` or `html` | `markdown` |
| `OUTPUT_DIR` | Output directory for downloaded files | `./quip_all_exports` |

## License

MIT