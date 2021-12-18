use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct Symbol {
    pub symbol: String,
    pub name: String,
}
