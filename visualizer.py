import streamlit as st
import pandas as pd
import altair as alt
import logging

logging.basicConfig(level=logging.DEBUG)

import matplotlib.pyplot as plt
import seaborn as sns

def display_data_table(data, title):
    st.write(title)
    st.dataframe(pd.DataFrame(data))

def bar_chart(data, x, y, title, xlabel, ylabel, rotation=0):
    fig, ax = plt.subplots()
    sns.barplot(data=data, x=x, y=y, ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=rotation)
    st.pyplot(fig)

def pie_chart(data, labels, values, title):
    fig, ax = plt.subplots()
    ax.pie(data[values], labels=data[labels], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title(title)
    st.pyplot(fig)

def visualize_new_api_data(processed_data):
    df_players = pd.DataFrame(processed_data['players'])
    df_top_10_players = pd.DataFrame(processed_data['top_10_players'])
    df_team_distribution = pd.DataFrame(list(processed_data['team_distribution'].items()), columns=['Team', 'Number of Players'])
    df_position_distribution = pd.DataFrame(list(processed_data['position_distribution'].items()), columns=['Position', 'Number of Players'])
    
    display_data_table(df_players, "Player Data from Premier League API")
    
    display_data_table(df_top_10_players, "Top 10 Players by Total Points")
    
    bar_chart(df_top_10_players, 'name', 'total_points', 'Top 10 Players by Total Points', 'Player', 'Total Points', rotation=90)
    
    bar_chart(df_team_distribution, 'Team', 'Number of Players', 'Team-wise Player Distribution', 'Team', 'Number of Players', rotation=90)
    
    pie_chart(df_position_distribution, 'Position', 'Number of Players', 'Distribution of Players by Position')


def display_data(league_entries_df, standings_df):
    try:
        st.write("## Raw League Entries Data")
        st.dataframe(league_entries_df)
        st.write("## Raw Standings Data")
        st.dataframe(standings_df)

        standings_df['league_entry'] = standings_df['league_entry'].astype(str)
        league_entries_df['id'] = league_entries_df['id'].astype(str)

        standings_ids = set(standings_df['league_entry'].unique())
        entries_ids = set(league_entries_df['id'].unique())
        mismatched_ids = standings_ids - entries_ids

        if mismatched_ids:
            st.write(f"Mismatched IDs: {mismatched_ids}")
    except Exception as e:
        logging.error(f"Error displaying data: {e}")
        st.error("Error displaying data")

def create_visualizations(league_entries_df, standings_df, choices_df, transactions_df, elements_df):
    try:
        merged_standings_df = standings_df.merge(league_entries_df[['id', 'entry_name']], left_on='league_entry', right_on='id', how='left')
        
        # Debug print to check merged_standings_df structure
        st.write("## Merged Standings Data")
        st.dataframe(merged_standings_df)

        st.write("## League Standings Over Weeks")
        line_chart = alt.Chart(merged_standings_df).mark_line().encode(
            x=alt.X('week:O', title='Week'),
            y=alt.Y('total:Q', title='Total Points'),
            color='entry_name:N',
            tooltip=['entry_name', 'week', 'total']
        ).interactive().properties(
            width=600,
            height=400,
            title='League Standings Over Weeks'
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        ).configure_title(
            fontSize=20
        )
        st.altair_chart(line_chart, use_container_width=True)

        st.write("## Draft Choices")
        choices_chart = alt.Chart(choices_df).mark_bar().encode(
            x=alt.X('round:O', title='Round'),
            y=alt.Y('pick:Q', title='Pick'),
            color='entry_name:N',
            tooltip=['player_first_name', 'player_last_name', 'entry_name', 'pick']
        ).interactive().properties(
            width=600,
            height=400,
            title='Draft Choices'
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        ).configure_title(
            fontSize=20
        )
        st.altair_chart(choices_chart, use_container_width=True)

        st.write("## Transactions")
        transactions_chart = alt.Chart(transactions_df).mark_bar().encode(
            x=alt.X('added:T', title='Date Added'),
            y=alt.Y('element_in:Q', title='Element In'),
            color='entry:N',
            tooltip=['element_in', 'element_out', 'entry', 'added']
        ).interactive().properties(
            width=600,
            height=400,
            title='Transactions'
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        ).configure_title(
            fontSize=20
        )
        st.altair_chart(transactions_chart, use_container_width=True)

        st.write("## Player Statistics")
        elements_chart = alt.Chart(elements_df).mark_circle().encode(
            x=alt.X('goals_scored:Q', title='Goals Scored'),
            y=alt.Y('assists:Q', title='Assists'),
            size=alt.Size('total_points:Q', title='Total Points'),
            color='web_name:N',
            tooltip=['web_name', 'goals_scored', 'assists', 'total_points']
        ).interactive().properties(
            width=600,
            height=400,
            title='Player Statistics'
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        ).configure_title(
            fontSize=20
        )
        st.altair_chart(elements_chart, use_container_width=True)
    except Exception as e:
        logging.error(f"Error creating visualizations: {e}")
        st.error("Error creating visualizations")
