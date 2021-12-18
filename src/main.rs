use std::fs::read_to_string;

use serde::Deserialize;

mod client;
mod models;
mod repository;

#[derive(Default, Deserialize)]
struct Configuration {
    environment: String,
    version: String,
    api_key: String,
}

fn read_config(config_path: &str) -> std::io::Result<Configuration> {
    let content = read_to_string(config_path)?;
    let configuration = toml::from_str(&content)?;
    Ok(configuration)
}

#[tokio::main]
async fn main() {
    let config = read_config("config.toml").unwrap();
    let host = format!("https://{}.iexapis.com/{}", config.environment, config.version);

    let iex_client = client::IEXClient { host: &host, api_key: &config.api_key };
    let result = iex_client.get_symbols().await;
    let symbols = result.unwrap(); // Panic if error
    repository::write_to_csv(symbols).unwrap(); // Panic if error
}
