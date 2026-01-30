# Output Files Explained

## Section 1: Performance Data Files

### 📊 **1_player_basic_stats.csv** (41 KB, 572 players)

**What it is:** Traditional basketball statistics for every NBA player in the 2023-24 season.

**Columns:**
- `Player` - Player name
- `Team` - Team abbreviation (e.g., LAL, GSW, BOS)
- `Games_Played` - Number of games played
- `Minutes` - Average minutes per game
- `Points` - Average points per game
- `Rebounds` - Average rebounds per game
- `Assists` - Average assists per game
- `Steals` - Average steals per game
- `Blocks` - Average blocks per game
- `Turnovers` - Average turnovers per game
- `FG_Pct` - Field goal percentage (shooting accuracy)
- `FG3_Pct` - 3-point percentage
- `FT_Pct` - Free throw percentage
- `Plus_Minus` - Point differential when player is on court

**Example row:**
```
Aaron Gordon, DEN, 73 games, 31.5 min, 13.9 pts, 6.5 reb, 3.5 ast, 0.8 stl, 0.6 blk
```

**Use for:**
- Player performance comparisons
- Identifying top scorers, rebounders, etc.
- Basic statistical analysis
- Filtering players by position or team

---

### 📈 **1_player_advanced_stats_nba_api.csv** (58 KB, 572 players)

**What it is:** Advanced analytics that go beyond traditional stats - measures efficiency and impact.

**Key Columns Explained:**
- `OFF_RATING` - Offensive Rating: Points produced per 100 possessions (higher = better offense)
- `DEF_RATING` - Defensive Rating: Points allowed per 100 possessions (lower = better defense)
- `NET_RATING` - Net Rating: Offensive - Defensive rating (point differential per 100 possessions)
- `TS_PCT` - True Shooting %: Shooting efficiency including 2s, 3s, and free throws
- `USG_PCT` - Usage %: Percentage of team plays used by player when on court
- `AST_PCT` - Assist %: Percentage of teammate field goals the player assisted
- `REB_PCT` - Rebound %: Percentage of available rebounds grabbed
- `PIE` - Player Impact Estimate: Overall contribution (0-1 scale)
- `PACE` - Pace: Possessions per 48 minutes (game tempo)

**Example:**
```
Aaron Gordon: OFF_RATING=120.5, DEF_RATING=112.3, NET_RATING=8.2
This means: When Gordon plays, his team scores 120.5 points per 100 possessions
and allows 112.3, for a net +8.2 advantage
```

**Use for:**
- Identifying efficient players (high TS%, positive NET_RATING)
- Finding undervalued players (good NET_RATING but lower salary)
- Understanding player roles (high USG% = primary option)
- Efficiency vs. volume analysis

---

### 🏀 **1_lineup_5player_stats.csv** (269 KB, 2000 lineups)

**What it is:** Performance data for specific 5-player combinations when they're on the court together.

**Columns:**
- `Lineup_Players` - Names of all 5 players (e.g., "Player1 - Player2 - Player3 - Player4 - Player5")
- `Team` - Team abbreviation
- `Games` - Number of games this lineup played together
- `Minutes` - Total minutes this exact lineup played together
- `Plus_Minus` - Cumulative point differential for this lineup
- `Player_1` through `Player_5` - Individual player names (parsed for analysis)

**Example:**
```
Lineup: K. Caldwell-Pope - A. Gordon - N. Jokic - J. Murray - M. Porter Jr.
Team: DEN (Denver Nuggets)
Games: 48
Minutes: 958.4 (about 20 min/game)
Plus_Minus: +282 (they outscored opponents by 282 points in those minutes)
```

**This tells you:** This Denver starting 5 is EXTREMELY effective - they dominate when playing together.

**Use for:**
- Finding which player combinations work best
- Identifying team chemistry
- Predicting optimal lineups
- Understanding coaching strategies (which 5-player groups get most minutes)

---

### 🔗 **1_lineup_network_edges.csv** (135 KB, 2902 connections) ⭐ MOST IMPORTANT

**What it is:** A network graph edge list showing player-to-player connections based on time played together.

**Structure:**
- Each row = one edge (connection) between two players
- Shows how well players perform when paired

**Columns:**
- `Player_A` - First player
- `Player_B` - Second player
- `Team` - Team abbreviation
- `Minutes_Together` - Total minutes these two players were on court together
- `Net_Rating` - Average point differential per 100 possessions when both play

**Example:**
```
Player_A: N. Jokic
Player_B: K. Caldwell-Pope
Team: DEN
Minutes_Together: 2014 minutes
Net_Rating: +28.6

Translation: When Jokic and Caldwell-Pope play together, Denver is
incredibly dominant, outscoring opponents by 28.6 points per 100 possessions.
```

**Network Analysis Concepts:**

1. **Edge Weight** = `Minutes_Together`
   - Thicker edges = players who share the court more
   - Reveals coaching preferences and lineup stability

2. **Edge Value** = `Net_Rating`
   - Positive = effective partnership
   - Negative = struggle when paired
   - High positive = elite chemistry

3. **Node (Player) Importance:**
   - **High degree** (many connections) = versatile player who pairs well with many teammates
   - **High betweenness centrality** = "bridge" player connecting different lineup groups
   - **High eigenvector centrality** = connected to other important players

**Use for:**
- Building network graphs (nodes = players, edges = partnerships)
- Finding "hub" players (high centrality = key to team success)
- Identifying player chemistry (high Net_Rating partnerships)
- Predicting untested lineup performance
- Trade analysis (how would removing a player affect network?)
- Optimal team composition

**Example Analysis Questions:**
- Who are the 5 most central players in the league? (Network hubs)
- Which player pairs have the best chemistry? (Highest Net_Rating)
- If LeBron James retires, how does it fragment the Lakers' network?
- Can we predict the Net_Rating of a lineup that's never played together?

---

### 👥 **1_lineup_2player_stats.csv** (599 KB, 2000 combinations)

**What it is:** Detailed statistics for every 2-player combination (more detailed than network edges).

**Columns:** (50+ columns with extensive stats)
- `GROUP_NAME` - The two players (e.g., "D. Sabonis - K. Murray")
- `TEAM_ABBREVIATION` - Team
- `GP` - Games played together
- `MIN` - Total minutes together
- `W` / `L` - Wins/Losses when both play
- `FGM`, `FGA`, `FG_PCT` - Field goal stats when both on court
- `FG3M`, `FG3A`, `FG3_PCT` - Three-point stats
- `PTS` - Total points scored when both play
- `PLUS_MINUS` - Point differential
- Plus many more advanced stats

**Difference from network edges:**
- Network edges: Simplified (just Minutes + Net_Rating) for graph analysis
- This file: Complete game statistics for the duo

**Use for:**
- Detailed analysis of specific player pairs
- Understanding how a duo plays (offense-heavy? defensive?)
- Win-loss records for specific combinations
- More granular than network edges, but harder to visualize

---

## Section 2: Financial Data Files

### 💰 **2_team_valuations_template.csv** (332 bytes, TEMPLATE ONLY)

**What it is:** A template/structure for entering team financial data.

**Columns:**
- `Team` - Team name
- `Valuation_Millions` - Team worth (in millions of dollars)
- `Revenue_Millions` - Annual revenue
- `Operating_Income_Millions` - Annual profit/loss
- `Year` - Data year
- `Source` - Where data came from

**Current Status:** Empty template (filled with zeros)

**Action Required:**
Fill in data from Forbes "Most Valuable Sports Teams" list:
- Lakers valuation: ~$6,000 million
- Warriors valuation: ~$7,000 million
- Visit: https://www.forbes.com/nba-valuations/

**Use for (once filled):**
- Correlating team value with performance
- Revenue vs. salary analysis
- Market size impact on valuations
- Expansion team financial projections

---

## Section 3: Soft Data Files

### 🏙️ **3_city_market_data.csv** (458 bytes, 10 cities)

**What it is:** Demographic and market information for major NBA cities.

**Columns:**
- `City` - City name
- `State` - State abbreviation
- `Population` - City population
- `Metro_Population` - Metropolitan area population (larger region)
- `GDP_Billions` - Regional GDP (currently empty - needs filling)
- `NBA_Team` - Team(s) in that city

**Example:**
```
Los Angeles: 3.9M city population, 13.2M metro population, Lakers/Clippers
New York: 8.3M city population, 19.2M metro population, Knicks/Nets
```

**Use for:**
- Expansion team location analysis (which cities could support a team?)
- Market size vs. team revenue correlation
- Geographic distribution of teams
- Identifying underserved large markets
- Fan base potential estimation

**Cities included:**
Los Angeles, New York, Chicago, Boston, San Francisco, Dallas, Houston, Miami, Phoenix, Philadelphia

**Analysis Ideas:**
- Compare metro population to team revenue
- Identify large cities without NBA teams
- Calculate "NBA team per capita" ratios
- Optimal geographic distribution for new teams

---

## How Files Work Together

### For Network Analysis:
1. **Start:** `1_lineup_network_edges.csv` (build graph)
2. **Add node attributes:** Join with `1_player_basic_stats.csv` (add player stats to nodes)
3. **Analyze:** Calculate centrality, communities, etc.

### For Player Value Analysis:
1. **Merge:** `1_player_basic_stats.csv` + `1_player_advanced_stats_nba_api.csv`
2. **Add:** Salary data (from Spotrac - manual collection needed)
3. **Calculate:** Value per dollar (WS / Salary, PER / Salary, etc.)

### For Market Analysis:
1. **Start:** `3_city_market_data.csv`
2. **Add:** `2_team_valuations_template.csv` (once filled)
3. **Add:** Google Trends data (popularity by region)
4. **Analyze:** Best cities for expansion

### For Comprehensive Team Analysis:
1. **Team performance:** Aggregate player stats by team
2. **Team chemistry:** Network metrics for each team
3. **Team value:** From valuations template
4. **Team market:** From city data
5. **Result:** Complete team profiles

---

## Quick Reference

| File | Size | Rows | Best For |
|------|------|------|----------|
| `1_player_basic_stats.csv` | 41 KB | 572 | Player comparisons, traditional stats |
| `1_player_advanced_stats_nba_api.csv` | 58 KB | 572 | Efficiency, advanced metrics |
| `1_lineup_5player_stats.csv` | 269 KB | 2000 | Lineup effectiveness, coaching patterns |
| `1_lineup_network_edges.csv` | 135 KB | 2902 | **Network analysis, player chemistry** ⭐ |
| `1_lineup_2player_stats.csv` | 599 KB | 2000 | Detailed duo statistics |
| `2_team_valuations_template.csv` | 332 B | 5 | Team finances (needs manual filling) |
| `3_city_market_data.csv` | 458 B | 10 | Expansion analysis, market sizing |

---

## Example: Complete Analysis Workflow

**Question:** "Who are the most valuable players in the NBA?"

**Step 1:** Load player stats
```python
import pandas as pd

basic = pd.read_csv('1_player_basic_stats.csv')
advanced = pd.read_csv('1_player_advanced_stats_nba_api.csv')

# Merge on player name
players = pd.merge(basic, advanced,
                   left_on='Player',
                   right_on='PLAYER_NAME')
```

**Step 2:** Add network centrality
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

# Add to player dataframe
players['Centrality'] = players['Player'].map(centrality)
```

**Step 3:** Calculate composite value score
```python
# Normalize and combine metrics
players['Value_Score'] = (
    players['Points'] * 0.3 +           # Scoring
    players['NET_RATING'] * 0.3 +       # Overall impact
    players['Centrality'] * 100 * 0.2 + # Team importance
    players['PIE'] * 100 * 0.2          # General contribution
)

# Top 10 most valuable
top_10 = players.nlargest(10, 'Value_Score')[
    ['Player', 'Team', 'Points', 'NET_RATING', 'Centrality', 'Value_Score']
]
```

**Step 4:** Add salary (once collected)
```python
# After manually collecting salary data
salaries = pd.read_csv('2_player_salaries.csv')
players = pd.merge(players, salaries, on='Player')

# Calculate value per dollar
players['Value_Per_Million'] = players['Value_Score'] / (players['Salary'] / 1_000_000)

# Find bargain players
bargains = players.nlargest(10, 'Value_Per_Million')
```

This gives you:
- Most valuable players overall
- Best value-for-money players
- Network analysis of team chemistry
- Ready for MCM modeling!
