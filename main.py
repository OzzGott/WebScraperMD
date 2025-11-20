import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

BASE_URL = "https://example.com"
SLUG_FILE = "slugs.txt"
with open(SLUG_FILE, "r") as f:
    slug_list = {line.strip().lstrip("/") for line in f}


def save_file(url, folder):
    os.makedirs(folder, exist_ok=True)
    filename = os.path.basename(urlparse(url).path)

    if not filename:
        filename = "file"

    path = os.path.join(folder, filename)

    try:
        r = requests.get(url)
        r.raise_for_status()
        with open(path, "wb") as f:
            f.write(r.content)
        return filename
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None


def extract_markdown(soup, page_url, download_folder):
    md_lines = []

    for element in soup.find_all(["p", "h1", "h2", "h3", "li", "a", "img"]):
        if element.name in ["h1", "h2", "h3"]:
            level = "#" * int(element.name[-1])
            md_lines.append(f"{level} {element.get_text(strip=True)}\n")

        elif element.name == "p":
            text = element.get_text(" ", strip=True)
            md_lines.append(text + "\n")

        elif element.name == "li":
            text = element.get_text(" ", strip=True)
            md_lines.append(f"- {text}")

        elif element.name == "a":
            text = element.get_text(strip=True)
            href = element.get("href")

            if not href:
                continue
            full_url = urljoin(page_url, href)
            path = urlparse(full_url).path.lstrip("/")

            if any(full_url.lower().endswith(ext) for ext in (".pdf", ".png", ".jpg", ".jpeg", ".gif", ".svg")):
                save_file(full_url, download_folder)

            elif path in slug_list:
                md_lines.append(f"[{text}]({path}.md)\n")

        elif element.name == "img":
            src = element.get("src")
            if not src:
                continue

            full_url = urljoin(page_url, src)
            filename = save_file(full_url, download_folder)

            if filename:
                md_lines.append(f"![image]({filename})\n")

    return "\n".join(md_lines)


def scrape_slug(slug):
    slug_clean = slug.strip().lstrip("/")
    if not slug_clean:
        return

    url = f"{BASE_URL}/{slug_clean}"
    print(f"Scraping: {url}")

    r = requests.get(url)
    if r.status_code != 200:
        print(f"Failed: {url} -> {r.status_code}")
        return

    soup = BeautifulSoup(r.text, "html.parser")

    download_folder = os.path.join("downloads", slug_clean)

    md_content = extract_markdown(soup, url, download_folder)

    os.makedirs("markdown", exist_ok=True)
    md_path = os.path.join("markdown", f"{slug_clean}.md")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"Saved: {md_path}")


def main():
    with open(SLUG_FILE, "r") as f:
        slugs = f.readlines()

    for slug in slugs:
        scrape_slug(slug)


if __name__ == "__main__":
    main()
