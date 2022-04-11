package com.jespinel.stockreader.scheduled_jobs;

import com.jespinel.stockreader.clients.StockAPIClient;
import com.jespinel.stockreader.entities.Stats;
import com.jespinel.stockreader.entities.Symbol;
import com.jespinel.stockreader.repositories.StatsRepository;
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
public class DownloadStats implements Job {

    private static final Logger log = LoggerFactory.getLogger(DownloadStats.class);

    private static final int THREADS = 8;

    private final SymbolRepository symbolRepository;
    private final StatsRepository statsRepository;
    private final StockAPIClient client;

    @Autowired
    public DownloadStats(SymbolRepository symbolRepository, StatsRepository statsRepository, StockAPIClient client) {
        this.symbolRepository = symbolRepository;
        this.statsRepository = statsRepository;
        this.client = client;
    }

    @Override
    public void execute() {
        try {
            log.info("DownloadStats: Start");
            List<Symbol> symbols = symbolRepository.getAll();
            List<Future<Stats>> futureStats = getStatsAsync(symbols);
            saveStats(futureStats);
            log.info("DownloadStats: Done");
        } catch (InterruptedException | ExecutionException e) {
            log.error("DownloadStats: Error: " + e.getMessage(), e);
        }
    }

    private List<Future<Stats>> getStatsAsync(List<Symbol> symbols) {
        ExecutorService threadPool = Executors.newFixedThreadPool(THREADS);
        List<Future<Stats>> futureStats = new ArrayList<>(symbols.size());
        for (Symbol symbol : symbols) {
            Future<Stats> future = threadPool.submit(() -> client.getSymbolStats(symbol));
            futureStats.add(future);
        }
        return futureStats;
    }

    private void saveStats(List<Future<Stats>> futureStats) throws InterruptedException, ExecutionException {
        List<Stats> statsToSave = new ArrayList<>();
        for (Future<Stats> future : futureStats) {
            statsToSave.add(future.get());
        }
        statsRepository.saveAll(statsToSave);
    }
}
