import json
import logging
import time
from typing import Callable, Any, Dict

import redis

GROUP_ALREADY_EXISTS_ERROR = "BUSYGROUP"
READ_UNDELIVERED_MESSAGES_SYMBOL = '>'

logger = logging.getLogger(__name__)


class RedisStreamConsumer:
	def __init__(
			self,
			redis_client: redis.Redis,
			stream_name: str,
			group_name: str,
			consumer_name: str
	):
		self.redis = redis_client
		self.stream = stream_name
		self.group = group_name
		self.consumer = consumer_name
		self._ensure_consumer_group()
	
	def _ensure_consumer_group(self):
		"""Creates the consumer group if it does not already exist."""
		try:
			self.redis.xgroup_create(self.stream, self.group, id='0', mkstream=True)
		except redis.exceptions.ResponseError as e:
			if GROUP_ALREADY_EXISTS_ERROR not in str(e):
				raise e
	
	def listen(self, callback: Callable[[Dict[str, Any]], None], block_ms: int = 2000):
		"""
		Starts an infinite loop listening for new messages.
		Passes parsed dictionary payload to the provided callback function.
		"""
		logger.info(f"Started listening to stream '{self.stream}' as consumer '{self.consumer}'")
		
		while True:
			try:
				response = self.redis.xreadgroup(
					groupname=self.group,
					consumername=self.consumer,
					streams={self.stream: READ_UNDELIVERED_MESSAGES_SYMBOL},
					count=1,
					block=block_ms
				)
				
				if not response:
					continue
				logger.info(response)
				for stream, messages in response:
					for message_id, payload in messages:
						self._handle_message(message_id, payload, callback)
			
			except redis.exceptions.ConnectionError:
				logger.error("Redis connection lost. Retrying in 5 seconds...")
				time.sleep(5)
			except Exception as e:
				logger.error(f"Unexpected error in stream listener: {e}", exc_info=True)
	
	def _handle_message(self, message_id: bytes, payload: dict, callback: Callable):
		logger.info(f"Received message '{message_id}' from consumer '{self.consumer}'")
		
		try:
			clean_payload = {k.decode('utf-8'): v.decode('utf-8') for k, v in payload.items()}
			data_str = clean_payload.get('data', '{}')
			logger.info(f"Received payload '{data_str}' from consumer '{self.consumer}'")
			data = json.loads(data_str)
			logger.info(f"Received data: {data}")
			callback(data)
			
			self.redis.xack(self.stream, self.group, message_id)
		
		except json.JSONDecodeError:
			logger.error(f"Failed to parse JSON data from message {message_id}")
		except Exception as e:
			logger.error(f"Callback failed for message {message_id}: {e}", exc_info=True)
