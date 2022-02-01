package com.jespinel.stockreader.scheduled_jobs;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class Scheduler {

    private final DownloadSymbols downloadSymbols;
    private final DownloadStats downloadStats;
    private final DownloadHistoricalPrices downloadHistoricalPrices;

    @Autowired
    public Scheduler(DownloadSymbols downloadSymbols, DownloadStats downloadStats,
                     DownloadHistoricalPrices downloadHistoricalPrices) {
        this.downloadSymbols = downloadSymbols;
        this.downloadStats = downloadStats;
        this.downloadHistoricalPrices = downloadHistoricalPrices;
    }

    // Every Sunday at 00:00
    @Scheduled(cron = "0 0 0 ? * SUN", zone = "UTC")
    public void downloadSymbols() {
        downloadSymbols.execute();
    }

    // Every Monday at 00:00
    @Scheduled(cron = "0 0 0 ? * MON", zone = "UTC")
    public void downloadStats() {
        downloadStats.execute();
    }

    // At 3:00am on the 1st and 15th of each month
    @Scheduled(cron = "0 0 3 1,15 * *", zone = "UTC")
    public void downloadHistoricalPrices() {
        downloadHistoricalPrices.execute();
    }
}
