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
