use std::fs::read_to_string;
use std::io::Error;

use serde::Deserialize;

#[derive(Default, Deserialize)]
pub(super) struct IEXConfig {
    pub environment: String,
    pub version: String,
    pub api_key: String,
}

#[derive(Default, Deserialize)]
pub(super) struct DatabaseConfig {
    pub host: String,
    pub username: String,
    pub password: String,
    pub port: String,
    pub name: String,
}

#[derive(Default, Deserialize)]
pub(super) struct Configuration {
    pub iex: IEXConfig,
    pub database: DatabaseConfig,
}

pub(super) fn read_config(config_path: &str) -> Result<Configuration, Error> {
    let content = read_to_string(config_path)?;
    let config = toml::from_str(&content)?;
    Ok(config)
}

pub(super) fn get_iex_host(iex_config: &IEXConfig) -> String {
    format!("https://{}.iexapis.com/{}", iex_config.environment, iex_config.version)
}

pub(super) fn get_database_url(db_config: DatabaseConfig) -> String {
    format!(
        "postgres://{}:{}@{}:{}/{}",
        db_config.username,
        db_config.password,
        db_config.host,
        db_config.port,
        db_config.name
    )
}
