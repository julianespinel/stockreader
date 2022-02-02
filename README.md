# Stockreader

Stockreader is a program that downloads US stock market data and stores it in a database.

It currently supports the following scheduled jobs:

| Job                               | Description                                   | Executed at                                   |
|-----------------------------------|-----------------------------------------------|-----------------------------------------------|
| Download symbols                  | Downloads stocks symbols and names            | Every Sunday at 00:00 UTC                     |
| Download stats                    | Downloads stocks stats                        | Every Monday at 00:00 UTC                     |
| Download prices from past 5 years | Downloads stocks prices from the past 5 years | At 3:00 UTC on the 1st and 15th of each month |

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
