"""
Dataset Merger - Combines all collected data into unified datasets
Creates player-level and team-level master datasets
"""

import pandas as pd
import os
from glob import glob

class DataMerger:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir

    def load_file(self, filename):
        """Safely load a CSV file"""
        filepath = os.path.join(self.data_dir, filename)
        if os.path.exists(filepath):
            try:
                df = pd.read_csv(filepath)
                print(f"[OK] Loaded {filename}: {len(df)} rows")
                return df
            except Exception as e:
                print(f"[ERROR] Error loading {filename}: {e}")
                return None
        else:
            print(f"[WARNING] File not found: {filename}")
            return None

    def standardize_player_names(self, df, name_col='Player'):
        """Standardize player names for merging"""
        if name_col in df.columns:
            df[name_col] = df[name_col].str.strip()
            df[name_col] = df[name_col].str.replace(r'\s+', ' ', regex=True)
        return df

    def merge_player_performance_data(self):
        """
        Merge all player performance data into a single master file
        """
        print("\n" + "="*60)
        print("MERGING PLAYER PERFORMANCE DATA")
        print("="*60)

        # Load basic stats
        basic = self.load_file('1_player_basic_stats.csv')

        # Load advanced stats from NBA API
        advanced_nba = self.load_file('1_player_advanced_stats_nba_api.csv')

        # Load advanced stats from Basketball Reference
        advanced_bbref = self.load_file('1_player_advanced_stats_bbref.csv')

        if basic is None:
            print("[ERROR] Cannot merge: basic stats file missing")
            return None

        # Start with basic stats
        master = basic.copy()

        # Merge NBA API advanced stats
        if advanced_nba is not None:
            master = pd.merge(
                master,
                advanced_nba,
                left_on='Player',
                right_on='PLAYER_NAME',
                how='left',
                suffixes=('', '_nba')
            )

        # Merge Basketball Reference advanced stats
        if advanced_bbref is not None:
            # Standardize names
            advanced_bbref = self.standardize_player_names(advanced_bbref, 'Player')
            master = self.standardize_player_names(master, 'Player')

            # Key metrics to merge
            bbref_cols = ['Player', 'PER', 'TS%', 'USG%', 'WS', 'WS/48',
                         'OBPM', 'DBPM', 'BPM', 'VORP']
            bbref_subset = advanced_bbref[[col for col in bbref_cols if col in advanced_bbref.columns]]

            master = pd.merge(
                master,
                bbref_subset,
                on='Player',
                how='left',
                suffixes=('', '_bbref')
            )

        print(f"\n[OK] Master player dataset: {len(master)} players, {len(master.columns)} columns")

        return master

    def calculate_player_network_metrics(self):
        """
        Calculate network metrics from lineup data
        """
        print("\n" + "="*60)
        print("CALCULATING PLAYER NETWORK METRICS")
        print("="*60)

        edges = self.load_file('1_lineup_network_edges.csv')

        if edges is None:
            return None

        # Calculate metrics for each player
        player_metrics = []

        all_players = set(edges['Player_A'].unique()) | set(edges['Player_B'].unique())

        for player in all_players:
            # Get all connections for this player
            connections = edges[
                (edges['Player_A'] == player) | (edges['Player_B'] == player)
            ]

            metrics = {
                'Player': player,
                'Network_Connections': len(connections),  # Degree
                'Total_Minutes_Played_With_Others': connections['Minutes_Together'].sum(),
                'Avg_Net_Rating_With_Others': connections['Net_Rating'].mean(),
                'Best_Partner_Net_Rating': connections['Net_Rating'].max(),
                'Worst_Partner_Net_Rating': connections['Net_Rating'].min()
            }

            player_metrics.append(metrics)

        df_network = pd.DataFrame(player_metrics)
        df_network = df_network.sort_values('Total_Minutes_Played_With_Others', ascending=False)

        print(f"[OK] Calculated network metrics for {len(df_network)} players")

        return df_network

    def merge_player_financial_data(self, master_performance):
        """
        Add salary data to player master dataset
        """
        print("\n" + "="*60)
        print("MERGING FINANCIAL DATA")
        print("="*60)

        salary = self.load_file('2_player_salaries.csv')

        if salary is None or master_performance is None:
            print("[WARNING] Cannot merge financial data")
            return master_performance

        # Standardize names
        salary = self.standardize_player_names(salary, 'Player' if 'Player' in salary.columns else 'Name')

        # Try to merge on player name
        name_col = 'Player' if 'Player' in salary.columns else 'Name'

        master_with_salary = pd.merge(
            master_performance,
            salary,
            left_on='Player',
            right_on=name_col,
            how='left',
            suffixes=('', '_salary')
        )

        print(f"[OK] Added financial data: {master_with_salary['Player'].count()} matches")

        return master_with_salary

    def add_social_data(self, master_player):
        """
        Add Google Trends and social media data
        """
        print("\n" + "="*60)
        print("ADDING SOCIAL MEDIA & TRENDS DATA")
        print("="*60)

        social = self.load_file('3_social_media_players_template.csv')

        if social is None or master_player is None:
            print("[WARNING] Cannot add social data")
            return master_player

        # Merge on player name
        master_with_social = pd.merge(
            master_player,
            social,
            on='Player',
            how='left',
            suffixes=('', '_social')
        )

        print(f"[OK] Added social media data")

        return master_with_social

    def create_team_master_dataset(self):
        """
        Create team-level master dataset
        """
        print("\n" + "="*60)
        print("CREATING TEAM MASTER DATASET")
        print("="*60)

        # Start with team valuations
        valuations = self.load_file('2_team_valuations_template.csv')

        if valuations is None:
            print("[WARNING] Creating basic team structure")
            valuations = pd.DataFrame({
                'Team': ['Lakers', 'Warriors', 'Celtics', 'Knicks', 'Bulls']
            })

        # Add social media data
        social_teams = self.load_file('3_social_media_teams_template.csv')

        if social_teams is not None:
            master_team = pd.merge(
                valuations,
                social_teams,
                on='Team',
                how='outer',
                suffixes=('', '_social')
            )
        else:
            master_team = valuations

        print(f"[OK] Team master dataset: {len(master_team)} teams")

        return master_team

    def create_all_master_datasets(self):
        """
        Main method to create all master datasets
        """
        print("="*70)
        print("DATASET MERGER - Creating Master Datasets")
        print("="*70)

        output_files = []

        # 1. Player Performance Master
        player_performance = self.merge_player_performance_data()
        if player_performance is not None:
            filepath = os.path.join(self.data_dir, 'MASTER_player_performance.csv')
            player_performance.to_csv(filepath, index=False)
            output_files.append(filepath)
            print(f"[OK] Saved: {filepath}")

        # 2. Player Network Metrics
        network_metrics = self.calculate_player_network_metrics()
        if network_metrics is not None:
            filepath = os.path.join(self.data_dir, 'MASTER_player_network_metrics.csv')
            network_metrics.to_csv(filepath, index=False)
            output_files.append(filepath)
            print(f"[OK] Saved: {filepath}")

        # 3. Complete Player Master (Performance + Network + Financial + Social)
        if player_performance is not None and network_metrics is not None:
            complete_player = pd.merge(
                player_performance,
                network_metrics,
                on='Player',
                how='left'
            )

            complete_player = self.merge_player_financial_data(complete_player)
            complete_player = self.add_social_data(complete_player)

            filepath = os.path.join(self.data_dir, 'MASTER_player_complete.csv')
            complete_player.to_csv(filepath, index=False)
            output_files.append(filepath)
            print(f"[OK] Saved: {filepath}")

            # Calculate some derived metrics
            if 'Points' in complete_player.columns and 'Salary' in complete_player.columns:
                complete_player['Points_Per_Million'] = complete_player['Points'] / (complete_player['Salary'] / 1000000)

            if 'WS' in complete_player.columns and 'Salary' in complete_player.columns:
                complete_player['WinShares_Per_Million'] = complete_player['WS'] / (complete_player['Salary'] / 1000000)

        # 4. Team Master
        team_master = self.create_team_master_dataset()
        if team_master is not None:
            filepath = os.path.join(self.data_dir, 'MASTER_team_data.csv')
            team_master.to_csv(filepath, index=False)
            output_files.append(filepath)
            print(f"[OK] Saved: {filepath}")

        # Summary
        print("\n" + "="*70)
        print("[SUCCESS] MERGE COMPLETE")
        print("="*70)
        print(f"\nCreated {len(output_files)} master datasets:")
        for f in output_files:
            print(f"  - {f}")

        print("\n[INFO] MASTER DATASETS:")
        print("   - MASTER_player_performance.csv - All performance metrics")
        print("   - MASTER_player_network_metrics.csv - Network analysis metrics")
        print("   - MASTER_player_complete.csv - Complete player profiles")
        print("   - MASTER_team_data.csv - Team-level data")

        print("\n[READY] READY FOR ANALYSIS!")
        print("   All data is now consolidated and ready for modeling")

if __name__ == "__main__":
    merger = DataMerger()
    merger.create_all_master_datasets()
