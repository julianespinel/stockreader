package com.jespinel.stockreader.clients;

import com.jespinel.stockreader.AbstractContainerBaseTest;
import com.jespinel.stockreader.clients.iex.IEXClient;
import com.jespinel.stockreader.entities.HistoricalPrice;
import com.jespinel.stockreader.entities.Stats;
import com.jespinel.stockreader.entities.Symbol;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

import java.io.IOException;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;

class IEXClientTest extends AbstractContainerBaseTest {

    @Autowired
    private IEXClient client;

    @BeforeEach
    void setUp() {
        mockServer.reset();
        cleanDatabase();
    }

    //-------------------------------------------------------------------------
    // Get Symbols tests
    //-------------------------------------------------------------------------

    @Test
    void getSymbols_gets200_returnsListOfSymbols() throws IOException, ClientException {
        // arrange
        serverConfig.whenGettingSymbolsReturn200AndValidSymbolList(mockServer);
        // act
        List<Symbol> symbols = client.getSymbols();
        // assert
        assertThat(symbols).hasSize(3);
    }

    @Test
    void getSymbols_gets403_throwsClientException() {
        // arrange
        serverConfig.whenGettingSymbolsReturn403(mockServer);
        // act and assert
        assertThrows(ClientException.class, () -> client.getSymbols());
    }

    @Test
    void getSymbols_getsMalformedJsonResponse_throwsClientException() throws IOException {
        // arrange
        serverConfig.whenGettingSymbolsReturn200AndNotValidJsonBody(mockServer);
        // act and assert
        assertThrows(ClientException.class, () -> client.getSymbols());
    }

    //-------------------------------------------------------------------------
    // Get symbol stats tests
    //-------------------------------------------------------------------------

    @Test
    void getSymbolStats_gets200_returnsSymbolStats() throws ClientException, IOException {
        // arrange
        Symbol symbol = testFactories.getRandomSymbol();
        serverConfig.whenGettingStatsReturn200AndValidStats(mockServer, symbol);
        // act
        Stats stats = client.getSymbolStats(symbol);
        // assert
        assertThat(stats.getSymbol()).isEqualTo(symbol.getSymbol());
        assertThat(stats.getMarketcap().toString()).isEqualTo("2872053733394");
        assertThat(stats.getTtmEps().toString()).isEqualTo("11.67");
        assertThat(stats.getExDividendDate().toString()).isEqualTo("2021-10-23");
        assertThat(stats.getPeRatio().toString()).isEqualTo("15.265667005447652");
    }

    @Test
    void getSymbolStats_gets403_throwsClientException() throws IOException {
        // arrange
        Symbol symbol = testFactories.getRandomSymbol();
        serverConfig.whenGettingStatsReturn403(mockServer, symbol);
        // act and assert
        assertThrows(ClientException.class, () -> client.getSymbolStats(symbol));
    }

    @Test
    void getSymbolStats_getsMalformedJsonResponse_throwsClientException() throws IOException {
        // arrange
        Symbol symbol = testFactories.getRandomSymbol();
        serverConfig.whenGettingStatsReturn200AndNotValidJsonBody(mockServer, symbol);
        // act and assert
        assertThrows(ClientException.class, () -> client.getSymbolStats(symbol));
    }

    //-------------------------------------------------------------------------
    // Get symbol historical prices last five years tests
    //-------------------------------------------------------------------------

    @Test
    void getSymbolHistoricalPrices_gets200_returnsSymbolHistoricalPrices() throws ClientException, IOException {
        // arrange
        Symbol symbol = testFactories.getRandomSymbol();
        serverConfig.whenGettingHistoricalPricesReturn200AndValidHistoricalPrices(mockServer, symbol);
        // act
        List<HistoricalPrice> prices = client.getSymbolHistoricalPricesLastFiveYears(symbol);
        // assert
        assertThat(prices).hasSize(5);

        HistoricalPrice firstPrice = prices.get(0);
        assertThat(firstPrice.getSymbol()).isEqualTo("AAPL");
        assertThat(firstPrice.getDate().toString()).isEqualTo("2017-02-01");
        assertThat(firstPrice.getOpen().toString()).isEqualTo("30.0731");
        assertThat(firstPrice.getClose().toString()).isEqualTo("30.6431");
        assertThat(firstPrice.getHigh().toString()).isEqualTo("31.232");
        assertThat(firstPrice.getLow().toString()).isEqualTo("29.972");
        assertThat(firstPrice.getVolume().toString()).isEqualTo("465511602");
        assertThat(firstPrice.getChange().toString()).isEqualTo("0");
        assertThat(firstPrice.getChangePercent().toString()).isEqualTo("0");
    }

    @Test
    void getSymbolHistoricalPrices_gets403_throwsClientException() {
        // arrange
        Symbol symbol = testFactories.getRandomSymbol();
        serverConfig.whenGettingHistoricalPricesReturn403(mockServer, symbol);
        // act and assert
        assertThrows(ClientException.class, () -> client.getSymbolHistoricalPricesLastFiveYears(symbol));
    }

    @Test
    void getSymbolHistoricalPrices_getsMalformedJsonResponse_throwsClientException() throws IOException {
        // arrange
        Symbol symbol = testFactories.getRandomSymbol();
        serverConfig.whenGettingHistoricalPricesReturn200AndNotValidJsonBody(mockServer, symbol);
        // act and assert
        assertThrows(ClientException.class,() -> client.getSymbolHistoricalPricesLastFiveYears(symbol));
    }
}
