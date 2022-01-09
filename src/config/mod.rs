use crate::config::models::Configuration;

pub mod models;

mod local;
mod remote;
mod env;

const PRODUCTION: &str = "prod";

pub async fn read_config(environment: &str) -> Result<Configuration, anyhow::Error> {
    if environment == PRODUCTION {
        let prod_config = remote::get_prod_config().await?;
        return Ok(prod_config);
    }

    let local_config = local::get_local_config();
    Ok(local_config)
}
