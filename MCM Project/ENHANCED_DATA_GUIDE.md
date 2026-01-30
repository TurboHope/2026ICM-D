# Enhanced Data Collection Guide

## Complete MCM Project Dataset - All 4 Sections

---

## 📊 SECTION 1: Performance Data (COMPLETE)

### ✅ Automated Collection - Ready to Use

#### **1_player_basic_stats.csv** (572 players)
**Source:** NBA Official API
**Status:** ✅ Complete

**Metrics Included:**
- Points (PTS), Rebounds (REB), Assists (AST)
- Steals (STL), Blocks (BLK), Turnovers (TOV)
- Field Goal % (FG%), 3-Point % (3P%), Free Throw % (FT%)
- Plus/Minus

**Use for:** Traditional player comparisons, scoring leaders, defensive stats

---

#### **1_player_advanced_stats_nba_api.csv** (572 players)
**Source:** NBA Official API
**Status:** ✅ Complete

**Advanced Metrics:**
- True Shooting % (TS%) - Overall shooting efficiency
- Usage Rate (USG%) - Percentage of team possessions used
- Offensive Rating (ORtg) - Points per 100 possessions
- Defensive Rating (DRtg) - Points allowed per 100 possessions
- Net Rating (NRtg) - ORtg - DRtg
- PIE (Player Impact Estimate)
- Pace, Assist %, Rebound %

**Use for:** Efficiency analysis, value metrics

---

#### **1_lineup_network_edges.csv** (2902 connections) ⭐
**Source:** NBA Official API
**Status:** ✅ Complete - YOUR MOST IMPORTANT FILE

**Contains:**
- Player-to-player connections (graph edges)
- Minutes played together
- Net Rating when paired

**Use for:**
- Network analysis (centrality, clustering)
- Player chemistry identification
- Optimal lineup prediction
- Trade impact simulation

---

### ⚠️ Manual Collection Needed

#### **Basketball-Reference Advanced Stats** (Blocked by 403)
**Target Metrics:**
- **PER** (Player Efficiency Rating) - Comprehensive efficiency score
- **Win Shares (WS)** - Offensive + Defensive win contribution
- **BPM** (Box Plus/Minus) - Point differential per 100 possessions
- **VORP** (Value Over Replacement Player) - Total value metric

**Manual Collection Options:**
1. **Option A:** Export from Basketball-Reference
   - Visit: https://www.basketball-reference.com/leagues/NBA_2024_advanced.html
   - Use browser "Save As CSV" or copy-paste table
   - Save as: `1_player_advanced_bbref.csv`

2. **Option B:** Use alternative data sources
   - NBA.com Advanced Stats (some overlap)
   - Stathead.com (paid subscription)

**Key Columns Needed:**
```
Player, Tm, PER, TS%, OWS, DWS, WS, WS/48, OBPM, DBPM, BPM, VORP
```

**Why These Matter:**
- **Win Shares:** Direct correlation with team wins (critical for expansion projections)
- **VORP:** Best single metric for overall player value
- **BPM:** Accounts for both offense and defense

---

#### **Team Performance Stats** (Not yet collected)
**Target Metrics:**
- Offensive Rating (ORtg) - Team points per 100 poss
- Defensive Rating (DRtg) - Points allowed per 100 poss
- Net Rating (NRtg) - Point differential
- Margin of Victory (MOV) - Average point differential
- Pace - Possessions per 48 minutes

**Manual Collection:**
Visit: https://www.basketball-reference.com/leagues/NBA_2024.html
Save as: `1_team_performance.csv`

**Format:**
```
Team, W, L, W/L%, MOV, ORtg, DRtg, NRtg, Pace
```

---

## 💰 SECTION 2: Financial Data (TEMPLATES CREATED)

### **2_player_salaries_complete.csv**
**Source:** Spotrac
**Status:** ⚠️ Template created - needs manual filling
**Records:** 20 top players (template)

**Fields to Fill:**
- `Annual_Salary_2024` - This year's salary
- `Total_Contract_Value` - Full contract worth
- `Contract_Length_Years` - Years remaining
- `Guaranteed_Money` - Guaranteed amount
- `Free_Agency_Year` - When contract expires
- `Cap_Hit_Percent` - % of team salary cap

**How to Collect:**
1. Visit: https://www.spotrac.com/nba/rankings/2024/cap-hit/
2. Export table or manually enter top 50-100 players
3. Focus on star players (>$30M annual salary)

**Why This Matters:**
- **Value Analysis:** Performance per dollar spent
- **Team Building:** Salary cap constraints
- **Market Value:** Predicting future contracts

---

### **2_team_valuations_forbes.csv**
**Source:** Forbes NBA Valuations
**Status:** ⚠️ Template created - needs manual filling
**Records:** All 30 teams (template)

**Fields to Fill:**
- `Current_Value_Millions` - Team valuation
- `Revenue_Millions` - Annual revenue
- `Operating_Income_Millions` - Annual profit
- `One_Year_Value_Change_Percent` - Growth rate
- `Owner` - Team owner name

**How to Collect:**
1. Visit: https://www.forbes.com/nba-valuations/ (may require subscription)
2. Forbes typically publishes in October each year
3. Alternative: Search for "Forbes NBA team valuations 2024"

**Recent Values (2023):**
- Golden State Warriors: ~$7.7B (highest)
- New York Knicks: ~$6.6B
- Los Angeles Lakers: ~$6.4B

**Why This Matters:**
- **Expansion Pricing:** What new teams might cost
- **Market Correlation:** Revenue vs. market size
- **Investment ROI:** Team value growth rates

---

### **2_merchandise_sales.csv**
**Source:** NBA Store
**Status:** ⚠️ Template created
**Records:** Top 15 players (template)

**Fields to Fill:**
- `Jersey_Sales_Rank` - Ranking (1-15+)
- `Estimated_Units_Sold` - If available
- `Merchandise_Category` - Jersey, shoes, etc.

**How to Collect:**
1. NBA Store: https://store.nba.com/top-sellers/
2. Or search for "NBA jersey sales rankings 2024"
3. Sports media often publishes quarterly rankings

**Typical Top Sellers:**
1. LeBron James
2. Stephen Curry
3. Giannis Antetokounmpo
4. Luka Doncic
5. Jayson Tatum

**Why This Matters:**
- **Brand Value:** Player marketability beyond performance
- **Revenue Generation:** Merchandise drives team revenue
- **Fan Engagement:** Sales correlate with popularity

---

## 📱 SECTION 3: Social Influence Data (PARTIALLY COMPLETE)

### ✅ Automated Collection - Ready to Use

#### **3_msa_demographic_data.csv**
**Source:** US Census / Canadian Census
**Status:** ✅ Complete
**Records:** 25 metro areas

**Metrics Included:**
- MSA Population (metro area total)
- City Population (city proper)
- Median Income
- GDP Per Capita
- Current NBA Team
- Existing Pro Sports Teams (total count)
- Arena Ready (Yes/Partial/No)
- **Market Potential Score** (calculated composite)

**Top Expansion Candidates:**
1. **Seattle, WA** - Market Score: 4.96
   - Population: 4M metro, No current NBA team
   - Strong sports culture (Seahawks, Mariners, Sounders)
   - Climate Pledge Arena ready

2. **San Diego, CA** - Market Score: 4.56
   - Population: 3.3M metro
   - Only 1 pro team (Padres)

3. **Baltimore, MD** - Market Score: 4.00
4. **St. Louis, MO** - Market Score: 3.88
5. **Austin, TX** - Market Score: 3.82

**Use for:**
- Expansion site selection
- Market size analysis
- Competition assessment (other pro sports)
- Infrastructure readiness

---

#### **3_google_trends_expansion_cities.csv**
**Source:** Google Trends
**Status:** ✅ Partial (2 cities collected, more possible)

**Metrics:**
- NBA Search Interest (0-100 scale)
- Geographic data by city

**How to Expand:**
1. Wait for Google rate limit to reset (24 hours)
2. Run: `python social_influence_collector.py`
3. Or manually search Google Trends for:
   - "NBA" in specific cities
   - "Seattle NBA expansion"
   - "Las Vegas NBA team"

---

### ⚠️ Manual Collection Needed

#### **3_player_social_media_detailed.csv**
**Status:** ⚠️ Template for 20 players
**Source:** Social Blade / Manual

**Fields to Fill:**
- `Instagram_Followers` - Total count
- `Instagram_30Day_Growth` - New followers in 30 days
- `Instagram_Engagement_Rate` - (Likes+Comments)/Followers %
- `Twitter_Followers`
- `Twitter_30Day_Growth`
- `TikTok_Followers`
- `YouTube_Subscribers`
- `Growth_Momentum_Score` - Calculate as: (30Day_Growth / Total_Followers) × 100

**How to Collect:**
1. **Option A:** Social Blade (recommended)
   - Visit: https://socialblade.com/
   - Search for each player
   - Record followers and 30-day stats

2. **Option B:** Manual platform checks
   - Instagram: View profile, check follower count
   - Twitter/X: Same process
   - Growth rates: Check again after 30 days

**Top Social Media Players (2024 estimates):**
- LeBron James: ~160M Instagram, ~53M Twitter
- Stephen Curry: ~53M Instagram, ~16M Twitter
- Giannis: ~16M Instagram, ~4M Twitter

**Why Growth Matters:**
- Static follower counts = past popularity
- Growth rate = current momentum and relevance
- High growth = increasing commercial value

---

#### **3_team_social_media_detailed.csv**
**Status:** ⚠️ Template for 30 teams

**Fields to Fill:**
- Instagram, Twitter, Facebook, TikTok followers
- Monthly growth rate
- Average attendance
- Ticket revenue (if available)
- Local TV ratings

**Top Team Accounts (estimates):**
- Lakers: ~22M Instagram
- Warriors: ~19M Instagram
- Bulls: ~9M Instagram

---

## 🔬 SECTION 4: Supplementary Data (TEMPLATES CREATED)

### **4_injury_history.csv**
**Source:** Pro Sports Transactions / Basketball-Reference
**Status:** ⚠️ Template for 15 players
**Records:** Focus on injury-prone stars

**Fields to Fill:**
- `Games_Missed_2023` - Last season
- `Games_Missed_2022` - 2 seasons ago
- `Games_Missed_2021` - 3 seasons ago
- `Total_Games_Missed_3Yr` - Sum of 3 years
- `Primary_Injury_Type` - Knee, ankle, back, etc.
- `Chronic_Injury` - Yes/No (recurring issue)
- `Availability_Rate` - (Games Played / 246) × 100

**How to Collect:**
1. Visit: https://www.prosportstransactions.com/basketball/
2. Search each player's name
3. Count IL (Injured List) transactions
4. Or use Basketball-Reference injury reports

**High-Risk Players to Track:**
- Joel Embiid (knee issues)
- Kawhi Leonard (knee management)
- Anthony Davis (various injuries)
- Zion Williamson (weight/foot)

**Why This Matters:**
- **Risk Assessment:** Player value adjusted for availability
- **Contract Negotiations:** Injury-prone = lower value
- **Lineup Reliability:** Can they be counted on?

**Calculation Example:**
```
Player: Joel Embiid
Games Missed 2023: 43
Games Missed 2022: 14
Games Missed 2021: 51
Total: 108 games missed out of 246 possible
Availability Rate: (138/246) × 100 = 56.1%
```

---

### **4_reddit_sentiment.csv**
**Source:** r/nba subreddit
**Status:** ⚠️ Template for 11 keywords

**Fields to Fill:**
- `Total_Posts_30d` - Posts mentioning keyword
- `Total_Comments_30d` - Total comments on those posts
- `Average_Upvotes` - Average post score
- `Sentiment_Score` - (-1 to +1) negative to positive
- `Trending_Up` - Yes/No (increasing mentions)

**How to Collect:**
1. **Option A:** Reddit API (requires setup)
   - Create app: https://www.reddit.com/prefs/apps
   - Install praw: `pip install praw`
   - Configure credentials in script

2. **Option B:** Manual Reddit search
   - Go to r/nba
   - Search each keyword
   - Filter by "Past Month"
   - Count posts and estimate sentiment

**Keywords to Track:**
- "NBA expansion"
- "Seattle NBA"
- "Las Vegas NBA"
- Player names (LeBron, Curry, etc.)

**Sentiment Estimation:**
- Read top 20 comments
- Count positive vs negative
- Score = (Positive% - Negative%) / 100

---

### **4_twitter_sentiment.csv**
**Source:** Twitter/X
**Status:** ⚠️ Template for 10 topics

**Fields to Fill:**
- `Tweets_30d` - Total tweets
- `Retweets_30d` - Total retweets
- `Likes_30d` - Total likes
- `Engagement_Rate` - (Retweets + Likes) / Tweets
- `Sentiment_Score`

**How to Collect:**
1. **Option A:** Twitter API v2 (requires developer account)
   - Apply: https://developer.twitter.com/
   - Can be expensive or time-consuming

2. **Option B:** Third-party analytics
   - Brandwatch, Hootsuite, Sprout Social
   - Usually paid services

3. **Option C:** Manual search
   - Search Twitter for hashtags
   - Estimate volume and sentiment

**Key Hashtags:**
- #NBAExpansion
- #SeattleNBA
- #VegasNBA
- #BringBackTheSonics

---

### **4_media_buzz_composite.csv**
**Source:** Multi-platform
**Status:** ⚠️ Template for 12 players

**Composite Metric Calculation:**
```
Media_Buzz_Score = (
    Reddit_Mentions × 1 +
    Twitter_Mentions × 0.5 +
    News_Articles × 10 +
    YouTube_Videos × 5
) / 1000
```

**Fields to Fill:**
- Reddit, Twitter, News, YouTube mention counts
- Controversy Index (% negative attention)
- Fan Sentiment (Positive/Neutral/Negative)

**Why This Matters:**
- **Brand Value:** Off-court worth
- **Marketability:** Commercial appeal
- **Media Draw:** Ticket sales driver

---

## 🎯 DATA COLLECTION PRIORITY GUIDE

### HIGH PRIORITY (Do First)
1. ✅ **Player basic & advanced stats** - COMPLETE
2. ✅ **Lineup network data** - COMPLETE
3. ⚠️ **Basketball-Reference advanced (WS, PER, BPM, VORP)** - Manual needed
4. ⚠️ **Player salaries (top 100)** - Template ready
5. ⚠️ **Team valuations** - Template ready

### MEDIUM PRIORITY
6. ⚠️ **Social media followers (top 20 players)** - Template ready
7. ⚠️ **MSA demographic data** - COMPLETE but can expand
8. ⚠️ **Injury history (key players)** - Template ready

### LOWER PRIORITY (Nice to Have)
9. ⚠️ **Merchandise sales** - Template ready
10. ⚠️ **Reddit/Twitter sentiment** - Templates ready
11. ⚠️ **Google Trends** - Partial, can expand

---

## 📋 QUICK START MANUAL COLLECTION

### 30-Minute Essential Data Collection

1. **Basketball-Reference Advanced (15 min)**
   - Visit: https://www.basketball-reference.com/leagues/NBA_2024_advanced.html
   - Export to CSV or copy table
   - Get: PER, WS, BPM, VORP for all players

2. **Spotrac Top 50 Salaries (10 min)**
   - Visit: https://www.spotrac.com/nba/rankings/
   - Copy salary data for top 50 players
   - Fill template: `2_player_salaries_complete.csv`

3. **Forbes Team Valuations (5 min)**
   - Search: "Forbes NBA team valuations 2024"
   - Find published list (usually free summary)
   - Fill template: `2_team_valuations_forbes.csv`

With just these 3 items, you'll have 80% of critical data!

---

## 💡 DATA INTEGRATION STRATEGY

### Step 1: Merge Performance Data
```python
import pandas as pd

# Load all performance files
basic = pd.read_csv('1_player_basic_stats.csv')
advanced_nba = pd.read_csv('1_player_advanced_stats_nba_api.csv')
advanced_bbref = pd.read_csv('1_player_advanced_bbref.csv')  # After manual collection

# Merge on player name
complete = basic.merge(advanced_nba, on='Player', how='left')
complete = complete.merge(advanced_bbref, on='Player', how='left')
```

### Step 2: Add Financial Data
```python
salaries = pd.read_csv('2_player_salaries_complete.csv')
complete = complete.merge(salaries, on='Player', how='left')

# Calculate value metrics
complete['Points_Per_Million'] = complete['Points'] / (complete['Annual_Salary_2024'] / 1e6)
complete['WS_Per_Million'] = complete['WS'] / (complete['Annual_Salary_2024'] / 1e6)
```

### Step 3: Add Network Metrics
```python
import networkx as nx

edges = pd.read_csv('1_lineup_network_edges.csv')
G = nx.Graph()

for _, row in edges.iterrows():
    G.add_edge(row['Player_A'], row['Player_B'],
               weight=row['Minutes_Together'],
               rating=row['Net_Rating'])

# Calculate centrality
centrality = nx.betweenness_centrality(G, weight='weight')
complete['Network_Centrality'] = complete['Player'].map(centrality)
```

---

## 🔧 TROUBLESHOOTING

### "403 Forbidden" Errors
- **Cause:** Websites blocking automated scraping
- **Solution:** Manual export or wait 24 hours and retry

### Google Trends Rate Limiting
- **Cause:** Too many requests
- **Solution:** Wait 24 hours or use VPN to reset IP

### Missing Player Names in Merge
- **Cause:** Name formatting differences
- **Solution:** Standardize names (remove periods, middle initials)

---

## 📊 EXPECTED FILE SIZES

| File | Expected Rows | Size |
|------|---------------|------|
| 1_player_basic_stats.csv | 572 | ~40 KB |
| 1_player_advanced_bbref.csv | 572 | ~50 KB |
| 1_lineup_network_edges.csv | 2902 | ~135 KB |
| 2_player_salaries_complete.csv | 100-500 | ~10-50 KB |
| 2_team_valuations_forbes.csv | 30 | ~2 KB |
| 3_msa_demographic_data.csv | 25 | ~2 KB |
| 4_injury_history.csv | 15-50 | ~5 KB |

---

## ✅ COMPLETION CHECKLIST

- [x] Player basic stats (572 players)
- [x] Player advanced stats from NBA API
- [x] Lineup network edges (2902 connections)
- [x] MSA demographic data (25 cities)
- [ ] Basketball-Reference advanced (WS, PER, BPM, VORP)
- [ ] Player salaries (top 100)
- [ ] Team valuations (30 teams)
- [ ] Social media followers (top 20 players)
- [ ] Injury history (15+ players)
- [ ] Merchandise sales (top 15)
- [ ] Google Trends expansion cities
- [ ] Reddit/Twitter sentiment

**Current Completion: ~45%**
**With 30-min manual collection: ~80%**
**Full completion (all templates filled): 100%**

---

Good luck with your MCM project! 🏀
