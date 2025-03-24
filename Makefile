.PHONY: clean

clean:
	rm reports/report.html
	rm data/processed/*

all: reports/report.html

# Generate file of merged game log data
data/processed/game_logs_2021-2024.csv:\
 data/raw/gl2021.txt\
 data/raw/gl2022.txt\
 data/raw/gl2023.txt\
 data/raw/gl2024.txt\
 src/merge_data.py
	python3 src/merge_data.py

# Clean game log data
data/processed/game_logs_2021-2024_cleaned.csv:\
 data/processed/game_logs_2021-2024.csv\
 src/clean_data.py
	python3 src/clean_data.py

# Pivot data longer
data/processed/team_games_2021-2024.csv:\
 data/processed/game_logs_2021-2024_cleaned.csv\
 src/pivot_data_long.py
	python3 src/pivot_data_long.py

# Calculate team win-loss records
data/processed/team_win_loss_records.csv:\
 data/processed/team_games_2021-2024.csv\
 src/calc_team_records.py
	python3 src/calc_team_records.py
	
# Generate plot of total average monthly runs for 2024
figures/avg_runs_scored_cumulative.png figures/avg_runs_scored_by_year.png:\
 data/processed/team_games_2021-2024.csv\
 src/plot_avg_monthly_runs.py
	python3 src/plot_avg_monthly_runs.py

# Perform k-means clustering on 2024 MLB teams
figures/kmeans_clustering_2024.png:\
 data/processed/team_games_2021-2024.csv\
 data/processed/team_win_loss_records.csv\
 src/cluster_teams_2024.py
	python3 src/cluster_teams_2024.py

# Render notebook
reports/report.html: reports/report.qmd\
 figures/avg_runs_scored_cumulative.png\
 figures/avg_runs_scored_by_year.png\
 figures/kmeans_clustering_2024.png
	quarto render reports/report.qmd --to html