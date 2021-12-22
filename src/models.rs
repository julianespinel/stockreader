use diesel::{Insertable, Queryable};
use serde::Deserialize;

use super::schema::symbols;

#[derive(Debug, Deserialize, Insertable, Queryable)]
#[table_name = "symbols"]
pub(super) struct Symbol {
    pub symbol: String,
    pub name: String,
}
