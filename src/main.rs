use anyhow::Result;

mod client;
mod models;
mod repository;
mod config;

#[tokio::main]
async fn main() -> Result<()> {
    let config = config::read_config("config-dev.toml")?;
    let host = format!("https://{}.iexapis.com/{}", config.environment, config.version);

    let iex_client = client::IEXClient { host: &host, api_key: &config.api_key };
    let symbols = iex_client.get_symbols().await?;
    repository::write_to_csv(symbols)?;
    Ok(())
}
