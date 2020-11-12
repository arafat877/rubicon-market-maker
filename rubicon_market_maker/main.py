import rubicon_market_maker.marketmaker as mm
import csv

def main():
    pair = "WAYNE/DAI" #Expressed as a string with a slash seperating the assets
    spread = 0.01 #Expressed as a decimal/percentage
    refresh_rate = 10 #Quantity of seconds before a refresh of market making trades

    #Read in keys
    with open('../rubicon-market-maker/secret.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            web3APILink = row[0]
        csvfile.close()
        
    #Initialize Market Making bot
    trading_bot = mm.MarketMaker(pair, spread, refresh_rate, web3APILink)
