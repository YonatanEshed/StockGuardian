import logging
import re
from pathlib import Path

from pydantic import Field, SecretStr, field_validator
from pydantic_core import Url
from pydantic_settings import BaseSettings, SettingsConfigDict

current_dir = Path(__file__).resolve().parent


class Config(BaseSettings):
	REDIS_HOST: str = Field(default="localhost", min_length=1)
	REDIS_PORT: int = Field(default=6379, ge=1, le=65535)
	REDIS_STREAM_KEY: str = Field(default="analyze-ticker", min_length=1)
	REDIS_GROUP_NAME: str = Field(default="ticker_analyzer_group", min_length=1)
	REDIS_CONSUMER_NAME: str = Field(default="ticker_analyzer_consumer", min_length=1)
	REDIS_BLOCK_TIMEOUT_MS: int = Field(default=2000, ge=0)
	REDIS_PASSWORD: SecretStr
	
	NEO4J_URI: Url = Field(default="bolt://localhost:7687")
	NEO4J_USER: str = Field(default="neo4j", min_length=1)
	NEO4J_PASSWORD: SecretStr
	
	LLM_API_KEY: SecretStr
	
	@field_validator("LLM_API_KEY", mode="after")
	def validate_gemini_key(cls, value: SecretStr) -> SecretStr:
		raw_key = value.get_secret_value()
		key_len = len(raw_key)
		
		if key_len not in (39, 53):
			raise ValueError(
				f"Gemini API key must be 39 or 53 characters long (got {key_len})"
			)
		
		gemini_regex = r"^(AIzaSy[a-zA-Z0-9_-]{35}|AQ\.Ab[a-zA-Z0-9_\.-]{48})$"
		
		if not re.match(gemini_regex, raw_key):
			raise ValueError(
				"Invalid Gemini API key format. Key must match a valid Google API key structure."
			)
		
		return value
	
	model_config = SettingsConfigDict(
		env_file=current_dir / ".env",
		env_file_encoding="utf-8",
		extra="ignore"
	)


logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
	handlers=[
		logging.StreamHandler()
	]
)

logger = logging.getLogger("TickerAnalyzer")

config = Config()
