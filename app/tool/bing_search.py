import asyncio
from typing import List
import requests
from app.logger import logger
from bs4 import BeautifulSoup
from app.tool.base import BaseTool

ABSTRACT_MAX_LENGTH = 300

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; pt-BR) AppleWebKit/533.3 (KHTML, like Gecko) QtWeb Internet Browser/3.7 http://www.QtWeb.net',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/532.2',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.4pre) Gecko/20070404 K-Ninja/2.1.3',
    'Mozilla/5.0 (Future Star Technologies Corp.; Star-Blade OS; x86_64; U; en-US) iNet Browser 4.7',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.13) Gecko/20080414 Firefox/2.0.0.13 Pogo/2.0.0.13.6866'
]

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": USER_AGENTS[0],
    "Referer": "https://www.bing.com/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

BING_HOST_URL = "https://www.bing.com"
BING_SEARCH_URL = "https://www.bing.com/search?q="


class BingSearch(BaseTool):
    name: str = "bing_search"
    description: str = """Perform a Bing search and return a list of relevant links.
Use this tool when you need to find information on the web, get up-to-date data, or research specific topics.
The tool returns a list of URLs that match the search query.
"""
    parameters: dict = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "(required) The search query to submit to Bing.",
            },
            "num_results": {
                "type": "integer",
                "description": "(optional) The number of search results to return. Default is 10.",
                "default": 10,
            },
        },
        "required": ["query"],
    }

    session: requests.Session = None

    def __init__(self, **data):
        """Initialize the BingSearch tool with a requests session."""
        super().__init__(**data)
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def _search_sync(self, query: str, num_results: int = 10) -> List[str]:
        """
        Synchronous Bing search implementation to retrieve a list of URLs matching a query.
        
        Args:
            query (str): The search query to submit to Bing. Must not be empty.
            num_results (int, optional): The maximum number of URLs to return. Defaults to 10.

        Returns:
            List[str]: A list of URLs from the search results, capped at `num_results`. 
                       Returns an empty list if the query is empty or no results are found.

        Notes:
            - Pagination is handled by incrementing the `first` parameter and following `next_url` links.
            - If fewer results than `num_results` are available, all found URLs are returned.
        """
        if not query:
            return []

        list_result = []
        first = 1
        next_url = BING_SEARCH_URL + query

        while len(list_result) < num_results:
            data, next_url = self._parse_html(next_url, rank_start=len(list_result), first=first)
            if data:
                list_result.extend([item["url"] for item in data])
            if not next_url:
                break
            first += 10

        return list_result[:num_results]

    def _parse_html(self, url: str, rank_start: int = 0, first: int = 1) -> tuple:
        """
        Parse Bing search result HTML synchronously to extract search results and the next page URL.

        Args:
            url (str): The URL of the Bing search results page to parse.
            rank_start (int, optional): The starting rank for numbering the search results. Defaults to 0.
            first (int, optional): Unused parameter (possibly legacy). Defaults to 1.
        Returns:
            tuple: A tuple containing:
                - list: A list of dictionaries with keys 'title', 'abstract', 'url', and 'rank' for each result.
                - str or None: The URL of the next results page, or None if there is no next page.
        Example:
            This function is called by `execute` in the following way:
            ```python
            results, next_url = self._parse_html(url, rank_start=0)
            ```
        """
        try:
            res = self.session.get(url=url)
            res.encoding = "utf-8"
            root = BeautifulSoup(res.text, "lxml")

            list_data = []
            ol_results = root.find("ol", id="b_results")
            if not ol_results:
                return [], None

            for li in ol_results.find_all("li", class_="b_algo"):
                title = ''
                url = ''
                abstract = ''
                try:
                    h2 = li.find("h2")
                    if h2:
                        title = h2.text.strip()
                        url = h2.a['href'].strip()

                    p = li.find("p")
                    if p:
                        abstract = p.text.strip()

                    if ABSTRACT_MAX_LENGTH and len(abstract) > ABSTRACT_MAX_LENGTH:
                        abstract = abstract[:ABSTRACT_MAX_LENGTH]

                    rank_start += 1
                    list_data.append({"title": title, "abstract": abstract, "url": url, "rank": rank_start})
                except Exception:
                    continue

            next_btn = root.find("a", title="Next page")
            if not next_btn:
                return list_data, None

            next_url = BING_HOST_URL + next_btn["href"]
            return list_data, next_url
        except Exception as e:
            logger.warning(f"Error parsing HTML: {e}")
            return [], None

    async def execute(self, query: str, num_results: int = 10) -> List[str]:
        """
        Execute a Bing search and return a list of URLs asynchronously.

        Args:
            query (str): The search query to submit to Bing.
            num_results (int, optional): The number of search results to return. Default is 10.

        Returns:
            List[str]: A list of URLs matching the search query.
        """
        loop = asyncio.get_event_loop()
        links = await loop.run_in_executor(
            None, lambda: self._search_sync(query, num_results=num_results)
        )
        return links
