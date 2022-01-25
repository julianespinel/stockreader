-- Your SQL goes here
CREATE TABLE historical_prices
(
    symbol         VARCHAR PRIMARY KEY,
    date           DATE      NOT NULL,
    open           DECIMAL   NOT NULL DEFAULT 0,
    close          DECIMAL   NOT NULL DEFAULT 0,
    high           DECIMAL   NOT NULL DEFAULT 0,
    low            DECIMAL   NOT NULL DEFAULT 0,
    volume         BIGINT    NOT NULL DEFAULT 0,
    change         DECIMAL   NOT NULL DEFAULT 0,
    change_percent DECIMAL   NOT NULL DEFAULT 0,
    created_at     TIMESTAMP NOT NULL,
    updated_at     TIMESTAMP NOT NULL,

    FOREIGN KEY (symbol) REFERENCES symbols (symbol)
);

CREATE UNIQUE INDEX idx_historical_prices_symbol_date ON historical_prices(symbol, date);
-- Your SQL goes here
