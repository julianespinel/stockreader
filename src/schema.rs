table! {
    stats (symbol) {
        symbol -> Varchar,
        created_at -> Timestamp,
        marketcap -> Int8,
        shares_outstanding -> Int8,
        employees -> Int8,
        ttm_eps -> Numeric,
        ttm_dividend_rate -> Numeric,
        dividend_yield -> Numeric,
        next_dividend_date -> Nullable<Date>,
        ex_dividend_date -> Nullable<Date>,
        next_earnings_date -> Nullable<Date>,
        pe_ratio -> Numeric,
        beta -> Numeric,
    }
}

table! {
    symbols (symbol) {
        symbol -> Varchar,
        name -> Varchar,
    }
}

joinable!(stats -> symbols (symbol));

allow_tables_to_appear_in_same_query!(
    stats,
    symbols,
);
