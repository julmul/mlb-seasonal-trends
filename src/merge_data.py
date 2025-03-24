#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  1 14:58:04 2025

Author: Julia Muller

Merge MLB game log data for 2021-2024
"""

import pandas as pd
from pathlib import Path

# Import raw data
filepath = Path(__file__).parent.parent
gl_2021 = pd.read_csv(filepath / 'data/raw/gl2021.txt', header = None)
gl_2022 = pd.read_csv(filepath / 'data/raw/gl2022.txt', header = None)
gl_2023 = pd.read_csv(filepath / 'data/raw/gl2023.txt', header = None)
gl_2024 = pd.read_csv(filepath / 'data/raw/gl2024.txt', header = None)

# Merge all game log data sets
games = pd.concat([gl_2021, gl_2022, gl_2023, gl_2024], ignore_index = True)

# Define columns based on Retrosheet documentation
retrosheet_cols = [
    # Game information
    'date', 'series_game_number', 'week_day', 'visitor_team', 'visitor_league',
    'visitor_game_number', 'home_team', 'home_league', 'home_game_number',
    'visitor_score', 'home_score', 'total_game_outs', 'day_or_night', 
    'game_completion', 'forfeit', 'protest', 'park_code', 'attendance', 
    'total_game_mins', 'visitor_line_score', 'home_line_score', 

    # Visiting team offensive statistics
    'visitor_ab', 'visitor_hits', 'visitor_2b', 'visitor_3b', 'visitor_hr', 
    'visitor_rbi', 'visitor_sh', 'visitor_sf', 'visitor_hbp', 'visitor_walks', 
    'visitor_ibb', 'visitor_so', 'visitor_sb', 'visitor_cs', 'visitor_gidp', 
    'visitor_ci', 'visitor_lob',

    # Visiting team pitching statistics
    'visitor_p', 'visitor_er', 'visitor_ter', 'visitor_wp', 'visitor_bk',

    # Visiting team defensive statistics
    'visitor_po', 'visitor_a', 'visitor_e', 'visitor_pb', 'visitor_dp', 'visitor_tp',

    # Home team offensive statistics
    'home_ab', 'home_hits', 'home_2b', 'home_3b', 'home_hr', 'home_rbi', 
    'home_sh', 'home_sf', 'home_hbp', 'home_walks', 'home_ibb', 'home_so', 
    'home_sb', 'home_cs', 'home_gidp', 'home_ci', 'home_lob',

    # Home team pitching statistics
    'home_p', 'home_er', 'home_ter', 'home_wp', 'home_bk',

    # Home team defensive statistics
    'home_po', 'home_a', 'home_e', 'home_pb', 'home_dp', 'home_tp',

    # Umpire crew
    'hp_ump_id', 'hp_ump_name', '1b_ump_id', '1b_ump_name',
    '2b_ump_id', '2b_ump_name', '3b_ump_id', '3b_ump_name', 'lf_ump_id',
    'lf_ump_name', 'rf_ump_id', 'rf_ump_name',

    # Managers
    'visitor_manager_id', 'visitor_manager_name', 'home_manager_id', 
    'home_manager_name', 

    # Key pitchers and RBI batters
    'winning_pitcher_id', 'winning_pitcher_name',
    'losing_pitcher_id', 'losing_pitcher_name', 'saving_pitcher_id',
    'saving_pitcher_name', 'winning_rbi_batter_id', 'winning_rbi_batter_name',
    'visitor_starting_pitcher_id', 'visitor_starting_pitcher_name',
    'home_starting_pitcher_id', 'home_starting_pitcher_name',

    # Visiting team starting lineup
    'visitor_starter_1_id', 'visitor_starter_1_name', 'visitor_starter_1_pos',
    'visitor_starter_2_id', 'visitor_starter_2_name', 'visitor_starter_2_pos',
    'visitor_starter_3_id', 'visitor_starter_3_name', 'visitor_starter_3_pos',
    'visitor_starter_4_id', 'visitor_starter_4_name', 'visitor_starter_4_pos',
    'visitor_starter_5_id', 'visitor_starter_5_name', 'visitor_starter_5_pos',
    'visitor_starter_6_id', 'visitor_starter_6_name', 'visitor_starter_6_pos',
    'visitor_starter_7_id', 'visitor_starter_7_name', 'visitor_starter_7_pos',
    'visitor_starter_8_id', 'visitor_starter_8_name', 'visitor_starter_8_pos',
    'visitor_starter_9_id', 'visitor_starter_9_name', 'visitor_starter_9_pos',

    # Home team starting lineup
    'home_starter_1_id', 'home_starter_1_name', 'home_starter_1_pos',
    'home_starter_2_id', 'home_starter_2_name', 'home_starter_2_pos',
    'home_starter_3_id', 'home_starter_3_name', 'home_starter_3_pos',
    'home_starter_4_id', 'home_starter_4_name', 'home_starter_4_pos',
    'home_starter_5_id', 'home_starter_5_name', 'home_starter_5_pos',
    'home_starter_6_id', 'home_starter_6_name', 'home_starter_6_pos',
    'home_starter_7_id', 'home_starter_7_name', 'home_starter_7_pos',
    'home_starter_8_id', 'home_starter_8_name', 'home_starter_8_pos',
    'home_starter_9_id', 'home_starter_9_name', 'home_starter_9_pos',

    # Additional information & acquisition info
    'additional_info', 'acquisition_info'
]

# Assign column names to game log data
games.columns = retrosheet_cols

# Create new column of game IDs
games['game_code'] = range(1, len(games) + 1)

# Export CSV of merged data
games.to_csv(filepath / 'data/processed/game_logs_2021-2024.csv', index = False)