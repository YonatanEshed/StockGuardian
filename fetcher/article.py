from dataclasses import dataclass
from typing import Optional


@dataclass
class Article:
	title: str
	description: str
	url: str
	source: str
	published_at: Optional[str] = None
	author: Optional[str] = None
	
	def __str__(self):
		return f"[{self.source}] {self.title}"
