from .client import GenericAIClient, GeminiClient


def get_ai_client(api_key: str) -> GenericAIClient:
	return GeminiClient(api_key=api_key)
