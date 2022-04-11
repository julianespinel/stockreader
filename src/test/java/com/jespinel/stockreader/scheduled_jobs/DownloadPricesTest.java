package com.jespinel.stockreader.scheduled_jobs;

import com.jespinel.stockreader.AbstractContainerBaseTest;
import com.jespinel.stockreader.entities.Price;
import com.jespinel.stockreader.entities.Symbol;
import com.jespinel.stockreader.repositories.PriceRepository;
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
class DownloadPricesTest extends AbstractContainerBaseTest {

    @Autowired
    private PriceRepository repository;

    @Autowired
    private DownloadPrices job;

    @BeforeEach
    void setUp() {
        mockServer.reset();
        cleanDatabase();
    }

    @Test
    void execute_givenNoExistingPrices_savePrices(CapturedOutput logOutput) throws IOException {
        // arrange
        testFactories.createAllSymbols(objectMapper);
        serverConfig.whenGettingMarketPricesFromPreviousDayReturn200AndValidPrices(mockServer);
        // act
        job.execute();
        // assert
        List<Price> prices = repository.getBySymbol("AAPL");
        assertThat(prices).hasSize(1);
        assertThat(logOutput).contains("DownloadPrices: Done");
    }

    @Test
    void execute_givenClientException_logErrorMessage(CapturedOutput logOutput) {
        // arrange
        int quantity = 1;
        Symbol symbol = testFactories.createRandomSymbols(quantity).get(0);
        serverConfig.whenGettingMarketPricesFromPreviousDayReturn403(mockServer);
        // act
        job.execute();
        // assert
        String error = "Error 403 getting market prices from IEX Cloud";
        assertThat(logOutput).contains(error);
    }
}
