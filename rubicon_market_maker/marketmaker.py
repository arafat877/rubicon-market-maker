from web3 import Web3
import json
import time

# Goal is to have MarketMaker represent the core object and logic of the package
#MarketMaker should have a "run" function in order to start the bot live on-chain based on a few inputs

class MarketMaker:
    # Constructor which takes a pair, spread, and refresh_rate
    def __init__(self, pair, spread, refresh_rate, web3APILink):
        #Map inputs to Class Variables
        self.pair = pair.split('/')
        self.baseAsset = self.pair[0]
        self.quoteAsset = self.pair[1]
        self.spread = spread
        self.refresh_rate = refresh_rate

        #Connect to Web3 provider
        web3 = Web3(Web3.HTTPProvider(web3APILink))
        print('***Bot Initialization Complete***\n')
