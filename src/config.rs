use std::fs::read_to_string;
use std::io::Error;

use serde::{Deserialize, Serialize};

#[derive(Default, Deserialize, Serialize, Clone)]
pub struct IEXConfig {
    pub environment: String,
    pub version: String,
    pub api_key: String,
}

#[derive(Default, Deserialize, Serialize)]
pub struct DatabaseConfig {
    pub host: String,
    pub username: String,
    pub password: String,
    pub port: u32,
    pub name: String,
}

#[derive(Default, Deserialize, Serialize)]
pub struct Configuration {
    pub iex: IEXConfig,
    pub database: DatabaseConfig,
}

pub fn read_config(config_path: &str) -> Result<Configuration, Error> {
    let content = read_to_string(config_path)?;
    let config = toml::from_str(&content)?;
    Ok(config)
}

pub(super) fn get_iex_host(iex_config: &IEXConfig) -> String {
    if iex_config.version.is_empty() { panic!("IEX version is empty") }
    if iex_config.environment.is_empty() { panic!("IEX environment is empty") }
    format!("https://{}.iexapis.com/{}", iex_config.environment, iex_config.version)
}

pub(super) fn get_database_url(db_config: &DatabaseConfig) -> String {
    if db_config.username.is_empty() { panic!("Database username is empty") }
    if db_config.password.is_empty() { panic!("Database password is empty") }
    if db_config.host.is_empty() { panic!("Database host is empty") }
    if db_config.port < 1 { panic!("Database port is < 1") }
    if db_config.name.is_empty() { panic!("Database name is empty") }
    format!(
        "postgres://{}:{}@{}:{}/{}",
        db_config.username,
        db_config.password,
        db_config.host,
        db_config.port,
        db_config.name
    )
}

#[cfg(test)]
mod tests {
    use crate::config::{DatabaseConfig, get_database_url, get_iex_host, IEXConfig};

    //-------------------------------------------------------------------------
    // get_iex_host tests
    //-------------------------------------------------------------------------

    #[test]
    fn get_iex_host_returns_valid_host() {
        // arrange
        let api_key = "ak";
        let version = "v1.0.0";
        let environment = "beta";
        let iex_config = IEXConfig {
            api_key: api_key.to_string(),
            version: version.to_string(),
            environment: environment.to_string(),
        };
        let expected_host = "https://beta.iexapis.com/v1.0.0";
        // act
        let real_host = get_iex_host(&iex_config);
        // assert
        assert_eq!(expected_host, real_host);
    }

    #[test]
    #[should_panic(expected = "IEX version is empty")]
    fn get_iex_host_panics_on_missing_version() {
        // arrange
        let api_key = "ak";
        let version = "";
        let environment = "beta";
        let iex_config = IEXConfig {
            api_key: api_key.to_string(),
            version: version.to_string(),
            environment: environment.to_string(),
        };
        // act
        get_iex_host(&iex_config);
    }

    #[test]
    #[should_panic(expected = "IEX environment is empty")]
    fn get_iex_host_panics_on_missing_environment() {
        // arrange
        let api_key = "ak";
        let version = "v1.0.0";
        let environment = "";
        let iex_config = IEXConfig {
            api_key: api_key.to_string(),
            version: version.to_string(),
            environment: environment.to_string(),
        };
        // act
        get_iex_host(&iex_config);
    }

    //-------------------------------------------------------------------------
    // get_database_url tests
    //-------------------------------------------------------------------------

    #[test]
    fn get_database_url_returns_valid_url() {
        // arrange
        let db_config = DatabaseConfig {
            username: "username".to_string(),
            password: "password".to_string(),
            host: "localhost".to_string(),
            port: 5432,
            name: "test_db".to_string(),
        };
        let expected_url = "postgres://username:password@localhost:5432/test_db";
        // act
        let real_url = get_database_url(&db_config);
        // assert
        assert_eq!(expected_url, real_url);
    }

    #[test]
    #[should_panic(expected = "Database password is empty")]
    fn get_database_url_panics_on_empty_password() {
        // arrange
        let db_config = DatabaseConfig {
            username: "username".to_string(),
            password: "".to_string(),
            host: "localhost".to_string(),
            port: 5432,
            name: "test_db".to_string(),
        };
        // act
        get_database_url(&db_config);
    }

    #[test]
    #[should_panic(expected = "Database port is < 1")]
    fn get_database_url_panics_on_port_less_than_1() {
        // arrange
        let db_config = DatabaseConfig {
            username: "username".to_string(),
            password: "password".to_string(),
            host: "localhost".to_string(),
            port: 0,
            name: "test_db".to_string(),
        };
        // act
        get_database_url(&db_config);
    }
}
