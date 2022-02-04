-- changeset julianespinel:3
CREATE TABLE prices
(
    symbol         VARCHAR,
    date           DATE      NOT NULL,
    open           DECIMAL,
    close          DECIMAL,
    high           DECIMAL,
    low            DECIMAL,
    volume         BIGINT,
    change         DECIMAL,
    change_percent DECIMAL,
    created_at     TIMESTAMP NOT NULL,
    updated_at     TIMESTAMP NOT NULL,

    PRIMARY KEY (symbol, date),
    FOREIGN KEY (symbol) REFERENCES symbols (symbol)
);
-- rollback drop table prices;
