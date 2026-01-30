"""
Master Script - Enhanced Data Collection
Runs all 4 sections of data collection with advanced metrics
"""

import os
import sys
from datetime import datetime

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def main():
    print_header("MCM PROJECT - ENHANCED DATA COLLECTION")
    print(f"\nStarted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    results = []

    # SECTION 1: Advanced Performance Data
    print_header("SECTION 1: ADVANCED PERFORMANCE METRICS")
    print("Collecting: PER, Win Shares, BPM, VORP, Team Stats")

    try:
        from advanced_stats_collector import AdvancedStatsCollector
        collector = AdvancedStatsCollector()
        collector.collect_all_advanced_stats(year=2024)
        results.append(("Advanced Performance Data", "[OK] Success"))
    except Exception as e:
        print(f"[ERROR] {e}")
        results.append(("Advanced Performance Data", f"[FAILED]: {e}"))

    # SECTION 2: Financial Data
    print_header("SECTION 2: FINANCIAL & BUSINESS DATA")
    print("Collecting: Salaries, Team Valuations, Merchandise Sales")

    try:
        from financial_data_collector import FinancialDataCollector
        collector = FinancialDataCollector()
        collector.collect_all_financial_data(year=2024)
        results.append(("Financial Data", "[OK] Success"))
    except Exception as e:
        print(f"[ERROR] {e}")
        results.append(("Financial Data", f"[FAILED]: {e}"))

    # SECTION 3: Social Influence Data
    print_header("SECTION 3: SOCIAL INFLUENCE & MARKET DATA")
    print("Collecting: Social Media, Google Trends, MSA Demographics")

    try:
        from social_influence_collector import SocialInfluenceCollector
        collector = SocialInfluenceCollector()
        collector.collect_all_social_data()
        results.append(("Social Influence Data", "[OK] Success"))
    except Exception as e:
        print(f"[ERROR] {e}")
        results.append(("Social Influence Data", f"[FAILED]: {e}"))

    # SECTION 4: Supplementary Data
    print_header("SECTION 4: SUPPLEMENTARY DATA (Risk & Sentiment)")
    print("Collecting: Injury History, Media Sentiment")

    try:
        from supplementary_data_collector import SupplementaryDataCollector
        collector = SupplementaryDataCollector()
        collector.collect_all_supplementary_data()
        results.append(("Supplementary Data", "[OK] Success"))
    except Exception as e:
        print(f"[ERROR] {e}")
        results.append(("Supplementary Data", f"[FAILED]: {e}"))

    # Summary
    print_header("COLLECTION SUMMARY")
    for task, status in results:
        print(f"  {task:<35} {status}")

    print(f"\n\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # List all files
    print("\n" + "="*70)
    print("DATA FILES ORGANIZED BY SECTION")
    print("="*70)

    if os.path.exists('data'):
        files = sorted([f for f in os.listdir('data') if f.endswith('.csv')])

        sections = {
            '1': 'SECTION 1: Performance Metrics',
            '2': 'SECTION 2: Financial Data',
            '3': 'SECTION 3: Social Influence',
            '4': 'SECTION 4: Supplementary Data'
        }

        for prefix, section_name in sections.items():
            section_files = [f for f in files if f.startswith(f'{prefix}_')]
            if section_files:
                print(f"\n{section_name}:")
                for f in section_files:
                    file_path = os.path.join('data', f)
                    size = os.path.getsize(file_path) / 1024  # KB
                    print(f"  [OK] {f:<50} ({size:>6.1f} KB)")

    print("\n" + "="*70)
    print("[NEXT STEPS]")
    print("="*70)
    print("  1. Review files in ./data/ directory")
    print("  2. Fill in template files marked 'Manual Entry Required'")
    print("  3. For Basketball-Reference: Wait if rate-limited, retry later")
    print("  4. For social media: Consider API access or manual collection")
    print("  5. Run merge_datasets.py to combine all data")
    print("\n")

if __name__ == "__main__":
    main()
