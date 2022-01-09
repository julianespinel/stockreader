use diesel::insert_into;
use diesel::pg::PgConnection;
use diesel::prelude::*;
use diesel::result::Error;
use log::debug;

use crate::models::Symbol;

use crate::schema::symbols;
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
}
