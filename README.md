## Rubicon Market Maker

A simple market making bot to provide liquidity and farm RBCN on the Rubicon exchange.

Presently, the bot utilizes a pure market making strategy in which the bot adds both "buy" and "sell" orders at a fixed spread around the asset's price. Important inputs for the bot will include:

- Pair: The desired ERC-20/ERC-20 token pair on Rubicon that the bot should market make for.
- Spread: desired spread between bids and asks around the asset's price as a %.
- Refresh Rate: speed at which the bot places updated orders around the midpoint of the order book in seconds.

Here is an overview of the logic flow for the current bot implementation:

1. The Bot is initialized and a target Pair, Spread, and Refresh Rate are selected by the user.
2. The Bot connects to a Web3 provider in order to link the bot to the blockchain.
3. The Bot connects to a user's wallet in order to provide capital.
4. The Bot places its first pair of Limit Buy and Limit Sell orders at the desired Spread around the midpoint of the Pair's existing orderbook.
5. The Bot continuously updates its Limit Buy and Limit Sell orders at Refresh Rate to target a fixed Spread around the Pair's existing orderbook midpoint.
6. The Bot listens for successful trades, either Limit Buys or Limit Sells, and readjusts the pair of Market Making orders accordingly.
7. Track accrued RBCN, P&L, and key statistics for the User throughout operation.

Ideas for future improvements:
[] - Implement logic that accounts for gas fees and network costs when executing a market-making strategy
[] - Package the bot into an app with an easy-to-understand UI in order to track P&L, risk, and Token rewards.
