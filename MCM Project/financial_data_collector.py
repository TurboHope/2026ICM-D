"""
Financial Data Collector
Scrapes salary data, team valuations, and merchandise sales
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import os
import json

class FinancialDataCollector:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.delay = 3

    def scrape_spotrac_salaries(self, year=2024):
        """
        Scrape Spotrac for comprehensive player salary data
        """
        print(f"\n[1/3] Scraping Spotrac salary data ({year})...")

        url = f"https://www.spotrac.com/nba/rankings/{year}/cap-hit/"

        try:
            time.sleep(self.delay)
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Try to parse the table
                tables = pd.read_html(response.text)

                if tables:
                    df = tables[0]

                    # Clean up column names
                    if 'Player' in df.columns:
                        # Expected columns: Rank, Player, Team, Cap Hit, etc.
                        print(f"[OK] Found salary data for {len(df)} players")
                        print(f"    Columns: {', '.join(df.columns[:8])}")

                        return df
                    else:
                        print("[WARNING] Could not identify player column")
                        print(f"    Available columns: {', '.join(df.columns[:5])}")

                        # Try alternative parsing
                        return df
                else:
                    print("[WARNING] No tables found")

            else:
                print(f"[ERROR] HTTP {response.status_code}")

            # Alternative: Try the cap page
            print("\n[INFO] Trying alternative Spotrac URL...")
            url_alt = f"https://www.spotrac.com/nba/rankings/"

            time.sleep(self.delay)
            response = requests.get(url_alt, headers=self.headers)

            if response.status_code == 200:
                tables = pd.read_html(response.text)
                if tables:
                    df = tables[0]
                    print(f"[OK] Alternative URL worked - {len(df)} entries")
                    return df

            return pd.DataFrame()

        except Exception as e:
            print(f"[ERROR] {e}")
            print("[TIP] Spotrac may require JavaScript. Consider manual export or Selenium.")
            return pd.DataFrame()

    def create_spotrac_manual_template(self):
        """
        Create detailed template for manual Spotrac data entry
        """
        print("\n[INFO] Creating Spotrac manual entry template...")

        # Top players template with structure
        top_players = [
            'Stephen Curry', 'LeBron James', 'Kevin Durant', 'Giannis Antetokounmpo',
            'Damian Lillard', 'Joel Embiid', 'Nikola Jokic', 'Luka Doncic',
            'Jayson Tatum', 'Bradley Beal', 'Paul George', 'Kawhi Leonard',
            'Jimmy Butler', 'Rudy Gobert', 'Karl-Anthony Towns', 'Anthony Davis',
            'Devin Booker', 'Trae Young', 'Donovan Mitchell', 'Zach LaVine'
        ]

        template = {
            'Player': top_players,
            'Team': [''] * len(top_players),
            'Annual_Salary_2024': [0] * len(top_players),
            'Total_Contract_Value': [0] * len(top_players),
            'Contract_Length_Years': [0] * len(top_players),
            'Guaranteed_Money': [0] * len(top_players),
            'Free_Agency_Year': [0] * len(top_players),
            'Cap_Hit_Percent': [0.0] * len(top_players),
            'Data_Source': ['Spotrac.com - Manual Entry Required'] * len(top_players)
        }

        df = pd.DataFrame(template)

        print(f"[OK] Created template for top {len(top_players)} players")
        print("\n[INSTRUCTIONS]:")
        print("  1. Visit: https://www.spotrac.com/nba/rankings/")
        print("  2. Export or copy the salary table")
        print("  3. Fill in this template with actual values")
        print("  4. Key fields: Annual_Salary_2024, Total_Contract_Value, Free_Agency_Year")

        return df

    def scrape_forbes_valuations(self):
        """
        Attempt to scrape Forbes NBA team valuations
        Note: Forbes often requires subscription or has anti-scraping measures
        """
        print("\n[2/3] Attempting Forbes team valuations...")

        url = "https://www.forbes.com/nba-valuations/list/"

        try:
            time.sleep(self.delay)
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Forbes may use JavaScript to load data
                # Try to find JSON data in script tags
                scripts = soup.find_all('script', type='application/ld+json')

                for script in scripts:
                    try:
                        data = json.loads(script.string)
                        print("[INFO] Found JSON data in page")
                        # Process if it contains team data
                    except:
                        pass

                # Try table parsing
                tables = pd.read_html(response.text)
                if tables:
                    print(f"[OK] Found {len(tables)} tables")
                    return tables[0]

            print(f"[WARNING] Forbes requires manual collection (HTTP {response.status_code})")

        except Exception as e:
            print(f"[ERROR] {e}")

        return self.create_forbes_manual_template()

    def create_forbes_manual_template(self):
        """
        Create Forbes valuation template with latest known data structure
        """
        print("\n[INFO] Creating Forbes manual entry template...")

        nba_teams = [
            'Golden State Warriors', 'New York Knicks', 'Los Angeles Lakers',
            'Boston Celtics', 'Los Angeles Clippers', 'Chicago Bulls',
            'Brooklyn Nets', 'Houston Rockets', 'Dallas Mavericks',
            'Toronto Raptors', 'Philadelphia 76ers', 'Miami Heat',
            'Phoenix Suns', 'Milwaukee Bucks', 'Denver Nuggets',
            'Cleveland Cavaliers', 'Portland Trail Blazers', 'Sacramento Kings',
            'San Antonio Spurs', 'Washington Wizards', 'Atlanta Hawks',
            'Utah Jazz', 'Indiana Pacers', 'Orlando Magic',
            'Charlotte Hornets', 'Oklahoma City Thunder', 'Detroit Pistons',
            'Minnesota Timberwolves', 'New Orleans Pelicans', 'Memphis Grizzlies'
        ]

        template = {
            'Rank': list(range(1, 31)),
            'Team': nba_teams,
            'Current_Value_Millions': [0] * 30,
            'One_Year_Value_Change_Percent': [0.0] * 30,
            'Revenue_Millions': [0] * 30,
            'Operating_Income_Millions': [0] * 30,
            'Owner': [''] * 30,
            'Year': [2024] * 30,
            'Data_Source': ['Forbes - Manual Entry Required'] * 30
        }

        df = pd.DataFrame(template)

        print(f"[OK] Created template for all 30 NBA teams")
        print("\n[INSTRUCTIONS]:")
        print("  1. Visit: https://www.forbes.com/nba-valuations/")
        print("  2. Note: May require Forbes subscription")
        print("  3. Key fields: Current_Value, Revenue, Operating_Income")
        print("  4. Latest Forbes NBA valuations typically published in October")

        return df

    def scrape_merchandise_sales(self):
        """
        Attempt to scrape NBA store jersey sales rankings
        """
        print("\n[3/3] Attempting NBA merchandise sales data...")

        # NBA Store top sellers
        url = "https://store.nba.com/top-sellers/x-463133+z-94499947-3163182119"

        try:
            time.sleep(self.delay)
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Try to find product listings
                products = soup.find_all(class_='product-card')

                if products:
                    sales_data = []
                    for i, product in enumerate(products[:15], 1):
                        # Try to extract player name
                        title = product.find(class_='product-card-title')
                        if title:
                            sales_data.append({
                                'Rank': i,
                                'Item': title.get_text(strip=True),
                                'Source': 'NBA Store'
                            })

                    if sales_data:
                        df = pd.DataFrame(sales_data)
                        print(f"[OK] Found top {len(df)} merchandise items")
                        return df

            print("[WARNING] NBA Store requires manual collection")

        except Exception as e:
            print(f"[ERROR] {e}")

        return self.create_merchandise_template()

    def create_merchandise_template(self):
        """
        Create merchandise sales template
        """
        print("\n[INFO] Creating merchandise sales template...")

        # Based on typical top sellers
        top_sellers = [
            'LeBron James', 'Stephen Curry', 'Giannis Antetokounmpo',
            'Luka Doncic', 'Jayson Tatum', 'Kevin Durant',
            'Damian Lillard', 'Joel Embiid', 'Nikola Jokic',
            'Anthony Edwards', 'Devin Booker', 'Ja Morant',
            'Trae Young', 'Donovan Mitchell', 'Jimmy Butler'
        ]

        template = {
            'Rank': list(range(1, 16)),
            'Player': top_sellers,
            'Team': [''] * 15,
            'Jersey_Sales_Rank': list(range(1, 16)),
            'Estimated_Units_Sold': [0] * 15,
            'Merchandise_Category': ['Jersey'] * 15,
            'Data_Source': ['NBA Store - Manual Entry Required'] * 15
        }

        df = pd.DataFrame(template)

        print(f"[OK] Created template for top 15 players")
        print("\n[INSTRUCTIONS]:")
        print("  1. Visit: https://store.nba.com/top-sellers/")
        print("  2. Or search for NBA merchandise sales reports")
        print("  3. Rankings change frequently - check recent data")

        return df

    def collect_all_financial_data(self, year=2024):
        """
        Main collection method
        """
        print("="*70)
        print("FINANCIAL DATA COLLECTION")
        print("="*70)

        os.makedirs('data', exist_ok=True)

        # Spotrac salaries
        salaries = self.scrape_spotrac_salaries(year)
        if salaries.empty:
            salaries = self.create_spotrac_manual_template()

        filepath = 'data/2_player_salaries_complete.csv'
        salaries.to_csv(filepath, index=False)
        print(f"\n[SAVED] {filepath}")

        # Forbes valuations
        valuations = self.scrape_forbes_valuations()
        filepath = 'data/2_team_valuations_forbes.csv'
        valuations.to_csv(filepath, index=False)
        print(f"[SAVED] {filepath}")

        # Merchandise sales
        merchandise = self.scrape_merchandise_sales()
        filepath = 'data/2_merchandise_sales.csv'
        merchandise.to_csv(filepath, index=False)
        print(f"[SAVED] {filepath}")

        print("\n" + "="*70)
        print("[SUCCESS] Financial data collection complete")
        print("="*70)

        print("\n[DATA COLLECTED]:")
        print(f"  - Player salaries: {len(salaries)} entries")
        print(f"  - Team valuations: {len(valuations)} teams")
        print(f"  - Merchandise rankings: {len(merchandise)} items")

        print("\n[NOTE]:")
        print("  Some data requires manual entry due to website restrictions.")
        print("  Template files created with proper structure.")
        print("  Fill in templates with data from source websites.")

if __name__ == "__main__":
    collector = FinancialDataCollector()
    collector.collect_all_financial_data(year=2024)
