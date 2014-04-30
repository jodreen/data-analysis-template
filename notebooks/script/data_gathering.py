
"""
Downloads Google Trends and stock data for search terms related to companies in the Dow Jones Index. 

Creates a csv file with "Date", "Google Trends value", and "Price" for each search term.

Files will be saved in the "../data/raw/" directory.
"""

# Imports all important modules for the program
import sys
import datetime
import pandas
import csv
import cookielib
import mechanize
import re
from StringIO import StringIO
 
# Reads "DowJones.csv" of stocks and ticker symbols into a pandas dataframe
def stocks_data(data='../data/DowJones.csv'):
    stocks = pandas.read_csv(data)
    company = stocks.Company
    ticker = stocks.Ticker
    return stocks, company, ticker
stocks, companies, tickers = stocks_data()


# Creates a list of lists with search terms for all companies in the format given by inputs
def query(*arg):
    queries = []
    for query in arg:
        queries.append([query[n] for n in range(0, len(stocks))])
    return queries       
queries = query(companies, tickers, "buy " + tickers, "sell " + tickers)

br = mechanize.Browser()
def browser_setup():
    # Open browser
    br.set_handle_robots(False)
    
    # Create cookie jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    
    # Act like we're a real browser
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    
    # Login in to Google
    response = br.open('https://accounts.google.com/ServiceLogin?hl=en&continue=https://www.google.com/')
    forms = mechanize.ParseResponse(response)
    form = forms[0]
    form['Email'] = "DherintoR"
    form['Passwd'] = "forthestars"
    response = br.open(form.click())
browser_setup()


# Pulls Yahoo Finance stock data for given ticker from 2004-present
def yahoo_finance(ticker_symbol):
    base_url = "http://ichart.yahoo.com/table.csv?s="
    dt_url = '%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s&g=d&ignore=.csv'% (ticker_symbol, "01", "01", "2004", "00", "00", "0000")
    return base_url + dt_url

    
# Create CSV for each stock in stocks list
for n in range(0,len(companies)):
    
    # Get stock data for the stock
    url = yahoo_finance(tickers[n])
    # Opens the Yahoo Finance csv file
    response1 = br.open(url)
    reader1 = csv.reader(StringIO(response1.read()))
    # Creates a dictionary that maps dates to closing prices for that day
    prices_dict = {row[0]: row[4] for row in reader1}

    for x in range(0,len(queries)):
        
        # Split queries list into a format that can be entered into the url                
        query_split = queries[x][n].split()
        query_params = '%20'.join(query_split)
        
        # Get CSV from Google Trends
        response = br.open('http://www.google.com/trends/trendsReport?hl=en-US&q=' + query_params + '&cmpt=q&content=1&export=1') 
        reader = csv.reader(StringIO(response.read()))
        
        # Creates empty lists to be populated with data
        dates = []
        values = []
        prices = []
        
        # Populate lists with dates and Google Trends values in the correct formate.
        for row in reader:
            # Looks for the right rows to get data from, ignoring the junk
            try:
                date, value = row
            except ValueError:
                continue
            # Takes the date for the Friday of the week and puts it in the correct format
            if re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}', date):
                dates.append(str((datetime.datetime.strptime(date[-10:], "%Y-%m-%d")-datetime.timedelta(days=1)).strftime("%Y-%m-%d"))) # Uses last date in time period
                values.append(value)
        
        # Adds stock prices to the corresponding dates found in the Google Trends data
        for date in dates:
            # Tries to add the price for the date from the Google Trends data
            try:
                prices.append(prices_dict[date])
            # Adds a blank value if the price is not available for the Google Trends date
            except:
                prices.append("")

        # Sets the filename as the query
        filename = queries[x][n]
        filename.replace(" ", "")
        
        # Creates a file and writes values from our three lists
        with open("../data/raw/" + filename + "_gtrends.csv", 'w') as file:
            writer = csv.writer(file, lineterminator = '\n')
            # Writes a header row with the titles: Date, Query, Price
            writer.writerow(['Date', queries[x][n], "Price"])
            # Writes a row for each value of date, value, and price
            for row in zip(dates, values, prices):
                writer.writerow(row)
            # Closes and saves the file
            file.close()