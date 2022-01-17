# Stockreader

Stockreader is a program that downloads US stock market data and stores it in a database.

It currently supports the following operations:

| Action           | Description                        | Time                      |
|------------------|------------------------------------|---------------------------|
| download_symbols | Downloads stocks symbols and names | Every sunday at 00:00 UTC |

## Test

### Unit tests

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
