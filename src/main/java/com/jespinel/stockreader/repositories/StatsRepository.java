package com.jespinel.stockreader.repositories;

import com.jespinel.stockreader.entities.Stats;
import org.springframework.dao.support.DataAccessUtils;
import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.jdbc.core.namedparam.SqlParameterSource;
import org.springframework.jdbc.core.namedparam.SqlParameterSourceUtils;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public class StatsRepository {

    private static final String GET_ALL_SQL = "SELECT * FROM stats";
    private static final String GET_BY_SYMBOL_SQL = "SELECT * FROM stats WHERE symbol = :symbol";
    private static final String INSERT_SQL = """
            INSERT INTO stats (symbol, marketcap, shares_outstanding, employees,
                                ttm_eps, ttm_dividend_rate, dividend_yield, next_dividend_date,
                                ex_dividend_date, next_earnings_date, pe_ratio, beta, created_at, updated_at)
            VALUES (:symbol, :marketcap, :sharesOutstanding, :employees,
                     :ttmEps, :ttmDividendRate, :dividendYield, :nextDividendDate,
                     :exDividendDate, :nextEarningsDate, :peRatio, :beta, :createdAt, :updatedAt)
            ON CONFLICT (symbol) DO UPDATE SET
                 marketcap = :marketcap,
                 shares_outstanding = :sharesOutstanding,
                 employees = :employees,
                 ttm_eps = :ttmEps,
                 ttm_dividend_rate = :ttmDividendRate,
                 dividend_yield = :dividendYield,
                 next_dividend_date = :nextDividendDate,
                 ex_dividend_date = :exDividendDate,
                 next_earnings_date = :nextEarningsDate,
                 pe_ratio = :peRatio,
                 beta = :beta,
                 updated_at = :updatedAt;
            """;

    private final NamedParameterJdbcTemplate jdbcTemplate;

    public StatsRepository(NamedParameterJdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    //--------------------------------------------------------------------------
    // public methods
    //--------------------------------------------------------------------------

    public List<Stats> getAll() {
        return jdbcTemplate.query(GET_ALL_SQL, new StatsRowMapper());
    }

    public void saveAll(List<Stats> stats) {
        SqlParameterSource[] batchValues = SqlParameterSourceUtils.createBatch(stats);
        jdbcTemplate.batchUpdate(INSERT_SQL, batchValues);
    }

    public Stats getBySymbol(String symbol) {
        MapSqlParameterSource params = new MapSqlParameterSource().addValue("symbol", symbol);
        List<Stats> results = jdbcTemplate.query(GET_BY_SYMBOL_SQL, params, new StatsRowMapper());
        return DataAccessUtils.singleResult(results);
    }
}
