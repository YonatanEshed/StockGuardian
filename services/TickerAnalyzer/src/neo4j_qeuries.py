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
