use std::fs::read_to_string;
use std::io::Error;

use serde::Deserialize;

#[derive(Default, Deserialize)]
pub struct Configuration {
    pub environment: String,
    pub version: String,
    pub api_key: String,
}

pub fn read_config(config_path: &str) -> Result<Configuration, Error> {
    let content = read_to_string(config_path)?;
    let config = toml::from_str(&content)?;
    Ok(config)
}
