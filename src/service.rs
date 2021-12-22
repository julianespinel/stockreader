use log::{info, warn};
use crate::client::IEXClient;
use crate::models::Symbol;
use crate::repository::Repository;

pub(super) struct Service<'a> {
    pub iex_client: &'a IEXClient<'a>,
    pub repository: &'a Repository<'a>
}

impl<'a> Service<'a> {

    pub async fn get_symbols(&self) -> Result<Vec<Symbol>, anyhow::Error> {
        let symbols = self.repository.get_symbols()?;
        if symbols.is_empty() {
            warn!("no symbols in DB, retrieving them from IEX");
            let symbols_from_iex = self.iex_client.get_symbols().await?;
            info!("got {} symbols from IEX", symbols_from_iex.len());
            self.repository.save_symbols(&symbols_from_iex)?;
            info!("symbols saved in DB");
            return Ok(symbols_from_iex);
        }
        info!("got {} symbols from DB", symbols.len());
        Ok(symbols)
    }
}


