package com.jespinel.stockreader.scheduled_jobs;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class Scheduler {

    private final DownloadSymbols downloadSymbols;

    @Autowired
    public Scheduler(DownloadSymbols downloadSymbols) {
        this.downloadSymbols = downloadSymbols;
    }

    // Every sunday at 00:00
    @Scheduled(cron = "0 0 0 ? * SUN", zone = "UTC")
    public void downloadSymbols() {
        downloadSymbols.execute();
    }
}
