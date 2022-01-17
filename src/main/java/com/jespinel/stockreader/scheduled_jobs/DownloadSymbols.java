package com.jespinel.stockreader.scheduled_jobs;

import com.jespinel.stockreader.clients.ClientException;
import com.jespinel.stockreader.clients.StockAPIClient;
import com.jespinel.stockreader.entities.Symbol;
import com.jespinel.stockreader.repositories.SymbolRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

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
            List<Symbol> existingSymbols = repository.getAll();
            List<Symbol> allSymbols = client.getSymbols();
            List<Symbol> newSymbols = getNewSymbols(existingSymbols, allSymbols);
            repository.saveAll(newSymbols);
            log.info("DownloadSymbols: saved {} new symbols", newSymbols.size());
            log.info("DownloadSymbols: Done");
        } catch (ClientException e) {
            log.error("DownloadSymbols: Error: " + e.getMessage(), e);
        }
    }

    private List<Symbol> getNewSymbols(List<Symbol> existingSymbols, List<Symbol> allSymbols) {
        List<Symbol> newSymbols = new ArrayList<>();
        Map<String, Symbol> symbolsMap = existingSymbols.stream().collect(Collectors.toMap(Symbol::getSymbol, Function.identity()));
        for (Symbol symbol : allSymbols) {
            if (!symbolsMap.containsKey(symbol.getSymbol())) {
                newSymbols.add(symbol);
            }
        }
        return newSymbols;
    }
}
