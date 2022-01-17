package com.jespinel.stockreader.clients;

import com.jespinel.stockreader.entities.Symbol;

import java.util.List;

public interface StockAPIClient {

    List<Symbol> getSymbols() throws ClientException;
}
