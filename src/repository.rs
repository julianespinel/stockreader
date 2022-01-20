use diesel::insert_into;
use diesel::pg::PgConnection;
use diesel::prelude::*;
use diesel::result::Error;
use log::debug;
use reqwest::Url;

use crate::models::{Stats, Symbol};
use crate::schema::{stats, symbols};
use crate::schema::symbols::dsl::*;

pub(super) struct Repository<'a> {
    pub db_url: &'a str,
}

impl<'a> Repository<'a> {
    // private functions

    fn get_connection(&self) -> PgConnection {
        PgConnection::establish(self.db_url)
            .expect(&format!("Error connecting to {}", self.db_url))
    }

    // public functions

    pub fn new (db_url: &'a str) -> Repository<'a> {
        if db_url.is_empty() { panic!("db_url must not be empty") }
        Url::parse(db_url).expect(&format!("db_url: '{}' is not valid", db_url));
        Repository { db_url }
    }

    pub fn save_symbols(&self, new_symbols: &Vec<Symbol>) -> Result<(), Error> {
        let conn = self.get_connection();
        let affected_rows = insert_into(symbols::table)
            .values(new_symbols)
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
            .execute(&conn)?;
        debug!("saved {} stats in DB", affected_rows);
        Ok(())
    }
}

#[cfg(test)]
mod tests {
//-------------------------------------------------------------------------
// new() tests
//-------------------------------------------------------------------------

    use crate::config::models::DatabaseConfig;
    use crate::repository::Repository;

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
        let db_config = DatabaseConfig {
            username: "username".to_string(),
            password: "password".to_string(),
            host: "localhost".to_string(),
            port: 5432,
            name: "some_db".to_string(),
        };
        let db_url = db_config.get_url();
        // act
        let repository = Repository::new(&db_url);
        // assert
        assert_eq!(repository.db_url, db_url);
    }
}
