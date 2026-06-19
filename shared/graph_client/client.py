from typing import Any, Dict, List, Optional

from neo4j import GraphDatabase


class Neo4jClient:
	def __init__(self, uri: str, user: str, password: str):
		
		self.driver = GraphDatabase.driver(uri, auth=(user, password))
	
	def _execute(self, query: str, parameters: Optional[Dict[str, Any]] = None, write: bool = False) -> List[
		Dict[str, Any]]:
		session = self.driver.session()
		try:
			def tx_worker(tx):
				return tx.run(query, parameters or {}).data()
			
			if write:
				return session.execute_write(tx_worker)
			
			return session.execute_read(tx_worker)
			
		finally:
			session.close()
	
	def run_query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
		return self._execute(query, parameters, write=False)
	
	def run_write(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
		return self._execute(query, parameters, write=True)
	
	def close(self) -> None:
		self.driver.close()


if __name__ == '__main__':
	# Example usage
	client = Neo4jClient(uri="bolt://localhost:7687", user="neo4j", password="admin123")
	try:
		# Cypher query to create an Event and link it to existing structural entities
		create_query = """
				// 1. Always create the base event node first
				CREATE (e:Event {
					headline: $headline,
					summary: $summary,
					source: $source,
					published_at: datetime($published_at),
					created_at: datetime($created_at)
				})

				// 2. Safely unpack tickers without breaking the execution flow if empty
				WITH e
				UNWIND case when $tickers is null then [null] else $tickers end AS ticker_code
				WITH e, ticker_code WHERE ticker_code IS NOT NULL
				MERGE (t:Ticker {ticker: ticker_code})
				MERGE (e)-[:AFFECTS]->(t)

				// 3. Safely unpack sectors
				WITH e
				UNWIND case when $sectors is null then [null] else $sectors end AS sector_name
				WITH e, sector_name WHERE sector_name IS NOT NULL
				MERGE (s:Sector {name: sector_name})
				MERGE (e)-[:AFFECTS]->(s)

				// 4. Safely unpack keywords
				WITH e
				UNWIND case when $keywords is null then [null] else $keywords end AS keyword_term
				WITH e, keyword_term WHERE keyword_term IS NOT NULL
				MERGE (k:Keyword {term: keyword_term})
				MERGE (e)-[:AFFECTS]->(k)

				// 5. Safely unpack competitors
				WITH e
				UNWIND case when $competitors is null then [null] else $competitors end AS comp_ticker
				WITH e, comp_ticker WHERE comp_ticker IS NOT NULL
				MERGE (c:Competitor {ticker: comp_ticker})
				MERGE (e)-[:AFFECTS]->(c)

				// 6. Gather and return what was created/linked
				WITH e
				OPTIONAL MATCH (e)-[:AFFECTS]->(target)
				RETURN elementId(e) AS event_id, collect(elementId(target)) AS connected_entity_ids
				"""
		
		# Sample data parameters representing an incoming news pipeline entry
		event_parameters = {
			"headline": "TSMC halts advanced chip production due to supply constraints",
			"summary": "A materials shortage has slowed down 3nm wafer production lines globally.",
			"source": "Bloomberg",
			"published_at": "2026-06-06T12:00:00Z",
			"created_at": "2026-06-06T12:05:00Z",
			"tickers": ["AAPL", "NVDA"],
			"sectors": ["Technology"],
			"keywords": ["semiconductor", "supply chain"],
			"competitors": ["INTC"]
		}
		
		# Execute write transaction
		result = client.run_write(create_query, event_parameters)
		print("Created Event and Links:", result)
	
	finally:
		client.close()
