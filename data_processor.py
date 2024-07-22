import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)

def process_data(data):
    try:
        league_name = data['league']['name']
        league_entries = data['league_entries']
        standings = data['standings']

        league_entries_df = pd.DataFrame(league_entries)
        standings_df = pd.DataFrame(standings)

        if 'week' not in standings_df.columns:
            standings_df['week'] = range(1, len(standings_df) + 1)

        # Process weekly points if available
        if 'weekly_points' in standings_df.columns:
            standings_df = standings_df.explode('weekly_points')
            standings_df['week'] = standings_df.groupby('league_entry').cumcount() + 1

        logging.debug(f"Processed data for league: {league_name}")
        return league_name, league_entries_df, standings_df
    except KeyError as e:
        logging.error(f"KeyError processing data: {e}")
        return None, None, None

def process_choices(data):
    try:
        choices_df = pd.DataFrame(data['choices'])
        logging.debug("Processed choices data")
        return choices_df
    except KeyError as e:
        logging.error(f"KeyError processing choices data: {e}")
        return None

def process_transactions(data):
    try:
        transactions_df = pd.DataFrame(data['transactions'])
        logging.debug("Processed transactions data")
        return transactions_df
    except KeyError as e:
        logging.error(f"KeyError processing transactions data: {e}")
        return None

def process_bootstrap(data):
    try:
        elements_df = pd.DataFrame(data['elements'])
        logging.debug("Processed bootstrap data")
        return elements_df
    except KeyError as e:
        logging.error(f"KeyError processing bootstrap data: {e}")
        return None
