package com.jespinel.stockreader.entities;

import com.fasterxml.jackson.annotation.JsonCreator;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.time.LocalDate;
import java.time.LocalDateTime;

public class Stats {

    private final String symbol;
    private final BigInteger marketcap;
    private final BigInteger sharesOutstanding;
    private final BigInteger employees;

    private final BigDecimal ttmEps;
    private final BigDecimal ttmDividendRate;
    private final BigDecimal dividendYield;

    private final LocalDate nextDividendDate;
    private final LocalDate exDividendDate;
    private final LocalDate nextEarningsDate;

    private final BigDecimal peRatio;
    private final BigDecimal beta;

    private final LocalDateTime createdAt;
    private final LocalDateTime updatedAt;

    @JsonCreator
    public Stats(String symbol, BigInteger marketcap, BigInteger sharesOutstanding,
                 BigInteger employees, BigDecimal ttmEps, BigDecimal ttmDividendRate,
                 BigDecimal dividendYield, LocalDate nextDividendDate, LocalDate exDividendDate,
                 LocalDate nextEarningsDate, BigDecimal peRatio, BigDecimal beta) {
        this.symbol = symbol;
        this.marketcap = marketcap;
        this.sharesOutstanding = sharesOutstanding;
        this.employees = employees;
        this.ttmEps = ttmEps;
        this.ttmDividendRate = ttmDividendRate;
        this.dividendYield = dividendYield;
        this.nextDividendDate = nextDividendDate;
        this.exDividendDate = exDividendDate;
        this.nextEarningsDate = nextEarningsDate;
        this.peRatio = peRatio;
        this.beta = beta;

        LocalDateTime now = LocalDateTime.now();
        this.createdAt = now;
        this.updatedAt = now;
    }

    public Stats(String symbol, BigInteger marketcap, BigInteger sharesOutstanding,
                 BigInteger employees, BigDecimal ttmEps, BigDecimal ttmDividendRate,
                 BigDecimal dividendYield, LocalDate nextDividendDate, LocalDate exDividendDate,
                 LocalDate nextEarningsDate, BigDecimal peRatio, BigDecimal beta, LocalDateTime createdAt,
                 LocalDateTime updatedAt) {
        this.symbol = symbol;
        this.marketcap = marketcap;
        this.sharesOutstanding = sharesOutstanding;
        this.employees = employees;
        this.ttmEps = ttmEps;
        this.ttmDividendRate = ttmDividendRate;
        this.dividendYield = dividendYield;
        this.nextDividendDate = nextDividendDate;
        this.exDividendDate = exDividendDate;
        this.nextEarningsDate = nextEarningsDate;
        this.peRatio = peRatio;
        this.beta = beta;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
    }

    public String getSymbol() {
        return symbol;
    }

    public BigInteger getMarketcap() {
        return marketcap;
    }

    public BigInteger getSharesOutstanding() {
        return sharesOutstanding;
    }

    public BigInteger getEmployees() {
        return employees;
    }

    public BigDecimal getTtmEps() {
        return ttmEps;
    }

    public BigDecimal getTtmDividendRate() {
        return ttmDividendRate;
    }

    public BigDecimal getDividendYield() {
        return dividendYield;
    }

    public LocalDate getNextDividendDate() {
        return nextDividendDate;
    }

    public LocalDate getExDividendDate() {
        return exDividendDate;
    }

    public LocalDate getNextEarningsDate() {
        return nextEarningsDate;
    }

    public BigDecimal getPeRatio() {
        return peRatio;
    }

    public BigDecimal getBeta() {
        return beta;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }
}
