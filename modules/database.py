import pandas as pd
import os

DATA_FILE = "data/observations.csv"

COLUMNS = [
    "Date",
    "1 - Place",
    "2 - Process",
    "3 - Players",
    "4 - Principle : W.I., Visual Aid, Measure Tech.",
    "5 - Procedure Used",
    "6 - Pain Point",
    "7 - Comment"
]

def initialize_database():

    os.makedirs("data", exist_ok=True)

    if not os.path.exists(DATA_FILE):

        empty_df = pd.DataFrame(columns=COLUMNS)

        empty_df.to_csv(DATA_FILE, index=False)

def load_data():

    initialize_database()

    return pd.read_csv(DATA_FILE)

def save_data(df):

    df.to_csv(DATA_FILE, index=False)

def clear_data():

    empty_df = pd.DataFrame(columns=COLUMNS)

    empty_df.to_csv(DATA_FILE, index=False)