# GET RICH OR TWEET TRYIN’
Brandon McNeil  
Metis Project 3 - Data Engineering
## Context
The cryptocurrency market has exploded over the last few years. Now that crypto coins like Bitcoin & Ethereum have entered the zeitgeist and have reached record high prices, average people are looking to get in on the cryptocurrency action!

Alternative coins - or any coin that is not one of the few mainstream names - are cheaper alternatives that average people can invest in without breaking the bank. Similar to penny stocks, you can purchase a lot of them with a small investment with the chance of turning large profit! Since risk is always a factor, any insight on a coin's demand would be a huge benefit to investors. This is why we are looking to Twitter to find if coin’s prices increase as its popularity increases via tweets.

The goal of this project is to create an end-to-end data pipeline that collects daily Twitter data, and hourly/daily prices crypto coins. 

 
## DATA
Since this is a proof of concept project, I started with 13 cryptocoins to investigate.  

Using Twitter’s API, I collected tweets that contained those coin’s ticker in a hashtag (ex. #LTC - the hashtag for LiteCoin). Our dataset begins on 4/20/2021.  

In addition to collecting Twitter Data, I also used Coinbase.com’s API to gather daily/hourly price data for each coin.  

At the end of the 2 week period, I had collected over 200,000 points of data.
 
## Tools
sqlalchemy 
Streamlit to present findings via a Web-application  
Altair for visualizations  
Pandas  
DateTime  
Ratelimit to monitor API requests  
Requests to pull JSON information  
SQLite Database
