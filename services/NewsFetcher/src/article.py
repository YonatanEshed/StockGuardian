from dataclasses import dataclass
from typing import Any


@dataclass
class Article:
	title: str
	summary: str
	url: str
	source: str
	published_at: str
	
	def to_dict(self) -> dict[str, Any]:
		return {
			"title": self.title,
			"summary": self.summary,
			"url": self.url,
			"source": self.source,
			"published_at": self.published_at
		}
	
	def __str__(self):
		return f"[{self.source}] {self.title}"
