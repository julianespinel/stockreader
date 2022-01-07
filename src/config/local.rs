use crate::config::env::get_env_variable;
use crate::config::models::{Configuration, DatabaseConfig, IEXConfig};

pub(super) fn get_local_config() -> Configuration {
    let iex_config = get_local_iex_config();
    let db_config = get_local_database_config();
    let local_config = Configuration { iex: iex_config, database: db_config };
    local_config
}

fn get_local_database_config() -> DatabaseConfig {
    let db_username = get_env_variable("DB_USERNAME");
    let db_password = get_env_variable("DB_PASSWORD");
    let db_host = get_env_variable("DB_HOST");
    let db_port = get_env_variable("DB_PORT");
    let db_name = get_env_variable("DB_NAME");

    let db_config = DatabaseConfig {
        username: db_username,
        password: db_password,
        host: db_host,
        port: db_port.parse::<u32>().unwrap(),
        name: db_name,
    };
    db_config
}

fn get_local_iex_config() -> IEXConfig {
    let iex_environment = get_env_variable("IEX_ENVIRONMENT");
    let iex_version = get_env_variable("IEX_VERSION");
    let iex_api_key = get_env_variable("IEX_API_KEY");

    let iex_config = IEXConfig {
        environment: iex_environment,
        version: iex_version,
        api_key: iex_api_key,
    };
    iex_config
}
