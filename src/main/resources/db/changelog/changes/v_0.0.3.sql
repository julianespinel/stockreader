-- changeset julianespinel:3
CREATE TABLE historical_prices
(
    symbol         VARCHAR,
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

    PRIMARY KEY (symbol, date),
    FOREIGN KEY (symbol) REFERENCES symbols (symbol)
);
-- rollback drop table historical_prices;
