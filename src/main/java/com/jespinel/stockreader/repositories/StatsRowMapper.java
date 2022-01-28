package com.jespinel.stockreader.repositories;

import com.jespinel.stockreader.entities.Stats;
import org.springframework.jdbc.core.RowMapper;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.sql.Date;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.LocalDate;
import java.time.LocalDateTime;

public class StatsRowMapper implements RowMapper<Stats> {

    @Override
    public Stats mapRow(ResultSet rs, int rowNum) throws SQLException {
        String symbol = rs.getString("symbol");
        BigInteger marketcap = BigInteger.valueOf(rs.getLong("marketcap"));
        BigInteger sharesOutstanding = BigInteger.valueOf(rs.getLong("shares_outstanding"));
        BigInteger employees = BigInteger.valueOf(rs.getLong("employees"));
        BigDecimal ttmEps = BigDecimal.valueOf(rs.getLong("ttm_eps"));
        BigDecimal ttmDividendRate = BigDecimal.valueOf(rs.getLong("ttm_dividend_rate"));
        BigDecimal dividendYield = BigDecimal.valueOf(rs.getLong("dividend_yield"));

        LocalDate nextDividendDate = getDate(rs, "next_dividend_date");
        LocalDate exDividendDate = getDate(rs, "ex_dividend_date");
        LocalDate nextEarningsDate = getDate(rs, "next_earnings_date");

        BigDecimal peRatio = BigDecimal.valueOf(rs.getLong("pe_ratio"));
        BigDecimal beta = BigDecimal.valueOf(rs.getLong("beta"));

        LocalDateTime createdAt = rs.getTimestamp("created_at").toLocalDateTime();
        LocalDateTime updatedAt = rs.getTimestamp("updated_at").toLocalDateTime();

        return new Stats(symbol, marketcap, sharesOutstanding, employees, ttmEps, ttmDividendRate,
                dividendYield, nextDividendDate, exDividendDate, nextEarningsDate, peRatio, beta,
                createdAt, updatedAt);
    }

    private LocalDate getDate(ResultSet resultSet, String key) throws SQLException {
        Date date = resultSet.getDate(key);
        if (date == null) {
            return null;
        }
        return date.toLocalDate();
    }
}
