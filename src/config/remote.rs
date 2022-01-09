use anyhow::Error;
use aws_sdk_secretsmanager::Client;
use serde::Deserialize;

use crate::config::env::get_env_variable;
use crate::config::models::{Configuration, DatabaseConfig, IEXConfig};

/// Structure to describe IEX secret returned by AWS
#[derive(Debug, Deserialize)]
struct IEXSecret {
    pub environment: String,
    pub version: String,
    pub api_key: String,
}

/// Structure to describe database secret returned by AWS
#[derive(Debug, Deserialize)]
#[serde(rename_all = "camelCase")]
struct DBSecret {
    pub host: String,
    pub port: u32,
    pub db_name: String,
    pub username: String,
    pub password: String,
}

pub(super) async fn get_prod_config() -> Result<Configuration, anyhow::Error> {
    get_env_variable("AWS_REGION");
    get_env_variable("AWS_ACCESS_KEY_ID");
    get_env_variable("AWS_SECRET_ACCESS_KEY");

    let iex_secret_arn = get_env_variable("IEX_SECRET_ARN");
    let db_secret_arn = get_env_variable("DB_SECRET_ARN");
    let config = read_config_from_aws(&iex_secret_arn, &db_secret_arn).await?;
    Ok(config)
}

async fn read_config_from_aws(iex_secret_arn: &str, db_secret_arn: &str) -> Result<Configuration, anyhow::Error> {
    let iex_secret = get_iex_secret(iex_secret_arn).await?;
    let iex_config = IEXConfig {
        environment: iex_secret.environment,
        version: iex_secret.version,
        api_key: iex_secret.api_key,
    };

    let db_secret = get_db_secret(db_secret_arn).await?;
    let db_config = DatabaseConfig {
        username: db_secret.username,
        password: db_secret.password,
        host: db_secret.host,
        port: db_secret.port,
        name: db_secret.db_name,
    };

    let config = Configuration { iex: iex_config, database: db_config };
    Ok(config)
}

async fn get_iex_secret(secret_arn: &str) -> Result<IEXSecret, Error> {
    let client = get_secrets_manager_client().await;
    let response = client.get_secret_value().secret_id(secret_arn).send().await?;
    let secret_string = response.secret_string.expect("error getting IEX secret");
    let iex_secret: IEXSecret = serde_json::from_str(&secret_string)?;
    Ok(iex_secret)
}

async fn get_db_secret(secret_arn: &str) -> Result<DBSecret, Error> {
    let client = get_secrets_manager_client().await;
    let response = client.get_secret_value().secret_id(secret_arn).send().await?;
    let secret_string = response.secret_string.expect("error getting database secret");
    let db_secret: DBSecret = serde_json::from_str(&secret_string)?;
    Ok(db_secret)
}

async fn get_secrets_manager_client() -> Client {
    let shared_config = aws_config::load_from_env().await;
    let client = Client::new(&shared_config);
    client
}
