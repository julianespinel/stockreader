use diesel::insert_into;
use diesel::pg::upsert::excluded;
use diesel::pg::PgConnection;
use diesel::prelude::*;
use diesel::result::Error;
use log::debug;
use reqwest::Url;

use crate::models::{HistoricalPrice, Stats, Symbol};
use crate::schema::symbols::dsl::*;
use crate::schema::{historical_prices, stats, symbols};
use crate::schema::stats::dsl::*;

pub(super) struct Repository<'a> {
    pub db_url: &'a str,
}

impl<'a> Repository<'a> {
    // private functions

    fn get_connection(&self) -> PgConnection {
        PgConnection::establish(self.db_url).expect(&format!("Error connecting to {}", self.db_url))
    }

    fn get_symbol(&self, some_symbol: &String) -> Result<Symbol, Error> {
        let conn = self.get_connection();
        let symbol_from_db: Symbol = symbols
            .filter(symbols::symbol.eq(some_symbol))
            .first(&conn)?;
        debug!("got {} symbol from database", &symbol_from_db.symbol);
        Ok(symbol_from_db)
    }

    fn get_stats(&self) -> Result<Vec<Stats>, Error> {
        let conn = self.get_connection();
        let stats_from_db = stats.load::<Stats>(&conn)?;
        debug!("got {} stats from database", &stats_from_db.len());
        Ok(stats_from_db)
    }

    // public functions

    pub fn new(db_url: &'a str) -> Repository<'a> {
        if db_url.is_empty() {
            panic!("db_url must not be empty")
        }
        Url::parse(db_url).expect(&format!("db_url: '{}' is not valid", db_url));
        Repository { db_url }
    }

    pub fn save_symbols(&self, new_symbols: &Vec<Symbol>) -> Result<(), Error> {
        let conn = self.get_connection();
        let affected_rows = insert_into(symbols::table)
            .values(new_symbols)
            .on_conflict(symbols::symbol)
            .do_update()
            .set(symbols::name.eq(excluded(symbols::name)))
            .execute(&conn)?;
        debug!("saved {} symbols in DB", affected_rows);
        Ok(())
    }

    pub fn get_symbols(&self) -> Result<Vec<Symbol>, Error> {
        let conn = self.get_connection();
        let symbols_from_db = symbols.load::<Symbol>(&conn)?;
        debug!("got {} symbols from database", &symbols_from_db.len());
        Ok(symbols_from_db)
    }

    pub fn save_stats(&self, new_stats: Vec<Stats>) -> Result<(), Error> {
        let conn = self.get_connection();
        let affected_rows = insert_into(stats::table)
            .values(new_stats)
            .on_conflict(stats::symbol)
            .do_update()
            .set((
                stats::created_at.eq(excluded(stats::created_at)),
                stats::marketcap.eq(excluded(stats::marketcap)),
                stats::shares_outstanding.eq(excluded(stats::shares_outstanding)),
                stats::employees.eq(excluded(stats::employees)),
                stats::ttm_eps.eq(excluded(stats::ttm_eps)),
                stats::ttm_dividend_rate.eq(excluded(stats::ttm_dividend_rate)),
                stats::dividend_yield.eq(excluded(stats::dividend_yield)),
                stats::next_dividend_date.eq(excluded(stats::next_dividend_date)),
                stats::ex_dividend_date.eq(excluded(stats::ex_dividend_date)),
                stats::next_earnings_date.eq(excluded(stats::next_earnings_date)),
                stats::pe_ratio.eq(excluded(stats::pe_ratio)),
                stats::beta.eq(excluded(stats::beta)),
            ))
            .execute(&conn)?;
        debug!("saved {} stats in DB", affected_rows);
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use testcontainers::clients;

    use crate::config::models::DatabaseConfig;
    use crate::models::Symbol;
    use crate::repository::Repository;

    const POSTGRES_CONTAINER_PORT: u16 = 5432;

    //-------------------------------------------------------------------------
    // new() tests
    //-------------------------------------------------------------------------

    #[test]
    #[should_panic(expected = "db_url must not be empty")]
    fn new_given_empty_db_url_it_panics() {
        // arrange
        let db_url = "";
        // act
        Repository::new(db_url);
    }

    #[test]
    #[should_panic(expected = "db_url: 'some_url' is not valid: RelativeUrlWithoutBase")]
    fn new_given_not_valid_db_url_it_panics() {
        // arrange
        let db_url = "some_url";
        // act
        Repository::new(db_url);
    }

    #[test]
    fn new_given_valid_db_url_returns_repository() {
        // arrange
        let db_config = get_db_config_for_tests();
        let db_url = db_config.get_url();
        // act
        let repository = Repository::new(&db_url);
        // assert
        assert_eq!(repository.db_url, db_url);
    }

    fn get_db_config_for_tests() -> DatabaseConfig {
        let db_config = DatabaseConfig {
            username: "username".to_string(),
            password: "password".to_string(),
            host: "localhost".to_string(),
            port: 5432,
            name: "some_db".to_string(),
        };
        db_config
    }

    //-------------------------------------------------------------------------
    // save_symbols tests
    //-------------------------------------------------------------------------

    #[test]
    fn save_symbols_given_empty_list_saves_nothing() {
        // arrange
        let db_config = get_db_config_for_tests();
        let docker = clients::Cli::default();
        let container = containers::start_postgres_container(&db_config, &docker);
        let host_port = container.get_host_port(POSTGRES_CONTAINER_PORT).unwrap();
        let db_url = containers::get_test_db_url(&db_config, &host_port);

        containers::execute_db_migrations(&db_url);
        let repository = Repository::new(&db_url);
        let symbols = vec![];
        // act
        repository
            .save_symbols(&symbols)
            .expect("error saving symbols");
        // assert
        let symbols_from_db = repository.get_symbols().expect("error getting symbols");
        assert!(symbols_from_db.is_empty());
    }

    #[test]
    fn save_symbols_given_non_empty_list_saves_symbols() {
        // arrange
        let db_config = get_db_config_for_tests();
        let docker = clients::Cli::default();
        let container = containers::start_postgres_container(&db_config, &docker);
        let host_port = container.get_host_port(POSTGRES_CONTAINER_PORT).unwrap();
        let db_url = containers::get_test_db_url(&db_config, &host_port);

        containers::execute_db_migrations(&db_url);
        let repository = Repository::new(&db_url);
        let list_size = 5;
        let symbols = test_factories::get_symbols_list(list_size);
        // act
        repository
            .save_symbols(&symbols)
            .expect("error saving symbols");
        // assert
        let symbols_from_db = repository.get_symbols().expect("error getting symbols");
        assert_eq!(symbols_from_db.len(), list_size as usize);
    }

    #[test]
    fn save_symbols_given_repeated_symbols_updates_symbol_name() {
        // arrange
        let db_config = get_db_config_for_tests();
        let docker = clients::Cli::default();
        let container = containers::start_postgres_container(&db_config, &docker);
        let host_port = container.get_host_port(POSTGRES_CONTAINER_PORT).unwrap();
        let db_url = containers::get_test_db_url(&db_config, &host_port);

        containers::execute_db_migrations(&db_url);
        let repository = Repository::new(&db_url);
        let list_size = 5;
        let symbols = test_factories::get_symbols_list(list_size);

        repository
            .save_symbols(&symbols)
            .expect("error saving symbols");

        let original_symbol = &symbols[0].symbol;
        let new_name = "Apple Inc";
        let duplicated_symbol = Symbol {
            symbol: original_symbol.to_string(),
            name: new_name.to_string()
        };
        // act
        repository
            .save_symbols(&vec![duplicated_symbol])
            .expect("error saving duplicated symbol");

        // assert
        let symbols_from_db = repository.get_symbols().expect("error getting symbols");
        assert_eq!(symbols_from_db.len(), list_size as usize);

        let updated_symbol = repository.get_symbol(original_symbol)
            .expect("error getting single symbol");

        assert_eq!(updated_symbol.symbol, original_symbol.to_string());
        assert_eq!(updated_symbol.name, new_name.to_string());
    }

    //-------------------------------------------------------------------------
    // save_stats() tests
    //-------------------------------------------------------------------------

    #[test]
    fn save_stats_given_non_empty_list_saves_stats() {
        // arrange
        let db_config = get_db_config_for_tests();
        let docker = clients::Cli::default();
        let container = containers::start_postgres_container(&db_config, &docker);
        let host_port = container.get_host_port(POSTGRES_CONTAINER_PORT).unwrap();
        let db_url = containers::get_test_db_url(&db_config, &host_port);

        containers::execute_db_migrations(&db_url);
        let repository = Repository::new(&db_url);
        let list_size = 1;
        let symbols = test_factories::get_symbols_list(list_size);

        repository
            .save_symbols(&symbols)
            .expect("error saving symbols");

        let symbol = &symbols[0];
        let symbol_stats = test_factories::get_symbol_stats(&symbol.symbol, 0);
        // act
        repository.save_stats(vec![symbol_stats]);
        // assert
        let stats_from_db = repository.get_stats()
            .expect("error getting stats");
        assert_eq!(stats_from_db.len(), 1);
    }

    #[test]
    fn save_stats_given_repeated_stats_updates_stats() {
        // arrange
        let db_config = get_db_config_for_tests();
        let docker = clients::Cli::default();
        let container = containers::start_postgres_container(&db_config, &docker);
        let host_port = container.get_host_port(POSTGRES_CONTAINER_PORT).unwrap();
        let db_url = containers::get_test_db_url(&db_config, &host_port);

        containers::execute_db_migrations(&db_url);
        let repository = Repository::new(&db_url);
        let list_size = 1;
        let symbols = test_factories::get_symbols_list(list_size);

        repository
            .save_symbols(&symbols)
            .expect("error saving symbols");

        let symbol = &symbols[0];
        let original_symbol_stats = test_factories::get_symbol_stats(&symbol.symbol, 0);
        repository.save_stats(vec![original_symbol_stats.clone()]);

        let updated_symbol_stats = test_factories::get_symbol_stats(&symbol.symbol, 1);
        // act
        repository.save_stats(vec![updated_symbol_stats.clone()]);
        // assert
        let stats_from_db = repository.get_stats()
            .expect("error getting stats");
        assert_eq!(stats_from_db.len(), 1);
        assert_eq!(stats_from_db[0].marketcap, original_symbol_stats.marketcap + 1)
    }

    /// Module for using containers in tests
    mod containers {
        use diesel::{Connection, PgConnection};
        use testcontainers::clients::Cli;
        use testcontainers::images::generic::{GenericImage, WaitFor};
        use testcontainers::{images, Container, Docker};

        use crate::config::models::DatabaseConfig;
        use crate::embedded_migrations;

        pub(super) fn get_test_db_url<'a>(
            db_config: &'a DatabaseConfig,
            host_port: &'a u16,
        ) -> String {
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

    mod test_factories {
        use std::iter;
        use bigdecimal::BigDecimal;
        use chrono::{NaiveDate, NaiveDateTime, Utc};

        use rand::distributions::Alphanumeric;
        use rand::{thread_rng, Rng};

        use crate::models::{Stats, Symbol};

        fn get_random_string() -> String {
            let mut rng = thread_rng();
            let random_string: String = iter::repeat(())
                .map(|()| rng.sample(Alphanumeric))
                .map(char::from)
                .take(7)
                .collect();
            random_string
        }

        pub(super) fn get_random_symbol(index: u32) -> Symbol {
            let random_string = get_random_string();
            let symbol = format!("{}{}", random_string.clone(), index);
            let name = format!("{}-name", &symbol);
            Symbol { symbol, name }
        }

        pub(super) fn get_symbols_list(quantity: u32) -> Vec<Symbol> {
            let mut symbols = vec![];
            for i in 0..quantity {
                let symbol = get_random_symbol(i);
                symbols.push(symbol);
            }
            symbols
        }

        pub(crate) fn get_symbol_stats(symbol: &String, index: i64) -> Stats {
            Stats {
                symbol: symbol.to_string(),
                created_at: Utc::now().naive_utc(),
                marketcap: index + 1,
                shares_outstanding: index + 2,
                employees: index + 3,
                ttm_eps: BigDecimal::from(index + 4),
                ttm_dividend_rate: BigDecimal::from(index + 5),
                dividend_yield: BigDecimal::from(index + 6),
                next_dividend_date: Option::None,
                ex_dividend_date: Option::None,
                next_earnings_date: Option::None,
                pe_ratio: BigDecimal::from(index + 7),
                beta: BigDecimal::from(index + 8),
            }
        }
    }
}
