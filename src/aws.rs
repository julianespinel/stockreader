use anyhow::Error;
use aws_sdk_secretsmanager::{Client, Region};
use aws_sdk_secretsmanager::output::GetSecretValueOutput;
use serde::Deserialize;

/// Structure to describe IEX secret returned by AWS
#[derive(Debug, Deserialize)]
pub struct IEXSecret {
    pub environment: String,
    pub version: String,
    pub api_key: String,
}

/// Structure to describe database secret returned by AWS
#[derive(Debug, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct DBSecret {
    pub db_instance_identifier: String,
    pub engine: String,
    pub host: String,
    pub port: u32,
    pub db_name: String,
    pub resource_id: String,
    pub username: String,
    pub password: String,
}

pub async fn get_iex_secret(region_name: &str, secret_arn: &str) -> Result<IEXSecret, Error> {
    let client = get_secrets_manager_client(region_name).await;
    let response = client.get_secret_value().secret_id(secret_arn).send().await?;
    let secret_string = response.secret_string.expect("error getting IEX secret");
    let iex_secret: IEXSecret = serde_json::from_str(&secret_string)?;
    Ok(iex_secret)
}

pub async fn get_db_secret(region_name: &str, secret_arn: &str) -> Result<DBSecret, Error> {
    let client = get_secrets_manager_client(region_name).await;
    let response = client.get_secret_value().secret_id(secret_arn).send().await?;
    let secret_string = response.secret_string.expect("error getting database secret");
    let db_secret: DBSecret = serde_json::from_str(&secret_string)?;
    Ok(db_secret)
}

async fn get_secrets_manager_client(region_name: &str) -> Client {
    let region = Region::new(region_name.to_string());
    let shared_config = aws_config::from_env().region(region).load().await;
    let client = Client::new(&shared_config);
    client
}
