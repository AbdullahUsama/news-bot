import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json

def scrape_dawn_articles(start_date=None, end_date=None):
    """
    Scrapes Dawn articles between given dates, extracts title and content,
    and prints them in JSON format.
    
    Args:
        start_date (str, optional): Format "YYYY-MM-DD". Defaults to today.
        end_date (str, optional): Format "YYYY-MM-DD". Defaults to today.
    """
    # Default to today if no dates are given
    if start_date is None:
        start_date = datetime.today().strftime("%Y-%m-%d")
    if end_date is None:
        end_date = datetime.today().strftime("%Y-%m-%d")

    def extract_article_text(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to fetch the URL: {e}")
            return {"title": "", "content": "", "url": url}

        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.select_one("h1.story__title, h2.story__title")
        title = title_tag.get_text(strip=True) if title_tag else "No title found"
        content = "\n".join(p.get_text(strip=True) for p in soup.select(".story__content p"))
        return {"title": title, "content": content.strip(), "url": url}

    def get_top_urls(start_date, end_date):
        all_urls = []
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        current = start

        while current <= end:
            date_str = current.strftime("%Y-%m-%d")
            page_url = f"https://www.dawn.com/newspaper/editorial/{date_str}"
            try:
                response = requests.get(page_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                count = 0
                for a_tag in soup.select("article.story a.story__link[href]"):
                    href = a_tag.get("href")
                    if href.startswith("https://www.dawn.com/news/") and href not in all_urls:
                        all_urls.append(href)
                        count += 1
                    if count == 3:
                        break
            except requests.RequestException as e:
                print(f"[{date_str}] Failed to fetch: {e}")
            current += timedelta(days=1)
        return all_urls

    # Fetch article URLs
    urls = get_top_urls(start_date, end_date)

    # Extract article data
    articles = [extract_article_text(url) for url in urls]

    # Print results as JSON
    # print(json.dumps(articles, indent=2, ensure_ascii=False))

    return articles

# Example usage:
# scrape_dawn_articles("2025-06-08", "2025-06-09")
# or just:
scrape_dawn_articles()
