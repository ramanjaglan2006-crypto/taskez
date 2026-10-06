import httpx
import re
from typing import Any, Dict
from taskez.tools.base import BaseTool

class WebScraperTool(BaseTool):
    name = "web_scraper"
    description = "Extracts body text, key headings, and metadata from a web page URL."

    def _run(self, url: str) -> Dict[str, Any]:
        if not url or not (url.startswith("http://") or url.startswith("https://")):
            raise ValueError(f"Invalid URL provided: '{url}'. Must start with http:// or https://")
            
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        try:
            with httpx.Client(timeout=8.0, follow_redirects=True) as client:
                resp = client.get(url, headers=headers)
                if resp.status_code != 200:
                    raise RuntimeError(f"HTTP Error {resp.status_code} while fetching {url}")
                
                html_text = resp.text
                
                # Strip out style and script content
                clean_html = re.sub(r'<script[^>]*>.*?</script>', '', html_text, flags=re.DOTALL | re.IGNORECASE)
                clean_html = re.sub(r'<style[^>]*>.*?</style>', '', clean_html, flags=re.DOTALL | re.IGNORECASE)
                
                # Extract title
                title_match = re.search(r'<title>(.*?)</title>', clean_html, re.IGNORECASE | re.DOTALL)
                title = title_match.group(1).strip() if title_match else "No Title Found"
                
                # Extract headings
                headings = re.findall(r'<h[1-3][^>]*>(.*?)</h[1-3]>', clean_html, re.IGNORECASE | re.DOTALL)
                clean_headings = [re.sub(r'<[^>]+>', '', h).strip() for h in headings[:5]]
                
                # Extract plain text content
                text_content = re.sub(r'<[^>]+>', ' ', clean_html)
                text_content = re.sub(r'\s+', ' ', text_content).strip()
                
                # Truncate content preview
                summary_text = text_content[:1500] if len(text_content) > 1500 else text_content
                
                return {
                    "url": url,
                    "title": title,
                    "headings": clean_headings,
                    "content_length": len(text_content),
                    "summary_text": summary_text
                }
        except Exception as e:
            # Provide structured error or fallback extraction
            raise RuntimeError(f"Failed to scrape webpage at '{url}': {str(e)}")
