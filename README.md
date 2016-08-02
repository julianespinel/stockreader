# Stockboard

[![Build Status](https://travis-ci.org/julianespinel/stockboard.svg?branch=master)](https://travis-ci.org/julianespinel/stockboard)
[![Coverage Status](https://coveralls.io/repos/github/julianespinel/stockboard/badge.svg?branch=master)](https://coveralls.io/github/julianespinel/stockboard?branch=master)

Stockboard helps investors to select the next public company to invest in.

## Description

The Stockboard system is composed by four microservices that perform independent and well defined business tasks:

1. Stocks Reader * add link to repository<br>
It's responsible for keeping the Stockboard database up to date. This system reads the stock data from the internet and saves it into the system's DB.

2. Portfolio Manager * add link to repository<br>
It's responsible for managing the portfolios of the investors. This system creates, updates and deletes portfolios.

3. Market Analyzer * add link to repository<br>
It's responsible for executing analysis on the stock market. This system answers questions about the stock market. e.g: "Which stocks have lost more than 15% in the last 5 days?".

4. Stockboard-UI * add link to repository<br>
The Stockboard-UI is responsible for the graphic user interaface. It is a web application that provides a simple way to use the Stockboard platform.

## How to install?

Stockboard is an open source project. You can either use the public deployment or you can download it and run a private deployment.

### Public deployment

Just go to: * public deployment URL

### Private deployment

In order to have a private deployment you have to install the dependencies and follow some simple steps using the terminal.

#### 1. Dependencies

The only two dependencies Stockboard needs to install are:
1. docker-engine * link
2. docker-compose * link (It will be automatically installed in Windows and OS X, follow the link if you are in Linux)

#### 2. Installation steps

Please copy and paste this commands in the terminal:

1. `git clone git@github.com:julianespinel/stockboard.git` <br>
2. `cd stockboard/scripts` <br>
3. `sh install.sh`

Now open a web browser and go to: http://private-host-url/stockboard <br>
If you can see a screenshot like this you have installed it correctly.

* add screenshot

## How to use?

1. Register * link
2. Login * link
3. Once you are in the home screen you can use three features:
  1. See and modify your portfolios * link
  2. Perform analysis over the US stock market * link
  3. Subscribe to analysis sent daily, weekly or monthly to your email.

