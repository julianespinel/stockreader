#[macro_use]
extern crate diesel;

use anyhow::Result;
use log::info;
use crate::config::models::Configuration;

use crate::service::Service;

pub mod config;

mod client;
mod models;
mod repository;
mod schema;
mod service;

pub async fn download_symbols(config: &Configuration) -> Result<()> {
    let host = config.iex.get_host();
    let db_url = config.database.get_url();

    let iex_client = client::IEXClient::new(&config.iex.api_key, &host);
    let repository = repository::Repository { db_url: &db_url };
    let service = Service { iex_client: &iex_client, repository: &repository };

    info!("start: getting symbols");
    service.download_symbols().await?;
    info!("done: getting symbols");
    Ok(())
}
