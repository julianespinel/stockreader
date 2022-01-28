package com.jespinel.stockreader;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.jespinel.stockreader.clients.MockServerConfigurations;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockserver.client.MockServerClient;
import org.mockserver.junit.jupiter.MockServerExtension;
import org.mockserver.junit.jupiter.MockServerSettings;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.jdbc.JdbcTestUtils;
import org.testcontainers.containers.PostgreSQLContainer;

@ExtendWith(MockServerExtension.class)
@MockServerSettings(ports = {18080})
@SpringBootTest
public class AbstractContainerBaseTest {

    private static final String TEST_POSTGRES_DB_NAME = "stockreaderdb_test";
    private static final String TEST_POSTGRES_USERNAME = "postgres";
    private static final String TEST_POSTGRES_PASSWORD = "example";

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Autowired
    protected TestFactories testFactories;

    @Autowired
    protected ObjectMapper objectMapper;

    @Autowired
    protected MockServerConfigurations serverConfig;

    protected static MockServerClient mockServer;

    @BeforeAll
    static void setupClass(MockServerClient mockServerClient) {
        mockServer = mockServerClient;
        mockServer.reset();
    }

    private static final PostgreSQLContainer<?> postgres;

    // Start a single container per all test cases that extend this class.
    static {
        postgres = new PostgreSQLContainer<>("postgres:14-alpine")
                .withDatabaseName(TEST_POSTGRES_DB_NAME)
                .withUsername(TEST_POSTGRES_USERNAME)
                .withPassword(TEST_POSTGRES_PASSWORD)
                .withReuse(true);
        postgres.start();
    }

    protected void cleanDatabase() {
        String[] tables = {"stats", "symbols"};
        JdbcTestUtils.deleteFromTables(jdbcTemplate, tables);
    }
}
