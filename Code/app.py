import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import altair as alt
import datetime
from datetime import timedelta


engine = create_engine("sqlite:///crypto_db.db")


st.set_page_config(page_title = 'CryptoWatch', layout='wide')

option_dict = {'Tron': 'TRX','The Graph': 'GRT', 'Stellar': 'XLM', 'Polygon': 'MATIC', 'Ox': 'ZRX', 'Orchid': 'OXT', 
         'LiteCoin': 'LTC', 'Iota': 'MIOTA', 'Filecoin': 'FIL', 'DogeCoin': 'DOGE', 
         'Cardano': 'ADA', 'Algorand': 'ALGO'}


max_date = (datetime.datetime.today().date() -timedelta(days=1))

st.title("CryptoCurrency and Twitter Data")

row1_1, row1_2 = st.beta_columns((1,1))


with row1_1:
	
	option_selection = st.selectbox('Select a Coin:', ('The Graph', 'Stellar', 'Polygon', 'Ox', 'Orchid', 'LiteCoin', 
		'Iota' , 'Filecoin', 'DogeCoin', 'Cardano', 'Algorand'))

	option = option_dict[option_selection]

with row1_2:
	date_input = st.date_input('Select a Date:', value=(max_date-timedelta(days=1)), min_value=datetime.date(2021,4,20), max_value=max_date, key=None, help=None)

col1_1, col1_2 = st.beta_columns([3, 2])

query_crypto_prices = """select crypto_coin_prices.coin_id, substr(Date_Time, 1,10) as "date", 
round(min(crypto_coin_prices.coin_price),2) as "Price Min", 
round(max(crypto_coin_prices.coin_price),2) as "Price Max", 
round(Closing_Price_Date,2) as "Closing Price"
from crypto_coin_prices
left join 
	(select coin_id, dates, Closing_Price_Date
	from
			(
			select coin_id, substr(Date_Time, 1,10) as "dates", max(Date_Time), coin_price as Closing_Price_Date
			from crypto_coin_prices group by coin_id, substr(Date_Time, 1,10) 
			)
		)
			as closing
on crypto_coin_prices.coin_id = closing.coin_id and substr(crypto_coin_prices.Date_Time, 1,10) = closing.dates
group by crypto_coin_prices.coin_id, substr(Date_Time, 1,10) """

df_crpyto_prices = pd.read_sql(query_crypto_prices, engine)
display_crpyto_prices = df_crpyto_prices.loc[(df_crpyto_prices['coin_id'] == option) & (df_crpyto_prices['date'] == str(date_input))][['Price Min', 'Price Max', 'Closing Price']]
display_crpyto_prices.index = [""] * len(display_crpyto_prices)


query_crypto_prices_timeline = """select coin_id, substr(Date_Time, 1, 10) as Date, substr(Date_Time, 1, 13) as Date_Time, coin_price from crypto_coin_prices"""
crypto_prices_timeline = pd.read_sql(query_crypto_prices_timeline, engine)
crypto_prices_timeline_filter = crypto_prices_timeline[(crypto_prices_timeline['coin_id'] == option) & (crypto_prices_timeline['Date'] == str(date_input))]

maxx = round(max(crypto_prices_timeline_filter['coin_price']),2)
minn = round(min(crypto_prices_timeline_filter['coin_price']),2)
crypto_price_timeline_graph = alt.Chart(crypto_prices_timeline_filter).mark_line(color="red").encode(
    x='Date_Time',
	y= alt.Y('coin_price:Q', axis=alt.Axis(format="$.2f"), scale=alt.Scale(domain=[minn,maxx]))
	).properties(width=720)


with col1_2:
	
	st.table(display_crpyto_prices.style.format("${:.2f}"))
	
	if date_input > datetime.date(2021,4,20):
		previous_close = float(df_crpyto_prices.loc[(df_crpyto_prices['coin_id'] == option) & (df_crpyto_prices['date'] == str(date_input -timedelta(days=1)))]['Closing Price'])
		current_close = float(df_crpyto_prices.loc[(df_crpyto_prices['coin_id'] == option) & (df_crpyto_prices['date'] == str(date_input))]['Closing Price'])
		percent_change = round((((current_close - previous_close) / previous_close) *100),2)

		st.write(f'The Percentage Change from Previous Day\'s Closing Price: **_{percent_change}%_**')

with col1_1:

	st.altair_chart(crypto_price_timeline_graph)

col2_1, col2_2, col2_3 = st.beta_columns([5, 1, 3])


#####First Query 
query2 = f"""select *, substr(date_tweet_created, 1, 13) as 'Date_Time' from crypto_tweet_data 
where coin_id = '{option}' and substr(date_tweet_created,1,10) = '{str(date_input)}'
"""
df_tweet_line = pd.read_sql(query2, engine)
df_tweet_filtered_line = df_tweet_line[df_tweet_line['coin_id'] == option]

#new_df
df_tweet_counts = df_tweet_filtered_line[['coin_id', 'Date_Time']].groupby(['Date_Time']).count()

df_tweet_counts = df_tweet_counts.reset_index()
df_tweet_counts = df_tweet_counts.rename(columns ={'coin_id': 'tweet_count'})
#base = alt.Chart(source).encode(x='date_tweeted:O')

tweet_counts_graph = alt.Chart(df_tweet_counts).mark_line().encode(
    x='Date_Time',
y='tweet_count'
).properties(width=650)

with col2_1:

	st.altair_chart(tweet_counts_graph)

#######Tweet count

query4 = """
select coin_id, substr(date_tweet_created, 1,10) as "date_tweet_created", count(1) as tweet_counts, sum(retweet_count+quote_rt_count) as retweet_counts, sum(reply_count) as reply_counts, sum(like_count) as like_counts
from  crypto_tweet_data
group by coin_id, substr(date_tweet_created, 1,10)"""

tweet_metrics = pd.read_sql(query4, engine)

filters2 = (tweet_metrics['coin_id'] == option ) & (tweet_metrics['date_tweet_created'] == str(date_input))
daily_tweets = tweet_metrics.loc[filters2][['tweet_counts']]
daily_tweets.index = [""] * len(daily_tweets)




daily_tweet_metrics = tweet_metrics.loc[filters2][['retweet_counts', 'reply_counts', 'like_counts']]
daily_tweet_metrics.index = [""] * len(daily_tweet_metrics)



with col2_2:
	st.table(daily_tweets)



with col2_3:
	st.table(daily_tweet_metrics)

	if date_input > datetime.date(2021,4,20):
		current_day_tweets = int(tweet_metrics.loc[filters2]['tweet_counts'])
		previous_day_tweets = int(tweet_metrics.loc[(tweet_metrics['coin_id'] == option ) & (tweet_metrics['date_tweet_created'] == str(date_input -timedelta(days=1)))]['tweet_counts'])
		percent_change_tweets = round((((current_day_tweets - previous_day_tweets) / previous_day_tweets) * 100),2)
		st.write(f'The Percentage Change of Tweet Volume from the Previous Day: **_{percent_change_tweets}%_**')





################
sql_query = """
select crypto_tweet_data.coin_id, substr(crypto_tweet_data.date_tweet_created, 1,10) as 'date_tweeted', 
count(1) as num_of_tweets, round(avg(crypto_coin_prices.coin_price), 2) as coin_price_daily_avg from crypto_tweet_data
    left join crypto_coin_prices
    on  substr(crypto_tweet_data.date_tweet_created, 1,10) = substr(crypto_coin_prices.Date_Time, 1,10)
    and crypto_tweet_data.coin_id = crypto_coin_prices.coin_id
    group by crypto_tweet_data.coin_id, substr(crypto_tweet_data.date_tweet_created, 1,10)
"""


df_tweets = pd.read_sql(sql_query, engine)
testing_df = df_tweets[df_tweets['coin_id'] == option]
min_val = round(min(testing_df['coin_price_daily_avg']),2)
max_val =round(max(testing_df['coin_price_daily_avg']),2)

source = testing_df

base = alt.Chart(source).encode(x='date_tweeted:O')

bar = base.mark_bar().encode(y='num_of_tweets:Q')

line =  base.mark_line(color='red').encode(
    y= alt.Y('coin_price_daily_avg:Q', axis=alt.Axis(format="$.2f"), scale=alt.Scale(domain=[min_val,max_val])))#, scale=alt.Scale(domain=(1, 2))))

yes = alt.layer(bar, line).resolve_scale(
    y = 'independent').properties(width=1200, height=500)

st.altair_chart(yes)
