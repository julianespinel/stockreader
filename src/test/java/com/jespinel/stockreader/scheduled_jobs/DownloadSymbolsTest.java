package com.jespinel.stockreader.scheduled_jobs;

import com.jespinel.stockreader.AbstractContainerBaseTest;
import com.jespinel.stockreader.clients.ClientException;
import com.jespinel.stockreader.entities.Symbol;
import com.jespinel.stockreader.repositories.SymbolRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.system.CapturedOutput;
import org.springframework.boot.test.system.OutputCaptureExtension;

import java.io.IOException;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;

@ExtendWith(OutputCaptureExtension.class)
class DownloadSymbolsTest extends AbstractContainerBaseTest {

    @Autowired
    private SymbolRepository repository;

    @Autowired
    private DownloadSymbols job;

    @BeforeEach
    void setUp() {
        mockServer.reset();
        cleanDatabase();
    }

    @Test
    void execute_givenNoExistingSymbols_saveAllSymbols(CapturedOutput logOutput) throws IOException {
        // arrange
        serverConfig.whenGettingSymbolsReturn200AndValidSymbolList(mockServer);
        // act
        job.execute();
        // assert
        List<Symbol> symbols = repository.getAll();
        assertThat(symbols).hasSize(3);
        assertThat(logOutput).contains("DownloadSymbols: saved 3 new symbols");
    }

    @Test
    void execute_givenExistingSymbols_saveNewSymbolsOnly(CapturedOutput logOutput) throws IOException {
        // arrange
        testFactories.createRandomSymbols(5);
        serverConfig.whenGettingSymbolsReturn200AndValidSymbolList(mockServer);
        // act
        job.execute();
        // assert
        List<Symbol> symbols = repository.getAll();
        assertThat(symbols).hasSize(8);
        assertThat(logOutput).contains("DownloadSymbols: saved 3 new symbols");
    }

    @Test
    void execute_givenClientException_logErrorMessage(CapturedOutput logOutput) {
        // arrange
        serverConfig.whenGettingSymbolsReturn403(mockServer);
        // act
        job.execute();
        // assert
        assertThat(logOutput).contains("Error 403 getting symbols from IEX Cloud");
    }
}
