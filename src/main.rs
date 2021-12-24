#[macro_use]
extern crate diesel;

use log::{info};
use log4rs;

use anyhow::Result;
use crate::service::Service;

mod client;
mod models;
mod repository;
mod config;
mod schema;
mod service;

#[tokio::main]
async fn main() -> Result<()> {
    log4rs::init_file("log4rs.yaml", Default::default())
        .expect("Could not initialize log4rs logger");

    info!("start");
    let config = config::read_config("config-dev.toml")?;
    let host = config::get_iex_host(&config.iex);
    let db_url = config::get_database_url(&config.database);
    info!("configuration was read");

    let iex_client = client::IEXClient { host: &host, api_key: &config.iex.api_key };
    let repository = repository::Repository { db_url: &db_url };
    let service = Service{ iex_client: &iex_client, repository: &repository };
    info!("startup is done");

    info!("start: getting symbols");
    service.get_symbols().await?;
    info!("done: getting symbols");
    info!("done");
    Ok(())
}
