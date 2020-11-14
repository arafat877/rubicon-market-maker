from web3 import Web3
import json
import time
import threading

# Goal is to have MarketMaker represent the core object and logic of the package
#MarketMaker should have a "run" function in order to start the bot live on-chain based on a few inputs

class MarketMaker:
    # Constructor which takes a pair, spread, and refresh_rate
    def __init__(self, pair, spread, refresh_rate, web3APILink, market_address, base, quote):
        #Map inputs to Class Variables
        self.pair = pair.split('/')
        self.baseAsset = self.pair[0]
        self.quoteAsset = self.pair[1]
        self.spread = spread
        self.refresh_rate = refresh_rate
        self.liveThreads = []
        self.marketAddress = market_address
        self.baseAsset = base
        self.quoteAsset = quote
        self.live = False


        #Connect to Web3 provider
        self.web3 = Web3(Web3.HTTPProvider(web3APILink))
        if (self.web3.isConnected()):
            print("Connected to Web3 provider via:", web3APILink)
        else:
            print("ERROR - Unable to connect to Web3 provider")
        
        #Initialize contract
        self.RubiconMarket = self.load_contract("RubiconMarket", self.marketAddress)

    
    def calculate(self):
        print('test')
        print(self.liveThreads)

    def start(self):
        #Interval and threading logic for potential later implementation
        # t = self.set_interval(self.test, 2)
        # self.liveThreads.append(t)
        self.live = True
        self.runLogic()
    
    def stop(self):
        self.live = False

    def runLogic(self):
        while self.live:
            print('runLogic Trigger')
            #Core logic center of the bot
            #1. Identify the midpoint of the order book
            best_offer_id = self.RubiconMarket.functions.getBestOffer(self.baseAsset, self.quoteAsset).call()
            best_offer = self.RubiconMarket.functions.getOffer(best_offer_id).call()
            if (best_offer[1] == self.quoteAsset):
                best_offer_price = best_offer[0]/best_offer[2]
            else:
                best_offer_price = best_offer[2]/best_offer[0]
            # print('best offer', best_offer)
            # print('best offer price', best_offer_price)
            

            midpointPrice = ''
            #2. Place (re-place) order at fixed spread around the orderbook


            if (self.live == False):
                return
            time.sleep(self.refresh_rate)

    #Initialize Contract function
    def load_contract(self, name, address):
        if name == "WAYNE" or name == "STARK": name = "EquityToken"
        with open("rubicon_market_maker/contractABI/" + name+ ".json") as a: 
            a_info_json = json.load(a)
            a.close()
        abi = a_info_json["abi"]
        contract = self.web3.eth.contract(address=address,
            abi = abi)
        return contract

    # def set_interval(self,func, sec):
    #     def func_wrapper():
    #         self.set_interval(func, sec)
    #         func()
    #     t = threading.Timer(sec, func_wrapper)
    #     t.start()
    #     return t
