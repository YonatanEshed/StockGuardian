import logging

from google.genai.errors import ClientError

from services.TickerAnalyzer.src.analyze_response_schema import AnalyzedTickerSchema
from services.TickerAnalyzer.src.exceptions import TickerAnalysisError
from services.TickerAnalyzer.src.prompts import LLM_PROMPT_TEMPLATE, LLM_SYSTEM_INSTRUCTION
from shared.llm_client import get_ai_client

logger = logging.getLogger(__name__)


class TickerAnalyzer:
	def __init__(self, api_key: str):
		logger.info("Initializing TickerAnalyzer...")
		self.ai_client = get_ai_client(api_key)
		logger.info("AI client successfully initialized.")
	
	def analyze_ticker(self, ticker: str, existing_sectors: list[str]) -> AnalyzedTickerSchema:
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
			raise TickerAnalysisError(f"LLM request failed for {ticker}") from e
		
		logger.info(f"Successfully received LLM response for ticker: {ticker}")
		
		return response
