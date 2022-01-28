package com.jespinel.stockreader.repositories;

import com.jespinel.stockreader.AbstractContainerBaseTest;
import com.jespinel.stockreader.entities.Symbol;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

import java.time.LocalDateTime;
import java.util.Collections;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

class SymbolRepositoryTest extends AbstractContainerBaseTest {

    @Autowired
    private SymbolRepository repository;

    @BeforeEach
    void setUp() {
        cleanDatabase();
    }

    @Test
    void getAll_givenThatTableIsEmpty_returnsEmptyList() {
        // act
        List<Symbol> symbols = repository.getAll();
        // assert
        assertThat(symbols).isEmpty();
    }

    @Test
    void getAll_givenThatTableIsNotEmpty_returnsSymbolsList() {
        // arrange
        int quantity = 5;
        testFactories.createRandomSymbols(quantity);
        // act
        List<Symbol> symbols = repository.getAll();
        // assert
        assertThat(symbols).hasSize(quantity);
    }

    @Test
    void saveAll_givenEmptyList_savesNothing() {
        // arrange
        List<Symbol> symbols = Collections.emptyList();
        // act
        repository.saveAll(symbols);
        // assert
        List<Symbol> savedSymbols = repository.getAll();
        assertThat(savedSymbols).isEmpty();
    }

    @Test
    void saveAll_givenNonEmptyList_savesSymbols() {
        // arrange
        int quantity = 7;
        List<Symbol> symbols = testFactories.getRandomSymbolList(quantity);
        // act
        repository.saveAll(symbols);
        // assert
        List<Symbol> savedSymbols = repository.getAll();
        assertThat(savedSymbols).hasSize(quantity);
    }

    @Test
    void saveAll_givenDuplicatedSymbols_updatesNameAndDate() {
        // arrange
        int quantity = 7;
        List<Symbol> symbols = testFactories.getRandomSymbolList(quantity);
        repository.saveAll(symbols);

        Symbol firstSymbol = symbols.get(0);
        String newName = "Some name";
        LocalDateTime date = LocalDateTime.now().plusMinutes(5);
        Symbol duplicatedSymbol = new Symbol(firstSymbol.getSymbol(), newName, date, date);
        // act
        repository.saveAll(Collections.singletonList(duplicatedSymbol));
        // assert
        List<Symbol> savedSymbols = repository.getAll();
        assertThat(savedSymbols).hasSize(quantity);

        Symbol updatedSymbol = repository.getBySymbol(firstSymbol.getSymbol());
        assertThat(updatedSymbol.getName()).isEqualTo(newName);
        assertThat(updatedSymbol.getCreatedAt()).isEqualToIgnoringNanos(firstSymbol.getCreatedAt());
        assertThat(updatedSymbol.getUpdatedAt()).isNotEqualTo(firstSymbol.getUpdatedAt());
    }
}
