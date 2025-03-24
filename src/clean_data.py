#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  1 15:04:04 2025

Author: Julia Muller

Clean MLB game log data
Drop irrelevant columns and reformat columns of interest
"""

import pandas as pd
from pathlib import Path

# Import data
filepath = Path(__file__).parent.parent
games = pd.read_csv(filepath / 'data/processed/game_logs_2021-2024.csv')

# Format date column as datetime and pull year into new column
games['date'] = pd.to_datetime(games['date'], format = '%Y%m%d')
games['year'] = games['date'].dt.year

# Get column of year/month for monthly performance trends
games['year_month'] = games['date'].dt.strftime('%Y-%m')
games['month'] = games['date'].dt.strftime('%m')

# Create new column of home/visitor wins
games['home_win'] = (games['home_score'] > games['visitor_score']).astype(int)
games['visitor_win'] = (games['home_score'] < games['visitor_score']).astype(int)

# Get rid of irrelevant columns
games = games.drop(columns = [
    'additional_info', 'acquisition_info', 'forfeit', 'protest', 
    'lf_ump_id', 'lf_ump_name', 'rf_ump_id', 'rf_ump_name'] + \
    [col for col in games.columns if col.endswith('_id')
])

# Recode team identifiers to current conventions
team_ids = {
    'ANA': 'LAA', # Angels
    'CHA': 'CHC', # Cubs
    'CHN': 'CHW', # White Sox
    'KCA': 'KAN', # Royals
    'LAN': 'LAD', # Dodgers
    'NYA': 'NYY', # Yankees
    'NYN': 'NYM', # Mets
    'SDN': 'SD', # Padres
    'SFN': 'SF', # Giants
    'SLN': 'STL', # Cardinals
    'TBA': 'TB' # Rays
    }

# Map updated team IDs to data set
games['home_team'] = games['home_team'].map(lambda x: team_ids.get(x, x))
games['visitor_team'] = games['visitor_team'].map(lambda x: team_ids.get(x, x))

# Export CSV
games.to_csv(filepath / 'data/processed/game_logs_2021-2024_cleaned.csv', index = False)