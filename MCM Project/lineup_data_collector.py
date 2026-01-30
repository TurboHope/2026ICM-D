"""
Lineup Data Collection - Critical for Network Analysis
Collects net rating when specific 5-player lineups are on court together
"""

import pandas as pd
import time
from nba_api.stats.endpoints import leaguedashlineups
import os

class LineupDataCollector:
    def __init__(self):
        self.delay = 2

    def get_lineup_stats(self, season='2023-24', min_minutes=10):
        """
        Get lineup statistics - net rating for 5-player combinations
        This is CRUCIAL for network analysis of player interactions

        Parameters:
        - season: NBA season (e.g., '2023-24')
        - min_minutes: Minimum minutes played together to filter noise
        """
        print(f"\n[LOADING] Fetching lineup data for {season}...")
        print(f"   (Filtering lineups with >= {min_minutes} minutes together)")

        try:
            # Get lineup data from NBA API
            lineups = leaguedashlineups.LeagueDashLineups(
                season=season,
                measure_type_detailed_defense='Base',
                per_mode_detailed='Totals',
                group_quantity=5  # 5-player lineups
            )

            df = lineups.get_data_frames()[0]

            # Filter by minimum minutes
            df_filtered = df[df['MIN'] >= min_minutes].copy()

            # Select key columns
            columns = [
                'GROUP_NAME',  # The 5 players
                'TEAM_ABBREVIATION',
                'GP',  # Games played together
                'MIN',  # Minutes together
                'PLUS_MINUS',  # Net rating (key metric!)
                'OFF_RATING',  # Offensive rating
                'DEF_RATING',  # Defensive rating
                'NET_RATING',  # Net rating
                'PACE',
                'PIE'  # Player Impact Estimate
            ]

            df_clean = df_filtered[[col for col in columns if col in df_filtered.columns]].copy()

            # Rename for clarity - create mapping for columns that exist
            rename_map = {
                'GROUP_NAME': 'Lineup_Players',
                'TEAM_ABBREVIATION': 'Team',
                'GP': 'Games',
                'MIN': 'Minutes',
                'PLUS_MINUS': 'Plus_Minus',
                'OFF_RATING': 'Off_Rating',
                'DEF_RATING': 'Def_Rating',
                'NET_RATING': 'Net_Rating',
                'PACE': 'Pace',
                'PIE': 'PIE'
            }
            # Only rename columns that exist
            df_clean = df_clean.rename(columns={k: v for k, v in rename_map.items() if k in df_clean.columns})

            # Sort by minutes (most played lineups first)
            df_clean = df_clean.sort_values('Minutes', ascending=False)

            # Parse player names for network analysis
            if 'Lineup_Players' in df_clean.columns:
                df_clean['Player_1'] = df_clean['Lineup_Players'].str.split(' - ').str[0]
                df_clean['Player_2'] = df_clean['Lineup_Players'].str.split(' - ').str[1]
                df_clean['Player_3'] = df_clean['Lineup_Players'].str.split(' - ').str[2]
                df_clean['Player_4'] = df_clean['Lineup_Players'].str.split(' - ').str[3]
                df_clean['Player_5'] = df_clean['Lineup_Players'].str.split(' - ').str[4]

            print(f"[OK] Collected {len(df_clean)} lineup combinations")
            if len(df_clean) > 0 and 'Lineup_Players' in df_clean.columns:
                print(f"   Top lineup: {df_clean.iloc[0]['Lineup_Players']}")
                rating_col = 'Net_Rating' if 'Net_Rating' in df_clean.columns else 'Plus_Minus'
                if rating_col in df_clean.columns:
                    print(f"   Minutes: {df_clean.iloc[0]['Minutes']:.1f}, {rating_col}: {df_clean.iloc[0][rating_col]:.1f}")

            time.sleep(self.delay)
            return df_clean

        except Exception as e:
            print(f"[ERROR] Error fetching lineup data: {e}")
            return pd.DataFrame()

    def get_two_player_lineups(self, season='2023-24'):
        """
        Get 2-player combination stats (useful for pairing analysis)
        """
        print(f"\n[LOADING] Fetching 2-player combination data...")

        try:
            lineups = leaguedashlineups.LeagueDashLineups(
                season=season,
                group_quantity=2  # 2-player combinations
            )

            df = lineups.get_data_frames()[0]

            df = df.sort_values('MIN', ascending=False)

            print(f"[OK] Collected {len(df)} 2-player combinations")

            time.sleep(self.delay)
            return df

        except Exception as e:
            print(f"[ERROR] Error fetching 2-player lineup data: {e}")
            return pd.DataFrame()

    def create_network_edge_list(self, lineup_df):
        """
        Convert lineup data to network edge list format
        Each edge represents two players playing together
        Weight = sum of minutes played together
        """
        print("\n[NETWORK] Creating network edge list from lineup data...")

        edges = []

        for _, row in lineup_df.iterrows():
            players = [
                row['Player_1'], row['Player_2'], row['Player_3'],
                row['Player_4'], row['Player_5']
            ]

            minutes = row['Minutes']
            net_rating = row.get('Net_Rating', row.get('Plus_Minus', 0))

            # Create edges for all player pairs in this lineup
            for i in range(len(players)):
                for j in range(i+1, len(players)):
                    edges.append({
                        'Player_A': players[i],
                        'Player_B': players[j],
                        'Minutes_Together': minutes,
                        'Net_Rating': net_rating,
                        'Team': row['Team']
                    })

        # Convert to DataFrame and aggregate
        edge_df = pd.DataFrame(edges)

        # Sum up minutes for each player pair across all lineups
        edge_agg = edge_df.groupby(['Player_A', 'Player_B', 'Team']).agg({
            'Minutes_Together': 'sum',
            'Net_Rating': 'mean'  # Average net rating
        }).reset_index()

        edge_agg = edge_agg.sort_values('Minutes_Together', ascending=False)

        print(f"[OK] Created {len(edge_agg)} unique player-pair connections")

        return edge_agg

    def collect_all_lineup_data(self, season='2023-24'):
        """
        Main method to collect all lineup data
        """
        print("="*60)
        print("LINEUP DATA COLLECTION - FOR NETWORK ANALYSIS")
        print("="*60)

        os.makedirs('data', exist_ok=True)

        # Get 5-player lineups
        lineup_5 = self.get_lineup_stats(season=season, min_minutes=10)

        if not lineup_5.empty:
            filepath = os.path.join('data', '1_lineup_5player_stats.csv')
            lineup_5.to_csv(filepath, index=False)
            print(f"\n[OK] Saved to {filepath}")

            # Create network edge list - check if we have all required columns
            required_cols = ['Player_1', 'Player_2', 'Player_3', 'Player_4', 'Player_5', 'Minutes']
            if all(col in lineup_5.columns for col in required_cols):
                edge_list = self.create_network_edge_list(lineup_5)
                if not edge_list.empty:
                    edge_filepath = os.path.join('data', '1_lineup_network_edges.csv')
                    edge_list.to_csv(edge_filepath, index=False)
                    print(f"[OK] Saved network edge list to {edge_filepath}")
            else:
                print(f"[WARNING] Cannot create network edge list - missing player columns")

        # Get 2-player lineups
        lineup_2 = self.get_two_player_lineups(season=season)

        if not lineup_2.empty:
            filepath = os.path.join('data', '1_lineup_2player_stats.csv')
            lineup_2.to_csv(filepath, index=False)
            print(f"[OK] Saved to {filepath}")

        print("\n" + "="*60)
        print("[SUCCESS] LINEUP DATA COLLECTION COMPLETE")
        print("="*60)
        print("\n[TIP] Usage for Network Analysis:")
        print("   - Use '1_lineup_network_edges.csv' to build player interaction network")
        print("   - Edge weight = Minutes_Together")
        print("   - Edge value = Net_Rating (performance when paired)")
        print("   - Can identify key players (high centrality) and effective combinations")

if __name__ == "__main__":
    collector = LineupDataCollector()
    collector.collect_all_lineup_data(season='2023-24')
