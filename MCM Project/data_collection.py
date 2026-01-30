"""
MCM Project - Basketball Data Collection
Collects performance, financial, and social media data for NBA/WNBA analysis
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import os

# Create data directory
os.makedirs('data', exist_ok=True)

class BasketballDataCollector:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.delay = 2  # Respectful delay between requests

    def save_to_csv(self, data, filename):
        """Save data to CSV in the data directory"""
        filepath = os.path.join('data', filename)
        data.to_csv(filepath, index=False)
        print(f"[OK] Saved {len(data)} records to {filepath}")
        return filepath

    # ========== SECTION 1: CORE PERFORMANCE DATA ==========

    def get_nba_player_stats_basic(self, season='2023-24'):
        """
        Get basic player stats using nba_api (official NBA data)
        Includes: PTS, TRB, AST, STL, BLK, TOV
        """
        try:
            from nba_api.stats.endpoints import leaguedashplayerstats
            from nba_api.stats.static import players

            print(f"\n[1/6] Fetching NBA basic player stats for {season}...")

            # Get player stats
            stats = leaguedashplayerstats.LeagueDashPlayerStats(
                season=season,
                per_mode_detailed='PerGame'
            )

            df = stats.get_data_frames()[0]

            # Select key columns
            columns = [
                'PLAYER_NAME', 'TEAM_ABBREVIATION', 'GP', 'MIN',
                'PTS', 'REB', 'AST', 'STL', 'BLK', 'TOV',
                'FG_PCT', 'FG3_PCT', 'FT_PCT', 'PLUS_MINUS'
            ]

            df_clean = df[columns].copy()
            df_clean.columns = [
                'Player', 'Team', 'Games_Played', 'Minutes',
                'Points', 'Rebounds', 'Assists', 'Steals', 'Blocks', 'Turnovers',
                'FG_Pct', 'FG3_Pct', 'FT_Pct', 'Plus_Minus'
            ]

            time.sleep(self.delay)
            return df_clean

        except Exception as e:
            print(f"Error fetching basic stats: {e}")
            return pd.DataFrame()

    def get_nba_advanced_stats(self, season='2023-24'):
        """
        Get advanced stats: PER, WS, BPM, USG%, TS%
        """
        try:
            from nba_api.stats.endpoints import leaguedashplayerstats

            print(f"[2/6] Fetching NBA advanced player stats for {season}...")

            stats = leaguedashplayerstats.LeagueDashPlayerStats(
                season=season,
                measure_type_detailed_defense='Advanced'
            )

            df = stats.get_data_frames()[0]

            # Key advanced metrics
            columns = [
                'PLAYER_NAME', 'TEAM_ABBREVIATION',
                'OFF_RATING', 'DEF_RATING', 'NET_RATING',
                'AST_PCT', 'AST_TO', 'AST_RATIO',
                'OREB_PCT', 'DREB_PCT', 'REB_PCT',
                'TM_TOV_PCT', 'EFG_PCT', 'TS_PCT',
                'USG_PCT', 'PACE', 'PIE'
            ]

            df_clean = df[[col for col in columns if col in df.columns]].copy()

            time.sleep(self.delay)
            return df_clean

        except Exception as e:
            print(f"Error fetching advanced stats: {e}")
            return pd.DataFrame()

    def scrape_basketball_reference_advanced(self, year=2024):
        """
        Scrape Basketball-Reference for PER, WS, BPM
        Note: Basketball-Reference allows scraping but requests respectful rate limiting
        """
        print(f"[3/6] Scraping Basketball Reference for PER, WS, BPM ({year})...")

        url = f"https://www.basketball-reference.com/leagues/NBA_{year}_advanced.html"

        try:
            time.sleep(self.delay)
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                # Read HTML table directly with pandas
                tables = pd.read_html(response.text)
                df = tables[0]

                # Clean the data
                df = df[df['Player'] != 'Player']  # Remove header rows

                # Select key columns
                columns = ['Player', 'Pos', 'Age', 'Tm', 'G', 'MP',
                          'PER', 'TS%', 'USG%', 'OWS', 'DWS', 'WS',
                          'WS/48', 'OBPM', 'DBPM', 'BPM', 'VORP']

                df_clean = df[[col for col in columns if col in df.columns]].copy()

                # Convert numeric columns
                numeric_cols = ['PER', 'TS%', 'USG%', 'OWS', 'DWS', 'WS',
                               'WS/48', 'OBPM', 'DBPM', 'BPM', 'VORP']
                for col in numeric_cols:
                    if col in df_clean.columns:
                        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

                return df_clean
            else:
                print(f"Failed to fetch data: Status {response.status_code}")
                return pd.DataFrame()

        except Exception as e:
            print(f"Error scraping Basketball Reference: {e}")
            return pd.DataFrame()

    # ========== SECTION 2: FINANCIAL & BUSINESS DATA ==========

    def scrape_spotrac_salaries(self, year=2024):
        """
        Scrape Spotrac for player salaries and contract details
        """
        print(f"[4/6] Scraping Spotrac for salary data ({year})...")

        url = f"https://www.spotrac.com/nba/rankings/{year}/"

        try:
            time.sleep(self.delay)
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Try to find the salary table
                tables = pd.read_html(response.text)

                if tables:
                    df = tables[0]

                    # Clean column names
                    if 'Player' in df.columns or 'Name' in df.columns:
                        df_clean = df.copy()
                        return df_clean

                return pd.DataFrame()
            else:
                print(f"Failed to fetch Spotrac data: Status {response.status_code}")
                return pd.DataFrame()

        except Exception as e:
            print(f"Error scraping Spotrac: {e}")
            print("Note: Consider checking Spotrac's robots.txt and terms of service")
            return pd.DataFrame()

    def get_team_valuations(self):
        """
        Create template for Forbes team valuations
        Note: Forbes data typically requires manual collection or API access
        """
        print("[5/6] Creating template for team valuation data...")
        print("Note: Forbes data often requires manual collection from their annual reports")

        # Template structure
        template = {
            'Team': ['Lakers', 'Warriors', 'Knicks', 'Bulls', 'Celtics'],
            'Valuation_Millions': [0, 0, 0, 0, 0],
            'Revenue_Millions': [0, 0, 0, 0, 0],
            'Operating_Income_Millions': [0, 0, 0, 0, 0],
            'Year': [2024, 2024, 2024, 2024, 2024],
            'Source': ['Forbes - Manual Entry Required'] * 5
        }

        return pd.DataFrame(template)

    # ========== SECTION 3: SOFT DATA & EXTERNAL VARIABLES ==========

    def get_google_trends_data(self, keywords=['NBA', 'Lakers', 'LeBron James']):
        """
        Get Google Trends data for teams/players
        """
        print(f"[6/6] Fetching Google Trends data...")

        try:
            from pytrends.request import TrendReq

            pytrends = TrendReq(hl='en-US', tz=360)

            # Get interest over time
            pytrends.build_payload(keywords, timeframe='today 12-m')
            df = pytrends.interest_over_time()

            if not df.empty:
                df = df.drop('isPartial', axis=1, errors='ignore')
                df = df.reset_index()

            time.sleep(self.delay)
            return df

        except Exception as e:
            print(f"Error fetching Google Trends: {e}")
            return pd.DataFrame()

    def create_city_data_template(self):
        """
        Create template for city-level data
        """
        print("Creating city data template...")

        # Sample NBA cities
        cities_data = {
            'City': ['Los Angeles', 'New York', 'Chicago', 'Boston', 'San Francisco',
                    'Dallas', 'Houston', 'Miami', 'Phoenix', 'Philadelphia'],
            'State': ['CA', 'NY', 'IL', 'MA', 'CA', 'TX', 'TX', 'FL', 'AZ', 'PA'],
            'Population': [3900000, 8336000, 2746000, 692000, 873000,
                          1343000, 2304000, 442000, 1608000, 1584000],
            'Metro_Population': [13200000, 19216000, 9618000, 4873000, 4749000,
                                7637000, 7122000, 6138000, 4845000, 6102000],
            'GDP_Billions': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # To be filled
            'NBA_Team': ['Lakers/Clippers', 'Knicks/Nets', 'Bulls', 'Celtics', 'Warriors',
                        'Mavericks', 'Rockets', 'Heat', 'Suns', '76ers']
        }

        return pd.DataFrame(cities_data)

    def collect_all_data(self):
        """
        Main method to collect all data
        """
        print("="*60)
        print("MCM PROJECT - BASKETBALL DATA COLLECTION")
        print("="*60)

        all_files = []

        # Section 1: Core Performance Data
        print("\n[SECTION 1: CORE PERFORMANCE DATA]")
        print("-"*60)

        basic_stats = self.get_nba_player_stats_basic()
        if not basic_stats.empty:
            all_files.append(self.save_to_csv(basic_stats, '1_player_basic_stats.csv'))

        advanced_stats = self.get_nba_advanced_stats()
        if not advanced_stats.empty:
            all_files.append(self.save_to_csv(advanced_stats, '1_player_advanced_stats_nba_api.csv'))

        bbref_stats = self.scrape_basketball_reference_advanced()
        if not bbref_stats.empty:
            all_files.append(self.save_to_csv(bbref_stats, '1_player_advanced_stats_bbref.csv'))

        # Section 2: Financial & Business Data
        print("\n[SECTION 2: FINANCIAL & BUSINESS DATA]")
        print("-"*60)

        salary_data = self.scrape_spotrac_salaries()
        if not salary_data.empty:
            all_files.append(self.save_to_csv(salary_data, '2_player_salaries.csv'))

        team_valuations = self.get_team_valuations()
        all_files.append(self.save_to_csv(team_valuations, '2_team_valuations_template.csv'))

        # Section 3: Soft Data
        print("\n[SECTION 3: SOFT DATA & EXTERNAL VARIABLES]")
        print("-"*60)

        trends_data = self.get_google_trends_data()
        if not trends_data.empty:
            all_files.append(self.save_to_csv(trends_data, '3_google_trends.csv'))

        city_data = self.create_city_data_template()
        all_files.append(self.save_to_csv(city_data, '3_city_market_data.csv'))

        # Summary
        print("\n" + "="*60)
        print("[SUCCESS] DATA COLLECTION COMPLETE")
        print("="*60)
        print(f"\nTotal files created: {len(all_files)}")
        print("\nFiles saved in ./data/ directory:")
        for f in all_files:
            print(f"  - {f}")

        print("\n[NOTES:]")
        print("  1. Some data sources may require manual collection (Forbes, Social Blade)")
        print("  2. For lineup data, consider using NBA.com's lineup stats API")
        print("  3. Respect rate limits and terms of service for all sources")
        print("  4. Social media data may require API keys (Twitter/Instagram APIs)")

if __name__ == "__main__":
    collector = BasketballDataCollector()
    collector.collect_all_data()
