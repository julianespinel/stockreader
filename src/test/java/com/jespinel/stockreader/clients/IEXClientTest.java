package com.jespinel.stockreader.clients;

import com.jespinel.stockreader.AbstractContainerBaseTest;
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
}
