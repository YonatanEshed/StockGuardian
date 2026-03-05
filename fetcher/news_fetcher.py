
import urllib.request
import xml.etree.ElementTree as ET

from .article import Article


class NewsFetcher:
	FEEDS = {
		# Finance & Markets
		"reuters_business": "https://feeds.reuters.com/reuters/businessNews",
		"reuters_markets": "https://feeds.reuters.com/reuters/financialsNews",
		"wsj_markets": "https://feeds.content.dowjones.io/public/rss/mw_topstories",
		"marketwatch": "https://feeds.content.dowjones.io/public/rss/mw_marketpulse",
		"ft": "https://www.ft.com/rss/home",
		"seeking_alpha": "https://seekingalpha.com/market_currents.xml",
		"investing_com": "https://www.investing.com/rss/news.rss",
		
		# Economics & Macro
		"reuters_economy": "https://feeds.reuters.com/reuters/economicNews",
		"bloomberg_economy": "https://feeds.bloomberg.com/economics/news.rss",
		"cnbc_economy": "https://www.cnbc.com/id/20910258/device/rss/rss.html",
		"cnbc_finance": "https://www.cnbc.com/id/10000664/device/rss/rss.html",
		
		# Tech (big market mover)
		"cnbc_tech": "https://www.cnbc.com/id/19854910/device/rss/rss.html",
		"techcrunch": "https://techcrunch.com/feed/",
		
		# Energy & Commodities
		"reuters_energy": "https://feeds.reuters.com/reuters/energyNews",
		"oilprice": "https://oilprice.com/rss/main",
		
		# Geopolitics (macro risk)
		"reuters_world": "https://feeds.reuters.com/Reuters/worldNews",
		"bbc_world": "https://feeds.bbci.co.uk/news/world/rss.xml",
	}
	
	def get_headlines(self, source: str, max_results: int = 10) -> list[Article]:
		"""
		Fetch headlines from a single RSS source.
		
		:param source: A key from FEEDS, or a custom RSS URL.
		:param max_results: Maximum number of articles to return.
		:return: List of Article objects.
		"""

		url = self.FEEDS.get(source, source)
		try:
			req = urllib.request.Request(url, headers={"User-Agent": "NewsHeadlines/1.0"})
			with urllib.request.urlopen(req, timeout=10) as resp:
				raw = resp.read()
		except Exception as exc:
			raise ConnectionError(f"Failed to fetch RSS from '{url}': {exc}") from exc
		
		try:
			root = ET.fromstring(raw)
		except ET.ParseError as exc:
			raise ValueError(f"Could not parse RSS XML: {exc}") from exc
		
		# Support both RSS 2.0 (<item>) and Atom (<entry>) formats
		items = root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry")
		
		articles = []
		for item in items[:max_results]:
			def _text(tag, ns=None):
				el = item.find(f"{{{ns}}}{tag}" if ns else tag)
				return el.text.strip() if el is not None and el.text else ""
			
			atom = "http://www.w3.org/2005/Atom"
			articles.append(Article(
				title=_text("title") or _text("title", atom),
				description=_text("description") or _text("summary", atom),
				url=_text("link") or _text("link", atom),
				source=source.upper(),
				published_at=_text("pubDate") or _text("published", atom) or None,
				author=_text("author") or _text("author", atom) or None,
			))
		
		return articles
	
	def get_headlines_multi(
			self,
			sources: list[str] = None,
			max_per_source: int = 5,
	) -> list[Article]:
		"""Fetch headlines from multiple RSS sources at once."""
		sources = sources or list(self.FEEDS.keys())
		all_articles = []
		for src in sources:
			try:
				all_articles.extend(self.get_headlines(src, max_per_source))
			except Exception as exc:
				print(f"  ⚠  Skipping '{src}': {exc}")
		return all_articles
	

if __name__ == "__main__":
	news = NewsFetcher()
	
	print("=== CNBC Tech Top Headlines ===")
	articles = news.get_headlines(source="cnbc_tech", max_results=5)
	for article in articles:
		print(article.title)
	