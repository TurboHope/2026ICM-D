# MCM Project - Basketball Data Collection System

Complete data collection pipeline for NBA/WNBA analysis with performance, financial, and social media data.

## 📋 Overview

This system collects data in **three main sections**:

### 1. Core Performance Data
- Basic stats: PTS, REB, AST, STL, BLK, TOV
- Advanced stats: PER, WS, BPM, USG%, TS%
- **Lineup data**: Net rating for 5-player combinations (critical for network analysis)

### 2. Financial & Business Data
- Player salaries and contract details
- Team valuations and revenue
- Salary cap information

### 3. Soft Data & External Variables
- Google Trends (search popularity)
- Social media following and engagement
- City demographics and market data

---

## 🚀 Quick Start

### Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the complete data collection:
```bash
python run_all_collectors.py
```

3. All data will be saved to `./data/` directory in CSV format

---

## 📁 Output Files

### Section 1: Performance Data (Prefix: `1_`)
- `1_player_basic_stats.csv` - Basic per-game stats
- `1_player_advanced_stats_nba_api.csv` - Advanced metrics from NBA API
- `1_player_advanced_stats_bbref.csv` - PER, WS, BPM from Basketball Reference
- `1_lineup_5player_stats.csv` - 5-player lineup combinations with net ratings
- `1_lineup_2player_stats.csv` - 2-player combinations
- **`1_lineup_network_edges.csv`** ⭐ - Network edge list for player interactions

### Section 2: Financial Data (Prefix: `2_`)
- `2_player_salaries.csv` - Player salary data from Spotrac
- `2_team_valuations_template.csv` - Template for Forbes team valuation data

### Section 3: Soft Data (Prefix: `3_`)
- `3_google_trends_teams.csv` - Google search trends for teams
- `3_google_trends_players.csv` - Google search trends for players
- `3_regional_interest.csv` - Regional/city-level search interest
- `3_social_media_players_template.csv` - Template for player social media stats
- `3_social_media_teams_template.csv` - Template for team social media stats
- `3_city_market_data.csv` - City demographics and NBA team presence

---

## 🔧 Individual Scripts

Run scripts separately if needed:

```bash
# Core performance data
python data_collection.py

# Lineup data (for network analysis)
python lineup_data_collector.py

# Social media & trends
python social_media_collector.py
```

---

## 📊 Data Sources

### Automated Collection
✅ **NBA.com/stats** (via nba_api)
- Official NBA statistics
- Lineup data
- Player tracking metrics

✅ **Basketball-Reference.com**
- Advanced stats (PER, WS, BPM)
- Historical data
- Note: Respects rate limiting

✅ **Google Trends** (via pytrends)
- Search popularity over time
- Regional interest by city
- Comparative trends

### Manual Collection Required
⚠️ **Spotrac.com** - Player salaries (automated script provided, may need verification)

⚠️ **Forbes** - Team valuations (requires manual entry from annual reports)

⚠️ **Social Media APIs**
- Instagram: Requires Meta Graph API access
- Twitter: Requires Twitter API v2 credentials
- Alternative: Use Social Blade or manual collection

---

## 🕸️ Network Analysis - Lineup Data

The most critical file for network analysis is:
### `1_lineup_network_edges.csv`

**Structure:**
```
Player_A, Player_B, Team, Minutes_Together, Net_Rating
```

**Usage:**
- Build a graph where nodes = players, edges = time played together
- Edge weight = Minutes_Together
- Edge attribute = Net_Rating (performance when paired)
- Identify key players using centrality metrics
- Find optimal player combinations

**Example Analysis:**
```python
import pandas as pd
import networkx as nx

# Load edge list
edges = pd.read_csv('data/1_lineup_network_edges.csv')

# Create network
G = nx.Graph()
for _, row in edges.iterrows():
    G.add_edge(row['Player_A'], row['Player_B'],
               weight=row['Minutes_Together'],
               net_rating=row['Net_Rating'])

# Find most central players
centrality = nx.betweenness_centrality(G, weight='weight')
```

---

## ⚙️ Configuration

### Adjust Season
Edit the scripts to change the season:
```python
collector.collect_all_data(season='2022-23')  # Change season here
```

### Adjust Rate Limiting
In each collector class, modify:
```python
self.delay = 2  # Seconds between requests
```

### Filter Lineup Data
Adjust minimum minutes threshold:
```python
collector.get_lineup_stats(min_minutes=20)  # Only lineups with 20+ min
```

---

## 📝 Data Notes

### Performance Data
- All stats are per-game unless noted
- Advanced metrics use NBA's official calculations
- Lineup data requires minimum minutes to reduce noise

### Financial Data
- Salary data is for the current season
- Team valuations are annual (typically March releases from Forbes)
- Includes salary cap space calculations

### Soft Data
- Google Trends scores are relative (0-100 scale)
- Social media templates need manual filling or API integration
- City data includes metropolitan area populations

---

## 🔒 Ethical Considerations

✅ **Respects robots.txt** - All scraping follows site rules

✅ **Rate limiting** - 2+ second delays between requests

✅ **Official APIs first** - Uses nba_api (official) before scraping

✅ **Attribution** - Data sources are documented

⚠️ **Terms of Service** - Review ToS for Basketball-Reference and Spotrac before extensive use

⚠️ **API Keys** - Social media data requires proper authentication

---

## 🐛 Troubleshooting

### "Connection Error"
- Check internet connection
- Increase `self.delay` for rate limiting
- Some sites may block automated requests

### "Module not found: nba_api"
```bash
pip install nba-api
```

### "Empty DataFrame"
- API may be temporarily down
- Check if season parameter is valid
- Verify data source is accessible

### Google Trends Rate Limiting
- Reduce number of keywords per request
- Increase delay between requests
- Google Trends has daily rate limits

---

## 📚 Additional Resources

### Documentation
- [nba_api Documentation](https://github.com/swar/nba_api)
- [Basketball-Reference](https://www.basketball-reference.com/)
- [pytrends Documentation](https://pypi.org/project/pytrends/)

### Data Glossary
- **PER**: Player Efficiency Rating (per-minute performance)
- **WS**: Win Shares (contribution to team wins)
- **BPM**: Box Plus/Minus (points above average per 100 possessions)
- **TS%**: True Shooting Percentage (shooting efficiency)
- **USG%**: Usage Rate (% of team plays used)
- **Net Rating**: Point differential per 100 possessions

---

## 🎯 For MCM Competition

### Recommended Analysis Workflow

1. **Performance Analysis**
   - Use `1_player_advanced_stats_bbref.csv` for player efficiency
   - Merge with `1_player_basic_stats.csv` for complete profiles

2. **Network Analysis**
   - Use `1_lineup_network_edges.csv` to build player interaction networks
   - Identify synergies and optimal combinations

3. **Financial Modeling**
   - Combine salary data with performance metrics
   - Calculate value per dollar spent

4. **Market Analysis**
   - Use Google Trends and city data for expansion decisions
   - Correlate social media presence with revenue potential

5. **Integration**
   - Merge all datasets using player/team names as keys
   - Create comprehensive player/team profiles

### Key Metrics for Expansion Analysis
- Market size (population, GDP)
- Search interest (Google Trends)
- Proximity to existing teams
- Revenue potential (demographics + engagement)

---

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation
3. Verify data source accessibility

---

## 📄 License

This code is provided for educational purposes (MCM competition).
Please respect the terms of service of all data sources.

---

**Last Updated:** January 2026
**For:** MCM Mathematical Modeling Competition
