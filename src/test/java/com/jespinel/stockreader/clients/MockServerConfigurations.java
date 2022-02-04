package com.jespinel.stockreader.clients;

import com.jespinel.stockreader.entities.Symbol;
import org.mockserver.client.MockServerClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.util.ResourceUtils;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;

import static org.mockserver.model.HttpRequest.request;
import static org.mockserver.model.HttpResponse.response;

@Component
public class MockServerConfigurations {

    @Value("${iex.api_key}")
    private String apiKey;

    public void whenGettingSymbolsReturn200AndValidSymbolList(MockServerClient mockServer) throws IOException {
        File file = ResourceUtils.getFile("classpath:mockserver_responses/symbols.json");
        String expectedBody = new String(Files.readAllBytes(file.toPath()));

        mockServer.when(
                        request()
                                .withMethod("GET")
                                .withPath("/ref-data/iex/symbols")
                                .withQueryStringParameter("token", apiKey)
                )
                .respond(
                        response()
                                .withStatusCode(200)
                                .withBody(expectedBody)
                );
    }

    public void whenGettingSymbolsReturn403(MockServerClient mockServer) {
        mockServer.when(
                        request()
                                .withMethod("GET")
                                .withPath("/ref-data/iex/symbols")
                                .withQueryStringParameter("token", apiKey)
                )
                .respond(response().withStatusCode(403));
    }

    public void whenGettingSymbolsReturn200AndNotValidJsonBody(MockServerClient mockServer) throws IOException {
        File file = ResourceUtils.getFile("classpath:mockserver_responses/not_valid.json");
        String expectedBody = new String(Files.readAllBytes(file.toPath()));
        mockServer.when(
                        request()
                                .withMethod("GET")
                                .withPath("/ref-data/iex/symbols")
                                .withQueryStringParameter("token", apiKey)
                )
                .respond(
                        response()
                                .withStatusCode(200)
                                .withBody(expectedBody)
                );
    }

    public void whenGettingStatsReturn200AndValidStats(MockServerClient mockServer, Symbol symbol) throws IOException {
        File file = ResourceUtils.getFile("classpath:mockserver_responses/symbol_stats.json");
        String expectedBody = new String(Files.readAllBytes(file.toPath()));

        mockServer.when(
                        request()
                                .withMethod("GET")
                                .withPath("/stock/%s/stats".formatted(symbol.getSymbol()))
                                .withQueryStringParameter("token", apiKey)
                )
                .respond(
                        response()
                                .withStatusCode(200)
                                .withBody(expectedBody)
                );
    }

    public void whenGettingStatsReturn403(MockServerClient mockServer, Symbol symbol) throws IOException {
        File file = ResourceUtils.getFile("classpath:mockserver_responses/symbol_stats.json");
        String expectedBody = new String(Files.readAllBytes(file.toPath()));

        mockServer.when(
                        request()
                                .withMethod("GET")
                                .withPath("/stock/%s/stats".formatted(symbol.getSymbol()))
                                .withQueryStringParameter("token", apiKey)
                )
                .respond(response().withStatusCode(403));
    }

    public void whenGettingStatsReturn200AndNotValidJsonBody(MockServerClient mockServer, Symbol symbol) throws IOException {
        File file = ResourceUtils.getFile("classpath:mockserver_responses/not_valid.json");
        String expectedBody = new String(Files.readAllBytes(file.toPath()));

        mockServer.when(
                        request()
                                .withMethod("GET")
                                .withPath("/stock/%s/stats".formatted(symbol.getSymbol()))
                                .withQueryStringParameter("token", apiKey)
                )
                .respond(
                        response()
                                .withStatusCode(200)
                                .withBody(expectedBody)
                );
    }

    public void whenGettingPricesReturn200AndValidPrices(MockServerClient mockServer, Symbol symbol) throws IOException {
        File file = ResourceUtils.getFile("classpath:mockserver_responses/symbol_prices.json");
        String expectedBody = new String(Files.readAllBytes(file.toPath()));

        String timeRange = "5y";
        mockServer.when(
                        request()
                                .withMethod("GET")
                                .withPath("/stock/%s/chart/%s".formatted(symbol.getSymbol(), timeRange))
                                .withQueryStringParameter("token", apiKey)
                )
                .respond(
                        response()
                                .withStatusCode(200)
                                .withBody(expectedBody)
                );
    }

    public void whenGettingPricesReturn403(MockServerClient mockServer, Symbol symbol) {
        String timeRange = "5y";
        mockServer.when(
                        request()
                                .withMethod("GET")
                                .withPath("/stock/%s/chart/%s".formatted(symbol.getSymbol(), timeRange))
                                .withQueryStringParameter("token", apiKey)
                )
                .respond(response().withStatusCode(403));
    }


    public void whenGettingPricesReturn200AndNotValidJsonBody(MockServerClient mockServer, Symbol symbol) throws IOException {
        File file = ResourceUtils.getFile("classpath:mockserver_responses/not_valid.json");
        String expectedBody = new String(Files.readAllBytes(file.toPath()));

        String timeRange = "5y";
        mockServer.when(
                        request()
                                .withMethod("GET")
                                .withPath("/stock/%s/chart/%s".formatted(symbol.getSymbol(), timeRange))
                                .withQueryStringParameter("token", apiKey)
                )
                .respond(
                        response()
                                .withStatusCode(200)
                                .withBody(expectedBody)
                );
    }

    public void whenGettingMarketPricesFromPreviousDayReturn200AndValidPrices(MockServerClient mockServer) throws IOException {
        File file = ResourceUtils.getFile("classpath:mockserver_responses/market_previous_day_prices.json");
        String expectedBody = new String(Files.readAllBytes(file.toPath()));

        mockServer.when(
                        request()
                                .withMethod("GET")
                                .withPath("/stock/market/previous")
                                .withQueryStringParameter("token", apiKey)
                )
                .respond(
                        response()
                                .withStatusCode(200)
                                .withBody(expectedBody)
                );
    }

    public void whenGettingMarketPricesFromPreviousDayReturn403(MockServerClient mockServer) {
        mockServer.when(
                        request()
                                .withMethod("GET")
                                .withPath("/stock/market/previous")
                                .withQueryStringParameter("token", apiKey)
                )
                .respond(response().withStatusCode(403));
    }

    public void whenGettingMarketPricesFromPreviousDayReturn200AndNotValidJsonBody(MockServerClient mockServer) throws IOException {
        File file = ResourceUtils.getFile("classpath:mockserver_responses/not_valid.json");
        String expectedBody = new String(Files.readAllBytes(file.toPath()));

        mockServer.when(
                        request()
                                .withMethod("GET")
                                .withPath("/stock/market/previous")
                                .withQueryStringParameter("token", apiKey)
                )
                .respond(
                        response()
                                .withStatusCode(200)
                                .withBody(expectedBody)
                );
    }
}
