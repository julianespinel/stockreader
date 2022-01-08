#[macro_use]
extern crate diesel_migrations;

use std::env;

use diesel::{Connection, PgConnection};
use diesel_migrations::embed_migrations;
use log::info;

use stockreader::config;

embed_migrations!("migrations/");

#[tokio::main]
async fn main() -> Result<(), anyhow::Error> {
    env_logger::init();

    let environment = env::var("ENV")
        .expect("ENV environment variable is not set");
    let config = config::read_config(&environment).await?;
    let db_url = config.database.get_url();
    info!("configuration was read");

    // Run database migrations
    let conn = PgConnection::establish(&db_url)
        .expect(&format!("Cannot connect to database: {}", db_url));
    embedded_migrations::run_with_output(&conn, &mut std::io::stdout())?;
    info!("startup is done");

    // let func = handler_fn(func);
    // lambda_runtime::run(func).await?;
    // Ok(())

    info!("start");
    stockreader::download_symbols(&config).await?;
    info!("done");
    Ok(())
}
