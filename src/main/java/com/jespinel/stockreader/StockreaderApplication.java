package com.jespinel.stockreader;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@EnableScheduling
@SpringBootApplication
public class StockreaderApplication {

	public static void main(String[] args) {
		SpringApplication.run(StockreaderApplication.class, args);
	}
}
