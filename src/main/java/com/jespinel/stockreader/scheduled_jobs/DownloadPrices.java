package com.jespinel.stockreader.scheduled_jobs;

import com.jespinel.stockreader.clients.ClientException;
import com.jespinel.stockreader.clients.StockAPIClient;
import com.jespinel.stockreader.entities.Price;
import com.jespinel.stockreader.entities.Symbol;
import com.jespinel.stockreader.repositories.PriceRepository;
import com.jespinel.stockreader.repositories.SymbolRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class DownloadPrices implements Job {

    private static final Logger log = LoggerFactory.getLogger(DownloadPrices.class);

    private final SymbolRepository symbolRepository;
    private final PriceRepository pricesRepository;
    private final StockAPIClient client;

    @Autowired
    public DownloadPrices(SymbolRepository symbolRepository, PriceRepository pricesRepository, StockAPIClient client) {
        this.symbolRepository = symbolRepository;
        this.pricesRepository = pricesRepository;
        this.client = client;
    }

    @Override
    public void execute() {
        try {
            log.info("DownloadPrices: Start");
            List<Symbol> symbols = symbolRepository.getAll();
            List<Price> pricesPreviousDay = client.getMarketPricesPreviousDay();
            List<Price> prices = getIntersectionBySymbol(symbols, pricesPreviousDay);
            pricesRepository.saveAll(prices);
            log.info("DownloadPrices: Done");
        } catch (ClientException e) {
            log.error("DownloadPrices: Error: " + e.getMessage(), e);
        }
    }

    private List<Price> getIntersectionBySymbol(List<Symbol> symbols, List<Price> prices) {
        Set<String> existingSymbols = new HashSet<>();
        for (Symbol symbol : symbols) {
            existingSymbols.add(symbol.getSymbol());
        }

        List<Price> pricesWithExistentSymbol = new ArrayList<>();
        for (Price price : prices) {
            if (existingSymbols.contains(price.getSymbol())) {
                pricesWithExistentSymbol.add(price);
            }
        }

        return pricesWithExistentSymbol;
    }
}
