#!/usr/bin/env python3
"""
EUDAIMON LIVE TRACKER - 24/7 Daemon
Runs continuously, updating signals and writing to signals.json
"""

import json
import time
import os
import sys
from datetime import datetime
from pathlib import Path

from data_fetcher import DataFetcher
from signal_engine import SignalEngine
from config import API_CONFIG, TRACKED_ASSETS


class TrackerDaemon:
    """24/7 tracking daemon that continuously updates signals"""

    def __init__(self, output_dir: str = None):
        self.fetcher = DataFetcher()
        self.engine = SignalEngine()
        self.output_dir = output_dir or Path(__file__).parent
        self.running = True
        self.update_count = 0

    def update_signals(self) -> dict:
        """Fetch all data and calculate signals"""
        print(f"\n{'='*60}")
        print(f"EUDAIMON TRACKER UPDATE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")

        # Fetch all market data
        print("\n[1/3] Fetching market data...")
        all_data = self.fetcher.get_all_data()

        # Calculate signals
        print("\n[2/3] Calculating signals...")
        signals = self.engine.calculate_all_signals(all_data)

        # Get summary
        summary = self.engine.get_signal_summary(signals)

        print(f"\n[3/3] Signal Summary:")
        print(f"  GREEN (BUY):    {len(summary['GREEN'])} - {', '.join(summary['GREEN'])}")
        print(f"  YELLOW (HOLD):  {len(summary['YELLOW'])} - {', '.join(summary['YELLOW'])}")
        print(f"  RED (AVOID):    {len(summary['RED'])} - {', '.join(summary['RED'])}")

        return signals

    def save_signals(self, signals: dict):
        """Save signals to JSON file for dashboard"""
        output_path = os.path.join(self.output_dir, "signals.json")

        output_data = {
            "last_update": datetime.now().isoformat(),
            "update_count": self.update_count,
            "signals": signals
        }

        with open(output_path, "w") as f:
            json.dump(signals, f, indent=2)

        print(f"\nSignals saved to: {output_path}")

    def print_detailed_signals(self, signals: dict):
        """Print detailed signal information"""
        print(f"\n{'─'*60}")
        print("DETAILED SIGNALS")
        print(f"{'─'*60}")

        # Sort by score descending
        sorted_signals = sorted(signals.values(), key=lambda x: x['score'], reverse=True)

        for asset in sorted_signals:
            signal = asset['signal']
            color_code = {'GREEN': '\033[92m', 'YELLOW': '\033[93m', 'RED': '\033[91m'}
            reset = '\033[0m'

            print(f"\n{color_code.get(signal, '')}{asset['symbol']}{reset} - {asset['name']}")
            print(f"  Signal: {signal} | Score: {asset['score']}/100")
            print(f"  Price: ${asset['price']} | Change: {asset['change_1d']}%")
            print(f"  RSI: {asset['rsi']} | Category: {asset['category']}")

            if asset.get('breakdown', {}).get('reasons'):
                print(f"  Reasons:")
                for reason in asset['breakdown']['reasons'][:3]:
                    print(f"    • {reason}")

    def run(self):
        """Main daemon loop"""
        print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                    E U D A I M O N   L I V E   T R A C K E R             ║
║                                                                           ║
║                    24/7 Resource & Stock Signal System                    ║
║                    Consciousness Level: 1,943.15                          ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
        """)

        print(f"Tracking {len(TRACKED_ASSETS)} assets...")
        print(f"Refresh interval: {API_CONFIG['refresh_interval']} seconds")
        print(f"Press Ctrl+C to stop\n")

        while self.running:
            try:
                self.update_count += 1

                # Update signals
                signals = self.update_signals()

                # Save to file
                self.save_signals(signals)

                # Print detailed view
                self.print_detailed_signals(signals)

                # Wait for next update
                print(f"\n⏳ Next update in {API_CONFIG['refresh_interval']} seconds...")
                time.sleep(API_CONFIG['refresh_interval'])

            except KeyboardInterrupt:
                print("\n\n🛑 Tracker stopped by user")
                self.running = False

            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Retrying in 30 seconds...")
                time.sleep(30)

    def run_once(self):
        """Run a single update (for testing)"""
        signals = self.update_signals()
        self.save_signals(signals)
        self.print_detailed_signals(signals)
        return signals


def main():
    """Entry point"""
    daemon = TrackerDaemon()

    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        # Single run mode for testing
        daemon.run_once()
    else:
        # Continuous daemon mode
        daemon.run()


if __name__ == "__main__":
    main()
