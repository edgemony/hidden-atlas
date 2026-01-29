import requests
import os

USER_AGENT = "HiddenAtlas/1.0 (https://github.com/edgemony/hidden-atlas; game project)"


def search_skyline(city_name, limit=5):
    """Search Wikimedia Commons for city skyline images."""
    url = "https://commons.wikimedia.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrnamespace": 6,  # File namespace
        "gsrsearch": f"{city_name} skyline",
        "gsrlimit": limit,
        "prop": "imageinfo",
        "iiprop": "url|extmetadata",
    }

    headers = {"User-Agent": USER_AGENT}

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    results = []
    pages = data.get("query", {}).get("pages", {})

    for page in pages.values():
        info = page.get("imageinfo", [{}])[0]
        results.append({
            "title": page.get("title"),
            "url": info.get("url"),
            "desc_url": info.get("descriptionurl"),
        })

    return results


def download_image(url, output_path):
    """Download an image from URL and save to output_path."""
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers, stream=True)
    response.raise_for_status()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"Saved: {output_path}")
    return output_path


def fetch_skyline_options(city_name, output_dir, limit=5):
    """
    Search and download skyline images for a city.

    Args:
        city_name: Name of the city to search for
        output_dir: Directory to save images (e.g., "public/maps/2026-01-26")
        limit: Number of images to download (default 5)

    Returns:
        List of downloaded file paths, or empty list if no results
    """
    print(f"Searching for {city_name} skyline images...")
    results = search_skyline(city_name, limit)

    if not results:
        print("No results found")
        return []

    for i, img in enumerate(results):
        print(f"\n{i+1}. {img['title']}")
        print(f"   URL: {img['url']}")

    print(f"\nDownloading {len(results)} images for review...")
    downloaded = []
    for i, img in enumerate(results):
        if img["url"]:
            output_path = f"{output_dir}/hint_option_{i+1}.jpg"
            download_image(img["url"], output_path)
            downloaded.append(output_path)

    return downloaded


# Ad-hoc usage example:
# from wikimedia_search import fetch_skyline_options
# fetch_skyline_options("Pittsburgh", "public/maps/2026-01-26")

if __name__ == "__main__":
    # Quick test - change these values as needed
    fetch_skyline_options("Pittsburgh", "public/maps/2026-01-26")