"""
Advanced Performance Metrics Collector
Collects Win Shares, PER, BPM, VORP, and team performance data
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import os

class AdvancedStatsCollector:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.delay = 3  # Respectful delay

    def scrape_basketball_reference_advanced(self, year=2024):
        """
        Scrape Basketball-Reference for PER, WS, BPM, VORP
        """
        print(f"\n[1/3] Scraping Basketball-Reference advanced stats ({year})...")

        url = f"https://www.basketball-reference.com/leagues/NBA_{year}_advanced.html"

        try:
            time.sleep(self.delay)
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                # Parse tables with pandas
                tables = pd.read_html(response.text)
                df = tables[0]

                # Remove header rows that appear in data
                df = df[df['Player'] != 'Player']

                # Select key columns
                columns = ['Player', 'Pos', 'Age', 'Tm', 'G', 'MP',
                          'PER', 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%',
                          'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%',
                          'OWS', 'DWS', 'WS', 'WS/48',
                          'OBPM', 'DBPM', 'BPM', 'VORP']

                df_clean = df[[col for col in columns if col in df.columns]].copy()

                # Convert numeric columns
                numeric_cols = ['PER', 'TS%', 'WS', 'WS/48', 'OBPM', 'DBPM', 'BPM', 'VORP',
                               'OWS', 'DWS', 'USG%', 'ORB%', 'DRB%', 'TRB%', 'AST%']
                for col in numeric_cols:
                    if col in df_clean.columns:
                        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

                # Remove duplicates (traded players appear multiple times)
                # Keep the 'TOT' (total) row for traded players
                df_clean['is_total'] = df_clean['Tm'] == 'TOT'
                df_clean = df_clean.sort_values('is_total', ascending=False)
                df_clean = df_clean.drop_duplicates(subset=['Player'], keep='first')
                df_clean = df_clean.drop('is_total', axis=1)

                print(f"[OK] Collected advanced stats for {len(df_clean)} players")
                print(f"    Metrics: PER, WS, BPM, VORP, TS%, USG%")

                return df_clean
            else:
                print(f"[ERROR] HTTP {response.status_code}")
                return pd.DataFrame()

        except Exception as e:
            print(f"[ERROR] {e}")
            return pd.DataFrame()

    def scrape_basketball_reference_per_game(self, year=2024):
        """
        Scrape per-game stats to supplement existing data
        """
        print(f"\n[2/3] Scraping Basketball-Reference per-game stats...")

        url = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"

        try:
            time.sleep(self.delay)
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                tables = pd.read_html(response.text)
                df = tables[0]

                df = df[df['Player'] != 'Player']

                # Key columns
                columns = ['Player', 'Pos', 'Age', 'Tm', 'G', 'GS', 'MP',
                          'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%',
                          'eFG%', 'FT', 'FTA', 'FT%',
                          'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']

                df_clean = df[[col for col in columns if col in df.columns]].copy()

                # Handle traded players
                df_clean['is_total'] = df_clean['Tm'] == 'TOT'
                df_clean = df_clean.sort_values('is_total', ascending=False)
                df_clean = df_clean.drop_duplicates(subset=['Player'], keep='first')
                df_clean = df_clean.drop('is_total', axis=1)

                print(f"[OK] Collected per-game stats for {len(df_clean)} players")

                return df_clean
            else:
                print(f"[ERROR] HTTP {response.status_code}")
                return pd.DataFrame()

        except Exception as e:
            print(f"[ERROR] {e}")
            return pd.DataFrame()

    def scrape_team_stats(self, year=2024):
        """
        Scrape team performance: Offensive Rating, Defensive Rating, MOV
        """
        print(f"\n[3/3] Scraping team statistics...")

        url = f"https://www.basketball-reference.com/leagues/NBA_{year}.html"

        try:
            time.sleep(self.delay)
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find team stats tables
                tables = pd.read_html(response.text)

                # Usually table index 0 or 1 has team stats
                for i, table in enumerate(tables):
                    if 'Team' in table.columns or 'Tm' in table.columns:
                        df = table.copy()

                        # Look for offensive/defensive rating
                        if 'ORtg' in df.columns or 'DRtg' in df.columns:
                            columns = ['Team', 'W', 'L', 'W/L%', 'MOV', 'ORtg', 'DRtg', 'NRtg', 'Pace']
                            df_clean = df[[col for col in columns if col in df.columns]].copy()

                            # Remove average row
                            df_clean = df_clean[df_clean['Team'] != 'League Average']

                            print(f"[OK] Collected stats for {len(df_clean)} teams")
                            print(f"    Metrics: ORtg, DRtg, NRtg, MOV, Pace")

                            return df_clean

                # If not found in main table, try advanced team stats
                url_advanced = f"https://www.basketball-reference.com/leagues/NBA_{year}_ratings.html"
                time.sleep(self.delay)
                response = requests.get(url_advanced, headers=self.headers)

                if response.status_code == 200:
                    tables = pd.read_html(response.text)
                    df = tables[0]

                    columns = ['Team', 'W', 'L', 'MOV', 'ORtg', 'DRtg', 'NRtg', 'Pace']
                    df_clean = df[[col for col in columns if col in df.columns]].copy()

                    print(f"[OK] Collected advanced team stats for {len(df_clean)} teams")
                    return df_clean

            print("[WARNING] Could not find team stats table")
            return pd.DataFrame()

        except Exception as e:
            print(f"[ERROR] {e}")
            return pd.DataFrame()

    def collect_all_advanced_stats(self, year=2024):
        """
        Main collection method
        """
        print("="*70)
        print("ADVANCED PERFORMANCE METRICS COLLECTION")
        print("="*70)

        os.makedirs('data', exist_ok=True)

        # Collect advanced stats
        advanced = self.scrape_basketball_reference_advanced(year)
        if not advanced.empty:
            filepath = 'data/1_player_advanced_bbref.csv'
            advanced.to_csv(filepath, index=False)
            print(f"\n[SAVED] {filepath}")

        # Collect per-game stats
        per_game = self.scrape_basketball_reference_per_game(year)
        if not per_game.empty:
            filepath = 'data/1_player_per_game_bbref.csv'
            per_game.to_csv(filepath, index=False)
            print(f"[SAVED] {filepath}")

        # Collect team stats
        team_stats = self.scrape_team_stats(year)
        if not team_stats.empty:
            filepath = 'data/1_team_performance.csv'
            team_stats.to_csv(filepath, index=False)
            print(f"[SAVED] {filepath}")

        print("\n" + "="*70)
        print("[SUCCESS] Advanced stats collection complete")
        print("="*70)

        print("\n[METRICS COLLECTED]:")
        if not advanced.empty:
            print("  - PER (Player Efficiency Rating)")
            print("  - WS (Win Shares) - OWS + DWS")
            print("  - BPM (Box Plus/Minus) - OBPM + DBPM")
            print("  - VORP (Value Over Replacement Player)")
            print("  - TS% (True Shooting Percentage)")
            print("  - USG% (Usage Rate)")

        if not team_stats.empty:
            print("  - ORtg (Offensive Rating)")
            print("  - DRtg (Defensive Rating)")
            print("  - NRtg (Net Rating)")
            print("  - MOV (Margin of Victory)")
            print("  - Pace (Possessions per 48 min)")

if __name__ == "__main__":
    collector = AdvancedStatsCollector()
    collector.collect_all_advanced_stats(year=2024)
