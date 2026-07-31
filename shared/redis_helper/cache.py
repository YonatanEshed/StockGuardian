import json
import logging
from typing import Optional, Any

from redis import Redis, RedisError

logger = logging.getLogger(__name__)


class RedisCacheHelper:
	def __init__(self, redis_client: Redis):
		"""
		Initializes the Redis Cache Helper.
		
		:param redis_client: An instance of a Redis client.
		:param ttl_seconds: Default Time-To-Live for cached keys.
		"""
		self.redis_client = redis_client
	
	def get(self, key: str) -> Optional[Any]:
		"""
		Retrieves and deserializes data from the cache.
		Returns None on a cache miss or if an error occurs.
		"""
		try:
			cached_data = self.redis_client.get(key)
			if cached_data:
				return json.loads(cached_data)
		
		except redis.RedisError as e:
			logger.error(f"Redis GET failed for key '{key}': {e}")
		
		return None
	
	def set(self, key: str, value: Any, ttl_seconds: int, nx: bool = False) -> bool:
		"""
		Unconditionally forces a set/overwrite of a key with the given value.
		"""
		try:
			serialized_data = json.dumps(value)
			
			return bool(self.redis_client.set(key, serialized_data, ex=ttl_seconds, nx=nx))
		
		except RedisError as e:
			logger.error(f"Redis SET failed for key '{key}': {e}")
			
			return False
	
	def delete(self, key: str) -> bool:
		"""
		Removes a key from the cache.
		Returns True if the key was deleted, False otherwise.
		"""
		try:
			return bool(self.redis_client.delete(key))
		
		except RedisError as e:
			logger.error(f"Redis DELETE failed for key '{key}': {e}")
			
			return False
	
	def clear_all(self) -> bool:
		"""
		Flushes the current Redis database. Use with caution.
		"""
		try:
			return bool(self.redis_client.flushdb())
		
		except RedisError as e:
			logger.error(f"Redis FLUSHDB failed: {e}")
			
			return False
