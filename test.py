import requests
import pandas as pd
import plotly.express as px
import numpy as np

# Coin Gecko simple markert url
url = 'https://api.coingecko.com/api/v3/coins/markets'
params = {
    'vs_currency':'usd',
    'order':'market_cap_desc',
    'per_page':10,
    'page':1,
    'sparkline':'false'
}



print("Fetching data from CoinGecko....")
r = requests.get(url,params=params)

if r.status_code == 200:
    print(f"Success: Status Code is {r.status_code}")
    data = r.json()
    
    df_raw = pd.DataFrame(data)

    column_keeping_mask = ['id','current_price','price_change_percentage_24h','total_supply']
     
     # Creating the dataframe by filtering out other columns that we dont want and creating a copy so it doesnt affect the original data
    df = df_raw[column_keeping_mask].copy()

    # Rename columns

    df = df.rename(
        columns={
            'id':'name',
            'current_price': 'current_price',
            'price_change_percentage_24h': '24h_price_change_pct',
            'total_supply': 'total_volume'
        }
    )
    
    df['log_volume'] = np.log10(df['total_volume'])

 
    


    
else:
    print(f"Unable to establish connection. Status Code {r.status_code}")


fig = px.bar(
    x=df['name'],
    y=df['24h_price_change_pct'],
    title='Top 10 Crypto Coins: Price Change in the last 24 hrs',
    labels={'x':'Coin','y':'Price Change (%)'},
    color=df['24h_price_change_pct'],
    color_continuous_scale=px.colors.sequential.RdBu
)

fig.write_html("crypto_dashboard.html")