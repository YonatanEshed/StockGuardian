from pydantic import BaseModel, field_validator


class Ticker(BaseModel):
	company_name: str
	ticker: str
	
	@field_validator("ticker")
	def uppercase_competitor_ticker(cls, v: str) -> str:
		return v.upper()


class AnalyzedTickerSchema(Ticker):
	sectors: list[str]
	keywords: list[str]
	competitors: list[Ticker]
	
	def to_dict(self) -> dict:
		return {
			"ticker": self.ticker,
			"company_name": self.company_name,
			"sectors": self.sectors,
			"keywords": self.keywords,
			"competitors": [comp.model_dump() for comp in self.competitors]
		}
