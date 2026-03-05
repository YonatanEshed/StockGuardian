import re

import json5
from google import genai


class StockAnalyzer:
	def __init__(self, api_key: str):
		self.client = genai.Client(api_key=api_key)
	
	def analyze(self, stocks: list[str], headlines: list[str]) -> list[dict]:
		"""
		The function analyzes a list of stocks based on news headlines
		:param stocks: list of stock names
		:param headlines: list of headlines
		:return: list of dictionaries with keys 'stock', 'ranking', 'explanation'
		"""
		prompt = f"""Analyze these stocks: {", ".join(stocks)}
				News headlines: {", ".join(headlines)}
				Return a JSON array where each item has:
				- "stock": ticker symbol
				- "ranking": integer 1–5, where:
					- 1 = strong downward signal (URGENT)
					- 2 = mild downward signal
					- 3 = neutral or irrelevant
					- 4 = mild upward signal
					- 5 = strong upward signal (URGENT)
					Reserve 1 and 5 ONLY for major, immediate impact events (e.g. earnings beats/misses, scandals, regulatory action, M&A). Default to 2–4 for ordinary news.
				- "explanation": one sentence max.
				Return only valid JSON, no commentary."""
		
		response = self.client.models.generate_content(
			model="gemini-2.5-flash",
			contents=prompt,
		)
		
		return self.__parse_output(response.text)
	
	def __parse_output(self, output: str) -> list[dict]:
		"""
		Parse the AI output into a list of dictionaries
		:param output: string response that holds a json object
		:return: list of dictionaries with keys 'stock', 'ranking', 'explanation'
		"""
		match = re.search(r"```json\s*(.*?)\s*```", output, re.DOTALL)
		
		json_str = match.group(1) if match else output
		
		return json5.loads(json_str)
