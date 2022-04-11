package com.jespinel.stockreader.scheduled_jobs;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class Scheduler {

    private final DownloadSymbols downloadSymbols;
    private final DownloadStats downloadStats;
    private final DownloadPrices downloadPrices;

    @Autowired
    public Scheduler(DownloadSymbols downloadSymbols, DownloadStats downloadStats,
                     DownloadPrices downloadPrices) {
        this.downloadSymbols = downloadSymbols;
        this.downloadStats = downloadStats;
        this.downloadPrices = downloadPrices;
    }

    // Every day at 06:00 UTC
    @Scheduled(cron = "0 0 6 * * MON-FRI", zone = "UTC")
    public void downloadSymbols() {
        downloadSymbols.execute();
    }

    // Every Sunday at 00:00 UTC
    @Scheduled(cron = "0 0 0 * * SUN", zone = "UTC")
    public void downloadStats() {
        downloadStats.execute();
    }

    // Every weekday at 07:00 UTC
    @Scheduled(cron = "0 0 7 * * MON-FRI", zone = "UTC")
    public void downloadPreviousDayPrices() {
        downloadPrices.execute();
    }
}
