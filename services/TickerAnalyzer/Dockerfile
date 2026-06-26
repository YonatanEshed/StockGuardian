FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

COPY services/TickerAnalyzer/requirements.txt ./services/TickerAnalyzer/requirements.txt
COPY shared/llm_client/requirements.txt ./shared/llm_client/requirements.txt
COPY shared/graph_client/requirements.txt ./shared/graph_client/requirements.txt
COPY shared/redis_helper/requirements.txt ./shared/redis_helper/requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r ./services/TickerAnalyzer/requirements.txt \
    && pip install --no-cache-dir -r ./shared/llm_client/requirements.txt \
    && pip install --no-cache-dir -r ./shared/graph_client/requirements.txt \
    && pip install --no-cache-dir -r ./shared/redis_helper/requirements.txt

COPY services/TickerAnalyzer ./services/TickerAnalyzer
COPY shared ./shared

WORKDIR /app/services/TickerAnalyzer

CMD ["python", "src/main.py"]
