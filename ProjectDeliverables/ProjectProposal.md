## Do Cryptocurrency Prices Relate to Twitter Popularity?

Cryptocurrency is an incredibly volatile investment market. This project will look to explore that volatile mystery by comparing a coin’s popularity on twitter to the coin’s estimated value.

For this project, we will be using a flat file of historical cryptocurrency prices as our starting off point (https://www.kaggle.com/sudalairajkumar/cryptocurrencypricehistory?select=coin_Cosmos.csv).
From there, we will be utilizing Twitter’s API (twitter has formally approved this project’s use of their API) to pull hashtag information about the selected coins in the base file. This information will be stored in a MongoDB for storage, and then modified to be joinable to the base file dataset.

After some exploratory analysis, we will aim to have an interactive web page that visualizes our findings for others to use and explore further! 

An MVP for this project will consist of a timeline comparison chart of a coin’s price and an aggregated total of hashtagged tweets about the coin.
