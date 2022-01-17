package com.jespinel.stockreader.repositories;

import com.jespinel.stockreader.entities.Symbol;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.jdbc.core.namedparam.SqlParameterSource;
import org.springframework.jdbc.core.namedparam.SqlParameterSourceUtils;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public class SymbolRepository {

    private static final String GET_ALL_SQL = "SELECT * FROM symbols";
    private static final String INSERT_SYMBOL_SQL =
            "INSERT INTO symbols (symbol, name, created_at, updated_at) " +
                    "VALUES (:symbol, :name, :createdAt, :updatedAt)";

    private final NamedParameterJdbcTemplate jdbcTemplate;

    public SymbolRepository(NamedParameterJdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    //--------------------------------------------------------------------------
    // public methods
    //--------------------------------------------------------------------------

    public List<Symbol> getAll() {
        return jdbcTemplate.query(GET_ALL_SQL, new SymbolRowMapper());
    }

    public void saveAll(List<Symbol> symbols) {
        SqlParameterSource[] batchValues = SqlParameterSourceUtils.createBatch(symbols);
        jdbcTemplate.batchUpdate(INSERT_SYMBOL_SQL, batchValues);
    }
}
