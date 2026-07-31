from redis import Redis

from services.NewsFetcher.src.fetchers.base_rss_fetcher import BaseRssFetcher
from services.NewsFetcher.src.article import Article
from services.NewsFetcher.src.config import config


class FinancialTimesFetcher(BaseRssFetcher):
	def __init__(self, redis_client: Redis):
		super().__init__(
			source_url="https://www.ft.com/world?format=rss",
			source_name="Financial Times",
			redis_client=redis_client
		)
	
	def _parse_entry(self, entry) -> Article:
		return Article(
			title=entry.title,
			summary=entry.summary,
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
	
	news = FinancialTimesFetcher(redis_client=redis_client)
	
	fetched_articles = news.fetch_new_articles()
	
	for article in fetched_articles:
		print(article)
