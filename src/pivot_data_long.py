#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  1 15:09:39 2025

Author: Julia Muller

Pivot data longer to get 1 row per team in each game
"""

import pandas as pd
from pathlib import Path

# Import data
filepath = Path(__file__).parent.parent
games = pd.read_csv(filepath / 'data/processed/game_logs_2021-2024_cleaned.csv')

# Home teams data frame
home_teams = games.loc[:, ~games.columns.str.startswith('visitor_')].copy()
home_teams.columns = home_teams.columns.str.replace('home_', '', regex = False)
home_teams['at_home'] = 1

# Visitor teams data frame
visitor_teams = games.loc[:, ~games.columns.str.startswith('home_')].copy()
visitor_teams.columns = visitor_teams.columns.str.replace('visitor_', '', regex = False)
visitor_teams['at_home'] = 0

# Temporary data frame of home teams' opponents
home_opponents = visitor_teams[['game_code', 'team', 'score']]
home_opponents = home_opponents.rename(columns = {'team': 'opponent', 'score': 'opponent_score'})

# Temporary data frame of visitor teams' opponents
visitor_opponents = home_teams[['game_code', 'team', 'score']]
visitor_opponents = visitor_opponents.rename(columns = {'team': 'opponent', 'score': 'opponent_score'})

# Join home teams with opponent data
home_teams_with_opponent = home_teams.merge(home_opponents, how = 'left', on = 'game_code')

# Join visitor teams with opponent data
visitor_teams_with_opponent = visitor_teams.merge(visitor_opponents, how = 'left', on = 'game_code')

# Combine home and visitor team data frames
teams = pd.concat([home_teams_with_opponent, visitor_teams_with_opponent], ignore_index = True)

# Export CSV
teams.to_csv(filepath / 'data/processed/team_games_2021-2024.csv', index = False)