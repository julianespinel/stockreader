package com.jespinel.stockreader.clients;

import com.jespinel.stockreader.entities.Price;
import com.jespinel.stockreader.entities.Stats;
import com.jespinel.stockreader.entities.Symbol;

import java.util.List;

public interface StockAPIClient {

    List<Symbol> getSymbols() throws ClientException;

    Stats getSymbolStats(Symbol symbol) throws ClientException;

    List<Price> getSymbolPricesLastFiveYears(Symbol symbol) throws ClientException;

    List<Price> getMarketPricesPreviousDay() throws ClientException;
}
