package com.jespinel.stockreader.repositories;

import com.jespinel.stockreader.entities.Symbol;
import org.springframework.jdbc.core.RowMapper;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.LocalDateTime;

public class SymbolRowMapper implements RowMapper<Symbol> {

    @Override
    public Symbol mapRow(ResultSet rs, int rowNum) throws SQLException {
        String symbol = rs.getString("symbol");
        String name = rs.getString("name");
        LocalDateTime createdAt = rs.getTimestamp("created_at").toLocalDateTime();
        LocalDateTime updatedAt = rs.getTimestamp("updated_at").toLocalDateTime();
        return new Symbol(symbol, name, createdAt, updatedAt);
    }
}
