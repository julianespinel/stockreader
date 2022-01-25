use bigdecimal::BigDecimal;
use chrono::{NaiveDate, NaiveDateTime};
use diesel::{Insertable, Queryable};
use serde::Deserialize;

use super::schema::{symbols, stats, historical_prices};

#[derive(Debug, Deserialize, Insertable, Queryable, Clone)]
#[table_name = "symbols"]
pub struct Symbol {
    pub symbol: String,
    pub name: String,
}

#[derive(Debug, Deserialize, Insertable, Queryable, Clone)]
#[table_name = "stats"]
pub struct Stats {
    pub symbol: String,
    pub created_at: NaiveDateTime,
    pub marketcap: i64,
    pub shares_outstanding: i64,
    pub employees: i64,
    pub ttm_eps: BigDecimal,
    pub ttm_dividend_rate: BigDecimal,
    pub dividend_yield: BigDecimal,
    pub next_dividend_date: Option<NaiveDate>,
    pub ex_dividend_date: Option<NaiveDate>,
    pub next_earnings_date: Option<NaiveDate>,
    pub pe_ratio: BigDecimal,
    pub beta: BigDecimal,
}

#[derive(Debug, Deserialize, Insertable, Queryable, Clone)]
#[table_name = "historical_prices"]
pub struct HistoricalPrice {
    pub symbol: String,
    pub date: NaiveDate,
    pub open: BigDecimal,
    pub close: BigDecimal,
    pub high: BigDecimal,
    pub low: BigDecimal,
    pub volume: i64,
    pub change: BigDecimal,
    pub change_percent: BigDecimal,
    pub created_at: NaiveDateTime,
    pub updated_at: NaiveDateTime,
}
