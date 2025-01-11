# MiLB Prospect Statline Projection

## Summary

This streamlit application allows users to select a minor league baseball player from 2024 (who has at least 150 pithches thrown/faced tracked by statcast), and predict their MLB statistics for their debut year, and the 2 years that follow. The app uses a linear regression model to predict MiLB players' major league statistics. The model is trained on data from players promoted to MLB from 2021-2023, using their MiLB data as the features, and their MLB data as the target. Models are seperated for debut year, debut + 1, and debut + 2 years, in order to get a better idea of players' progession as they spend more time in MLB. The app outputs two plots. The first plot contains predictions for the player's batting average (AVG), on-base percentage (OBP), slugging percentage (SLG), and [weighted on-base average (wOBA)](https://www.mlb.com/glossary/advanced-stats/weighted-on-base-average). The second plot contains predictions for the player's strikeout percentage (K%), walk percentage (BB%), and strikeout percentage minus walk percentage (K%-BB%). For pitchers, these statistics refer to the values allowed to batters they face.

## Requirements

- requests
- bs4
- pandas
- numpy
- python-TIME
- streamlit
- matplotlib
- scikit-learn

## Installation and Usage

- Clone and enter the repository:

  '''sh
  git clone <repo_url>
  cd <repo_directory>
  '''

- Install requirements

  '''sh
  pip install -r requirements.txt
  '''

- Run App

'''sh
streamlit run app.py
'''

- In a browser open the local host url shown by streamlit

- Select a position (pitcher or batter) and a player

