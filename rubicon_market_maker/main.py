import rubicon_market_maker.marketmaker as mm
import csv

def main():
    pair = "STARK/DAI" #Expressed as a string with a slash seperating the assets
    spread = 0.01 #Expressed as a decimal/percentage
    refresh_rate = 5 #Quantity of seconds before a refresh of market making trades
    market_address = '0x9C735089059689803F507DAAad78c6970468124d'
    base_address = '0x4Ff66BDa878d0A656d4a292cD7FBd0A8E1Dc1C8c' #STARK  
    quote_address = '0x7f21271358765A4b04dB20Ba0BBFE309EC91259a' #DAI
    order_size = 1 #Size of market making orders in base assset
    bot_address = ''
    #Read in keys
    with open('../rubicon-market-maker/secret.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in (reader):
            print(row)
            if row[0] == 'api': 
                web3APILink = row[1].strip()
            if row[0] == 'address': 
                bot_address = row[1].strip()
            if row[0] == 'privateKey': 
                privateKey = row[1].strip()
                break
        csvfile.close()
        
    #Initialize Market Making bot
    trading_bot = mm.MarketMaker(pair, spread, refresh_rate, web3APILink, market_address, base_address, quote_address, order_size, bot_address, privateKey)
    
    #Start the Market Making bot
    trading_bot.start()
