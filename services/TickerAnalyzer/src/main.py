from typing import Any

import redis

from config import config, logger
from services.TickerAnalyzer.src.analyzer import TickerAnalyzer
from shared.graph_client import Neo4jClient
from shared.redis_helper import RedisStreamConsumer

TICKER_ALREADY_EXISTS_QUERY = """
OPTIONAL MATCH (t:Ticker { ticker: $ticker })
RETURN t IS NOT NULL AS exists
"""

GET_ALL_SECTORS_QUERY = """
MATCH (s:Sector)
RETURN s.name AS sector_name
"""

WRITE_ANALYZED_NODES_QUERY = """
MERGE (t:Ticker { ticker: $ticker })
ON CREATE SET
	t.company_name = $company_name,
	t.added_at = datetime()
ON MATCH SET
	t.company_name = $company_name

WITH t
UNWIND $sectors AS sector_name
MERGE (s:Sector { name: sector_name })
MERGE (t)-[:IN_SECTOR]->(s)

WITH t
UNWIND $competitors AS comp
MERGE (c:Ticker { ticker: comp.ticker })
ON CREATE SET
	c.company_name = comp.company_name,
	c.added_at = datetime()
MERGE (t)-[:HAS_COMPETITOR]->(c)

WITH t
UNWIND $keywords AS kw_term
MERGE (k:Keyword { term: kw_term })
MERGE (t)-[:RELATED_TO]->(k)

RETURN t.ticker AS processed_ticker
"""


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
		
		logger.info(f"Analyzing ticker: {ticker}")
		analysis_result = self.analyzer.analyze_ticker(ticker, existing_sectors)
		
		if not analysis_result:
			logger.error(f"Analysis failed for ticker: {ticker}. No result returned.")
			return
		
		logger.info(f"analyzing result: {analysis_result}")
		
		self.neo4j_client.run_write(WRITE_ANALYZED_NODES_QUERY, parameters=analysis_result.to_dict())
		
		logger.info(f"Successfully saved {ticker} metrics.")


def main():
	service = TickerAnalyzerService()
	service.run()


if __name__ == '__main__':
	main()
