"""
Supplementary Data Collector
Collects injury history and media sentiment data
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import os

# Reddit API is optional
try:
    import praw
    PRAW_AVAILABLE = True
except ImportError:
    PRAW_AVAILABLE = False
    print("[INFO] praw not installed - Reddit API features disabled")

class SupplementaryDataCollector:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.delay = 3

    def scrape_injury_data(self, year=2024):
        """
        Scrape injury history from Pro Sports Transactions or Basketball-Reference
        """
        print(f"\n[1/3] Scraping injury history data...")

        # Try Basketball-Reference injury report
        url = f"https://www.basketball-reference.com/friv/injuries.fcgi"

        try:
            time.sleep(self.delay)
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                tables = pd.read_html(response.text)

                if tables:
                    df = tables[0]
                    print(f"[OK] Found current injury report with {len(df)} entries")

                    # Clean up
                    df.columns = ['Player', 'Team', 'Update', 'Description']

                    return df

            print("[WARNING] Could not access injury data")

        except Exception as e:
            print(f"[ERROR] {e}")

        return self.create_injury_template()

    def create_injury_template(self):
        """
        Create injury history template
        """
        print("\n[INFO] Creating injury history template...")

        # Key players who have had injury concerns
        players = [
            'Joel Embiid', 'Kawhi Leonard', 'Anthony Davis', 'Kyrie Irving',
            'Zion Williamson', 'Ben Simmons', 'Paul George', 'Klay Thompson',
            'Jamal Murray', 'Michael Porter Jr.', 'Kristaps Porzingis',
            'John Wall', 'Bradley Beal', 'Donovan Mitchell', 'Ja Morant'
        ]

        template = {
            'Player': players,
            'Team': [''] * len(players),
            'Games_Missed_2023': [0] * len(players),
            'Games_Missed_2022': [0] * len(players),
            'Games_Missed_2021': [0] * len(players),
            'Total_Games_Missed_3Yr': [0] * len(players),
            'Primary_Injury_Type': [''] * len(players),
            'Injury_Location': [''] * len(players),
            'Chronic_Injury': [False] * len(players),
            'Games_Possible': [246] * len(players),  # 3 seasons * 82 games
            'Availability_Rate': [0.0] * len(players),
            'Data_Source': ['Pro Sports Transactions - Manual Entry'] * len(players)
        }

        df = pd.DataFrame(template)

        print(f"[OK] Created template for {len(players)} injury-prone players")
        print("\n[INSTRUCTIONS]:")
        print("  1. Visit: https://www.prosportstransactions.com/basketball/")
        print("  2. Search for each player's transaction history")
        print("  3. Count games missed due to injury (IL, DNP, etc.)")
        print("  4. Calculate: Availability_Rate = (Games_Played / 246) * 100")

        return df

    def scrape_reddit_sentiment(self, subreddit='nba', keywords=None, limit=100):
        """
        Scrape Reddit r/nba for sentiment analysis
        Note: Requires Reddit API credentials
        """
        print(f"\n[2/3] Attempting Reddit sentiment collection...")

        if keywords is None:
            keywords = ['expansion', 'Seattle', 'Las Vegas', 'LeBron', 'Curry']

        try:
            # This requires Reddit API credentials
            # Users need to create an app at: https://www.reddit.com/prefs/apps

            print("[INFO] Reddit API requires authentication")
            print("      Create app at: https://www.reddit.com/prefs/apps")
            print("      Then configure credentials in code")

            # Placeholder for Reddit API
            # reddit = praw.Reddit(
            #     client_id='YOUR_CLIENT_ID',
            #     client_secret='YOUR_CLIENT_SECRET',
            #     user_agent='MCM_Project_Data_Collector'
            # )
            #
            # subreddit_obj = reddit.subreddit(subreddit)
            # posts = []
            #
            # for keyword in keywords:
            #     for submission in subreddit_obj.search(keyword, limit=limit):
            #         posts.append({
            #             'Keyword': keyword,
            #             'Title': submission.title,
            #             'Score': submission.score,
            #             'Comments': submission.num_comments,
            #             'Created': submission.created_utc,
            #             'URL': submission.url
            #         })
            #
            # if posts:
            #     df = pd.DataFrame(posts)
            #     print(f"[OK] Collected {len(df)} Reddit posts")
            #     return df

        except Exception as e:
            print(f"[ERROR] {e}")

        return self.create_reddit_sentiment_template()

    def create_reddit_sentiment_template(self):
        """
        Create Reddit sentiment template
        """
        print("\n[INFO] Creating Reddit sentiment template...")

        keywords = [
            'NBA expansion', 'Seattle NBA', 'Las Vegas NBA',
            'LeBron James', 'Stephen Curry', 'Nikola Jokic',
            'Lakers', 'Warriors', 'Celtics',
            'NBA playoffs', 'NBA Finals'
        ]

        template = {
            'Keyword': keywords,
            'Total_Posts_30d': [0] * len(keywords),
            'Total_Comments_30d': [0] * len(keywords),
            'Average_Upvotes': [0] * len(keywords),
            'Sentiment_Score': [0.0] * len(keywords),  # -1 to 1
            'Trending_Up': [False] * len(keywords),
            'Peak_Discussion_Date': [''] * len(keywords),
            'Data_Source': ['r/nba - Manual Collection'] * len(keywords)
        }

        df = pd.DataFrame(template)

        print(f"[OK] Created template for {len(keywords)} keywords")
        print("\n[INSTRUCTIONS]:")
        print("  1. Option A: Use Reddit API (requires app credentials)")
        print("  2. Option B: Manual search on r/nba")
        print("  3. Search each keyword and count posts/comments in last 30 days")
        print("  4. Estimate sentiment: Positive comments % - Negative comments %")

        return df

    def create_twitter_sentiment_template(self):
        """
        Create Twitter/X sentiment template
        """
        print(f"\n[3/3] Creating Twitter sentiment template...")

        topics = [
            'NBA Expansion',
            'LeBron James retirement',
            'Stephen Curry legacy',
            'Lakers championship odds',
            'Seattle NBA team',
            'Las Vegas NBA team',
            'NBA All-Star voting',
            'NBA trade deadline',
            'MVP race',
            'Rookie of the Year'
        ]

        template = {
            'Topic': topics,
            'Tweets_30d': [0] * len(topics),
            'Retweets_30d': [0] * len(topics),
            'Likes_30d': [0] * len(topics),
            'Mentions_30d': [0] * len(topics),
            'Sentiment_Score': [0.0] * len(topics),
            'Trending_Rank': [0] * len(topics),
            'Engagement_Rate': [0.0] * len(topics),
            'Data_Source': ['Twitter API / Manual'] * len(topics)
        }

        df = pd.DataFrame(template)

        print(f"[OK] Created template for {len(topics)} topics")
        print("\n[INSTRUCTIONS]:")
        print("  1. Option A: Twitter API v2 (requires developer account)")
        print("  2. Option B: Third-party tools like Brandwatch, Hootsuite")
        print("  3. Option C: Manual Twitter search and count engagement")
        print("  4. Track hashtags: #NBAExpansion, #SeattleNBA, #VegasNBA")

        return df

    def create_media_buzz_composite(self):
        """
        Create composite media buzz score template
        """
        print("\n[INFO] Creating composite media buzz template...")

        players = [
            'LeBron James', 'Stephen Curry', 'Giannis Antetokounmpo',
            'Luka Doncic', 'Nikola Jokic', 'Joel Embiid',
            'Kevin Durant', 'Damian Lillard', 'Jayson Tatum',
            'Anthony Edwards', 'Victor Wembanyama', 'Ja Morant'
        ]

        template = {
            'Player': players,
            'Reddit_Mentions': [0] * len(players),
            'Twitter_Mentions': [0] * len(players),
            'News_Articles_30d': [0] * len(players),
            'YouTube_Videos_30d': [0] * len(players),
            'Instagram_Posts_Tagged': [0] * len(players),
            'Media_Buzz_Score': [0] * len(players),  # Composite score
            'Controversy_Index': [0.0] * len(players),  # Negative attention %
            'Fan_Sentiment': ['Neutral'] * len(players),  # Positive/Neutral/Negative
            'Data_Source': ['Multi-platform - Manual'] * len(players)
        }

        df = pd.DataFrame(template)

        print(f"[OK] Created template for {len(players)} players")
        print("\n[CALCULATION]:")
        print("  Media_Buzz_Score = (")
        print("      Reddit_Mentions * 1 +")
        print("      Twitter_Mentions * 0.5 +")
        print("      News_Articles * 10 +")
        print("      YouTube_Videos * 5")
        print("  ) / 1000")

        return df

    def collect_all_supplementary_data(self):
        """
        Main collection method
        """
        print("="*70)
        print("SUPPLEMENTARY DATA COLLECTION")
        print("="*70)

        os.makedirs('data', exist_ok=True)

        # Injury data
        injuries = self.scrape_injury_data()
        filepath = 'data/4_injury_history.csv'
        injuries.to_csv(filepath, index=False)
        print(f"\n[SAVED] {filepath}")

        # Reddit sentiment
        reddit_data = self.scrape_reddit_sentiment()
        filepath = 'data/4_reddit_sentiment.csv'
        reddit_data.to_csv(filepath, index=False)
        print(f"[SAVED] {filepath}")

        # Twitter sentiment
        twitter_data = self.create_twitter_sentiment_template()
        filepath = 'data/4_twitter_sentiment.csv'
        twitter_data.to_csv(filepath, index=False)
        print(f"[SAVED] {filepath}")

        # Media buzz composite
        media_buzz = self.create_media_buzz_composite()
        filepath = 'data/4_media_buzz_composite.csv'
        media_buzz.to_csv(filepath, index=False)
        print(f"[SAVED] {filepath}")

        print("\n" + "="*70)
        print("[SUCCESS] Supplementary data collection complete")
        print("="*70)

        print("\n[DATA COLLECTED]:")
        print(f"  - Injury history: {len(injuries)} players")
        print(f"  - Reddit sentiment: {len(reddit_data)} keywords")
        print(f"  - Twitter sentiment: {len(twitter_data)} topics")
        print(f"  - Media buzz composite: {len(media_buzz)} players")

        print("\n[USE CASES]:")
        print("  - Injury history: Risk assessment for player value")
        print("  - Reddit/Twitter: Public opinion and market sentiment")
        print("  - Media buzz: Brand value and marketability")
        print("  - Composite scores: Overall influence metrics")

        print("\n[NOTE]:")
        print("  Social media APIs require authentication:")
        print("  - Reddit API: https://www.reddit.com/prefs/apps")
        print("  - Twitter API: https://developer.twitter.com/")
        print("  - Alternative: Manual data collection from websites")

if __name__ == "__main__":
    collector = SupplementaryDataCollector()
    collector.collect_all_supplementary_data()
