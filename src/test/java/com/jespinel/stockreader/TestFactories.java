package com.jespinel.stockreader;

import com.github.javafaker.Faker;
import com.jespinel.stockreader.entities.Symbol;
import com.jespinel.stockreader.repositories.SymbolRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class TestFactories {

    private static final Faker faker = new Faker();

    private final SymbolRepository symbolRepository;

    @Autowired
    public TestFactories(SymbolRepository symbolRepository) {
        this.symbolRepository = symbolRepository;
    }

    public Symbol getRandomSymbol() {
        String symbol = faker.stock().nsdqSymbol();
        String name = faker.company().name();
        return new Symbol(symbol, name);
    }

    public Symbol getRandomSymbol(int index) {
        String symbol = faker.stock().nsdqSymbol() + index;
        String name = faker.company().name();
        return new Symbol(symbol, name);
    }

    public List<Symbol> getRandomSymbolList(int quantity) {
        List<Symbol> symbols = new ArrayList<>(quantity);
        for (int i = 0; i < quantity; i++) {
            Symbol symbol = getRandomSymbol(i);
            symbols.add(symbol);
        }
        return symbols;
    }

    public List<Symbol> createRandomSymbols(int quantity) {
        List<Symbol> symbols = new ArrayList<>(quantity);
        for (int i = 0; i < quantity; i++) {
            Symbol symbol = getRandomSymbol(i);
            symbols.add(symbol);
        }
        symbolRepository.saveAll(symbols);
        return symbols;
    }
}
