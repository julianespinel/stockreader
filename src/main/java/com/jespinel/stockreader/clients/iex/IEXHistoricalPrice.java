package com.jespinel.stockreader.clients.iex;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.jespinel.stockreader.entities.HistoricalPrice;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.time.LocalDate;

class IEXHistoricalPrice {

    private final String symbol;
    private final LocalDate date;
    @JsonProperty("fOpen")
    private final BigDecimal open;
    @JsonProperty("fClose")
    private final BigDecimal close;
    @JsonProperty("fHigh")
    private final BigDecimal high;
    @JsonProperty("fLow")
    private final BigDecimal low;
    @JsonProperty("fVolume")
    private final BigInteger volume;
    private final BigDecimal change;
    private final BigDecimal changePercent;

    @JsonCreator
    public IEXHistoricalPrice(String symbol, LocalDate date, BigDecimal open,
                              BigDecimal close, BigDecimal high, BigDecimal low,
                              BigInteger volume, BigDecimal change,
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
    }

    public HistoricalPrice toHistoricalPrice() {
        return new HistoricalPrice(symbol, date, open, close, high, low,
                volume, change, changePercent);
    }
}
