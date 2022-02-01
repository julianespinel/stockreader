package com.jespinel.stockreader.scheduled_jobs;

import com.jespinel.stockreader.AbstractContainerBaseTest;
import com.jespinel.stockreader.entities.HistoricalPrice;
import com.jespinel.stockreader.entities.Symbol;
import com.jespinel.stockreader.repositories.HistoricalPriceRepository;
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
class DownloadHistoricalPricesTest extends AbstractContainerBaseTest {

    @Autowired
    private HistoricalPriceRepository repository;

    @Autowired
    private DownloadHistoricalPrices job;

    @BeforeEach
    void setUp() {
        mockServer.reset();
        cleanDatabase();
    }

    @Test
    void execute_givenNoExistingHistoricalPrices_saveHistoricalPrices(CapturedOutput logOutput) throws IOException {
        // arrange
        Symbol symbol = testFactories.createSymbol("AAPL", "Apple Inc");
        serverConfig.whenGettingHistoricalPricesReturn200AndValidHistoricalPrices(mockServer, symbol);
        // act
        job.execute();
        // assert
        List<HistoricalPrice> prices = repository.getBySymbol(symbol.getSymbol());
        assertThat(prices).hasSize(5);
        assertThat(logOutput).contains("DownloadHistoricalPrices: Done");
    }

    @Test
    void execute_givenClientException_logErrorMessage(CapturedOutput logOutput) {
        // arrange
        int quantity = 1;
        Symbol symbol = testFactories.createRandomSymbols(quantity).get(0);
        serverConfig.whenGettingHistoricalPricesReturn403(mockServer, symbol);
        // act
        job.execute();
        // assert
        String error = "Error 403 getting %s historical prices from IEX Cloud".formatted(symbol.getSymbol());
        assertThat(logOutput).contains(error);
    }
}
