#!/usr/bin/python
# -*- coding: utf-8 -*-

# quandl_data.py

import pandas as pd
import urllib2


def construct_futures_symbols(symbol, start_year=2010, end_year=2014):
    """Constructs a list of futures contract codes for a 
    particular symbol and timeframe."""
    futures = []
    months = 'HMUZ'  # March, June, September and December delivery codes
    for y in range(start_year, end_year+1):
        for m in months:
            futures.append("%s%s%s" % (symbol, m, y))
    return futures

def download_contract_from_quandl(contract, auth_token, dl_dir):
    """Download an individual futures contract from Quandl and then
    store it to disk in the 'dl_dir' directory. An auth_token is 
    required, which is obtained from the Quandl upon sign-up."""

    # Construct the API call from the contract and auth_token    
    api_call_head = "http://www.quandl.com/api/v1/datasets/OFDP/FUTURE_%s.csv" % contract
    params = "?&auth_token=%s&sort_order=asc" % auth_token
    
    # Download the data from Quandl
    data = urllib2.urlopen("%s%s" % (api_call_head, params)).read()
    
    # Store the data to disk
    fc = open('%s/%s.csv' % (dl_dir, contract), 'w')
    fc.write(data)
    fc.close()

def download_historical_contracts(symbol, auth_token, dl_dir, start_year=2010, end_year=2014):
    """Downloads all futures contracts for a specified symbol
    between a start_year and an end_year."""
    contracts = construct_futures_symbols(symbol, start_year, end_year)
    for c in contracts:
        download_contract_from_quandl(c, auth_token, dl_dir)

if __name__ == "__main__":
    symbol = 'ES'

    # Make sure you've created this relative directory beforehand
    dl_dir = 'quandl/futures/ES'

    # Replace this with your authorisation token
    auth_token = 'YOUR_AUTH_TOKEN'
    start_year = 2010
    end_year = 2014

    # Download the contracts into the directory
    download_historical_contracts(symbol, auth_token, dl_dir, start_year, end_year)

    # Open up a single contract via read_csv and plot the closing price
    es = pd.io.parsers.read_csv("%s/ESZ2014.csv" % dl_dir)
