CREATE TABLE IF NOT EXISTS users (
    id          SERIAL PRIMARY KEY,
    telegram_chat_id BIGINT NOT NULL UNIQUE,
    username    VARCHAR(255),
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS stocks (
    id           SERIAL PRIMARY KEY,
    ticker       VARCHAR(10)  NOT NULL UNIQUE,
    company_name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS portfolio (
    id         SERIAL PRIMARY KEY,
    user_id    INTEGER NOT NULL REFERENCES users(id)  ON DELETE CASCADE,
    stock_id   INTEGER NOT NULL REFERENCES stocks(id) ON DELETE CASCADE,
    added_at   TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, stock_id)
);

-- Index for the Correlation Engine's core query:
-- "give me all users who hold ticker X"
CREATE INDEX IF NOT EXISTS idx_portfolio_stock_id ON portfolio(stock_id);

-- Index for the bot's portfolio query:
-- "give me all stocks for user X"
CREATE INDEX IF NOT EXISTS idx_portfolio_user_id ON portfolio(user_id);
