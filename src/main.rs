#[macro_use]
extern crate diesel;

use anyhow::Result;

mod client;
mod models;
mod repository;
mod config;
mod schema;

#[tokio::main]
async fn main() -> Result<()> {
    let config = config::read_config("config-dev.toml")?;
    let host = config::get_iex_host(&config.iex);
    let db_url = config::get_database_url(config.database);

    let iex_client = client::IEXClient { host: &host, api_key: &config.iex.api_key };
    let symbols = iex_client.get_symbols().await?;
    repository::save_symbols(&db_url, symbols)?;
    Ok(())
}
