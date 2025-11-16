import streamlit as st

st.title("All Coins")
selected_coin = st.selectbox("Select which coin you want to see data for"
             , st.session_state.coins)

#User selects time interval
if 'days' not in st.session_state:
  st.session_state.days = 1

options = ['Day', 'Week','Month']
selected = st.pills("Interval",options, selection_mode = 'single')
if selected == "Day":
  st.session_state.days = 1
if selected == "Week":
  st.session_state.days = 7
if selected == "Month":
 st.session_state.days = 30

#Get selected coin data
@st.cache_data(ttl = 60)
def get_coin_data(selected_coin, days):
   import requests
   import pandas as pd
   url = f'https://api.coingecko.com/api/v3/coins/{selected_coin}/market_chart'
   params = {
      'vs_currency': 'usd',
      'days': days
   }
   response = requests.get(url, params = params)
   status_code = response.status_code
   data = response.json()

   if status_code == 429:
     return
   else:
      df = pd.DataFrame({
            'timestamp': [x[0] for x in data['prices']],
            'price': [x[1] for x in data['prices']],
            'cap': [x[1] for x in data['market_caps']],
            'volume': [x[1] for x in data['total_volumes']]
      })

      df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
      df.set_index('timestamp', inplace=True)

   return df

#Display the data
coin_data = get_coin_data(selected_coin,st.session_state.days)
try:
  st.header('Price')
  st.line_chart(coin_data['price'], x_label = 'Time', y_label = 'Price $')
  st.header('Market Cap')
  st.caption('Circulating supply x current price')
  st.line_chart(coin_data['cap'], x_label = 'Time', y_label = 'Market Cap $', color = '#ffaa00')
  st.header('Volume')
  st.caption('Total dollar value of all trades within the selected time period')
  st.line_chart(coin_data['volume'], x_label = 'Time', y_label = 'Volume', color = "#16a33c")
except Exception:
  st.warning("API CALLS EXCEEDED: TRY AGAIN IN ONE MINUTE") #Exceeded API Calls

