use diesel::{Insertable, Queryable};
use serde::Deserialize;

use crate::schema::symbols;

#[derive(Debug, Deserialize, Insertable, Queryable)]
#[table_name = "symbols"]
pub struct Symbol {
    pub symbol: String,
    pub name: String,
}
