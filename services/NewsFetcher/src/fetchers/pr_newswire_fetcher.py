from redis import Redis

from services.NewsFetcher.src.article import Article
from services.NewsFetcher.src.config import config
from services.NewsFetcher.src.fetchers.base_rss_fetcher import BaseRssFetcher


class PrNewswireFetcher(BaseRssFetcher):
	def __init__(self, redis_client: Redis):
		super().__init__(
			source_url="https://www.prnewswire.com/rss/news-releases-list.rss",
			source_name="PR Newswire",
			redis_client=redis_client
		)
	
	def _parse_entry(self, entry) -> Article:
		return Article(
			title=entry.title,
			summary=self._strip_html_tags(entry.summary),
			source=self.source_name,
			url=entry.link,
			published_at=entry.published
		)


if __name__ == '__main__':
	redis_client = Redis(
		password=config.REDIS_PASSWORD.get_secret_value() if config.REDIS_PASSWORD else None,
		host=config.REDIS_HOST,
		port=config.REDIS_PORT
	)
	
	news = PrNewswireFetcher(redis_client=redis_client)
	
	fetched_articles = news.fetch_new_articles()
	
	for article in fetched_articles:
		print(article)
