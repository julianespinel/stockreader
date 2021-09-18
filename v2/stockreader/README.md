# Stockreader

Stockreader is a system that analyses stock data from US financial markets.

**Currently this is a work in progress, I'm re-writing the system in Haskell.**

The system will do the following:

1. Load a list of stocks that it will analyse from a CSV file.
2. Download historical data for each stock during the last year.
3. Calculate the following stock data every day:
   1. Gainers
      1. Top per day
      2. Top per week
      3. Top per month
      4. Top per year
   2. Losers
      1. Top per day
      2. Top per week
      3. Top per month
      4. Top per year
   3. Volatility
      1. Highest
         1. Per week
         2. Per month
         3. Per year
      2. Lowest
         1. Per week
         2. Per month
         3. Per year
4. Send an email to a list of recipients with the stock analysis every day.

## Test

1. `git clone git@github.com:julianespinel/stockreader.git`
2. `cd stockreader`
3. `git checkout v2/update-code`
4. `cd v2/stockreader`
5. `stack test`

## Run

To run the project please follow these steps:

1. `git clone git@github.com:julianespinel/stockreader.git`
2. `cd stockreader`
3. `git checkout v2/update-code`
4. `cd v2/stockreader`
5. `stack run "resources/US_LIST_OF_SYMBOLS.csv"`
