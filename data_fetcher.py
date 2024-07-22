import requests
import streamlit as st

@st.cache_data
def fetch_new_api_data(api_url="https://draft.premierleague.com/api/bootstrap-static"):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

@st.cache_data
def fetch_data(league_id):
    url = f"https://draft.premierleague.com/api/league/{league_id}/details"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data for League ID {league_id}. Status code: {response.status_code}")
        return None

@st.cache_data
def fetch_choices(league_id):
    url = f"https://draft.premierleague.com/api/draft/{league_id}/choices"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch choices data for League ID {league_id}. Status code: {response.status_code}")
        return None

@st.cache_data
def fetch_transactions(league_id):
    url = f"https://draft.premierleague.com/api/draft/league/{league_id}/transactions"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch transactions data for League ID {league_id}. Status code: {response.status_code}")
        return None

@st.cache_data
def fetch_bootstrap():
    url = "https://draft.premierleague.com/api/bootstrap-static"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch bootstrap data. Status code: {response.status_code}")
        return None
