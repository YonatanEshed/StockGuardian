import logging
from abc import ABC, abstractmethod
from typing import Type, TypeVar

from google.genai.types import GenerateContentConfigDict
from pydantic import BaseModel

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)


class GenericAIClient(ABC):
	@abstractmethod
	def ask_llm(self, prompt: str, system_instruction: str, expected_schema: Type[T]) -> T:
		"""Sends text to an LLM and guarantees a structured Pydantic object back"""
		pass


class GeminiClient(GenericAIClient):
	def __init__(self, api_key: str):
		from google import genai  # Lazy import to avoid loading missing packages
		self.client = genai.Client(api_key=api_key)
		logger.info("GeminiClient initialized")
	
	def ask_llm(self, prompt: str, system_instruction: str, expected_schema: Type[T]) -> T:
		config: GenerateContentConfigDict = {
			"response_mime_type": "application/json",
			"response_schema": expected_schema,
			"system_instruction": system_instruction
		}
		
		logger.info("Sending request to Gemini LLM...")
		
		response = self.client.models.generate_content(
			model="gemini-2.5-flash-lite",
			contents=prompt,
			config=config
		)
		
		logger.info(f"response: {response}")
		
		return response.parsed
