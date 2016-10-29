# Stockreader

[![Build Status](https://travis-ci.org/julianespinel/stockreader.svg?branch=master)](https://travis-ci.org/julianespinel/stockreader)
[![Coverage Status](https://coveralls.io/repos/github/julianespinel/stockreader/badge.svg?branch=master)](https://coveralls.io/github/julianespinel/stockreader?branch=master)

Read stock data from the US stock market.

## Description

Stockreader is a system that retrieves current stock data and historical stock data from the US stock market.

The system executes this steps automatically at start-up:

1. Read the stocks from the files listed in the config-*.toml file.
2. Save the stocks of the step one into the DB.
3. Download and save the stock historical data of the past ten years.

Additionally the system repeat the following tasks in different period of times:

1. Download and save the stocks current data every one hour.
4. Download and save the stocks historical data of the past week every day at 18:00.
5. Download and save the stock historical data of the past ten years every last day of the month at 23:00.

This recurring tasks guarantee that the system has the historical stock data of at least the last 10 years.

## How to install?

#### 1. Dependencies

The only two dependencies stockreader needs to install are:

1. [docker-engine](https://docs.docker.com/engine/installation) (It will automatically install docker-compose in Windows and OS X. If you are using Linux please go to step 2 of this list)
2. [docker-compose](https://docs.docker.com/compose/install)

#### 2. Installation steps

Please copy and paste this commands in the terminal:

1. `git clone git@github.com:julianespinel/stockreader.git` <br>
2. `cd stockreader/scripts` <br>
3. `sh start-docker.sh`

Now open a web browser and go to: `http://localhost:5000/stockreader/admin/ping` <br>
If you can see `pong` in the web browser, then Stockreader is being correctly installed.

## Tests

1. Run all Tests: `nosetests`
1. Run a single test file: `nosetests test/job_test.py`

## How to use?

Stockreader has a simple HTTP API,  with it you can request stock current data and historical data. <br>
Please refer to the API documentation. * link.

## Generate API docs

To generate API docs please follow this steps:

1. `npm install -g aglio`
2. `cd docs/`
3. `aglio -i input.apib -s`
4. `http://localhost:3000`
