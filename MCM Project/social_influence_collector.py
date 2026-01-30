"""
Social Influence & Market Data Collector
Collects social media metrics, Google Trends, and demographic data
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import os
from pytrends.request import TrendReq

class SocialInfluenceCollector:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.delay = 3

    def get_google_trends_by_city(self, keywords, cities_geo_codes):
        """
        Get Google Trends data for specific cities/regions
        """
        print(f"\n[1/5] Fetching Google Trends by city...")

        try:
            pytrends = TrendReq(hl='en-US', tz=360)

            all_data = []

            for keyword in keywords[:5]:  # Process in batches
                print(f"  - Searching: {keyword}")

                # Get interest by region (city level)
                pytrends.build_payload([keyword], timeframe='today 12-m', geo='US')

                # Get city-level data
                regional = pytrends.interest_by_region(resolution='CITY', inc_low_vol=True)

                if not regional.empty:
                    regional = regional.reset_index()
                    regional = regional.rename(columns={keyword: 'Search_Interest'})
                    regional['Keyword'] = keyword
                    regional = regional.sort_values('Search_Interest', ascending=False)

                    all_data.append(regional)

                time.sleep(self.delay)

            if all_data:
                combined = pd.concat(all_data, ignore_index=True)
                print(f"[OK] Collected trends for {len(all_data)} keywords across cities")
                return combined

        except Exception as e:
            print(f"[ERROR] {e}")
            print("[TIP] Google Trends may be rate-limited. Wait and retry.")

        return pd.DataFrame()

    def get_expansion_city_trends(self):
        """
        Focused trends for potential expansion cities
        """
        print(f"\n[2/5] Analyzing expansion city search interest...")

        expansion_cities = {
            'Seattle WA': 'US-WA-819',
            'Las Vegas NV': 'US-NV-839',
            'Kansas City MO': 'US-MO-616',
            'Louisville KY': 'US-KY-529',
            'San Diego CA': 'US-CA-825',
            'Pittsburgh PA': 'US-PA-770',
            'Nashville TN': 'US-TN-659',
            'Austin TX': 'US-TX-635',
            'Vancouver BC': 'CA-BC',  # Canada
            'Montreal QC': 'CA-QC'
        }

        keywords = ['NBA', 'NBA expansion', 'Seattle NBA', 'Las Vegas NBA', 'professional basketball']

        try:
            pytrends = TrendReq(hl='en-US', tz=360)

            results = []

            for city, geo_code in list(expansion_cities.items())[:5]:  # Sample cities
                print(f"  - Analyzing: {city}")

                try:
                    # Get interest for this specific geo location
                    pytrends.build_payload(['NBA'], timeframe='today 12-m', geo=geo_code.split('-')[0])

                    regional = pytrends.interest_by_region(resolution='CITY', inc_low_vol=True)

                    if not regional.empty:
                        # Get the specific city's interest
                        city_name = city.split()[0]  # Extract city name
                        matching_rows = regional[regional.index.str.contains(city_name, case=False, na=False)]

                        if not matching_rows.empty:
                            interest_score = matching_rows['NBA'].values[0]
                            results.append({
                                'City': city,
                                'NBA_Search_Interest': interest_score,
                                'Geo_Code': geo_code
                            })

                    time.sleep(self.delay)

                except Exception as e:
                    print(f"    [WARNING] Could not get data for {city}: {e}")
                    results.append({
                        'City': city,
                        'NBA_Search_Interest': 0,
                        'Geo_Code': geo_code
                    })

            if results:
                df = pd.DataFrame(results)
                print(f"[OK] Analyzed {len(df)} expansion cities")
                return df

        except Exception as e:
            print(f"[ERROR] {e}")

        return self.create_expansion_trends_template()

    def create_expansion_trends_template(self):
        """
        Template for expansion city search trends
        """
        expansion_cities = [
            'Seattle WA', 'Las Vegas NV', 'Kansas City MO', 'Louisville KY',
            'San Diego CA', 'Pittsburgh PA', 'Nashville TN', 'Austin TX',
            'Vancouver BC', 'Montreal QC', 'Baltimore MD', 'St. Louis MO'
        ]

        template = {
            'City': expansion_cities,
            'NBA_Search_Interest': [0] * len(expansion_cities),
            'NBA_Expansion_Search': [0] * len(expansion_cities),
            'Local_Team_Search': [0] * len(expansion_cities),
            'Basketball_Interest_Index': [0] * len(expansion_cities),
            'Data_Source': ['Google Trends - Manual Entry'] * len(expansion_cities)
        }

        return pd.DataFrame(template)

    def create_social_media_detailed_template(self):
        """
        Detailed social media template with growth metrics
        """
        print(f"\n[3/5] Creating social media detailed template...")

        top_players = [
            'LeBron James', 'Stephen Curry', 'Kevin Durant', 'Giannis Antetokounmpo',
            'Luka Doncic', 'Jayson Tatum', 'Damian Lillard', 'Joel Embiid',
            'Nikola Jokic', 'Anthony Edwards', 'Ja Morant', 'Devin Booker',
            'Trae Young', 'Donovan Mitchell', 'Jimmy Butler', 'Kawhi Leonard',
            'Paul George', 'Anthony Davis', 'James Harden', 'Russell Westbrook'
        ]

        template = {
            'Player': top_players,
            'Instagram_Followers': [0] * len(top_players),
            'Instagram_30Day_Growth': [0] * len(top_players),
            'Instagram_Engagement_Rate': [0.0] * len(top_players),
            'Twitter_Followers': [0] * len(top_players),
            'Twitter_30Day_Growth': [0] * len(top_players),
            'Twitter_Engagement_Rate': [0.0] * len(top_players),
            'TikTok_Followers': [0] * len(top_players),
            'YouTube_Subscribers': [0] * len(top_players),
            'Total_Social_Reach': [0] * len(top_players),
            'Growth_Momentum_Score': [0.0] * len(top_players),
            'Data_Source': ['Social Blade / Manual Entry'] * len(top_players)
        }

        df = pd.DataFrame(template)

        print(f"[OK] Created template for {len(top_players)} players")
        print("\n[INSTRUCTIONS]:")
        print("  1. Visit Social Blade: https://socialblade.com/")
        print("  2. Search for each player's accounts")
        print("  3. Record follower counts and 30-day growth")
        print("  4. Calculate Growth_Momentum_Score = (30Day_Growth / Total_Followers) * 100")

        return df

    def create_team_social_media_template(self):
        """
        Team-level social media template
        """
        print(f"\n[4/5] Creating team social media template...")

        nba_teams = [
            'Los Angeles Lakers', 'Golden State Warriors', 'Boston Celtics',
            'New York Knicks', 'Chicago Bulls', 'Miami Heat',
            'Brooklyn Nets', 'Dallas Mavericks', 'Phoenix Suns',
            'Philadelphia 76ers', 'Toronto Raptors', 'Milwaukee Bucks',
            'Denver Nuggets', 'Cleveland Cavaliers', 'Portland Trail Blazers',
            'Houston Rockets', 'Sacramento Kings', 'San Antonio Spurs',
            'Washington Wizards', 'Atlanta Hawks', 'Utah Jazz',
            'Indiana Pacers', 'Orlando Magic', 'Charlotte Hornets',
            'Oklahoma City Thunder', 'Detroit Pistons', 'Minnesota Timberwolves',
            'New Orleans Pelicans', 'Memphis Grizzlies', 'LA Clippers'
        ]

        template = {
            'Team': nba_teams,
            'Instagram_Followers': [0] * 30,
            'Twitter_Followers': [0] * 30,
            'Facebook_Followers': [0] * 30,
            'TikTok_Followers': [0] * 30,
            'Total_Social_Reach': [0] * 30,
            'Monthly_Growth_Rate': [0.0] * 30,
            'Average_Attendance': [0] * 30,
            'Ticket_Revenue_Millions': [0] * 30,
            'Local_TV_Rating': [0.0] * 30,
            'Data_Source': ['Manual Entry Required'] * 30
        }

        df = pd.DataFrame(template)

        print(f"[OK] Created template for all 30 NBA teams")

        return df

    def get_msa_demographic_data(self):
        """
        Get Metropolitan Statistical Area demographic data for expansion analysis
        """
        print(f"\n[5/5] Compiling MSA demographic data...")

        # Comprehensive expansion candidate cities
        msa_data = {
            'City': [
                'Seattle', 'Las Vegas', 'Kansas City', 'San Diego', 'Pittsburgh',
                'Nashville', 'Austin', 'Louisville', 'Baltimore', 'St. Louis',
                'Vancouver', 'Montreal', 'Columbus', 'Virginia Beach', 'Cincinnati',
                'Los Angeles', 'New York', 'Chicago', 'Boston', 'San Francisco',
                'Dallas', 'Houston', 'Miami', 'Phoenix', 'Philadelphia'
            ],
            'State': [
                'WA', 'NV', 'MO', 'CA', 'PA',
                'TN', 'TX', 'KY', 'MD', 'MO',
                'BC', 'QC', 'OH', 'VA', 'OH',
                'CA', 'NY', 'IL', 'MA', 'CA',
                'TX', 'TX', 'FL', 'AZ', 'PA'
            ],
            'MSA_Population': [
                4010000, 2227000, 2192000, 3298000, 2370000,
                1989000, 2295000, 1397000, 2844000, 2820000,
                2632000, 4220000, 2138000, 1799000, 2256000,
                13200000, 19216000, 9618000, 4873000, 4749000,
                7637000, 7122000, 6138000, 4845000, 6102000
            ],
            'City_Population': [
                733000, 641000, 495000, 1386000, 303000,
                689000, 961000, 633000, 585000, 301000,
                675000, 1762000, 905000, 450000, 309000,
                3900000, 8336000, 2746000, 692000, 873000,
                1343000, 2304000, 442000, 1608000, 1584000
            ],
            'Median_Income': [
                93500, 64200, 59700, 88000, 65500,
                64100, 80100, 59600, 76000, 59600,
                79500, 62500, 62000, 75000, 60500,
                71000, 72000, 68000, 85000, 112000,
                68000, 65000, 61000, 65000, 71000
            ],
            'GDP_Per_Capita': [
                102000, 65000, 72000, 78000, 73000,
                76000, 70000, 68000, 82000, 75000,
                58000, 54000, 69000, 63000, 71000,
                78000, 94000, 79000, 98000, 124000,
                83000, 77000, 69000, 63000, 88000
            ],
            'Current_NBA_Team': [
                'None', 'None', 'None', 'None', 'None',
                'None', 'None', 'None', 'None', 'None',
                'None', 'None', 'None', 'None', 'None',
                'Lakers/Clippers', 'Knicks/Nets', 'Bulls', 'Celtics', 'Warriors',
                'Mavericks', 'Rockets', 'Heat', 'Suns', '76ers'
            ],
            'Existing_Pro_Sports_Teams': [
                4, 2, 3, 1, 4,
                4, 1, 1, 3, 3,
                5, 5, 2, 0, 3,
                8, 9, 5, 4, 5,
                4, 4, 4, 4, 4
            ],
            'Arena_Ready': [
                'Yes', 'Yes', 'Partial', 'Yes', 'Yes',
                'Partial', 'No', 'Yes', 'Partial', 'Yes',
                'Yes', 'Yes', 'Partial', 'No', 'Partial',
                'Yes', 'Yes', 'Yes', 'Yes', 'Yes',
                'Yes', 'Yes', 'Yes', 'Yes', 'Yes'
            ]
        }

        df = pd.DataFrame(msa_data)

        # Calculate market potential score
        df['Market_Potential_Score'] = (
            (df['MSA_Population'] / 1000000) * 0.4 +  # Population weight
            (df['GDP_Per_Capita'] / 10000) * 0.3 +    # Wealth weight
            (5 - df['Existing_Pro_Sports_Teams']) * 0.2 +  # Competition (inverse)
            (df['Arena_Ready'] == 'Yes').astype(int) * 0.1  # Infrastructure
        )

        df = df.sort_values('Market_Potential_Score', ascending=False)

        print(f"[OK] Compiled data for {len(df)} cities/metros")
        print(f"    Top expansion candidates by Market Potential Score:")
        top_5 = df[df['Current_NBA_Team'] == 'None'].head(5)
        for idx, row in top_5.iterrows():
            print(f"      {row['City']}, {row['State']}: {row['Market_Potential_Score']:.2f}")

        return df

    def collect_all_social_data(self):
        """
        Main collection method
        """
        print("="*70)
        print("SOCIAL INFLUENCE & MARKET DATA COLLECTION")
        print("="*70)

        os.makedirs('data', exist_ok=True)

        # Google Trends by city
        expansion_keywords = ['NBA', 'NBA expansion', 'Seattle NBA', 'Las Vegas NBA']
        trends_city = self.get_expansion_city_trends()

        filepath = 'data/3_google_trends_expansion_cities.csv'
        trends_city.to_csv(filepath, index=False)
        print(f"\n[SAVED] {filepath}")

        # Player social media template
        player_social = self.create_social_media_detailed_template()
        filepath = 'data/3_player_social_media_detailed.csv'
        player_social.to_csv(filepath, index=False)
        print(f"[SAVED] {filepath}")

        # Team social media template
        team_social = self.create_team_social_media_template()
        filepath = 'data/3_team_social_media_detailed.csv'
        team_social.to_csv(filepath, index=False)
        print(f"[SAVED] {filepath}")

        # MSA demographic data
        msa_data = self.get_msa_demographic_data()
        filepath = 'data/3_msa_demographic_data.csv'
        msa_data.to_csv(filepath, index=False)
        print(f"[SAVED] {filepath}")

        print("\n" + "="*70)
        print("[SUCCESS] Social influence data collection complete")
        print("="*70)

        print("\n[DATA COLLECTED]:")
        print(f"  - Expansion city trends: {len(trends_city)} cities")
        print(f"  - Player social media template: {len(player_social)} players")
        print(f"  - Team social media template: {len(team_social)} teams")
        print(f"  - MSA demographic data: {len(msa_data)} metro areas")

        print("\n[KEY METRICS FOR EXPANSION ANALYSIS]:")
        print("  - MSA Population (market size)")
        print("  - GDP Per Capita (purchasing power)")
        print("  - Existing Pro Sports Teams (competition level)")
        print("  - Arena Ready status (infrastructure)")
        print("  - Market Potential Score (composite metric)")

if __name__ == "__main__":
    collector = SocialInfluenceCollector()
    collector.collect_all_social_data()
