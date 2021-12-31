#[macro_use]
extern crate diesel_migrations;

use std::fs::write;

use diesel::{Connection, PgConnection};
use diesel_migrations::embed_migrations;
use testcontainers::{clients, Container, Docker, images};
use testcontainers::clients::Cli;
use testcontainers::images::generic::{GenericImage, WaitFor};
use tokio_postgres::Client;

use stockreader::config::{Configuration, DatabaseConfig};

embed_migrations!("migrations/");

const POSTGRES_CONTAINER_PORT: u16 = 5432;

//------------------------------------------------------------------------------
// test cases
//------------------------------------------------------------------------------

/// Integration test for the function `download_symbols`.
///
/// This test case does the following:
/// 1. Reads a config file for the test environment.
/// 1. Creates a docker container with an empty Postgres test database.
/// 1. Runs the Diesel migrations into the test database.
/// 1. Updates the host port of the docker container in the test config file.
/// 1. Executes the `download_symbols` function using the test config file.
/// 1. Checks that the symbols has been inserted into the database.
#[tokio::test]
async fn download_symbols_adds_symbols_to_database() {
    // arrange
    let config_file_path = "config-test.toml";
    let config = &stockreader::config::read_config(config_file_path)
        .expect(&format!("error reading config file: {}", config_file_path));

    let docker = clients::Cli::default();
    let container = start_postgres_container(&config, &docker);
    let host_port = container.get_host_port(POSTGRES_CONTAINER_PORT).unwrap();
    let db_url = get_test_db_url(&config, &host_port);

    execute_db_migrations(&db_url);
    update_database_port_in_config_file(config, host_port, config_file_path);

    // act
    stockreader::download_symbols(config_file_path).await
        .expect("Expected to download symbols");

    // assert
    let pg_client = get_postgres_client(&db_url).await;

    let row = pg_client
        .query_one("select count(*) from symbols", &[])
        .await.expect("error counting symbols");
    let symbols_count: i64 = row.get(0);
    assert_eq!(true, symbols_count > 11_000);
}

//------------------------------------------------------------------------------
// helper functions for tests
//------------------------------------------------------------------------------

fn get_test_db_url<'a>(config: &'a Configuration, host_port: &'a u16) -> String {
    let db_config = &config.database;
    let db_url = format!(
        "postgres://{}:{}@{}:{}/{}",
        db_config.username, db_config.password, db_config.host, host_port, db_config.name
    );
    db_url
}

fn execute_db_migrations(db_url: &str) {
    let conn = PgConnection::establish(db_url)
        .expect(&format!("Cannot connect to database: {}", db_url));

    embedded_migrations::run(&conn).expect("error running diesel migrations");
}

async fn get_postgres_client(db_url: &str) -> Client {
    let (client, connection) =
        tokio_postgres::connect(db_url, postgres::NoTls)
            .await.expect("error connecting to postgres");

    tokio::spawn(async move {
        if let Err(e) = connection.await {
            eprintln!("connection error: {}", e);
        }
    });

    client
}

fn start_postgres_container<'a>(config: &Configuration, docker: &'a Cli) -> Container<'a, Cli, GenericImage> {
    let db_config = &config.database;

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

fn update_database_port_in_config_file(config: &Configuration, host_port: u16, file_path: &str) {
    let db_config = &config.database;
    let updated_config = Configuration {
        iex: config.iex.clone(),
        database: DatabaseConfig {
            username: db_config.username.to_string(),
            password: db_config.password.to_string(),
            host: db_config.host.to_string(),
            port: u32::from(host_port),
            name: db_config.name.to_string(),
        },
    };
    let contents = toml::to_string(&updated_config)
        .expect("error converting configuration to string");
    write(file_path, contents)
        .expect("error writing updated configuration file");
}
