use diesel::insert_into;
use diesel::pg::PgConnection;
use diesel::prelude::*;

use crate::models::Symbol;

// private functions

fn get_connection(database_url: &str) -> PgConnection {
    PgConnection::establish(database_url)
        .expect(&format!("Error connecting to {}", database_url))
}

// public functions

pub fn save_symbols(database_url: &str, symbols: Vec<Symbol>) -> Result<(), diesel::result::Error> {
    use crate::schema::symbols;

    let conn = get_connection(database_url);
    insert_into(symbols::table)
        .values(symbols)
        .execute(&conn)?;
    Ok(())
}
