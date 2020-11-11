## Rubicon Market Maker

A simple market making bot to provide liquidity and farm RBCN on the Rubicon exchange.

Presently, the bot utilizes a pure market making strategy in which the bot adds both "buy" and "sell" orders at a fixed spread around the asset's price. Important inputs for the bot will include:

- Pair: The desired ERC-20/ERC-20 token pair on Rubicon that the bot should market make for.
- Spread: desired spread between bids and asks around the asset's price as a %.
- Refresh Time: speed at which the bot places updated orders around the midpoint of the order book in seconds.

