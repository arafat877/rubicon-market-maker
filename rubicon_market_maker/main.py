import rubicon_market_maker.marketmaker as mm
import csv

def main():
    pair = "WAYNE/DAI" #Expressed as a string with a slash seperating the assets
    spread = 0.01 #Expressed as a decimal/percentage
    refresh_rate = 5 #Quantity of seconds before a refresh of market making trades
    market_address = '0x9C735089059689803F507DAAad78c6970468124d'
    base_address = '0x4Ff66BDa878d0A656d4a292cD7FBd0A8E1Dc1C8c'
    quote_address = '0x7f21271358765A4b04dB20Ba0BBFE309EC91259a'
    #Read in keys
    with open('../rubicon-market-maker/secret.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            web3APILink = row[0]
        csvfile.close()
        
    #Initialize Market Making bot
    trading_bot = mm.MarketMaker(pair, spread, refresh_rate, web3APILink, market_address, base_address, quote_address)
    
    #Start the Market Making bot
    trading_bot.start()
