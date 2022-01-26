#[macro_use]
extern crate diesel_migrations;

use diesel_migrations::embed_migrations;
use httpmock::MockServer;
use testcontainers::clients;

use stockreader::models::Symbol;

embed_migrations!("migrations/");

const POSTGRES_CONTAINER_PORT: u16 = 5432;

//------------------------------------------------------------------------------
// test cases
//------------------------------------------------------------------------------

/// Integration test for the function `download_symbols`.
///
/// This test case does the following:
/// 1. Reads the configuration file from environment variables.
/// 1. Creates a docker container with an empty Postgres test database.
/// 1. Runs the Diesel migrations into the test database.
/// 1. Creates a http mock server to mock the IEX Cloud API.
/// 1. Updates the environment variables to use Postgres and HTTPMock:
///     1. Updates the database port of the docker container in the environment variable.
///     1. Updates the base_url of the IEX client in the environment variable.
/// 1. Executes the `download_symbols` function using the given configuration.
/// 1. Checks that the symbols has been inserted in the database.
#[tokio::test]
async fn download_symbols_adds_symbols_to_database() {
    // arrange
    let environment = "test";
    let config = stockreader::config::read_config(environment)
        .await
        .expect("error getting configuration values");

    let docker = clients::Cli::default();
    let container = containers::start_postgres_container(&config.database, &docker);
    let db_port = container.get_host_port(POSTGRES_CONTAINER_PORT).unwrap();
    let db_url = databases::get_test_db_url(&config.database, &db_port);
    databases::execute_db_migrations(&db_url);

    let server = MockServer::start();
    let iex_base_url = server.base_url();
    let get_symbols_mock =
        http_mocks::configure_iex_to_return_list_of_symbols(&server, &config.iex);
    let expected_symbols_size = 3;

    let updated_config = configs::get_config_with_correct_db_port_and_iex_base_url(
        environment,
        db_port,
        &iex_base_url,
    )
    .await;

    // act
    stockreader::download_symbols(&updated_config)
        .await
        .expect("Error downloading symbols");

    // assert
    get_symbols_mock.assert();
    let symbols_count = databases::get_symbols_count(&db_url).await;
    assert_eq!(symbols_count, expected_symbols_size);
}

/// Integration test for the function `download_stats`.
///
/// This test case does the following:
/// 1. Reads the configuration file from environment variables.
/// 1. Creates a docker container with an empty Postgres test database.
/// 1. Runs the Diesel migrations into the test database.
/// 1. Creates a http mock server to mock the IEX Cloud API.
/// 1. Updates the environment variables to use Postgres and HTTPMock:
///     1. Updates the database port of the docker container in the environment variable.
///     1. Updates the base_url of the IEX client in the environment variable.
/// 1. Inserts three symbols in the database.
/// 1. Executes the `download_stats` function using the given configuration.
/// 1. Checks that the stats has been inserted in the database.
#[tokio::test]
async fn download_stats_adds_stats_to_database() {
    // arrange
    let environment = "test";
    let config = stockreader::config::read_config(environment)
        .await
        .expect("error getting configuration values");

    let docker = clients::Cli::default();
    let container = containers::start_postgres_container(&config.database, &docker);
    let db_port = container.get_host_port(POSTGRES_CONTAINER_PORT).unwrap();
    let db_url = databases::get_test_db_url(&config.database, &db_port);
    databases::execute_db_migrations(&db_url);

    let server = MockServer::start();
    let iex_base_url = server.base_url();

    let a_symbol = Symbol {
        symbol: "A".to_string(),
        name: "A Inc".to_string(),
    };
    databases::insert_symbol(&db_url, &a_symbol).await;
    let aa_symbol = Symbol {
        symbol: "AA".to_string(),
        name: "AA Inc".to_string(),
    };
    databases::insert_symbol(&db_url, &aa_symbol).await;
    let aaa_symbol = Symbol {
        symbol: "AAA".to_string(),
        name: "AAA Inc".to_string(),
    };
    databases::insert_symbol(&db_url, &aaa_symbol).await;

    let get_a_stats_mock =
        http_mocks::configure_iex_to_return_stats(&server, &config.iex, &a_symbol.symbol);
    let get_aa_stats_mock =
        http_mocks::configure_iex_to_return_stats(&server, &config.iex, &aa_symbol.symbol);
    let get_aaa_stats_mock =
        http_mocks::configure_iex_to_return_stats(&server, &config.iex, &aaa_symbol.symbol);

    let updated_config = configs::get_config_with_correct_db_port_and_iex_base_url(
        environment,
        db_port,
        &iex_base_url,
    )
    .await;

    // act
    stockreader::download_stats(&updated_config)
        .await
        .expect("Error downloading stats");

    // assert
    get_a_stats_mock.assert();
    get_aa_stats_mock.assert();
    get_aaa_stats_mock.assert();
    let stats_count = databases::get_stats_count(&db_url).await;
    assert_eq!(stats_count, 3);
}

/// Integration test for the function `download_historical_prices`.
///
/// This test case does the following:
/// 1. Reads the configuration file from environment variables.
/// 1. Creates a docker container with an empty Postgres test database.
/// 1. Runs the Diesel migrations into the test database.
/// 1. Creates a http mock server to mock the IEX Cloud API.
/// 1. Updates the environment variables to use Postgres and HTTPMock:
///     1. Updates the database port of the docker container in the environment variable.
///     1. Updates the base_url of the IEX client in the environment variable.
/// 1. Inserts one symbol into the database.
/// 1. Executes the `download_historical_prices` function using the given configuration.
/// 1. Checks that the historical prices have been inserted in the database.
#[tokio::test]
async fn download_historical_prices_adds_historical_prices_to_the_database() {
    // arrange
    let environment = "test";
    let config = stockreader::config::read_config(environment)
        .await
        .expect("error getting configuration values");

    let docker = clients::Cli::default();
    let container = containers::start_postgres_container(&config.database, &docker);
    let db_port = container.get_host_port(POSTGRES_CONTAINER_PORT).unwrap();
    let db_url = databases::get_test_db_url(&config.database, &db_port);
    databases::execute_db_migrations(&db_url);

    let server = MockServer::start();
    let iex_base_url = server.base_url();

    let apple = Symbol {
        symbol: "AAPL".to_string(),
        name: "Apple Inc".to_string(),
    };
    databases::insert_symbol(&db_url, &apple).await;

    let get_apple_historical_prices_mock = http_mocks::configure_iex_to_return_historical_prices(
        &server,
        &config.iex,
        &apple.symbol,
    );

    let updated_config = configs::get_config_with_correct_db_port_and_iex_base_url(
        environment,
        db_port,
        &iex_base_url,
    )
    .await;

    // act
    stockreader::download_historical_prices(&updated_config)
        .await
        .expect("Error downloading historical prices");

    // assert
    get_apple_historical_prices_mock.assert();
    let historical_prices_count = databases::get_historical_prices_count(&db_url).await;
    assert_eq!(historical_prices_count, 5);
}

//------------------------------------------------------------------------------
// helper modules for tests
//------------------------------------------------------------------------------

mod containers {
    use testcontainers::clients::Cli;
    use testcontainers::images::generic::{GenericImage, WaitFor};
    use testcontainers::{images, Container, Docker};

    use stockreader::config::models::DatabaseConfig;

    pub(super) fn start_postgres_container<'a>(
        db_config: &DatabaseConfig,
        docker: &'a Cli,
    ) -> Container<'a, Cli, GenericImage> {
        let generic_postgres = images::generic::GenericImage::new("postgres")
            .with_wait_for(WaitFor::message_on_stderr(
                "database system is ready to accept connections",
            ))
            .with_env_var("POSTGRES_USER", &db_config.username)
            .with_env_var("POSTGRES_PASSWORD", &db_config.password)
            .with_env_var("POSTGRES_DB", &db_config.name);

        let container = docker.run(generic_postgres);
        container
    }
}

mod databases {
    use diesel::{Connection, PgConnection};
    use tokio_postgres::types::ToSql;
    use tokio_postgres::Client;

    use stockreader::config::models::DatabaseConfig;
    use stockreader::models::Symbol;

    use crate::embedded_migrations;

    pub(super) fn get_test_db_url<'a>(db_config: &'a DatabaseConfig, host_port: &'a u16) -> String {
        let db_url = format!(
            "postgres://{}:{}@{}:{}/{}",
            db_config.username, db_config.password, db_config.host, host_port, db_config.name
        );
        db_url
    }

    pub(super) fn execute_db_migrations(db_url: &str) {
        let conn = PgConnection::establish(db_url)
            .expect(&format!("Cannot connect to database: {}", db_url));

        embedded_migrations::run(&conn).expect("error running diesel migrations");
    }

    pub(super) async fn get_postgres_client(db_url: &str) -> Client {
        let (client, connection) = tokio_postgres::connect(db_url, postgres::NoTls)
            .await
            .expect("error connecting to postgres");

        tokio::spawn(async move {
            if let Err(e) = connection.await {
                eprintln!("connection error: {}", e);
            }
        });

        client
    }

    pub(super) async fn get_symbols_count(db_url: &String) -> i64 {
        let pg_client = get_postgres_client(&db_url).await;
        let row = pg_client
            .query_one("select count(*) from symbols", &[])
            .await
            .expect("error counting symbols");
        let symbols_count: i64 = row.get(0);
        symbols_count
    }

    pub(super) async fn get_stats_count(db_url: &String) -> i64 {
        let pg_client = get_postgres_client(&db_url).await;
        let row = pg_client
            .query_one("select count(*) from stats", &[])
            .await
            .expect("error counting stats");
        let stats_count: i64 = row.get(0);
        stats_count
    }

    pub(super) async fn get_historical_prices_count(db_url: &String) -> i64 {
        let pg_client = get_postgres_client(&db_url).await;
        let row = pg_client
            .query_one("select count(*) from historical_prices", &[])
            .await
            .expect("error counting historical prices");
        let historical_prices_count: i64 = row.get(0);
        historical_prices_count
    }

    pub(crate) async fn insert_symbol(db_url: &str, symbol: &Symbol) {
        let pg_client = get_postgres_client(db_url).await;
        let insert_statement = pg_client
            .prepare("INSERT INTO symbols (symbol, name) VALUES ($1, $2)")
            .await
            .expect("Error creating insert statement");

        let mut params: Vec<&(dyn ToSql + Sync)> = Vec::new();
        params.push(&symbol.symbol);
        params.push(&symbol.name);

        pg_client
            .execute(&insert_statement, &params)
            .await
            .expect("error inserting symbols");
    }
}

mod http_mocks {
    use httpmock::Method::GET;
    use httpmock::{Mock, MockServer};

    use stockreader::config::models::IEXConfig;

    pub(super) fn configure_iex_to_return_list_of_symbols<'a>(
        server: &'a MockServer,
        iex_config: &'a IEXConfig,
    ) -> Mock<'a> {
        let get_symbols_mock = server.mock(|when, then| {
            when.method(GET)
                .path("/ref-data/symbols")
                .query_param("token", &iex_config.api_key);
            then.status(200)
                .header("content-type", "application/json")
                .body_from_file("tests/resources/httpmock_files/symbols.json");
        });
        get_symbols_mock
    }

    pub(super) fn configure_iex_to_return_stats<'a>(
        server: &'a MockServer,
        iex_config: &'a IEXConfig,
        symbol: &'a str,
    ) -> Mock<'a> {
        let endpoint_path = format!("/stock/{}/stats", &symbol);
        let file_path = format!("tests/resources/httpmock_files/{}_stats.json", symbol);
        let get_symbols_mock = server.mock(|when, then| {
            when.method(GET)
                .path(endpoint_path)
                .query_param("token", &iex_config.api_key);
            then.status(200)
                .header("content-type", "application/json")
                .body_from_file(file_path);
        });
        get_symbols_mock
    }

    pub(super) fn configure_iex_to_return_historical_prices<'a>(
        server: &'a MockServer,
        iex_config: &'a IEXConfig,
        symbol: &'a str,
    ) -> Mock<'a> {
        let time_interval = "5y";
        let endpoint_path = format!("/stock/{}/chart/{}", symbol, time_interval);
        let file_path = "tests/resources/httpmock_files/aapl_historical_prices.json";
        let get_symbols_mock = server.mock(|when, then| {
            when.method(GET)
                .path(endpoint_path)
                .query_param("token", &iex_config.api_key);
            then.status(200)
                .header("content-type", "application/json")
                .body_from_file(file_path);
        });
        get_symbols_mock
    }
}

mod configs {
    use std::env::set_var;

    use stockreader::config::models::Configuration;
    use stockreader::config::read_config;

    pub(super) async fn get_config_with_correct_db_port_and_iex_base_url(
        environment: &str,
        db_port: u16,
        iex_base_url: &str,
    ) -> Configuration {
        // Update port with the one used by the container
        set_var("DB_PORT", db_port.to_string());
        set_var("IEX_BASE_URL", iex_base_url);
        read_config(environment)
            .await
            .expect("error reading updated configuration")
    }
}
