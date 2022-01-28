package com.jespinel.stockreader.scheduled_jobs;

import com.jespinel.stockreader.clients.ClientException;
import com.jespinel.stockreader.clients.StockAPIClient;
import com.jespinel.stockreader.entities.Symbol;
import com.jespinel.stockreader.repositories.SymbolRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class DownloadSymbols implements Job {

    private static final Logger log = LoggerFactory.getLogger(DownloadSymbols.class);

    private final SymbolRepository repository;
    private final StockAPIClient client;

    @Autowired
    public DownloadSymbols(SymbolRepository repository, StockAPIClient client) {
        this.repository = repository;
        this.client = client;
    }

    @Override
    public void execute() {
        try {
            log.info("DownloadSymbols: Start");
            List<Symbol> allSymbols = client.getSymbols();
            repository.saveAll(allSymbols);
            log.info("DownloadSymbols: Done");
        } catch (ClientException e) {
            log.error("DownloadSymbols: Error: " + e.getMessage(), e);
        }
    }
}
