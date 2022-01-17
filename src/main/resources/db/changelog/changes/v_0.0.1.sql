--changeset julianespinel:1
CREATE TABLE symbols
(
    symbol     VARCHAR(256) PRIMARY KEY,
    name       VARCHAR(256) NOT NULL,
    created_at TIMESTAMP    NOT NULL,
    updated_at TIMESTAMP    NOT NULL
);
--rollback drop table symbols;
