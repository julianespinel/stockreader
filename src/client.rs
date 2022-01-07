use std::ops::Not;

use anyhow::anyhow;
use log::{debug, error};

use crate::models::Symbol;

pub(super) struct IEXClient<'a> {
    pub api_key: &'a str,
    pub host: &'a str,
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
}

#[cfg(test)]
mod tests {
    use httpmock::Method::GET;
    use httpmock::MockServer;

    use crate::client::IEXClient;

// new() tests

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
}
