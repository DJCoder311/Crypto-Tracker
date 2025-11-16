import streamlit as st

@st.cache_data(ttl = 600)
def fetch_top_coins():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 100,
        'page': 1,
    }
    import requests
    response = requests.get(url, params = params)
    coins = response.json()

    return [x['id'] for x in coins]
    
if 'coins' not in st.session_state:
    st.session_state.coins = fetch_top_coins()

main_page = st.Page("main_page.py", title = "All Coins", icon ='🪙')
page_2 = st.Page("page_2.py", title = 'Coin Data', icon = '📊')

pg = st.navigation([main_page, page_2])
pg.run()


