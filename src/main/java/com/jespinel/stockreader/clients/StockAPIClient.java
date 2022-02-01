package com.jespinel.stockreader.clients;

import com.jespinel.stockreader.entities.HistoricalPrice;
import com.jespinel.stockreader.entities.Stats;
import com.jespinel.stockreader.entities.Symbol;

import java.util.List;

public interface StockAPIClient {

    List<Symbol> getSymbols() throws ClientException;

    Stats getSymbolStats(Symbol symbol) throws ClientException;

    List<HistoricalPrice> getSymbolHistoricalPricesLastFiveYears(Symbol symbol) throws ClientException;
}
