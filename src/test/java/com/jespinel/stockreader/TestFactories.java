package com.jespinel.stockreader;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.javafaker.Faker;
import com.jespinel.stockreader.entities.Price;
import com.jespinel.stockreader.entities.Stats;
import com.jespinel.stockreader.entities.Symbol;
import com.jespinel.stockreader.repositories.StatsRepository;
import com.jespinel.stockreader.repositories.SymbolRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.ResourceUtils;

import java.io.File;
import java.io.IOException;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.nio.file.Files;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

@Service
public class TestFactories {

    private static final Faker faker = new Faker();

    private final SymbolRepository symbolRepository;
    private final StatsRepository statsRepository;

    @Autowired
    public TestFactories(SymbolRepository symbolRepository, StatsRepository statsRepository) {
        this.symbolRepository = symbolRepository;
        this.statsRepository = statsRepository;
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

    public Symbol createSymbol(String symbol, String name) {
        Symbol aSymbol = new Symbol(symbol, name);
        symbolRepository.saveAll(Collections.singletonList(aSymbol));
        return aSymbol;
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

    public Stats getStatsForSymbol(String symbol, int index) {
        BigInteger integer = BigInteger.valueOf(index);
        BigDecimal decimal = BigDecimal.valueOf(index);
        LocalDate date = LocalDate.now().plusDays(index);
        return new Stats(symbol, integer, integer, integer, decimal, decimal,
                decimal, date, date, date, decimal, decimal);
    }

    public List<Stats> getStatsForSymbols(List<Symbol> symbols) {
        List<Stats> stats = new ArrayList<>();
        for (int i = 0; i < symbols.size(); i++) {
            Symbol symbol = symbols.get(i);
            Stats symbolStats = getStatsForSymbol(symbol.getSymbol(), i);
            stats.add(symbolStats);
        }
        return stats;
    }

    public List<Stats> createSymbolStats(List<Symbol> symbols) {
        List<Stats> stats = getStatsForSymbols(symbols);
        statsRepository.saveAll(stats);
        return stats;
    }

    /**
     * Return a new stats object containing the values of the given stat
     * plus a delta.
     *
     * @param stat  Original stat
     * @param delta Delta to add to all values
     * @return object containing the values of the given stat plus a delta.
     */
    public Stats from(Stats stat, int delta) {
        return new Stats(
                stat.getSymbol(),
                stat.getMarketcap().add(BigInteger.valueOf(delta)),
                stat.getSharesOutstanding().add(BigInteger.valueOf(delta)),
                stat.getEmployees().add(BigInteger.valueOf(delta)),
                stat.getTtmEps().add(BigDecimal.valueOf(delta)),
                stat.getTtmDividendRate().add(BigDecimal.valueOf(delta)),
                stat.getDividendYield().add(BigDecimal.valueOf(delta)),
                stat.getNextDividendDate().plusDays(delta),
                stat.getExDividendDate().plusDays(delta),
                stat.getNextEarningsDate().plusDays(delta),
                stat.getPeRatio().add(BigDecimal.valueOf(delta)),
                stat.getBeta().add(BigDecimal.valueOf(delta)),
                stat.getCreatedAt(),
                stat.getUpdatedAt().plusMinutes(delta)
        );
    }

    public Price getPriceForSymbol(Symbol symbol, int index) {
        LocalDate date = LocalDate.now().plusDays(index);
        BigDecimal bigDecimal = BigDecimal.valueOf(index);
        BigInteger bigInt = BigInteger.valueOf(index);
        return new Price(symbol.getSymbol(),
                date, bigDecimal, bigDecimal, bigDecimal, bigDecimal, bigInt,
                bigDecimal, bigDecimal);
    }

    public List<Price> getPricesForSymbol(Symbol symbol, int quantity) {
        List<Price> prices = new ArrayList<>(quantity);
        for (int i = 0; i < quantity; i++) {
            Price price = getPriceForSymbol(symbol, i);
            prices.add(price);
        }
        return prices;
    }

    /**
     * Return a new Price object containing the values of the given
     * price plus a delta.
     *
     * @param price Original price
     * @param delta Delta to add to all values
     * @return object containing the values of the given price plus a delta.
     */
    public Price from(Price price, int delta) {
        return new Price(
                price.getSymbol(),
                price.getDate(),
                price.getOpen().add(BigDecimal.valueOf(delta)),
                price.getClose().add(BigDecimal.valueOf(delta)),
                price.getHigh().add(BigDecimal.valueOf(delta)),
                price.getLow().add(BigDecimal.valueOf(delta)),
                price.getVolume().add(BigInteger.valueOf(delta)),
                price.getChange().add(BigDecimal.valueOf(delta)),
                price.getChangePercent().add(BigDecimal.valueOf(delta)),
                price.getCreatedAt(),
                price.getUpdatedAt().plusMinutes(delta)
        );
    }

    public void createAllSymbols(ObjectMapper mapper) throws IOException {
        File file = ResourceUtils.getFile("classpath:mockserver_responses/symbols.json");
        String symbolsString = new String(Files.readAllBytes(file.toPath()));
        TypeReference<List<Symbol>> symbolList = new TypeReference<>() {};
        List<Symbol> symbols = mapper.readValue(symbolsString, symbolList);
        symbolRepository.saveAll(symbols);
    }
}
