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
