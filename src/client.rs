use crate::models::Symbol;

pub(super) struct IEXClient<'a> {
    pub host: &'a str,
    pub api_key: &'a str,
}

impl<'a> IEXClient<'a> {
    pub async fn get_symbols(&self) -> Result<Vec<Symbol>, reqwest::Error> {
        let url = format!("{}/ref-data/symbols?token={}", self.host, self.api_key);
        let symbols = reqwest::get(&url).await?.json::<Vec<Symbol>>().await?;
        Ok(symbols)
    }
}

#[cfg(test)]
mod tests {
    use httpmock::Method::GET;
    use httpmock::MockServer;

    use crate::client::IEXClient;

//-------------------------------------------------------------------------
    // get_iex_host tests
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
                .body_from_file("tests/httpmock_files/symbols.json");
        });

        // act
        let symbols = client.get_symbols().await.unwrap();
        // assert
        get_symbols_mock.assert();
        assert_eq!(symbols.len(), 3);
    }
}
