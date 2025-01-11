import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

st.title("MLB Stat Projector for Current MiLB Players")

col1, col2 = st.columns(2)

positions = ["Pitcher", "Batter"]
batters = pd.read_csv(f'milb_data/milb_batter_2024.csv')
batter_names = batters['Player'].unique()
pitchers = pd.read_csv(f'milb_data/milb_pitcher_2024.csv')
pitcher_names = pitchers['Player'].unique()



with col1:
    position = st.selectbox(
        "Position:",
        positions
    )

with col2:
    if position == "Pitcher":
        player = st.selectbox(
            "Player:",
            pitcher_names
        )
    if position == "Batter":
        player = st.selectbox(
            "Player:",
            batter_names
        )


