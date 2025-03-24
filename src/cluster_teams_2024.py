#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  1 15:14:03 2025

Author: Julia Muller

Perform k-means clustering of 2024 MLB teams
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import seaborn as sns
import plotly.graph_objects as go

# Import data
home_dir = Path(__file__).parent.parent
teams = pd.read_csv(home_dir / 'data/processed/team_games_2021-2024.csv')
records = pd.read_csv(home_dir / 'data/processed/team_win_loss_records.csv')


"""
Perform the clustering
"""
# Filter for 2024 data only
teams = teams[teams['year'] == 2024]

# Aggregate team-level stats for clustering
team_stats = teams.groupby('team').agg(
    total_hits = ('hits', 'sum'),
    total_hr = ('hr', 'sum'),
    total_rbi = ('rbi', 'sum'),
    total_walks = ('walks', 'sum'),
    total_so = ('so', 'sum'),
    total_er = ('er', 'sum'),
    total_opponent_score = ('opponent_score', 'sum')
).reset_index()

# Scale the data
scaler = StandardScaler()
team_stats_scaled = scaler.fit_transform(team_stats.drop(columns = 'team'))

# Apply k-means clustering (k = 3)
kmeans = KMeans(n_clusters = 3, n_init = 100, random_state = 123)
kmeans_result = kmeans.fit(team_stats_scaled)


"""
Perform PCA
"""
pca = PCA(n_components = 2)
pca_result = pca.fit_transform(team_stats_scaled)

pca_df = pd.DataFrame(pca_result, columns = ['PC1', 'PC2'])
pca_df['Cluster'] = kmeans.labels_

# Calculate PCA loadings
loadings = pd.DataFrame(pca.components_.T, columns=[f"PC{i+1}" for i in range(pca.n_components_)], index=team_stats.drop(columns='team').columns)

# Display PCA loadings
print(loadings)
loadings.to_csv(home_dir / 'data/processed/pca_loadings.csv', index = True)


"""
Visualize the clustering
"""
# Generate scatterplot of clustering results
sns.set(style = 'whitegrid')
plt.figure(figsize = (8, 6))
# sns.scatterplot(
#     x = team_stats_scaled[:, 0], 
#     y = team_stats_scaled[:, 1], 
#     hue = team_stats['cluster'], 
#     palette = 'Set1'
# )

# # Add title and labels
# plt.title('K-Means Clustering of MLB Teams', fontsize = 16)
# plt.xlabel('PC1', fontsize = 14)
# plt.ylabel('PC2', fontsize = 14)

# # Adjust legend
# plt.legend(title = 'Cluster', loc = 'upper left', fontsize = 12)

# # Export
# plt.savefig(home_dir / 'figures/kmeans_clustering_2024.png', dpi = 300, bbox_inches = 'tight')

sns.scatterplot(data = pca_df, x = 'PC1', y = 'PC2', hue = 'Cluster', palette = 'Set1', s = 50, marker = 'o')
plt.title('Clustering 2024 MLB Teams Based on Performance', fontsize = 16)
plt.xlabel('Principal Component 1', fontsize = 14)
plt.ylabel('Principal Component 2', fontsize = 14)
plt.legend(title = 'Cluster')
plt.savefig(home_dir / 'figures/kmeans_clustering_2024.png', dpi = 300, bbox_inches = 'tight')


"""
Merge cluster results with team win percentage
"""
# Add cluster labels to the dataset
team_stats['cluster'] = kmeans_result.labels_

# Merge cluster results and win percentage
records = records[records['year'] == 2024]
results_merged = pd.merge(team_stats, records, on = ['team'])
results_merged_sorted = results_merged.sort_values(by = 'win_pct', ascending = False)  # Sort descending

# Create a plotly table of win percentages and clustering results
fig = go.Figure(data = [go.Table(
    header = dict(values = ['Team', 'Win %', 'Cluster'],
                fill_color = 'black',
                align = 'center',
                font = dict(size = 12, color = 'white')),
    cells = dict(values = [results_merged_sorted['team'], 
                       results_merged['win_pct'].round(2), 
                       results_merged_sorted['cluster']],
               fill_color = 'white',
               align = 'left',
               font = dict(size = 11, color = 'black'))
)])

# Update layout
fig.update_layout(
    width = 400,
    height = 900,
    margin = dict(l = 10, r = 10, t = 10, b = 10)
)

# Export
fig.write_image(home_dir / 'figures/team_win_pct_cluster_table.svg')
# fig.show(renderer='browser')