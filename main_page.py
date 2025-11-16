import streamlit as st

#Setting variables to persist
if 'coinDict' not in st.session_state:
  st.session_state.coinDict = {}
if 'last_data' not in st.session_state:
  st.session_state.last_data = {}

#Gets the coin data
@st.cache_data(ttl = 1000)
def get_data(coins):
  import requests
  api_key = st.secrets['api_key']
  url = 'https://api.coingecko.com/api/v3/simple/price'
  headers = {
      api_key
  }
 
  params = {
      'ids': ','.join(coins),
      'vs_currencies': 'usd',
      'include_market_cap': 'true',
      'include_24hr_change': 'true',
      "include_24hr_vol": 'true'

  }

  response = requests.get(url, params = params)
  status_code = response.status_code
  data = response.json()
  return data, status_code  

#Stores coin data properly
def create_coin_table(data):
 for coin in st.session_state.coins:
    if coin in data:
      price = data[coin]['usd']
      cap = data[coin]['usd_market_cap']
      dailyChange = data[coin]['usd_24h_change']
      dailyVol = data[coin]['usd_24h_vol']

      st.session_state.coinDict[coin] = [price,cap,dailyChange,dailyVol]
    else:
      pass

#If API calls exceeded it will return the last data
def determine_data_source(status_code): 
  if status_code == 200:
     st.session_state.last_data = st.session_state.coinDict
  try:
    data_source = st.session_state.last_data  if status_code == 429 else st.session_state.coinDict
  except Exception:
    st.warning("COINS NOT FOUND")
    data_source = {}
  return data_source


def display_coin_table(data_source):
  import pandas as pd
  df = pd.DataFrame.from_dict(data_source,orient = 'index', columns = ['Current Price',"Market Cap",'24 Hour Change','24 Hour Volume'])
  
  #Display
  st.dataframe(df.style.format({"Current Price": "{:,.2f}", "Market Cap": "${:,.2f}", "24 Hour Change": "{:.2f}","24 Hour Volume": "${:,.2f}"}).set_table_styles([
      {'selector': 'th',
      'props': [('font-weight', 'bold'),
                ('text-align', 'center')]}
  ]),
  height = 800
  )



st.title('Crypto Tracker')
st.caption("Top 100 coins")
data,status_code = get_data(st.session_state.coins) #Get the data
create_coin_table(data) #Create the table with the data
data_source = determine_data_source(status_code) #Ensure correct data source
display_coin_table(data_source)#Display the data

