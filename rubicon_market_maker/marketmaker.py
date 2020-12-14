from web3 import Web3
import json
import time
import threading

# Goal is to have MarketMaker represent the core object and logic of the package
#MarketMaker should have a "run" function in order to start the bot live on-chain based on a few inputs

class MarketMaker:
    # Constructor which takes a pair, spread, and refresh_rate
    def __init__(self, pair, spread, refresh_rate, web3APILink, market_address, base, quote, order_size,bot_address, privateKey):
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
        self.order_size = order_size
        self.bot_address = bot_address
        self.pk = privateKey


        #Connect to Web3 provider
        self.web3 = Web3(Web3.HTTPProvider(web3APILink))
        if (self.web3.isConnected()):
            print("Connected to Web3 provider via:", web3APILink)
        else:
            print("ERROR - Unable to connect to Web3 provider")
        
        #Initialize contract
        self.RubiconMarket = self.load_contract("RubiconMarket", self.marketAddress)
        self.baseContract = self.load_contract("DaiWithFaucet", self.baseAsset)
        self.quoteContract = self.load_contract("EquityToken", self.baseAsset)

    
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

    def getOrderbookMidpoint(self):
        best_offer_id_sell = self.RubiconMarket.functions.getBestOffer(self.baseAsset, self.quoteAsset).call()
        best_sell_offer = self.RubiconMarket.functions.getOffer(best_offer_id_sell).call()
        # print('sell', best_sell_offer)
   
        best_offer_id_buy = self.RubiconMarket.functions.getBestOffer(self.quoteAsset, self.baseAsset).call()
        best_buy_offer = self.RubiconMarket.functions.getOffer(best_offer_id_buy).call()
        # print('buy offer', best_buy_offer)

        #Handle logic if no offer is in the order book
        if best_sell_offer[0] != 0 and best_sell_offer[2] != 0:
            best_sell_offer_price = best_sell_offer[2]/best_sell_offer[0]
            # print('best offer', best_offer)
            # print('best sell offer price', best_sell_offer_price)
        else:
            print('there is no sell order in the order book!')

        if best_buy_offer[0] != 0 and best_buy_offer[2] != 0:
            best_buy_offer_price = best_buy_offer[0]/best_buy_offer[2]
                # print('best offer', best_offer)
            print('best buy offer price', best_buy_offer_price)
        else:
            print('there is no buy order in the order book!')

            #Float that represents the midpoint of the orderbook
        midpointPrice = (best_sell_offer_price + best_buy_offer_price) / 2
        
        return midpointPrice

    def runLogic(self):
        #https://web3py.readthedocs.io/en/stable/filters.html
        # event_filter = self.RubiconMarket.events.LogTrade.createFilter(fromBlock="latest", argument_filters={
        #     'arg1': '',
        #     'arg2':self.baseAsset, 
        #     'arg4': self.quoteAsset
        #     })

        #Logic control for to not replace unfilled orders
        originalOrdersPlaced = False

        while self.live:
            print('runLogic Trigger')
            #Core logic center of the bot
            #1. Identify the midpoint of the order book
            midpointPrice = self.getOrderbookMidpoint()
            print(midpointPrice)

            #2. Place (re-place) order at fixed spread around the orderbook
            # Should these be rounded?
            targetBid = round(midpointPrice * (1 - self.spread), 4)
            targetAsk = round(midpointPrice * (1 + self.spread), 4)
            print('targetBid', targetBid)
            print('targetAsk', targetAsk)

            #Check the balance of the bot to verify has the assets
            if (self.baseContract.functions.balanceOf(self.bot_address).call() < self.order_size or self.quoteContract.functions.balanceOf(self.bot_address).call() < (self.order_size*targetBid)):
                print('Insufficient funds in bot to market make')

            #offer a bid at targetBid for self.order_size
            targetBidABI = self.RubiconMarket.encodeABI(fn_name = 'offer', args = 
                [
                self.web3.toWei(self.order_size * targetBid, 'ether'), 
                self.quoteAsset,
                self.web3.toWei(self.order_size, 'ether'), 
                self.baseAsset
                ])
            
            try:
                targetBid_tx = self.send_transaction(
                    targetBidABI, 
                    self.bot_address, 
                    'targetBid at '+ str(targetBid),
                    self.marketAddress,
                    0,
                    True,
                    self.pk
                    )
                print(targetBid_tx)  
            except:
                print('****An error occured placing the targetBid transaction****')
            time.sleep(5)
            #Approve bid
            targetAskApprovalABI = self.baseContract.encodeABI(fn_name = 'approve', args = [self.marketAddress, self.web3.toWei(self.order_size * targetAsk, 'ether')])
            targetAskApproval_tx = self.send_transaction(targetAskApprovalABI, self.bot_address, 'approval for targetAsk for baseContract' + str(self.order_size * targetAsk), self.baseAsset,0,False, self.pk)
            print('Transaction hash of: ',targetAskApproval_tx)
            
            #TODO: Need to make the function wait until approval is hashed on chain then proceed
            #TODO: Easy solution could be a waitFor(txHash) function that proceeds only when tx is hashed.
            time.sleep(7)

            #offer an ask at targetAsk for self.order_size
            targetAskABI = self.RubiconMarket.encodeABI(fn_name = 'offer', args = 
                [
                self.web3.toWei(self.order_size, 'ether'), 
                self.baseAsset,
                self.web3.toWei(self.order_size * targetAsk, 'ether'), 
                self.quoteAsset
                ])
            
            try:
                targetAsk_tx = self.send_transaction(
                    targetAskABI, 
                    self.bot_address, 
                    'targetAsk at '+ str(targetAsk),
                    self.marketAddress,
                    0,
                    True,
                    self.pk
                    )
                print(targetAsk_tx)  
            except:
                print('****An error occured placing the targetAsk transaction****')

            time.sleep(5)

            originalOrdersPlaced = True

            #Logic catch to keep bot loop running    
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

    #helper function to send transactions
    def send_transaction(self, encodedABI, sender, desc, to, value, sendIT, PK):
        txCount = self.web3.eth.getTransactionCount(sender)
        txData = {
            'nonce': txCount,
            'to': to,
            'from': sender,
            'data': encodedABI,
            'value': self.web3.toWei(value, 'ether'),
        #TODO: Need to implement an optimal gas calculator for any transaction
            'gas': 6721975,
            'gasPrice': self.web3.toWei('20', 'gwei')
        }

            # GAS CHECK
        try:
            print('Estimated Gas for' + desc, self.web3.eth.estimateGas(txData))
        except Exception as e:
            raise e
        if sendIT == False: return True
        if sendIT == True:
            signed_tx = self.web3.eth.account.signTransaction(txData, PK)
            tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            print('Sent TX of ' + desc, self.web3.toHex(tx_hash))
            print(tx_hash)
            return True


        # def set_interval(self,func, sec):
        #     def func_wrapper():
        #         self.set_interval(func, sec)
        #         func()
        #     t = threading.Timer(sec, func_wrapper)
        #     t.start()
        #     return t
