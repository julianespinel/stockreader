# Stockreader

Stockreader is a program that downloads US stock market data and stores it in a database.

It currently supports the following scheduled jobs:

| Job                               | Description                                     | Executed at                |
|-----------------------------------|-------------------------------------------------|----------------------------|
| Download symbols                  | Downloads US stock symbols and names            | Every weekday at 06:00 UTC |
| Download stats                    | Downloads US stock stats                        | Every Sunday at 00:00 UTC  |
| Download prices from previous day | Downloads US stock prices from the previous day | Every weekday at 07:00 UTC |

## Test

To run the tests please execute the following command:

```bash
make test
```

## DB migrations

Database migrations will be executed automatically on startup.

To create a new database migration we need to do the following:

1. Create a new sql file in: `src/main/resources/db/changelog/changes/`
2. Restart the program to execute the new migration

## Run

### Local

To run the program in our localhost please do the following:

1. Add your IEXCloud API key to the file: `src/main/resources/application-local.properties`

```properties
iex.api_key=<your_API_key_here>
```

2. Run the project locally:

```bash
make run
```

### Current cost in IEX credits

| Job                               | IEX credits per execution        | IEX credits per month |
|-----------------------------------|----------------------------------|-----------------------|
| Download symbols                  | 0                                | 0                     |
| Download stats                    | 5 * symbol = 5 * 11_000 = 55_000 | 55_000 * 4 = 220_000  |
| Download prices from previous day | 2 * symbol = 2 * 11_000 = 22_000 | 22_000 * 20 = 440_000 |

Total IEX prices per month = 0 + 220_000 + 440_000 = 663_000

Source:

- https://iexcloud.io/docs/api/#iex-symbols
- https://iexcloud.io/docs/api/#stats-basic
- https://iexcloud.io/docs/api/#previous-day-price
