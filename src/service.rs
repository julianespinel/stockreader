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

    pub async fn download_stats(&self) -> Result<(), anyhow::Error> {
        let symbols = self.repository.get_symbols()?;
        let mut stats_list = vec![];
        for symbol in symbols {
            let stats = self.iex_client.get_stats(symbol.symbol).await?;
            stats_list.push(stats);
        }
        self.repository.save_stats(stats_list)?;
        info!("download_stats: done");
        Ok(())
    }

    pub async fn download_historical_prices(&self) -> Result<(), anyhow::Error> {
        let symbols = self.repository.get_symbols()?;
        for symbol in symbols {
            let historical_prices = self.iex_client.get_historical_prices_last_five_years(symbol.symbol).await?;
            self.repository.save_historical_prices(historical_prices)?;
        }
        info!("download_historical_prices: done");
        Ok(())
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
