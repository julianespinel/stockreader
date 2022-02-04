package com.jespinel.stockreader.entities;

import com.fasterxml.jackson.annotation.JsonCreator;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.time.LocalDate;
import java.time.LocalDateTime;

public class Price {

    private final String symbol;
    private final LocalDate date;
    private final BigDecimal open;
    private final BigDecimal close;
    private final BigDecimal high;
    private final BigDecimal low;
    private final BigInteger volume;
    private final BigDecimal change;
    private final BigDecimal changePercent;
    private final LocalDateTime createdAt;
    private final LocalDateTime updatedAt;

    @JsonCreator
    public Price(String symbol, LocalDate date, BigDecimal open, BigDecimal close,
                 BigDecimal high, BigDecimal low, BigInteger volume, BigDecimal change,
                 BigDecimal changePercent) {
        this.symbol = symbol;
        this.date = date;
        this.open = open;
        this.close = close;
        this.high = high;
        this.low = low;
        this.volume = volume;
        this.change = change;
        this.changePercent = changePercent;

        LocalDateTime now = LocalDateTime.now();
        this.createdAt = now;
        this.updatedAt = now;
    }

    public Price(String symbol, LocalDate date, BigDecimal open, BigDecimal close,
                 BigDecimal high, BigDecimal low, BigInteger volume, BigDecimal change,
                 BigDecimal changePercent, LocalDateTime createdAt, LocalDateTime updatedAt) {
        this.symbol = symbol;
        this.date = date;
        this.open = open;
        this.close = close;
        this.high = high;
        this.low = low;
        this.volume = volume;
        this.change = change;
        this.changePercent = changePercent;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
    }

    public String getSymbol() {
        return symbol;
    }

    public LocalDate getDate() {
        return date;
    }

    public BigDecimal getOpen() {
        return open;
    }

    public BigDecimal getClose() {
        return close;
    }

    public BigDecimal getHigh() {
        return high;
    }

    public BigDecimal getLow() {
        return low;
    }

    public BigInteger getVolume() {
        return volume;
    }

    public BigDecimal getChange() {
        return change;
    }

    public BigDecimal getChangePercent() {
        return changePercent;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }
}
