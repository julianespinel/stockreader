#[macro_use]
extern crate diesel_migrations;

use std::env::set_var;

use diesel::{Connection, PgConnection};
use diesel_migrations::embed_migrations;
use testcontainers::clients::Cli;
use testcontainers::images::generic::{GenericImage, WaitFor};
use testcontainers::{clients, images, Container, Docker};
use tokio_postgres::Client;

use stockreader::config::models::{Configuration, DatabaseConfig};
use stockreader::config::read_config;

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
/// 1. Updates the host port of the docker container in the environment variable.
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
    let container = start_postgres_container(&config.database, &docker);
    let host_port = container.get_host_port(POSTGRES_CONTAINER_PORT).unwrap();
    let db_url = get_test_db_url(&config.database, &host_port);

    execute_db_migrations(&db_url);
    let updated_config = get_config_with_correct_port(environment, host_port).await;

    // act
    stockreader::download_symbols(&updated_config)
        .await
        .expect("Expected to download symbols");

    // assert
    let pg_client = get_postgres_client(&db_url).await;

    let row = pg_client
        .query_one("select count(*) from symbols", &[])
        .await
        .expect("error counting symbols");
    let symbols_count: i64 = row.get(0);
    assert_eq!(true, symbols_count > 11_000);
}

//------------------------------------------------------------------------------
// helper functions for tests
//------------------------------------------------------------------------------

fn get_test_db_url<'a>(db_config: &'a DatabaseConfig, host_port: &'a u16) -> String {
    let db_url = format!(
        "postgres://{}:{}@{}:{}/{}",
        db_config.username, db_config.password, db_config.host, host_port, db_config.name
    );
    db_url
}

fn execute_db_migrations(db_url: &str) {
    let conn =
        PgConnection::establish(db_url).expect(&format!("Cannot connect to database: {}", db_url));

    embedded_migrations::run(&conn).expect("error running diesel migrations");
}

async fn get_postgres_client(db_url: &str) -> Client {
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

fn start_postgres_container<'a>(
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

async fn get_config_with_correct_port(environment: &str, host_port: u16) -> Configuration {
    // Update port with the one used by the container
    set_var("DB_PORT", host_port.to_string());
    read_config(environment)
        .await
        .expect("error reading updated configuration")
}
