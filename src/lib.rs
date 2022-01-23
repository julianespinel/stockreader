#[macro_use]
extern crate diesel;
#[macro_use]
extern crate diesel_migrations;
#[macro_use]
extern crate bigdecimal;

use anyhow::Result;
use diesel::{Connection, PgConnection};
use diesel_migrations::embed_migrations;
use log::{info, warn};

use crate::config::models::Configuration;
use crate::service::Service;

embed_migrations!("migrations/");

pub mod config;
pub mod models;

mod client;
mod repository;
mod schema;
mod service;

pub async fn execute(action: &str, config: &Configuration) -> Result<()> {
    match action {
        "migrate" => run_db_migrations(config)?,
        "download_symbols" => download_symbols(config).await?,
        "download_stats" => download_stats(config).await?,
        _ => warn!("Unknown action: {}", action)
    }
    Ok(())
}

pub fn run_db_migrations(config: &Configuration) -> Result<()> {
    let db_url = config.database.get_url();
    let conn = PgConnection::establish(&db_url)
        .expect(&format!("Cannot connect to the database: {}", db_url));
    embedded_migrations::run_with_output(&conn, &mut std::io::stdout())?;
    Ok(())
}

pub async fn download_symbols(config: &Configuration) -> Result<()> {
    let base_url = &config.iex.base_url;
    let db_url = config.database.get_url();

    let iex_client = client::IEXClient::new(&config.iex.api_key, &base_url);
    let repository = repository::Repository::new(&db_url);
    let service = Service { iex_client: &iex_client, repository: &repository };

    info!("start: getting symbols");
    service.download_symbols().await?;
    info!("done: getting symbols");
    Ok(())
}

pub async fn download_stats(config: &Configuration) -> Result<()> {
    let base_url = &config.iex.base_url;
    let db_url = config.database.get_url();

    let iex_client = client::IEXClient::new(&config.iex.api_key, base_url);
    let repository = repository::Repository::new(&db_url);
    let service = Service { iex_client: &iex_client, repository: &repository };

    info!("start: getting stats");
    service.download_stats().await?;
    info!("done: getting stats");
    Ok(())
}
