import logging
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

current_dir = Path(__file__).resolve().parent


class Config(BaseSettings):
	REDIS_HOST: str = Field(default="localhost", min_length=1)
	REDIS_PORT: int = Field(default=6379, ge=1, le=65535)
	REDIS_PASSWORD: SecretStr
	
	NEXT_SERVICE_STREAM_KEY: str = Field(default="analyze-event", min_length=1)
	
	HEADLINE_CACHE_TTL_SECONDS: int = Field(default=3600 * 24 * 7, ge=1)
	
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
