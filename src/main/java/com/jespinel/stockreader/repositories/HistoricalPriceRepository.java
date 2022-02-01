package com.jespinel.stockreader.repositories;

import com.jespinel.stockreader.entities.HistoricalPrice;
import org.springframework.dao.support.DataAccessUtils;
import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.jdbc.core.namedparam.SqlParameterSource;
import org.springframework.jdbc.core.namedparam.SqlParameterSourceUtils;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;

@Repository
public class HistoricalPriceRepository {

    private static final String GET_ALL_SQL = "SELECT * FROM historical_prices";
    private static final String GET_BY_SYMBOL_SQL = "SELECT * FROM historical_prices WHERE symbol = :symbol";
    private static final String GET_BY_SYMBOL_AND_DATE_SQL = "SELECT * FROM historical_prices WHERE symbol = :symbol AND date = :date";
    private static final String INSERT_SQL = """
            INSERT INTO historical_prices (symbol, date, open, close, high, low, volume, change, change_percent, created_at, updated_at)
            VALUES (:symbol, :date, :open, :close, :high, :low, :volume, :change, :changePercent, :createdAt, :updatedAt)
            ON CONFLICT (symbol, date) DO UPDATE SET
                 open = :open,
                 close = :close,
                 high = :high,
                 low = :low,
                 volume = :volume,
                 change = :change,
                 change_percent = :changePercent,
                 updated_at = :updatedAt;
            """;

    private final NamedParameterJdbcTemplate jdbcTemplate;

    public HistoricalPriceRepository(NamedParameterJdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    //--------------------------------------------------------------------------
    // public methods
    //--------------------------------------------------------------------------

    public void saveAll(List<HistoricalPrice> historicalPrices) {
        SqlParameterSource[] batchValues = SqlParameterSourceUtils.createBatch(historicalPrices);
        jdbcTemplate.batchUpdate(INSERT_SQL, batchValues);
    }

    public List<HistoricalPrice> getBySymbol(String symbol) {
        MapSqlParameterSource params = new MapSqlParameterSource().addValue("symbol", symbol);
        return jdbcTemplate.query(GET_BY_SYMBOL_SQL, params, new HistoricalPriceRowMapper());
    }

    public HistoricalPrice getBySymbolAndDate(String symbol, LocalDate date) {
        MapSqlParameterSource params = new MapSqlParameterSource()
                .addValue("symbol", symbol)
                .addValue("date", date);
        List<HistoricalPrice> prices = jdbcTemplate.query(
                GET_BY_SYMBOL_AND_DATE_SQL, params, new HistoricalPriceRowMapper());
        return DataAccessUtils.singleResult(prices);
    }
}
