import streamlit as st
from data_fetcher import fetch_data, fetch_choices, fetch_transactions, fetch_bootstrap, fetch_new_api_data
from data_processor import process_data, process_choices, process_transactions, process_bootstrap, process_new_api_data
from visualizer import display_data, create_visualizations, visualize_new_api_data
import logging

logging.basicConfig(level=logging.DEBUG)

# Load custom CSS to hide Streamlit branding
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("static/styles.css")

st.title("Premier League Fantasy Football Dashboard")
st.write("Welcome to the Premier League Fantasy Football Dashboard!")

# User input for league ID
league_id = st.text_input("Enter your League ID:", value="148968")

# Automatically fetch data from the new API
new_api_data = fetch_new_api_data()

if new_api_data:
    processed_new_api_data = process_new_api_data(new_api_data)
    visualize_new_api_data(processed_new_api_data)
else:
    st.write("Failed to fetch data from the Premier League API.")

if st.button("Fetch Data"):
    data = fetch_data(league_id)
    choices_data = fetch_choices(league_id)
    transactions_data = fetch_transactions(league_id)
    bootstrap_data = fetch_bootstrap()

    if data and choices_data and transactions_data and bootstrap_data:
        league_name, league_entries_df, standings_df = process_data(data)
        choices_df = process_choices(choices_data)
        transactions_df = process_transactions(transactions_data)
        elements_df = process_bootstrap(bootstrap_data)

        st.subheader(f"League: {league_name}")

        display_data(league_entries_df, standings_df)
        create_visualizations(league_entries_df, standings_df, choices_df, transactions_df, elements_df)

        # Display additional tables
        st.write("## Draft Choices Data")
        st.dataframe(choices_df)

        st.write("## Transactions Data")
        st.dataframe(transactions_df)

        st.write("## Player Elements Data")
        st.dataframe(elements_df)
    else:
        st.write("Enter a valid League ID to see the standings.")
