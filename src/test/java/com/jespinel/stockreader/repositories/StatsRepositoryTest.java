package com.jespinel.stockreader.repositories;

import com.jespinel.stockreader.AbstractContainerBaseTest;
import com.jespinel.stockreader.entities.Stats;
import com.jespinel.stockreader.entities.Symbol;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.Collections;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

class StatsRepositoryTest extends AbstractContainerBaseTest {

    @Autowired
    private StatsRepository repository;

    @BeforeEach
    void setUp() {
        cleanDatabase();
    }

    @Test
    void getAll_givenThatTableIsEmpty_returnsEmptyList() {
        // act
        List<Stats> stats = repository.getAll();
        // assert
        assertThat(stats).isEmpty();
    }

    @Test
    void getAll_givenThatTableIsNotEmpty_returnsSymbolsList() {
        // arrange
        int quantity = 5;
        List<Symbol> symbols = testFactories.createRandomSymbols(quantity);
        testFactories.createSymbolStats(symbols);
        // act
        List<Stats> stats = repository.getAll();
        // assert
        assertThat(stats).hasSize(quantity);
    }

    @Test
    void saveAll_givenEmptyList_savesNothing() {
        // arrange
        List<Stats> stats = Collections.emptyList();
        // act
        repository.saveAll(stats);
        // assert
        List<Stats> savedStats = repository.getAll();
        assertThat(savedStats).isEmpty();
    }

    @Test
    void saveAll_givenNonEmptyList_savesStats() {
        // arrange
        int quantity = 7;
        List<Symbol> symbols = testFactories.createRandomSymbols(quantity);
        List<Stats> stats = testFactories.getStatsForSymbols(symbols);
        // act
        repository.saveAll(stats);
        // assert
        List<Stats> savedStats = repository.getAll();
        assertThat(savedStats).hasSize(quantity);
    }

    @Test
    void saveAll_givenDuplicatedStats_updatesStats() {
        // arrange
        int quantity = 7;
        List<Symbol> symbols = testFactories.createRandomSymbols(quantity);
        List<Stats> stats = testFactories.getStatsForSymbols(symbols);
        repository.saveAll(stats);

        Stats original = stats.get(0);
        int delta = 1;
        Stats modifiedStats = testFactories.from(original, delta);
        // act
        repository.saveAll(Collections.singletonList(modifiedStats));
        // assert
        List<Stats> savedStats = repository.getAll();
        assertThat(savedStats).hasSize(quantity);

        Stats updated = repository.getBySymbol(original.getSymbol());
        checkUpdatedEqualsOriginalPlusDelta(updated, original, delta);
        assertThat(updated.getCreatedAt()).isEqualToIgnoringNanos(original.getCreatedAt());
        assertThat(updated.getUpdatedAt()).isNotEqualTo(original.getUpdatedAt());
    }

    private void checkUpdatedEqualsOriginalPlusDelta(Stats updated, Stats original, int delta) {
        assertThat(updated.getMarketcap()).isEqualTo(original.getMarketcap().add(BigInteger.valueOf(delta)));
        assertThat(updated.getSharesOutstanding()).isEqualTo(original.getSharesOutstanding().add(BigInteger.valueOf(delta)));
        assertThat(updated.getEmployees()).isEqualTo(original.getEmployees().add(BigInteger.valueOf(delta)));
        assertThat(updated.getTtmEps()).isEqualTo(original.getTtmEps().add(BigDecimal.valueOf(delta)));
        assertThat(updated.getTtmDividendRate()).isEqualTo(original.getTtmDividendRate().add(BigDecimal.valueOf(delta)));
        assertThat(updated.getDividendYield()).isEqualTo(original.getDividendYield().add(BigDecimal.valueOf(delta)));
        assertThat(updated.getNextDividendDate()).isEqualTo(original.getNextDividendDate().plusDays(delta));
        assertThat(updated.getExDividendDate()).isEqualTo(original.getExDividendDate().plusDays(delta));
        assertThat(updated.getNextEarningsDate()).isEqualTo(original.getNextEarningsDate().plusDays(delta));
        assertThat(updated.getPeRatio()).isEqualTo(original.getPeRatio().add(BigDecimal.valueOf(delta)));
        assertThat(updated.getBeta()).isEqualTo(original.getBeta().add(BigDecimal.valueOf(delta)));
    }
}
