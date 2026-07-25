import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def _clean_text(value):
    if not value:
        return ""
    return " ".join(str(value).split())


def _is_valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def analyze_website(url):
    if not _is_valid_url(url):
        return {"error": "Invalid URL"}

    try:
        start_time = time.time()
        response = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        end_time = time.time()
        response_time = round(end_time - start_time, 2)
    except requests.exceptions.Timeout:
        return {"error": "Request Timed Out"}
    except requests.exceptions.RequestException as exc:
        return {"error": f"Unable to access website: {str(exc)}"}
    except Exception as exc:
        return {"error": f"Unexpected request error: {str(exc)}"}

    content_type = response.headers.get("Content-Type", "")
    if "text/html" not in content_type:
        return {"error": "This is not an HTML page"}

    soup = BeautifulSoup(response.text, "html.parser")

    title = _clean_text(soup.title.string) if soup.title and soup.title.string else "No Title"

    meta_tag = None
    for tag in soup.find_all("meta"):
        name_value = tag.get("name")
        if isinstance(name_value, str) and name_value.lower() == "description":
            meta_tag = tag
            break

    meta_description = "No Meta Description"
    if meta_tag and meta_tag.get("content"):
        meta_description = _clean_text(meta_tag.get("content"))

    h1_count = len(soup.find_all("h1"))

    images = soup.find_all("img")
    missing_alt = 0
    for image in images:
        if not image.get("alt"):
            missing_alt += 1

    text = soup.get_text(separator=" ", strip=True)
    word_count = len(text.split())

    parsed_url = urlparse(url)
    favicon = f"https://www.google.com/s2/favicons?domain={parsed_url.netloc}&sz=128"

    score = 100
    issues = []

    if title == "No Title":
        score -= 20
        issues.append("Missing page title")

    if meta_description == "No Meta Description":
        score -= 20
        issues.append("Missing meta description")

    if h1_count == 0:
        score -= 20
        issues.append("No H1 heading found")

    if missing_alt > 5:
        score -= 15
        issues.append("Too many images missing alt text")

    if response_time > 2:
        score -= 10
        issues.append("Page response time is slow")

    if word_count < 100:
        score -= 5
        issues.append("Content appears short")

    score = max(score, 0)

    return {
        "status": response.status_code,
        "response_time": f"{response_time} sec",
        "title": title,
        "meta_description": meta_description,
        "h1_count": h1_count,
        "missing_alt_images": missing_alt,
        "word_count": word_count,
        "favicon": favicon,
        "seo_score": score,
        "issues": issues,
    }