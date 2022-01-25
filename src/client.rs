use std::ops::Not;

use anyhow::anyhow;
use bigdecimal::BigDecimal;
use chrono::{NaiveDate, Utc};
use log::{debug, error};
use serde::Deserialize;

use crate::models::{HistoricalPrice, Stats, Symbol};

const DATE_FORMAT: &str = "%Y-%m-%d";

pub(super) struct IEXClient<'a> {
    pub api_key: &'a str,
    pub base_url: &'a str,
}

/// Object given by IEX to represent stats from a stock
#[derive(Debug, Deserialize)]
#[serde(rename_all = "camelCase")]
struct IEXStats {
    pub marketcap: i64,
    pub shares_outstanding: i64,
    pub employees: i64,
    // #[serde(alias = "ttmEPS")]
    #[serde(rename(deserialize = "ttmEPS"))]
    pub ttm_eps: BigDecimal,
    pub ttm_dividend_rate: BigDecimal,
    pub dividend_yield: BigDecimal,
    pub next_dividend_date: String,
    pub ex_dividend_date: String,
    pub next_earnings_date: String,
    pub pe_ratio: BigDecimal,
    pub beta: BigDecimal,
}

/// Object given by IEX to represent historical prices
#[derive(Debug, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct IEXHistoricalPrice {
    pub symbol: String,
    pub date: String,
    #[serde(rename(deserialize = "fOpen"))]
    pub open: BigDecimal, // Fully adjusted open price
    #[serde(rename(deserialize = "fClose"))]
    pub close: BigDecimal, // Fully adjusted close price
    #[serde(rename(deserialize = "fHigh"))]
    pub high: BigDecimal, // Fully adjusted high price
    #[serde(rename(deserialize = "fLow"))]
    pub low: BigDecimal, // Fully adjusted low price
    #[serde(rename(deserialize = "fVolume"))]
    pub volume: i64, // Fully adjusted volume
    pub change: BigDecimal,
    pub change_percent: BigDecimal,
}

impl<'a> IEXClient<'a> {
    pub fn new(api_key: &'a str, base_url: &'a str) -> IEXClient<'a> {
        if api_key.is_empty() {
            panic!("api_key must not be empty")
        }
        if base_url.is_empty() {
            panic!("base_url must not be empty")
        }
        IEXClient { api_key, base_url }
    }

    pub async fn get_symbols(&self) -> Result<Vec<Symbol>, anyhow::Error> {
        let url = format!("{}/ref-data/symbols?token={}", self.base_url, self.api_key);
        let response = reqwest::get(&url).await?;

        if response.status().is_success().not() {
            let error_message = response.text().await?;
            error!("get_symbols: {}", error_message);
            return Err(anyhow!(error_message));
        }

        let symbols = response.json::<Vec<Symbol>>().await?;
        debug!("got {} symbols from IEX", &symbols.len());
        Ok(symbols)
    }

    pub async fn get_stats(&self, symbol: String) -> Result<Stats, anyhow::Error> {
        let url = format!(
            "{}/stock/{}/stats?token={}",
            self.base_url, symbol, self.api_key
        );
        let response = reqwest::get(&url).await?;

        if response.status().is_success().not() {
            let error_message = response.text().await?;
            error!("get_stats: {}", error_message);
            return Err(anyhow!(error_message));
        }

        let iex_stats = response.json::<IEXStats>().await?;
        debug!("got {} stats from IEX", symbol);
        let stats = to_stats(&symbol, &iex_stats);
        Ok(stats)
    }

    pub async fn get_historical_prices_last_five_years(
        &self,
        symbol: &str,
    ) -> Result<Vec<HistoricalPrice>, anyhow::Error> {
        let time_range = "5y";
        let url = format!(
            "{}/stock/{}/chart/{}?token={}",
            self.base_url, symbol, time_range, self.api_key
        );
        let response = reqwest::get(&url).await?;

        if response.status().is_success().not() {
            let error_message = response.text().await?;
            error!("get_historical_price: {}", error_message);
            return Err(anyhow!(error_message));
        }

        let iex_historical_price = response.json::<Vec<IEXHistoricalPrice>>().await?;
        debug!("got {} historical prices from IEX", symbol);
        let historical_prices = to_historical_prices(&iex_historical_price);
        Ok(historical_prices)
    }
}

fn to_historical_prices(iex_historical_prices: &Vec<IEXHistoricalPrice>) -> Vec<HistoricalPrice> {
    let mut prices = vec![];
    for iex_price in iex_historical_prices {
        let iex_date =
            date_from_string(&iex_price.date).expect("Error getting date from IEXHistoricalPrice");
        let now = Utc::now().naive_utc();

        let historical_price = HistoricalPrice {
            symbol: iex_price.symbol.to_string(),
            date: iex_date,
            open: iex_price.open.clone(),
            close: iex_price.close.clone(),
            high: iex_price.high.clone(),
            low: iex_price.low.clone(),
            volume: iex_price.volume,
            change: iex_price.change.clone(),
            change_percent: iex_price.change_percent.clone(),
            created_at: now,
            updated_at: now,
        };
        prices.push(historical_price);
    }
    prices
}

fn to_stats(symbol: &String, iex_stats: &IEXStats) -> Stats {
    let next_dividend_date = date_from_string(&iex_stats.next_dividend_date);
    let ex_dividend_date = date_from_string(&iex_stats.ex_dividend_date);
    let next_earnings_date = date_from_string(&iex_stats.next_earnings_date);
    Stats {
        symbol: symbol.to_string(),
        created_at: Utc::now().naive_utc(),
        marketcap: iex_stats.marketcap,
        shares_outstanding: iex_stats.shares_outstanding,
        employees: iex_stats.employees,
        ttm_eps: iex_stats.ttm_eps.clone(),
        ttm_dividend_rate: iex_stats.ttm_dividend_rate.clone(),
        dividend_yield: iex_stats.dividend_yield.clone(),
        next_dividend_date,
        ex_dividend_date,
        next_earnings_date,
        pe_ratio: iex_stats.pe_ratio.clone(),
        beta: iex_stats.beta.clone(),
    }
}

fn date_from_string(string: &String) -> Option<NaiveDate> {
    if string.is_empty() {
        return None;
    }
    let result = NaiveDate::parse_from_str(&string, DATE_FORMAT);
    let option = match result {
        Ok(date) => Some(date),
        Err(_) => {
            error!("Error parsing date: {}", string);
            None
        }
    };
    option
}

#[cfg(test)]
mod tests {
    use bigdecimal::BigDecimal;
    use chrono::NaiveDate;
    use httpmock::Method::GET;
    use httpmock::MockServer;

    use crate::client::{IEXClient, DATE_FORMAT};

    //-------------------------------------------------------------------------
    // new() tests
    //-------------------------------------------------------------------------

    #[test]
    fn new_given_api_key_and_base_url_returns_iex_client() {
        // arrange
        let api_key = "ak";
        let base_url = "http://localhost";
        // act
        let client = IEXClient::new(api_key, base_url);
        // assert
        assert_eq!(client.api_key, api_key);
        assert_eq!(client.base_url, base_url);
    }

    #[test]
    #[should_panic(expected = "api_key must not be empty")]
    fn new_given_empty_api_key_it_panics() {
        // arrange
        let api_key = "";
        let base_url = "http://localhost";
        // act
        IEXClient::new(api_key, base_url);
    }

    #[test]
    #[should_panic(expected = "base_url must not be empty")]
    fn new_given_empty_base_url_it_panics() {
        // arrange
        let api_key = "ak";
        let base_url = "";
        // act
        IEXClient::new(api_key, base_url);
    }

    //-------------------------------------------------------------------------
    // get_symbols() tests
    //-------------------------------------------------------------------------

    #[tokio::test]
    async fn get_symbols_returns_200() {
        // arrange
        let server = MockServer::start();

        let api_key = "ak";
        let base_url = server.base_url();
        let client = IEXClient {
            api_key,
            base_url: &base_url,
        };

        let get_symbols_mock = server.mock(|when, then| {
            when.method(GET)
                .path("/ref-data/symbols")
                .query_param("token", client.api_key);
            then.status(200)
                .header("content-type", "application/json")
                .body_from_file("tests/resources/httpmock_files/symbols.json");
        });

        // act
        let symbols = client.get_symbols().await.unwrap();
        // assert
        get_symbols_mock.assert();
        assert_eq!(symbols.len(), 3);
    }

    #[tokio::test]
    #[should_panic(expected = "The API key provided is not valid.")]
    async fn get_symbols_token_is_empty_returns_400() {
        // arrange
        let server = MockServer::start();

        let api_key = "";
        let base_url = server.base_url();
        let client = IEXClient {
            api_key,
            base_url: &base_url,
        };

        let get_symbols_mock = server.mock(|when, then| {
            when.method(GET)
                .path("/ref-data/symbols")
                .query_param("token", client.api_key);
            then.status(400)
                .header("content-type", "text/html; charset=utf-8")
                .body("The API key provided is not valid.");
        });

        // act
        client.get_symbols().await.unwrap();
        // assert
        get_symbols_mock.assert();
    }

    //-------------------------------------------------------------------------
    // get_stats() tests
    //-------------------------------------------------------------------------

    #[tokio::test]
    async fn get_stats_returns_200() {
        // arrange
        let server = MockServer::start();

        let api_key = "ak";
        let base_url = server.base_url();
        let client = IEXClient {
            api_key,
            base_url: &base_url,
        };
        let symbol = "AAPL";

        let get_stats_mock = server.mock(|when, then| {
            when.method(GET)
                .path(format!("/stock/{}/stats", symbol))
                .query_param("token", client.api_key);
            then.status(200)
                .header("content-type", "application/json")
                .body_from_file("tests/resources/httpmock_files/aapl_stats.json");
        });

        // act
        let stats = client.get_stats(symbol.to_string()).await.unwrap();
        // assert
        get_stats_mock.assert();
        assert_eq!(stats.symbol, symbol);
        assert_eq!(stats.marketcap, 2872053733394);
        assert_eq!(stats.ttm_eps, BigDecimal::from(11.67));
        assert_eq!(stats.next_dividend_date, None);

        let date =
            NaiveDate::parse_from_str("2022-01-21", DATE_FORMAT).expect("Error parsing date");
        assert_eq!(stats.next_earnings_date, Some(date));
    }

    #[tokio::test]
    async fn get_stats_returns_not_valid_json() {
        // arrange
        let server = MockServer::start();

        let api_key = "ak";
        let base_url = server.base_url();
        let client = IEXClient {
            api_key,
            base_url: &base_url,
        };
        let symbol = "AAPL";

        let get_stats_mock = server.mock(|when, then| {
            when.method(GET)
                .path(format!("/stock/{}/stats", symbol))
                .query_param("token", client.api_key);
            then.status(200)
                .header("content-type", "application/json")
                .body_from_file("tests/resources/httpmock_files/not_valid.json");
        });

        // act
        let stats = client.get_stats(symbol.to_string()).await;
        // assert
        get_stats_mock.assert();
        assert!(stats.is_err());
        assert!(stats
            .err()
            .unwrap()
            .to_string()
            .contains("error decoding response body"));
    }

    //-------------------------------------------------------------------------
    // get_historical_data_last_five_years() tests
    //-------------------------------------------------------------------------

    #[tokio::test]
    async fn get_historical_data_last_five_years_returns_200() {
        // arrange
        let server = MockServer::start();

        let api_key = "ak";
        let base_url = server.base_url();
        let client = IEXClient {
            api_key,
            base_url: &base_url,
        };
        let symbol = "AAPL";
        let time_interval = "5y";

        let get_historical_prices_mock = server.mock(|when, then| {
            when.method(GET)
                .path(format!("/stock/{}/chart/{}", symbol, time_interval))
                .query_param("token", client.api_key);
            then.status(200)
                .header("content-type", "application/json")
                .body_from_file("tests/resources/httpmock_files/aapl_historical_prices.json");
        });

        // act
        let historical_prices = client
            .get_historical_prices_last_five_years(symbol)
            .await
            .expect("error getting historical prices");

        // assert
        get_historical_prices_mock.assert();
        assert_eq!(historical_prices.len(), 5);

        let historical_price = &historical_prices[0];
        let expected_date =
            NaiveDate::parse_from_str("2022-01-18", DATE_FORMAT).expect("error getting date");

        assert_eq!(historical_price.symbol, "AAPL");
        assert_eq!(historical_price.date, expected_date);
        assert_eq!(historical_price.open, BigDecimal::from(175.59));
        assert_eq!(historical_price.close, BigDecimal::from(176.9));
        assert_eq!(historical_price.high, BigDecimal::from(179.08));
        assert_eq!(historical_price.low, BigDecimal::from(171.53));
        assert_eq!(historical_price.volume, 92092199);
        assert_eq!(
            historical_price.change,
            BigDecimal::from(-3.316723584476459)
        );
        assert_eq!(historical_price.change_percent, BigDecimal::from(-0.0193));
        assert!(historical_price.created_at.to_string().len() > 0);
        assert!(historical_price.updated_at.to_string().len() > 0);
    }
}
