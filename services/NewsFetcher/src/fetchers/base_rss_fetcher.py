from abc import ABC, abstractmethod

import feedparser
from bs4 import BeautifulSoup
from redis import Redis

from services.NewsFetcher.src.article import Article
from services.NewsFetcher.src.config import config
from shared.redis_helper import RedisCacheHelper

EMPTY_VALUE_PLACEHOLDER = 1


class BaseRssFetcher(ABC):
	def __init__(self, source_url: str, source_name: str, redis_client: Redis):
		self.source_url = source_url
		self.source_name = source_name
		self.redis_cache = RedisCacheHelper(redis_client=redis_client)
	
	def fetch_new_articles(self) -> list[Article]:
		"""
		Fetch headlines from a single RSS source.

		:return: List of Article objects.
		"""
		# TODO: Change implementation to work asynchronously(maybe even change the redis client to be async).
		feed = feedparser.parse(self.source_url)
		
		articles = []
		
		for entry in feed.entries:
			article = self._parse_entry(entry)
			if self._cache_if_new(article):
				articles.append(article)
		
		return articles
	
	def _cache_if_new(self, article: Article) -> bool:
		"""
		Redis cache the headline to avoid duplicates.

		:param article: The Article object to cache.
		:return: True if the headline is new and cached, False if it was already cached.
		"""
		return self.redis_cache.set(
			key=article.url,
			value=EMPTY_VALUE_PLACEHOLDER,
			ttl_seconds=config.HEADLINE_CACHE_TTL_SECONDS,
			nx=True
		)
	
	@staticmethod
	def _strip_html_tags(text: str) -> str:
		"""
		Strip HTML tags from a string.

		:param text: The string to strip HTML tags from.
		:return: The string without HTML tags.
		"""
		return BeautifulSoup(text, "html.parser").get_text()
	
	@abstractmethod
	def _parse_entry(self, entry) -> Article:
		"""
		Parse a single RSS entry into an Article object.

		:param entry: The RSS entry to parse.
		:return: An Article object.
		"""
		pass
