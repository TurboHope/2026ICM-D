============================================================
LINEUP DATA COLLECTION - FOR NETWORK ANALYSIS
============================================================

[LOADING] Fetching lineup data for 2023-24...
   (Filtering lineups with >= 10 minutes together)
[ERROR] Error fetching lineup data: Length mismatch: Expected axis has 5 elements, new values have 10 elements

[LOADING] Fetching 2-player combination data...
[OK] Collected 2000 2-player combinations
[OK] Saved to data\1_lineup_2player_stats.csv

============================================================
✅ LINEUP DATA COLLECTION COMPLETE
============================================================

[TIP] Usage for Network Analysis:
   • Use '1_lineup_network_edges.csv' to build player interaction network
   • Edge weight = Minutes_Together
   • Edge value = Net_Rating (performance when paired)
   • Can identify key players (high centrality) and effective combinations
