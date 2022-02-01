package com.jespinel.stockreader.repositories;

import com.jespinel.stockreader.AbstractContainerBaseTest;
import com.jespinel.stockreader.entities.HistoricalPrice;
import com.jespinel.stockreader.entities.Symbol;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.Collections;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

class HistoricalPriceRepositoryTest extends AbstractContainerBaseTest {

    @Autowired
    private HistoricalPriceRepository repository;

    @BeforeEach
    void setUp() {
        cleanDatabase();
    }

    @Test
    void saveAll_givenEmptyList_savesNothing() {
        // arrange
        List<HistoricalPrice> prices = Collections.emptyList();
        // act
        repository.saveAll(prices);
        // assert
        Integer count = jdbcTemplate.queryForObject("SELECT COUNT(*) FROM historical_prices", Integer.class);
        assertThat(count).isZero();
    }

    @Test
    void saveAll_givenNonEmptyList_savesHistoricalPrices() {
        // arrange
        Symbol symbol = testFactories.createRandomSymbols(1).get(0);
        int quantity = 7;
        List<HistoricalPrice> generatedPrices = testFactories.getPricesForSymbol(symbol, quantity);
        // act
        repository.saveAll(generatedPrices);
        // assert
        List<HistoricalPrice> pricesFromDB = repository.getBySymbol(symbol.getSymbol());
        assertThat(pricesFromDB).hasSize(quantity);
        assertThat(pricesFromDB.get(0)).usingRecursiveComparison()
                .ignoringFields("createdAt", "updatedAt")
                .isEqualTo(generatedPrices.get(0));
    }

    @Test
    void saveAll_givenDuplicatedHistoricalPrices_updatesHistoricalPrices() {
        // arrange
        Symbol symbol = testFactories.createRandomSymbols(1).get(0);
        int quantity = 7;
        List<HistoricalPrice> generatedPrices = testFactories.getPricesForSymbol(symbol, quantity);
        repository.saveAll(generatedPrices);

        HistoricalPrice original = generatedPrices.get(0);
        int delta = 1;
        HistoricalPrice modified = testFactories.from(original, delta);
        // act
        repository.saveAll(Collections.singletonList(modified));
        // assert
        List<HistoricalPrice> savedPrices = repository.getBySymbol(symbol.getSymbol());
        assertThat(savedPrices).hasSize(quantity);

        HistoricalPrice updated = repository.getBySymbolAndDate(original.getSymbol(), original.getDate());
        checkUpdatedEqualsOriginalPlusDelta(updated, original, delta);
        assertThat(updated.getCreatedAt()).isEqualToIgnoringNanos(original.getCreatedAt());
        assertThat(updated.getUpdatedAt()).isNotEqualTo(original.getUpdatedAt());
    }

    private void checkUpdatedEqualsOriginalPlusDelta(HistoricalPrice updated, HistoricalPrice original, int delta) {
        assertThat(updated.getSymbol()).isEqualTo(original.getSymbol());
        assertThat(updated.getDate()).isEqualTo(original.getDate());
        assertThat(updated.getOpen()).isEqualTo(original.getOpen().add(BigDecimal.valueOf(delta)));
        assertThat(updated.getClose()).isEqualTo(original.getClose().add(BigDecimal.valueOf(delta)));
        assertThat(updated.getHigh()).isEqualTo(original.getHigh().add(BigDecimal.valueOf(delta)));
        assertThat(updated.getLow()).isEqualTo(original.getLow().add(BigDecimal.valueOf(delta)));
        assertThat(updated.getVolume()).isEqualTo(original.getVolume().add(BigInteger.valueOf(delta)));
        assertThat(updated.getChange()).isEqualTo(original.getChange().add(BigDecimal.valueOf(delta)));
        assertThat(updated.getChangePercent()).isEqualTo(original.getChangePercent().add(BigDecimal.valueOf(delta)));
    }
}
