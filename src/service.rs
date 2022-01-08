use std::collections::HashMap;

use log::{debug, info};

use crate::client::IEXClient;
use crate::models::Symbol;
use crate::repository::Repository;

pub(super) struct Service<'a> {
    pub iex_client: &'a IEXClient<'a>,
    pub repository: &'a Repository<'a>,
}

impl<'a> Service<'a> {
    pub async fn download_symbols(&self) -> Result<Vec<Symbol>, anyhow::Error> {
        let mut symbols_from_db = self.repository.get_symbols()?;
        let symbols_from_iex = self.iex_client.get_symbols().await?;
        let new_symbols = get_symbols_not_in_db(&symbols_from_db, &symbols_from_iex);
        self.repository.save_symbols(&new_symbols)?;
        symbols_from_db.extend(new_symbols);
        info!("get_symbols: returned {} symbols", &symbols_from_db.len());
        return Ok(symbols_from_db);
    }
}

fn get_symbols_not_in_db(symbols_from_db: &Vec<Symbol>, symbols_from_iex: &Vec<Symbol>) -> Vec<Symbol> {
    let mut existing_symbols = HashMap::new();
    for symbol in symbols_from_db {
        existing_symbols.insert(&symbol.symbol, symbol);
    }

    let mut new_symbols = Vec::new();
    for symbol in symbols_from_iex {
        if existing_symbols.get(&symbol.symbol).is_none() {
            new_symbols.push(symbol.clone());
        }
    }
    debug!("got {} new symbols", &new_symbols.len());
    new_symbols
}


