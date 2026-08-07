from typing import Any

import redis

from config import config, logger
from services.TickerAnalyzer.src.analyzer import TickerAnalyzer
from services.TickerAnalyzer.src.exceptions import TickerAnalysisError
from services.TickerAnalyzer.src.neo4j_qeuries import TICKER_ALREADY_EXISTS_QUERY, GET_ALL_SECTORS_QUERY, \
	WRITE_ANALYZED_NODES_QUERY
from shared.graph_client import Neo4jClient
from shared.redis_helper import RedisStreamConsumer


class TickerAnalyzerService(RedisStreamConsumer):
	"""Main service class for TickerAnalyzer."""
	
	def __init__(self):
		try:
			redis_client = redis.Redis(
				password=config.REDIS_PASSWORD.get_secret_value() if config.REDIS_PASSWORD else None,
				host=config.REDIS_HOST,
				port=config.REDIS_PORT
			)
			
			self.neo4j_client = Neo4jClient(
				uri=str(config.NEO4J_URI),
				user=config.NEO4J_USER,
				password=config.NEO4J_PASSWORD.get_secret_value()
			
			)
			
			self.analyzer = TickerAnalyzer(
				api_key=config.LLM_API_KEY.get_secret_value()
			)
			
			super().__init__(
				redis_client=redis_client,
				stream_name=config.REDIS_STREAM_KEY,
				group_name=config.REDIS_GROUP_NAME,
				consumer_name=config.REDIS_CONSUMER_NAME
			)
			
			logger.info("TickerAnalyzer service successfully initialized.")
		except Exception as e:
			logger.critical(f"Initialization failure: {e}")
			return
	
	def handle_event(self, data: dict[str, Any]) -> None:
		ticker = data.get("ticker")
		
		if not ticker:
			logger.warning("Missing 'ticker' in data. Skipping message.")
			return
		
		ticker = ticker.upper()
		
		exists_result = self.neo4j_client.run_query(TICKER_ALREADY_EXISTS_QUERY, parameters={"ticker": ticker})
		if exists_result and exists_result[0].get("exists"):
			logger.info(f"Ticker '{ticker}' already exists in the graph. Skipping analysis.")
			return
		
		existing_sectors = self.neo4j_client.run_query(GET_ALL_SECTORS_QUERY)
		existing_sectors = [sector.get("sector_name") for sector in existing_sectors]
		
		logger.info(f"Existing sectors({len(existing_sectors)}): {existing_sectors}")
		
		try:
			logger.info(f"Analyzing ticker: {ticker}")
			analysis_result = self.analyzer.analyze_ticker(ticker, existing_sectors)
		except TickerAnalysisError:
			logger.error(f"Analysis failed for ticker: {ticker}")
			return
		
		logger.info(f"analyzing result: {analysis_result}")
		
		self.neo4j_client.run_write(WRITE_ANALYZED_NODES_QUERY, parameters=analysis_result.to_dict())
		
		logger.info(f"Successfully saved {ticker} metrics.")


def main():
	service = TickerAnalyzerService()
	service.run()


if __name__ == '__main__':
	main()
