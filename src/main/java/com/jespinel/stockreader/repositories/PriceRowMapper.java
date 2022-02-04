package com.jespinel.stockreader.repositories;

import com.jespinel.stockreader.entities.Price;
import org.springframework.jdbc.core.RowMapper;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.LocalDate;
import java.time.LocalDateTime;

public class PriceRowMapper implements RowMapper<Price> {

    @Override
    public Price mapRow(ResultSet rs, int rowNum) throws SQLException {
        String symbol = rs.getString("symbol");
        LocalDate date = RowMapperUtils.getDate(rs, "date");
        BigDecimal open = BigDecimal.valueOf(rs.getLong("open"));
        BigDecimal close = BigDecimal.valueOf(rs.getLong("close"));
        BigDecimal high = BigDecimal.valueOf(rs.getLong("high"));
        BigDecimal low = BigDecimal.valueOf(rs.getLong("low"));
        BigInteger volume = BigInteger.valueOf(rs.getLong("volume"));
        BigDecimal change = BigDecimal.valueOf(rs.getLong("change"));
        BigDecimal changePercent = BigDecimal.valueOf(rs.getLong("change_percent"));
        LocalDateTime createdAt = rs.getTimestamp("created_at").toLocalDateTime();
        LocalDateTime updatedAt = rs.getTimestamp("updated_at").toLocalDateTime();

        return new Price(symbol, date, open, close, high, low, volume,
                change, changePercent, createdAt, updatedAt);
    }
}
