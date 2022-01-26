# Stockreader

Stockreader is a program that downloads US stock market data and stores it in a database.

It currently supports the following operations:

| Action                     | Description                                                   |
|----------------------------|---------------------------------------------------------------|
| migrate_db_schema          | Execute database schema changes                               |
| download_symbols           | Downloads stocks symbols and names                            |
| download_stats             | Downloads basic stats from stocks                             |
| download_historical_prices | Downloads historical prices from stocks from the past 5 years |

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

IEX_BASE_URL="http://localhost/stable"
IEX_API_KEY="ak"

DB_USERNAME=username
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=stockreader_db
```

2. In the file `.env` add your IEX Cloud sandbox API key into the variable `IEX_API_KEY`:
```bash
IEX_API_KEY="" # add your sandbox api key here
```

3. Execute the tests:
```bash
cd scripts
sh test.sh
```

## Run

### DB migrations

Stockreader uses Diesel for database migrations.

You need to install Diesel CLI to be able to perform the following steps,
you can install it using this command:

```bash
cargo install diesel_cli --no-default-features --features postgres
```

If you want to create new database migration or run them (locally) without
running the whole program you can do it following these steps:

1. Start the database: `docker-compose up -d`
2. Setup Diesel migrations:
```bash
diesel setup --database-url postgres://username:password@localhost:5432/stockreader_db
```
3. Run migrations
```bash
diesel migration run --database-url postgres://username:password@localhost:5432/stockreader_db
````

Run the following commands if you need to change the database schema:

1. Add migration: `diesel migration generate <migration_name>`
2. Test your migrations can be reverted **(do not run this in prod)**: `diesel migration redo`

If you want to revert the latest migration please do:
```bash
diesel migration revert --database-url postgres://username:password@localhost:5432/stockreader_db
```

If you want to print the schema please do:
```bash
diesel print-schema --database-url postgres://username:password@localhost:5432/stockreader_db
```

### Run Locally

This program runs as an AWS Lambda.

We need to set some environment variables first:

1. In the file `.env` add your IEX Cloud sandbox API key into the variable `IEX_API_KEY`:
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
2. download_symbols: download stock symbols from IEX Cloud
```bash
curl -d '{ "action": "download_symbols" }' http://localhost:9001/2015-03-31/functions/myfunction/invocations
```

You should get the following response:
```json
{ "message": "hello <action>" }
```

## Deployment (AWS Lambda)

### AWS Setup

We need to perform the following steps to create the required infrastructure:

1. Create a VPC (VPC X), with:
    1. At least 1 public subnet (subnet A)
        1. Route table: 0.0.0.0/0 -> internet gateway
    2. Create a NAT gateway in the public subnet (subnet A)
    3. At least 2 private subnets (subnet B and C) to deploy the lambdas in different AZ
        1. Route table: 0.0.0.0/0 -> NAT gateway
2. Create an RDS database (Aurora serverless) in the VPC X
3. Create RDS database credentials as a secret in AWS Secrets Manager
4. Create Lambda function
    1. Add permissions to access RDS
    2. Add permissions to access Secrets manager
    3. Deploy the lambda in VPC X, using private subnets only (subnets B and C)

This is how the required infrastructure looks like:

![Infrastructure view](docs/stockreader-deploy-aws.jpg "Infrastructure view")

#### Why do we need this setup?

1. Because the Aurora serverless database is created in a private subnet with no
   internet access.
2. The only way to access the database is deploying the lambda function in a 
   private subnet within the same VPC that the database is deployed on.
3. The lambda function needs internet access to get data from IEX Cloud,
   that's why we need the NAT gateway.

### Deploy as a lambda function

We need to set these environment variables in the AWS Lambda console:

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
2. Upload `lambda.zip` using the AWS Lambda console
