package com.jespinel.stockreader.scheduled_jobs;

import com.jespinel.stockreader.AbstractContainerBaseTest;
import com.jespinel.stockreader.entities.Stats;
import com.jespinel.stockreader.entities.Symbol;
import com.jespinel.stockreader.repositories.StatsRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.system.CapturedOutput;
import org.springframework.boot.test.system.OutputCaptureExtension;

import java.io.IOException;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

@ExtendWith(OutputCaptureExtension.class)
class DownloadStatsTest extends AbstractContainerBaseTest {

    @Autowired
    private StatsRepository repository;

    @Autowired
    private DownloadStats job;

    @BeforeEach
    void setUp() {
        mockServer.reset();
        cleanDatabase();
    }

    @Test
    void execute_givenNoExistingStats_saveStats(CapturedOutput logOutput) throws IOException {
        // arrange
        int quantity = 5;
        List<Symbol> symbols = testFactories.createRandomSymbols(quantity);
        for (Symbol symbol : symbols) {
            serverConfig.whenGettingStatsReturn200AndValidStats(mockServer, symbol);
        }
        // act
        job.execute();
        // assert
        List<Stats> stats = repository.getAll();
        assertThat(stats).hasSize(quantity);
        assertThat(logOutput).contains("DownloadStats: Done");
    }

    @Test
    void execute_givenClientException_logErrorMessage(CapturedOutput logOutput) throws IOException {
        // arrange
        int quantity = 1;
        List<Symbol> symbols = testFactories.createRandomSymbols(quantity);
        for (Symbol symbol : symbols) {
            serverConfig.whenGettingStatsReturn403(mockServer, symbol);
        }
        // act
        job.execute();
        // assert
        assertThat(logOutput).contains("Error 403 getting symbol stats from IEX Cloud");
    }
}
