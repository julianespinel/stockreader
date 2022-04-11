-- changeset julianespinel:2
CREATE TABLE stats
(
    symbol             VARCHAR PRIMARY KEY,
    marketcap          BIGINT    NOT NULL DEFAULT 0,
    shares_outstanding BIGINT    NOT NULL DEFAULT 0,
    employees          BIGINT    NOT NULL DEFAULT 0,
    ttm_eps            DECIMAL   NOT NULL DEFAULT 0,
    ttm_dividend_rate  DECIMAL   NOT NULL DEFAULT 0,
    dividend_yield     DECIMAL   NOT NULL DEFAULT 0,
    next_dividend_date DATE,
    ex_dividend_date   DATE,
    next_earnings_date DATE,
    pe_ratio           DECIMAL   NOT NULL DEFAULT 0,
    beta               DECIMAL   NOT NULL DEFAULT 0,
    created_at         TIMESTAMP NOT NULL,
    updated_at         TIMESTAMP NOT NULL,

    FOREIGN KEY (symbol) REFERENCES symbols (symbol)
);
-- rollback drop table stats;
