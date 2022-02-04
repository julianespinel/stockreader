package com.jespinel.stockreader.scheduled_jobs;

import com.jespinel.stockreader.clients.StockAPIClient;
import com.jespinel.stockreader.entities.HistoricalPrice;
import com.jespinel.stockreader.entities.Symbol;
import com.jespinel.stockreader.repositories.HistoricalPriceRepository;
import com.jespinel.stockreader.repositories.SymbolRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

@Service
public class DownloadHistoricalPrices implements Job {

    private static final Logger log = LoggerFactory.getLogger(DownloadHistoricalPrices.class);

    private static final int THREADS = 8;

    private final SymbolRepository symbolRepository;
    private final HistoricalPriceRepository pricesRepository;
    private final StockAPIClient client;

    @Autowired
    public DownloadHistoricalPrices(SymbolRepository symbolRepository, HistoricalPriceRepository pricesRepository, StockAPIClient client) {
        this.symbolRepository = symbolRepository;
        this.pricesRepository = pricesRepository;
        this.client = client;
    }

    @Override
    public void execute() {
        try {
            log.info("DownloadHistoricalPrices: Start");
            List<Symbol> symbols = symbolRepository.getAll();
            List<Future<List<HistoricalPrice>>> futurePrices = downloadHistoricalPricesAsync(symbols);
            saveHistoricalPrices(futurePrices);
            log.info("DownloadHistoricalPrices: Done");
        } catch (ExecutionException | InterruptedException e) {
            log.error("DownloadHistoricalPrices: Error: " + e.getMessage(), e);
        }
    }

    private List<Future<List<HistoricalPrice>>> downloadHistoricalPricesAsync(List<Symbol> symbols) {
        ExecutorService pool = Executors.newFixedThreadPool(THREADS);
        List<Future<List<HistoricalPrice>>> futurePrices = new ArrayList<>();
        for (Symbol symbol : symbols) {
            Future<List<HistoricalPrice>> future = pool.submit(() -> client.getSymbolHistoricalPricesLastFiveYears(symbol));
            futurePrices.add(future);
        }
        return futurePrices;
    }

    private void saveHistoricalPrices(List<Future<List<HistoricalPrice>>> futurePrices) throws ExecutionException, InterruptedException {
        for (Future<List<HistoricalPrice>> futurePrice : futurePrices) {
            List<HistoricalPrice> prices = futurePrice.get();
            pricesRepository.saveAll(prices);
        }
    }
}
