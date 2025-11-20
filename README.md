# WebScraperMD: Web Scraper to Markdown Converter

## Overview

**WebScraperMD** is a command-line utility written in Python designed to systematically scrape content from a target website and convert it into clean, offline-ready Markdown files.

The tool operates by taking a base URL and a list of specific "slugs" (the tail end of the URLs), fetching each page, converting the HTML to Markdown, and critically, downloading all associated assets (images and documents) to ensure the local Markdown files are self-contained and fully functional offline.

## Features

  * **Batch Scraping:** Efficiently process a large number of pages defined in a simple text file (`slugs.txt`).
  * **Markdown Conversion:** Converts complex HTML pages into clean, readable Markdown (`.md`) files.
  * **Asset Download:** Automatically identifies and downloads linked resources such as images (`.png`, `.jpg`, etc.) and documents (`.pdf`, `.docx`, etc.).
  * **Local Link Rewriting:** Updates the Markdown file content to point to the newly downloaded local assets instead of the original web links.
  * **Organized Output:** Saves all scraped Markdown files and their corresponding assets into a neatly structured local directory.

## Installation

This project requires Python 3.x and a few common scraping libraries.

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/OzzGott/WebScraperMD.git](https://github.com/OzzGott/WebScraperMD.git)
    cd WebScraperMD
    ```

2.  **Install Dependencies:**
    While a `requirements.txt` file is not explicitly provided, the following libraries are typically required for this type of operation:

    ```bash
    pip install requests beautifulsoup4 markdownify
    ```

    *Note: If you encounter an error, you may need to install other dependencies based on the exact implementation in `main.py`.*

## Usage

To run the scraper, you need to configure your target base URL and populate the list of page slugs you wish to download.

### 1. Configure the Target

**a. Define the Base URL:**
The base URL (e.g., `https://example.com/docs/`) should be defined within the `main.py` file or passed as a command-line argument, depending on the script's design. Ensure this is set correctly.

**b. Populate `slugs.txt`:**
The `slugs.txt` file must contain a new slug on each line. A slug is the part of the URL that comes *after* the base path.

### 2. Run the Scraper

Execute the main Python script from your terminal:

```bash
python main.py
