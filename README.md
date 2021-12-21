# StockReader

## Deployment

### Local

1. Start the database: `docker-compose up -d`
2. Create migrations: `diesel setup --database-url postgres://username:password@localhost:5432/stockreader_db`
3. Run migrations: `diesel migration run`

Run the following commands if you need to change the database schema:

1. Add migration: `diesel migration generate <migration_name>`
2. Run down.sql and then up.sql (Do not run this in prod): `diesel migration redo`

### Run

```bash
cargo run
```
