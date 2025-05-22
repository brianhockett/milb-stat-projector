import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from model import process_statcast, combine_leagues, train_batter, train_pitcher
from plots import plot_slashline, plot_k_and_bb





st.title("MLB Stat Projector for Current MiLB Players")

col1, col2 = st.columns(2)

positions = ["Pitcher", "Batter"]
batters = pd.read_csv(f'milb_data/milb_batter_2024.csv')
batters['Player'] = batters['Player'].str.replace(r'(, [^ ]+).*', r'\1', regex=True)
batter_names = batters['Player'].unique()
pitchers = pd.read_csv(f'milb_data/milb_pitcher_2024.csv')
pitchers['Player'] = pitchers['Player'].str.replace(r'(, [^ ]+).*', r'\1', regex=True)
pitcher_names = pitchers['Player'].unique()

batter_columns = ['Pitches', 'K%', 'BB%', 'BA', 'xBA', 'OBP', 'xOBP',
       'SLG', 'xSLG', 'wOBA', 'xwOBA', 'BABIP', 'ISO', 'Whiff%', 'EV (MPH)',
       'Adj. EV (MPH)', 'LA (°)', 'Hard Hit%', 'Barrel/BBE%', 'Barrel/PA%']

pitcher_columns = ['Pitches', 'K%', 'BB%', 'BA', 'xBA', 'OBP', 'xOBP',
       'SLG', 'xSLG', 'wOBA', 'xwOBA', 'BABIP', 'ISO', 'Whiff%', 'Pitch (MPH)',
       'Perceived Velocity', 'Extension (ft)', 'PX (ft)', 'PZ (ft)',
       'EV (MPH)', 'Adj. EV (MPH)', 'LA (°)', 'Hard Hit%', 'Barrel/BBE%',
       'Barrel/PA%']

output_batter_columns = ['K%', 'BB%', 'BA', 'OBP', 'SLG', 'wOBA']
output_pitcher_columns = ['K%', 'BB%', 'BA', 'OBP', 'SLG', 'wOBA']

milb_batters, milb_pitchers, mlb_batters, mlb_pitchers = process_statcast()
milb_batters = combine_leagues(milb_batters, mlb_batters, batter_columns)
milb_pitchers = combine_leagues(milb_pitchers, mlb_pitchers, pitcher_columns)

year_plus_0_batter_columns = [col + '_0' for col in output_batter_columns]
year_plus_1_batter_columns = [col + '_1' for col in output_batter_columns]
year_plus_2_batter_columns = [col + '_2' for col in output_batter_columns]
year_plus_0_pitcher_columns = [col + '_0' for col in output_pitcher_columns]
year_plus_1_pitcher_columns = [col + '_1' for col in output_pitcher_columns]
year_plus_2_pitcher_columns = [col + '_2' for col in output_pitcher_columns]

with col1:
    position = st.selectbox(
        "Position:",
        positions
    )

with col2:
    if position == "Pitcher":
        pitcher = st.selectbox(
            "Player:",
            pitcher_names
        )
    if position == "Batter":
        batter = st.selectbox(
            "Player:",
            batter_names
        )


if position == 'Pitcher':
    model_0 = train_pitcher(milb_pitchers, pitcher_columns, year_plus_0_pitcher_columns)
    model_1 = train_pitcher(milb_pitchers, pitcher_columns, year_plus_1_pitcher_columns)
    model_2 = train_pitcher(milb_pitchers, pitcher_columns, year_plus_2_pitcher_columns)
    player = pitchers[pitchers['Player'] == pitcher]
    player = player[pitcher_columns]
    player.insert(0, 'Player', pitcher)


    prediction_0 = model_0.predict(player[pitcher_columns])
    prediction_0 = pd.DataFrame(prediction_0, columns = year_plus_0_pitcher_columns)
    prediction_0.insert(0, 'Player', f'{pitcher} + 0')

    prediction_1 = model_1.predict(player[pitcher_columns])
    prediction_1 = pd.DataFrame(prediction_1, columns = year_plus_1_pitcher_columns)
    prediction_1.insert(0, 'Player', f'{pitcher} + 1')

    prediction_2 = model_2.predict(player[pitcher_columns])
    prediction_2 = pd.DataFrame(prediction_2, columns = year_plus_2_pitcher_columns)
    prediction_2.insert(0, 'Player', f'{pitcher} + 2')

    col1, col2 = st.columns([2,2])
    with col1:
        fig, axs = plt.subplots(figsize = (8,6))
        plot_slashline(player, prediction_0, prediction_1, prediction_2, axs)
        st.pyplot(fig, bbox_inches='tight')
    with col2:
        fig, axs = plt.subplots(figsize = (8,6))
        plot_k_and_bb(player, prediction_0, prediction_1, prediction_2, axs)
        st.pyplot(fig, bbox_inches='tight')

    

if position == 'Batter':
    model_0 = train_batter(milb_batters, batter_columns, year_plus_0_batter_columns)
    model_1 = train_batter(milb_batters, batter_columns, year_plus_1_batter_columns)
    model_2 = train_batter(milb_batters, batter_columns, year_plus_2_batter_columns)
    player = batters[batters['Player'] == batter]
    player = player[batter_columns]
    player.insert(0, 'Player', batter)


    prediction_0 = model_0.predict(player[batter_columns])
    prediction_0 = pd.DataFrame(prediction_0, columns = year_plus_0_batter_columns)
    prediction_0.insert(0, 'Player', f'{batter} + 0')

    prediction_1 = model_1.predict(player[batter_columns])
    prediction_1 = pd.DataFrame(prediction_1, columns = year_plus_1_batter_columns)
    prediction_1.insert(0, 'Player', f'{batter} + 1')

    prediction_2 = model_2.predict(player[batter_columns])
    prediction_2 = pd.DataFrame(prediction_2, columns = year_plus_2_batter_columns)
    prediction_2.insert(0, 'Player', f'{batter} + 2')

    col1, col2 = st.columns([2,2])
    with col1:
        fig, axs = plt.subplots(figsize = (8,6))
        plot_slashline(player, prediction_0, prediction_1, prediction_2, axs)
        st.pyplot(fig, bbox_inches='tight')
    with col2:
        fig, axs = plt.subplots(figsize = (8,6))
        plot_k_and_bb(player, prediction_0, prediction_1, prediction_2, axs)
        st.pyplot(fig, bbox_inches='tight')
