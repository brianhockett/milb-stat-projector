from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import os
import time

def process_statcast():
    # Reading in the MiLB Data
    milb_batters_2021 = pd.read_csv("milb_data/milb_batter_2021.csv")
    milb_batters_2022 = pd.read_csv("milb_data/milb_batter_2022.csv")
    milb_batters_2023 = pd.read_csv("milb_data/milb_batter_2023.csv")
    milb_pitchers_2021 = pd.read_csv("milb_data/milb_pitcher_2021.csv")
    milb_pitchers_2022 = pd.read_csv("milb_data/milb_pitcher_2022.csv")
    milb_pitchers_2023 = pd.read_csv("milb_data/milb_pitcher_2023.csv")

    # Grouping together batter and pitcher data for MiLB
    milb_batters = pd.concat([milb_batters_2021, milb_batters_2022, milb_batters_2023], ignore_index = True)
    milb_pitchers = pd.concat([milb_pitchers_2021, milb_pitchers_2022, milb_pitchers_2023], ignore_index = True)

    # Reading in the MLB Data
    mlb_batters_2021 = pd.read_csv("mlb_data/mlb_batter_2021.csv")
    mlb_batters_2022 = pd.read_csv("mlb_data/mlb_batter_2022.csv")
    mlb_batters_2023 = pd.read_csv("mlb_data/mlb_batter_2023.csv")
    mlb_batters_2024 = pd.read_csv("mlb_data/mlb_batter_2024.csv")
    mlb_pitchers_2021 = pd.read_csv("mlb_data/mlb_pitcher_2021.csv")
    mlb_pitchers_2022 = pd.read_csv("mlb_data/mlb_pitcher_2022.csv")
    mlb_pitchers_2023 = pd.read_csv("mlb_data/mlb_pitcher_2023.csv")
    mlb_pitchers_2024 = pd.read_csv("mlb_data/mlb_pitcher_2024.csv")

    # Grouping together batter and pitcher data for MLB
    mlb_batters = pd.concat([mlb_batters_2021, mlb_batters_2022, mlb_batters_2023, mlb_batters_2024], ignore_index = True)
    mlb_pitchers = pd.concat([mlb_pitchers_2021, mlb_pitchers_2022, mlb_pitchers_2023, mlb_pitchers_2024], ignore_index = True)

    # Dropping useless/disruptive columns
    milb_pitchers = milb_pitchers.drop(columns = ['Total', 'Pitch %', 'Hits', '1B', '2B', '3B', 'HR', 'SO', 'BB', 'Whiffs', 'Swings', 'Barrels', 'Dist (ft)', 'Spin (RPM)'])
    mlb_pitchers = mlb_pitchers.drop(columns = ['Total', 'Pitch %', 'Hits', '1B', '2B', '3B', 'HR', 'SO', 'BB', 'Whiffs', 'Swings', 'Barrels', 'Dist (ft)', 'Spin (RPM)'])
    milb_batters = milb_batters.drop(columns = ['Total', 'Pitch %', 'Hits', '1B', '2B', '3B', 'HR', 'SO', 'BB', 'Whiffs', 'Swings', 'Barrels', 'Dist (ft)'])
    mlb_batters = mlb_batters.drop(columns = ['Total', 'Pitch %', 'Hits', '1B', '2B', '3B', 'HR', 'SO', 'BB', 'Whiffs', 'Swings', 'Barrels', 'Dist (ft)'])

    # Getting rid of prospect rankings to ensure matching between MiLB and MLB names
    milb_batters['Player'] = milb_batters['Player'].str.replace(r' \w+ #\d+', '', regex = True)
    milb_pitchers['Player'] = milb_pitchers['Player'].str.replace(r' \w+ #\d+', '', regex = True)
    mlb_batters['Player'] = mlb_batters['Player'].str.replace(r' \w+ #\d+', '', regex = True)
    mlb_pitchers['Player'] = mlb_pitchers['Player'].str.replace(r' \w+ #\d+', '', regex = True)

    # Sorting data by name and year for the purpose of dropping dupllicate MiLB players, keeping only their last year prior to promotion
    milb_pitchers = milb_pitchers.sort_values(by = ['Player', 'Year'])
    milb_pitchers = milb_pitchers.drop_duplicates(subset = 'Player', keep = 'last')

    mlb_pitchers = mlb_pitchers.sort_values(by = ['Player', 'Year'])

    milb_batters = milb_batters.sort_values(by = ['Player', 'Year'])
    milb_batters = milb_batters.drop_duplicates(subset = 'Player', keep = 'last')

    mlb_batters = mlb_batters.sort_values(by = ['Player', 'Year'])

    # Filtering both MiLB and MLB data down to only players who are present in both (been promoted from minor leagues since 2021)
    common_pitchers = set(milb_pitchers['Player']).intersection(mlb_pitchers['Player'])
    milb_pitchers = milb_pitchers[milb_pitchers['Player'].isin(common_pitchers)]
    mlb_pitchers = mlb_pitchers[mlb_pitchers['Player'].isin(common_pitchers)]

    common_batters = set(milb_batters['Player']).intersection(mlb_batters['Player'])
    milb_batters = milb_batters[milb_batters['Player'].isin(common_batters)]
    mlb_batters = mlb_batters[mlb_batters['Player'].isin(common_batters)]

    return milb_batters, milb_pitchers, mlb_batters, mlb_pitchers


# Function to take MLB data and put it in the MiLB dataframe, with years since last minor league appearance appended to each major league stat
def combine_leagues(milb, mlb, stats_columns):
    for year_offset in range(3):
        for stat in stats_columns:
            milb[f'{stat}_{year_offset}'] = pd.NA
    
    for idx, milb_row in milb.iterrows():
        player = milb_row['Player']
        milb_year = milb_row['Year']
        
        player_mlb_data = mlb[mlb['Player'] == player]
        
        
        for year_offset in range(3):
            target_year = milb_year + year_offset
            matching_mlb = player_mlb_data[player_mlb_data['Year'] == target_year]
            
            if not matching_mlb.empty:
                for stat in stats_columns:
                    milb.at[idx, f'{stat}_{year_offset}'] = matching_mlb[stat].values[0]
    
    return milb

# Models for batter and pitcher
def train_batter(milb_batters, batter_columns, year_plus_num_columns):
    milb_batters = milb_batters.dropna(subset=batter_columns + year_plus_num_columns)
    X = milb_batters[batter_columns]
    y = milb_batters[year_plus_num_columns]
    
    # Split the data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create the model and train it on the training set
    model = LinearRegression()
    model.fit(X_train, y_train)

    return model

def train_pitcher(milb_pitchers, pitcher_columns, year_plus_num_columns):
    milb_pitchers = milb_pitchers.dropna(subset=pitcher_columns + year_plus_num_columns)
    X = milb_pitchers[pitcher_columns]
    y = milb_pitchers[year_plus_num_columns]
    
    # Split the data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create the model and train it on the training set
    model = LinearRegression()
    model.fit(X_train, y_train)

    return model

# Example Usage
'''
year_plus_0_pitcher_columns = [col + '_0' for col in pitcher_columns]
model = train_pitcher(milb_pitchers, pitcher_columns, year_plus_0_pitcher_columns)
pitchers = pd.read_csv(f'milb_data/milb_pitcher_2024.csv')
pitcher = pitchers[:1]
pitcher_name = pitcher['Player'].iloc[0]
prediction = model.predict(pitcher[pitcher_columns])
prediction = pd.DataFrame(prediction, columns = year_plus_0_pitcher_columns)
prediction.insert(0, 'Player', pitcher_name)

pitcher[['Player'] + pitcher_columns].head()

prediction.head()
'''
