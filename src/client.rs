use std::ops::Not;
use anyhow::anyhow;
use bigdecimal::BigDecimal;
use chrono::{NaiveDate, Utc};
use log::{debug, error};
use serde::Deserialize;

use crate::models::{Stats, Symbol};

const DATE_FORMAT: &str = "%Y-%m-%d";

pub(super) struct IEXClient<'a> {
    pub api_key: &'a str,
    pub host: &'a str,
}

#[derive(Debug, Deserialize)]
#[serde(rename_all = "camelCase")]
struct IEXStats {
    pub marketcap: i64,
    pub shares_outstanding: i64,
    pub employees: i64,
    #[serde(alias = "ttmEPS")]
    pub ttm_eps: BigDecimal,
    pub ttm_dividend_rate: BigDecimal,
    pub dividend_yield: BigDecimal,
    pub next_dividend_date: String,
    pub ex_dividend_date: String,
    pub next_earnings_date: String,
    pub pe_ratio: BigDecimal,
    pub beta: BigDecimal,
}

impl<'a> IEXClient<'a> {
    pub fn new(api_key: &'a str, host: &'a str) -> IEXClient<'a> {
        if api_key.is_empty() { panic!("api_key must not be empty") }
        if host.is_empty() { panic!("host must not be empty") }
        IEXClient { api_key, host }
    }

    pub async fn get_symbols(&self) -> Result<Vec<Symbol>, anyhow::Error> {
        let url = format!("{}/ref-data/symbols?token={}", self.host, self.api_key);
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
        let url = format!("{}/stock/{}/stats?token={}", self.host, symbol, self.api_key);
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
        },
    };
    option
}

#[cfg(test)]
mod tests {
    use bigdecimal::BigDecimal;
    use chrono::NaiveDate;
    use httpmock::Method::GET;
    use httpmock::MockServer;

    use crate::client::{DATE_FORMAT, IEXClient};

//-------------------------------------------------------------------------
// new() tests
//-------------------------------------------------------------------------

    #[test]
    fn new_given_api_key_and_host_returns_iex_client() {
        // arrange
        let api_key = "ak";
        let host = "http://localhost";
        // act
        let client = IEXClient::new(api_key, host);
        // assert
        assert_eq!(client.api_key, api_key);
        assert_eq!(client.host, host);
    }

    #[test]
    #[should_panic(expected = "api_key must not be empty")]
    fn new_given_empty_api_key_it_panics() {
        // arrange
        let api_key = "";
        let host = "http://localhost";
        // act
        IEXClient::new(api_key, host);
    }

    #[test]
    #[should_panic(expected = "host must not be empty")]
    fn new_given_empty_host_it_panics() {
        // arrange
        let api_key = "ak";
        let host = "";
        // act
        IEXClient::new(api_key, host);
    }

//-------------------------------------------------------------------------
// get_symbols() tests
//-------------------------------------------------------------------------

    #[tokio::test]
    async fn get_symbols_returns_200() {
        // arrange
        let server = MockServer::start();

        let api_key = "ak";
        let host = server.base_url();
        let client = IEXClient { api_key, host: &host };

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
        let host = server.base_url();
        let client = IEXClient { api_key, host: &host };

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
        let host = server.base_url();
        let client = IEXClient { api_key, host: &host };
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
        let stats = client
            .get_stats(symbol.to_string())
            .await.unwrap();
        // assert
        get_stats_mock.assert();
        assert_eq!(stats.symbol, symbol);
        assert_eq!(stats.marketcap, 2872053733394);
        assert_eq!(stats.ttm_eps, BigDecimal::from(11.67));
        assert_eq!(stats.next_dividend_date, None);

        let date = NaiveDate::parse_from_str("2022-01-21", DATE_FORMAT)
            .expect("Error parsing date");
        assert_eq!(stats.next_earnings_date, Some(date));

    }
}
