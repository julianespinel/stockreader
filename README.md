# StockReader

StockReader is a program that downloads US stock market data and stores it in a database.

The following data is downloaded automatically at these times:

| Job name         | Description                        | Time                  | Cron expression |
|------------------|------------------------------------|-----------------------|-----------------|
| download_symbols | Downloads stocks symbols and names | Every day at 00:00 ET |                 |

## Test

### Unit tests

To run the unit tests only, please execute the following command:

```bash
cargo test --lib
```

### Integration tests

To run all the tests (unit and integration), please do the following:

1. In the root folder of the repository, create the file `.env` with the following content:
```bash
ENV="local"
RUST_LOG="info"

IEX_ENVIRONMENT="sandbox"
IEX_VERSION="stable"
IEX_API_KEY=""

DB_USERNAME=username
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=stockreader_db
```

2. In the file `.env` add your IEXCloud sandbox API key into the variable `IEX_API_KEY`:
```bash
IEX_API_KEY="" # add your sandbox api key here
```

3. Then execute the tests:
```bash
cd scripts
sh test.sh
```

## Run

### DB migrations

If you want to create new database migrations or run them without running
the program you can do it following these steps:

1. Start the database: `docker-compose up -d`
2. Setup Diesel migrations: `diesel setup --database-url postgres://username:password@localhost:5432/stockreader_db`
3. Run migrations: `diesel migration run`

Run the following commands if you need to change the database schema:

1. Add migration: `diesel migration generate <migration_name>`
2. Run down.sql and then up.sql (Do not run this in prod): `diesel migration redo`

### Local

This program runs as an AWS Lambda.

We need to set some environment variables first:

1. In the file `.env` add your IEXCloud sandbox API key into the variable `IEX_API_KEY`:
```bash
IEX_API_KEY="" # add your sandbox API key here
```
2. To run the program please execute the following commands:
```bash
cd scripts
sh package.sh
sh deploy_locally.sh
```

This lambda function supports two actions:

1. migrate: execute database migrations
```bash
curl -d '{ "action": "migrate" }' http://localhost:9001/2015-03-31/functions/myfunction/invocations
```
2. download_symbols: download stock symbols from IEXCloud
```bash
curl -d '{ "action": "download_symbols" }' http://localhost:9001/2015-03-31/functions/myfunction/invocations
```

You should get the following response:
```json
{ "message": "hello <action>" }
```

## Deployment (AWS Lambda)

We need to set some environment variables first the AWS Lambda console:

 ```bash
ENV="prod"
RUST_LOG="info"

AWS_REGION="us-east-1"
AWS_ACCESS_KEY_ID="" # add value here
AWS_SECRET_ACCESS_KEY="" # add value here

IEX_SECRET_ARN="" # add value here
DB_SECRET_ARN="" # add value here
```

1. Create binary
```bash
cd scripts
sh package.sh
```
2. Upload `lambda.zip` to AWS Lambda console
