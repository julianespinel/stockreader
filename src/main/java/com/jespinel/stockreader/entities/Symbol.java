package com.jespinel.stockreader.entities;

import com.fasterxml.jackson.annotation.JsonCreator;

import java.time.LocalDateTime;

public class Symbol {

    private final String symbol;
    private final String name;
    private final LocalDateTime createdAt;
    private final LocalDateTime updatedAt;

    @JsonCreator
    public Symbol(String symbol, String name) {
        this.symbol = symbol;
        this.name = name;
        LocalDateTime now = LocalDateTime.now();
        this.createdAt = now;
        this.updatedAt = now;
    }

    public Symbol(String symbol, String name, LocalDateTime createdAt, LocalDateTime updatedAt) {
        this.symbol = symbol;
        this.name = name;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
    }

    public String getSymbol() {
        return symbol;
    }

    public String getName() {
        return name;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }
}
