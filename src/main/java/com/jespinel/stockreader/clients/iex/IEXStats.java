package com.jespinel.stockreader.clients.iex;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.jespinel.stockreader.entities.Stats;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.time.LocalDate;

class IEXStats {

    private final BigInteger marketcap;
    private final BigInteger sharesOutstanding;
    private final BigInteger employees;

    @JsonProperty("ttmEPS")
    private final BigDecimal ttmEps;
    private final BigDecimal ttmDividendRate;
    private final BigDecimal dividendYield;

    private final LocalDate nextDividendDate;
    private final LocalDate exDividendDate;
    private final LocalDate nextEarningsDate;

    private final BigDecimal peRatio;
    private final BigDecimal beta;

    @JsonCreator
    public IEXStats(BigInteger marketcap, BigInteger sharesOutstanding, BigInteger employees,
                    BigDecimal ttmEps, BigDecimal ttmDividendRate, BigDecimal dividendYield,
                    LocalDate nextDividendDate, LocalDate exDividendDate, LocalDate nextEarningsDate,
                    BigDecimal peRatio, BigDecimal beta) {
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

    public Stats toStats(String symbol) {
        return new Stats(
                symbol,
                marketcap,
                sharesOutstanding,
                employees,
                ttmEps,
                ttmDividendRate,
                dividendYield,
                nextDividendDate,
                exDividendDate,
                nextEarningsDate,
                peRatio,
                beta
        );
    }
}
