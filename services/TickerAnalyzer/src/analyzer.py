import json
import logging

from google.genai.errors import ClientError

from services.TickerAnalyzer.src.analyze_response_schema import AnalyzedTickerSchema
from shared.llm_client import get_ai_client

LLM_SYSTEM_INSTRUCTION = """
You are a specialized geopolitical risk analyst and macroeconomic graph architect. Your objective is to extract data that connects a company to real-world global news events, market shocks, and regulatory shifts.

CRITICAL GRAPH PHILOSOPHY:
A keyword is only useful if a major headline in the Wall Street Journal, Reuters, or Bloomberg could directly impact it. If a keyword cannot be linked to a real-world news catalyst (e.g., a trade ban, a budget cut, an election, a resource shortage), it must be discarded.

STRICT EXTRACTION CONSTRAINTS:
1. BAN INTERNAL TECH JARGON: Do not extract internal software mechanics or standard IT stack layers (e.g., DO NOT use 'Graph Database', 'Hybrid Cloud', 'Zero Trust').
2. TARGET NEWS VECTORS: Focus entirely on geographic exposures, defense procurement lines, specific raw material chains, legislative bills, and macro risks.
3. COMPETITOR RULE: Focus exclusively on peers who will move in tandem with this stock when a specific industry-wide macro event occurs.
"""

LLM_PROMPT_TEMPLATE = """
You are analyzing the news-catalyst blueprint for the following equity:
Ticker: {ticker}

Available Base Sectors in Graph:
{existing_sectors}

Execute your analysis strictly across the following macro dimensions, then map the findings directly to the required JSON schema fields:

--- STEP 1: MACRO SECTOR ASSIGNMENT ---
Identify up to 3 broad macro-economic sectors. Prioritize exact text matches from 'Available Base Sectors' if they apply.

--- STEP 2: NEWS-CATALYST & RISK KEYWORDS ---
Extract exactly 6 to 10 highly specific keywords representing the company's real-world operational surface area. Every keyword must be a direct bridge to potential news headlines. 

Force yourself to extract across these 4 news-reactive dimensions:
1. GEOPOLITICAL & DEFENSE VECTORS: Which military command structures, sovereign alliances, or specific regional conflicts drive their revenue?
	- Instead of 'Government Contracting': Use 'US DoD Procurement', 'NATO Defense Budgets', or 'Sovereign Intelligence Systems'.
2. LEGISLATIVE & POLICY IMPACTS: What specific laws, trade policies, or government spending bills dictate their financial health?
	- Instead of 'Regulations': Use 'NDAA Appropriations', 'EU Data Sovereignty Laws', or 'Export Control Restrictions'.
3. INDUSTRIAL & VALUE CHAIN EXPANSIONS: What real-world macro trends or critical infrastructure domains are they actively deploying into?
	- Instead of 'Enterprise Platforms': Use 'Grid Modernization', 'Healthcare Records Digitization', or 'Supply Chain Interdiction'.
4. CYBER & SYSTEMIC RISK EXPOSURES: What types of real-world crises or systemic shocks directly place this company on the frontline of news coverage?
	- Instead of 'Cybersecurity': Use 'Nation-State Cyber Attacks', 'Critical Infrastructure Protection', or 'Data Privacy Breaches'.

Map the output strictly to your specified JSON format.
"""

logger = logging.getLogger(__name__)


class TickerAnalyzer:
	def __init__(self, api_key: str):
		logger.info("Initializing TickerAnalyzer...")
		self.ai_client = get_ai_client(api_key)
		logger.info("AI client successfully initialized.")
	
	def analyze_ticker(self, ticker: str, existing_sectors: list[str]) -> AnalyzedTickerSchema | None:
		logger.info(f"Starting analysis for ticker: {ticker}")
		
		prompt = LLM_PROMPT_TEMPLATE.format(
			ticker=ticker,
			existing_sectors=existing_sectors
		)
		
		logger.info(f"Sending request to LLM for ticker: {ticker}")
		try:
			response = self.ai_client.ask_llm(
				prompt=prompt,
				system_instruction=LLM_SYSTEM_INSTRUCTION,
				expected_schema=AnalyzedTickerSchema
			)
		except ClientError as e:
			logger.error(f"Error during LLM request for ticker {ticker}: {e}")
			return None
		
		logger.info(f"Successfully received LLM response for ticker: {ticker}")
		
		return response
