"""
Social Media & Soft Data Collection
Collects engagement metrics, search trends, and social media following
"""

import pandas as pd
import requests
from pytrends.request import TrendReq
import time
import os

class SocialMediaCollector:
    def __init__(self):
        self.delay = 2

    def get_google_trends_teams(self, teams=None, timeframe='today 12-m'):
        """
        Get Google Trends data for NBA teams
        """
        if teams is None:
            teams = [
                'Los Angeles Lakers', 'Golden State Warriors',
                'Boston Celtics', 'New York Knicks', 'Chicago Bulls'
            ]

        print(f"\n[SEARCH] Fetching Google Trends for {len(teams)} teams...")

        try:
            pytrends = TrendReq(hl='en-US', tz=360)

            all_data = []

            # Process in batches of 5 (Google Trends limit)
            for i in range(0, len(teams), 5):
                batch = teams[i:i+5]

                pytrends.build_payload(batch, timeframe=timeframe)
                df = pytrends.interest_over_time()

                if not df.empty:
                    df = df.drop('isPartial', axis=1, errors='ignore')
                    all_data.append(df)

                time.sleep(self.delay)

            if all_data:
                combined = pd.concat(all_data, axis=1)
                combined = combined.reset_index()
                print(f"[OK] Collected trends data for {len(batch)} teams")
                return combined

        except Exception as e:
            print(f"[ERROR] Error fetching Google Trends: {e}")

        return pd.DataFrame()

    def get_google_trends_players(self, players=None, timeframe='today 12-m'):
        """
        Get Google Trends data for star players
        """
        if players is None:
            players = [
                'LeBron James', 'Stephen Curry', 'Kevin Durant',
                'Giannis Antetokounmpo', 'Luka Doncic'
            ]

        print(f"\n[SEARCH] Fetching Google Trends for {len(players)} players...")

        try:
            pytrends = TrendReq(hl='en-US', tz=360)

            # Process in batches
            all_data = []

            for i in range(0, len(players), 5):
                batch = players[i:i+5]

                pytrends.build_payload(batch, timeframe=timeframe)
                df = pytrends.interest_over_time()

                if not df.empty:
                    df = df.drop('isPartial', axis=1, errors='ignore')
                    all_data.append(df)

                time.sleep(self.delay)

            if all_data:
                combined = pd.concat(all_data, axis=1)
                combined = combined.reset_index()
                print(f"[OK] Collected trends data for players")
                return combined

        except Exception as e:
            print(f"[ERROR] Error fetching player trends: {e}")

        return pd.DataFrame()

    def create_social_media_template(self):
        """
        Create template for social media data
        Note: Instagram/Twitter API access requires authentication
        This creates a template for manual data entry or API integration
        """
        print("\n[SOCIAL] Creating social media template...")

        # Top NBA players (example data structure)
        players = [
            'LeBron James', 'Stephen Curry', 'Kevin Durant',
            'Giannis Antetokounmpo', 'Luka Doncic',
            'Jayson Tatum', 'Joel Embiid', 'Nikola Jokic',
            'Damian Lillard', 'Anthony Davis'
        ]

        template = {
            'Player': players,
            'Instagram_Followers': [0] * len(players),
            'Instagram_Engagement_Rate': [0.0] * len(players),
            'Twitter_Followers': [0] * len(players),
            'Twitter_Engagement_Rate': [0.0] * len(players),
            'Jersey_Sales_Rank': [0] * len(players),
            'Search_Popularity_Score': [0] * len(players),
            'Commercial_Endorsements': [0] * len(players),
            'Data_Source': ['Manual Entry Required'] * len(players)
        }

        df = pd.DataFrame(template)

        print(f"[OK] Created template for {len(players)} players")
        print("\n[WARNING] Note: Social media APIs require authentication:")
        print("   • Instagram: Requires Meta API access")
        print("   • Twitter: Requires Twitter API key")
        print("   • Consider using Social Blade or manual collection")

        return df

    def create_team_social_template(self):
        """
        Create template for team social media presence
        """
        print("\n[SOCIAL] Creating team social media template...")

        teams = [
            'Los Angeles Lakers', 'Golden State Warriors', 'Boston Celtics',
            'New York Knicks', 'Chicago Bulls', 'Miami Heat',
            'Brooklyn Nets', 'Dallas Mavericks', 'Phoenix Suns',
            'Philadelphia 76ers'
        ]

        template = {
            'Team': teams,
            'Instagram_Followers': [0] * len(teams),
            'Twitter_Followers': [0] * len(teams),
            'Facebook_Followers': [0] * len(teams),
            'Average_Attendance': [0] * len(teams),
            'Ticket_Revenue_Millions': [0] * len(teams),
            'Merchandise_Sales_Rank': [0] * len(teams),
            'Google_Search_Interest': [0] * len(teams),
            'Data_Source': ['Manual Entry Required'] * len(teams)
        }

        return pd.DataFrame(template)

    def get_regional_interest(self, keywords, geo='US'):
        """
        Get regional interest from Google Trends
        Useful for expansion team analysis
        """
        print(f"\n[MAP] Fetching regional interest for: {keywords}")

        try:
            pytrends = TrendReq(hl='en-US', tz=360)

            pytrends.build_payload(keywords, timeframe='today 12-m', geo=geo)
            regional = pytrends.interest_by_region(resolution='CITY', inc_low_vol=True)

            regional = regional.reset_index()
            regional = regional.sort_values(keywords[0], ascending=False)

            print(f"[OK] Collected regional data for {len(regional)} cities")

            time.sleep(self.delay)
            return regional

        except Exception as e:
            print(f"[ERROR] Error fetching regional interest: {e}")
            return pd.DataFrame()

    def collect_all_social_data(self):
        """
        Main collection method
        """
        print("="*60)
        print("SOCIAL MEDIA & SOFT DATA COLLECTION")
        print("="*60)

        os.makedirs('data', exist_ok=True)
        files_created = []

        # Google Trends - Teams
        trends_teams = self.get_google_trends_teams()
        if not trends_teams.empty:
            filepath = os.path.join('data', '3_google_trends_teams.csv')
            trends_teams.to_csv(filepath, index=False)
            files_created.append(filepath)
            print(f"[OK] Saved to {filepath}")

        # Google Trends - Players
        trends_players = self.get_google_trends_players()
        if not trends_players.empty:
            filepath = os.path.join('data', '3_google_trends_players.csv')
            trends_players.to_csv(filepath, index=False)
            files_created.append(filepath)
            print(f"[OK] Saved to {filepath}")

        # Regional Interest
        regional = self.get_regional_interest(['NBA'])
        if not regional.empty:
            filepath = os.path.join('data', '3_regional_interest.csv')
            regional.to_csv(filepath, index=False)
            files_created.append(filepath)
            print(f"[OK] Saved to {filepath}")

        # Social Media Templates
        social_players = self.create_social_media_template()
        filepath = os.path.join('data', '3_social_media_players_template.csv')
        social_players.to_csv(filepath, index=False)
        files_created.append(filepath)
        print(f"✓ Saved to {filepath}")

        social_teams = self.create_team_social_template()
        filepath = os.path.join('data', '3_social_media_teams_template.csv')
        social_teams.to_csv(filepath, index=False)
        files_created.append(filepath)
        print(f"✓ Saved to {filepath}")

        print("\n" + "="*60)
        print("[SUCCESS] SOCIAL DATA COLLECTION COMPLETE")
        print("="*60)
        print(f"\nFiles created: {len(files_created)}")
        for f in files_created:
            print(f"  - {f}")

if __name__ == "__main__":
    collector = SocialMediaCollector()
    collector.collect_all_social_data()
