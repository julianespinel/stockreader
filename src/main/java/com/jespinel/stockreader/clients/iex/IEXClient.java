package com.jespinel.stockreader.clients.iex;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.common.base.Strings;
import com.jespinel.stockreader.clients.ClientException;
import com.jespinel.stockreader.clients.StockAPIClient;
import com.jespinel.stockreader.entities.Price;
import com.jespinel.stockreader.entities.Stats;
import com.jespinel.stockreader.entities.Symbol;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.List;
import java.util.stream.Collectors;

import static java.time.temporal.ChronoUnit.SECONDS;

@Component
@ConditionalOnProperty(
        value = "stockApiProvider",
        havingValue = "iex",
        matchIfMissing = true
)
public class IEXClient implements StockAPIClient {

    private static final Logger log = LoggerFactory.getLogger(IEXClient.class);

    private final ObjectMapper objectMapper;
    private final String apiKey;
    private final String host;

    @Autowired
    public IEXClient(ObjectMapper objectMapper,
                     @Value("${iex.api_key}") String apiKey,
                     @Value("${iex.host}") String host) {

        validateOrThrow(apiKey, "apiKey should not be empty or null");
        validateOrThrow(host, "host should not be empty or null");

        this.objectMapper = objectMapper;
        this.apiKey = apiKey;
        this.host = host;
    }

    //-------------------------------------------------------------------------
    // public methods
    //-------------------------------------------------------------------------

    @Override
    public List<Symbol> getSymbols() throws ClientException {
        try {
            String url = "%s/ref-data/iex/symbols?token=%s".formatted(host, apiKey);
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(new URI(url))
                    .timeout(Duration.of(30, SECONDS))
                    .GET()
                    .build();

            HttpClient client = HttpClient.newHttpClient();
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            if (response.statusCode() != HttpStatus.OK.value()) {
                String errorMessage = "Error %s getting symbols from IEX Cloud. Details: url: %s, response: %s"
                        .formatted(response.statusCode(), url, response.body());
                log.error(errorMessage);
                throw new ClientException(errorMessage);
            }

            TypeReference<List<Symbol>> symbolList = new TypeReference<>() {
            };
            return objectMapper.readValue(response.body(), symbolList);

        } catch (IOException | InterruptedException | URISyntaxException e) {
            log.error(e.getMessage(), e);
            throw new ClientException(e.getMessage(), e);
        }
    }

    @Override
    public Stats getSymbolStats(Symbol symbol) throws ClientException {
        try {
            String url = "%s/stock/%s/stats?token=%s".formatted(host, symbol.getSymbol(), apiKey);
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(new URI(url))
                    .timeout(Duration.of(30, SECONDS))
                    .GET()
                    .build();

            HttpClient client = HttpClient.newHttpClient();
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            if (response.statusCode() != HttpStatus.OK.value()) {
                String errorMessage = "Error %s getting symbol stats from IEX Cloud. Details: url: %s, response: %s"
                        .formatted(response.statusCode(), url, response.body());
                log.error(errorMessage);
                throw new ClientException(errorMessage);
            }

            IEXStats iexStats = objectMapper.readValue(response.body(), IEXStats.class);
            return iexStats.toStats(symbol.getSymbol());

        } catch (IOException | InterruptedException | URISyntaxException e) {
            log.error(e.getMessage(), e);
            throw new ClientException(e.getMessage(), e);
        }
    }

    @Override
    public List<Price> getSymbolPricesLastFiveYears(Symbol symbol) throws ClientException {
        try {
            String timeRange = "5y";
            String url = "%s/stock/%s/chart/%s?token=%s"
                    .formatted(host, symbol.getSymbol(), timeRange, apiKey);
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(new URI(url))
                    .timeout(Duration.of(30, SECONDS))
                    .GET()
                    .build();

            HttpClient client = HttpClient.newHttpClient();
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            if (response.statusCode() != HttpStatus.OK.value()) {
                String errorMessage = "Error %s getting %s prices from IEX Cloud. Details: url: %s, response: %s"
                        .formatted(response.statusCode(), symbol.getSymbol(), url, response.body());
                log.error(errorMessage);
                throw new ClientException(errorMessage);
            }

            TypeReference<List<IEXPrice>> symbolList = new TypeReference<>() {};
            List<IEXPrice> iexPrices = objectMapper.readValue(response.body(), symbolList);
            return iexPrices.stream().map(IEXPrice::toPrice).collect(Collectors.toList());

        } catch (IOException | InterruptedException | URISyntaxException e) {
            log.error(e.getMessage(), e);
            throw new ClientException(e.getMessage(), e);
        }
    }

    @Override
    public List<Price> getMarketPricesPreviousDay() throws ClientException {
        try {
            String url = "%s/stock/market/previous?token=%s".formatted(host, apiKey);
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(new URI(url))
                    .timeout(Duration.of(30, SECONDS))
                    .GET()
                    .build();

            HttpClient client = HttpClient.newHttpClient();
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            if (response.statusCode() != HttpStatus.OK.value()) {
                String errorMessage = "Error %s getting market prices from IEX Cloud. Details: url: %s, response: %s"
                        .formatted(response.statusCode(), url, response.body());
                log.error(errorMessage);
                throw new ClientException(errorMessage);
            }

            TypeReference<List<IEXPrice>> symbolList = new TypeReference<>() {};
            List<IEXPrice> iexPrices = objectMapper.readValue(response.body(), symbolList);
            return iexPrices.stream().map(IEXPrice::toPrice).collect(Collectors.toList());

        } catch (IOException | InterruptedException | URISyntaxException e) {
            log.error(e.getMessage(), e);
            throw new ClientException(e.getMessage(), e);
        }
    }

    //-------------------------------------------------------------------------
    // private methods
    //-------------------------------------------------------------------------

    private void validateOrThrow(String string, String errorMessage) {
        if (Strings.isNullOrEmpty(string)) {
            throw new IllegalArgumentException(errorMessage);
        }
    }
}
