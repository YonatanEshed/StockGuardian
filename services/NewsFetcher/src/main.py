import threading
import time

from redis import Redis

from services.NewsFetcher.src.config import config, logger
from services.NewsFetcher.src.fetchers.base_rss_fetcher import BaseRssFetcher
from services.NewsFetcher.src.fetchers.cnbc_fetcher import CNBCFetcher
from services.NewsFetcher.src.fetchers.financial_times_fetcher import FinancialTimesFetcher
from services.NewsFetcher.src.fetchers.pr_newswire_fetcher import PrNewswireFetcher
from shared.redis_helper import RedisStreamPublisher


class NewsFetcherService:
	def __init__(self):
		logger.info("Initializing NewsFetcherService...")
		
		self.redis_client: Redis = Redis(
			password=config.REDIS_PASSWORD.get_secret_value() if config.REDIS_PASSWORD else None,
			host=config.REDIS_HOST,
			port=config.REDIS_PORT
		)
		
		self.redis_stream_publisher = RedisStreamPublisher(
			redis_client=self.redis_client,
		)
		
		self.rss_fetchers: list[BaseRssFetcher] = [
			CNBCFetcher(redis_client=self.redis_client),
			FinancialTimesFetcher(redis_client=self.redis_client),
			PrNewswireFetcher(redis_client=self.redis_client),
		]
		
		logger.info(f"Loaded {len(self.rss_fetchers)} rss fetchers.")
	
	def process_news_source(self, fetcher: BaseRssFetcher):
		fetcher_name = fetcher.__class__.__name__
		logger.info(f"Starting article fetch for {fetcher_name}")
		
		articles = fetcher.fetch_new_articles()
		logger.info(f"Successfully fetched {len(articles)} new articles from {fetcher_name}")
		
		for article in articles:
			logger.info(f"Processing article: {article}")
			
			self.redis_stream_publisher.publish(
				data=article.to_dict(),
				stream_name=config.NEXT_SERVICE_STREAM_KEY
			)
	
	def start_fetcher_workers(self):
		logger.info("Starting new batch fetch cycle")
		threads = []
		
		for index, fetcher in enumerate(self.rss_fetchers):
			thread = threading.Thread(target=lambda: self.process_news_source(fetcher), name=f"Worker-{index}")
			threads.append(thread)
			thread.start()
	
	def start_job(self):
		try:
			while True:
				self.start_fetcher_workers()
				time.sleep(60)
		except KeyboardInterrupt:
			logger.info("\nService stopped by user.")
		except Exception as e:
			logger.critical(f"Application crashed unexpectedly: {e}", exc_info=True)
		finally:
			logger.info("Service stopped. Cleanup finished.")


def main():
	service = NewsFetcherService()
	service.start_job()


if __name__ == "__main__":
	main()
	# TODO: Convert service to async instead of using threads.
