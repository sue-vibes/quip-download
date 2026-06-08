# Quip Download

A Python script to download all your Quip documents and convert them to Markdown or HTML format.

## Getting Started

If you've never used Git before, follow these simple steps:

### Download the Repository

1. Click the green **"Code"** button on the GitHub page
2. Click **"Download ZIP"** 
3. Extract the ZIP file to a folder on your computer
4. Open Terminal (Mac/Linux) or Command Prompt (Windows)

### Install and Run

```bash
# Navigate to the extracted folder
cd path/to/quip-download

# Create a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip3 install -r requirements.txt

# Copy the example environment file
cp .env.example .env  # On Windows: copy .env.example .env
```

### Edit Your Quip Token

Open `.env` in a text editor and replace `your_quip_personal_access_token_here` with your actual token from https://quip.com/dev/token.

### Running the Script

After saving `.env`, run the script:

```bash
python3 quip_download.py
```

Documents will be saved to `./quip_all_exports` by default.

## Features

- Downloads documents from your Quip desktop, private, archive, and shared folders
- Supports Markdown and HTML export formats
- Sanitises filenames to prevent OS compatibility issues
- Handles nested subfolders recursively

## Requirements

- Python 3.6+
- `requests` library
- `markdownify` library

All dependencies are installed with the `pip install` command above.

## Configuration

Configure via environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `QUIP_TOKEN` | Your Quip Personal Access Token | (required) |
| `EXPORT_FORMAT` | Export format: `markdown` or `html` | `markdown` |
| `OUTPUT_DIR` | Output directory for downloaded files | `./quip_all_exports` |

## License

MIT