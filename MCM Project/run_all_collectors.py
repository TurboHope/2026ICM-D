"""
Master Script - Run All Data Collectors
Executes all data collection scripts in sequence
"""

import os
import sys
from datetime import datetime

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def main():
    print_header("MCM PROJECT - COMPLETE DATA COLLECTION PIPELINE")
    print(f"\nStarted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Track success/failure
    results = []

    # 1. Core Performance Data
    print_header("STEP 1: CORE PERFORMANCE DATA")
    try:
        from data_collection import BasketballDataCollector
        collector1 = BasketballDataCollector()
        collector1.collect_all_data()
        results.append(("Core Performance Data", "[OK] Success"))
    except Exception as e:
        print(f"[ERROR] {e}")
        results.append(("Core Performance Data", f"[FAILED]: {e}"))

    # 2. Lineup Data (Critical for Network Analysis)
    print_header("STEP 2: LINEUP DATA (Network Analysis)")
    try:
        from lineup_data_collector import LineupDataCollector
        collector2 = LineupDataCollector()
        collector2.collect_all_lineup_data(season='2023-24')
        results.append(("Lineup Data", "[OK] Success"))
    except Exception as e:
        print(f"[ERROR] {e}")
        results.append(("Lineup Data", f"[FAILED]: {e}"))

    # 3. Social Media & Soft Data
    print_header("STEP 3: SOCIAL MEDIA & SOFT DATA")
    try:
        from social_media_collector import SocialMediaCollector
        collector3 = SocialMediaCollector()
        collector3.collect_all_social_data()
        results.append(("Social Media Data", "[OK] Success"))
    except Exception as e:
        print(f"[ERROR] {e}")
        results.append(("Social Media Data", f"[FAILED]: {e}"))

    # Summary
    print_header("COLLECTION SUMMARY")
    for task, status in results:
        print(f"  {task:<30} {status}")

    print(f"\n\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    print("\n" + "="*70)
    print("All data saved in ./data/ directory")
    print("="*70)

    # List all files
    if os.path.exists('data'):
        files = [f for f in os.listdir('data') if f.endswith('.csv')]
        print(f"\nTotal CSV files: {len(files)}\n")

        print("Section 1 - Performance Data:")
        for f in sorted([x for x in files if x.startswith('1_')]):
            print(f"  [OK] {f}")

        print("\nSection 2 - Financial Data:")
        for f in sorted([x for x in files if x.startswith('2_')]):
            print(f"  [OK] {f}")

        print("\nSection 3 - Soft Data:")
        for f in sorted([x for x in files if x.startswith('3_')]):
            print(f"  [OK] {f}")

    print("\n" + "="*70)
    print("[NEXT STEPS:]")
    print("="*70)
    print("  1. Review template files and fill in manual data where needed")
    print("  2. Check '1_lineup_network_edges.csv' for network analysis")
    print("  3. For financial data, visit Spotrac.com and Forbes manually")
    print("  4. For social media, consider Social Blade or manual collection")
    print("  5. Merge datasets using player names as keys")
    print("\n")

if __name__ == "__main__":
    main()
