import json
import os

from dotenv import load_dotenv

from analyzer.stock_analyzer import StockAnalyzer
from fetcher.news_fetcher import NewsFetcher

load_dotenv(verbose=True)

API_KEY = os.getenv("API_KEY")

stocks = [
	"NASDAQ: PLTR",
	"NASDAQ: QQQ",
	"NASDAQ: NVDA",
	"NYSEARCA: SLV",
	"NYSEARCA: USO",
	"TLV: 137",
	"BATS: ITA"
]

news_fetcher = NewsFetcher()
articles = news_fetcher.get_headlines(source="ft", max_results=5)
headlines = []

for article in articles:
	print(article)
	headlines.append(f'"{article.title}"')

stock_analyzer = StockAnalyzer(API_KEY)
analyzed_data = stock_analyzer.analyze(stocks, headlines)
print(analyzed_data)
with open("results.json", "w") as file:
	file.write(json.dumps(analyzed_data, indent=4))
