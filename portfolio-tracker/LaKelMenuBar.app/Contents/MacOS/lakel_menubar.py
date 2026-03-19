#!/usr/bin/env python3
"""
LaKel Menu Bar Portfolio Tracker
Displays portfolio signals in macOS menu bar
"""

import rumps
import json
import os

# Portfolio Configuration - EDIT THIS TO UPDATE SIGNALS
PORTFOLIO = {
    "holdings": [
        {"ticker": "ASX", "name": "ASE Technology", "signal": "yellow", "action": "HOLD"},
        {"ticker": "AMSC", "name": "American Superconductor", "signal": "yellow", "action": "HOLD"},
    ],
    "buy": [
        {"ticker": "LEU", "name": "Centrus Energy", "signal": "green", "action": "BUY"},
        {"ticker": "DDOG", "name": "Datadog", "signal": "green", "action": "BUY"},
        {"ticker": "CCJ", "name": "Cameco", "signal": "green", "action": "BUY"},
    ],
    "watch": [
        {"ticker": "VRT", "name": "Vertiv", "signal": "yellow", "action": "WATCH"},
        {"ticker": "AVAV", "name": "AeroVironment", "signal": "yellow", "action": "WATCH"},
        {"ticker": "ASML", "name": "ASML Holding", "signal": "yellow", "action": "WATCH"},
        {"ticker": "MP", "name": "MP Materials", "signal": "yellow", "action": "WATCH"},
    ]
}

# Signal icons
SIGNALS = {
    "green": "🟢",
    "yellow": "🟡",
    "red": "🔴"
}

class LaKelMenuBar(rumps.App):
    def __init__(self):
        super(LaKelMenuBar, self).__init__("LaKel", title="◈ LaKel")
        self.build_menu()

    def build_menu(self):
        menu_items = []

        # Header
        menu_items.append(rumps.MenuItem("━━━ HOLDINGS ━━━", callback=None))
        for stock in PORTFOLIO["holdings"]:
            icon = SIGNALS.get(stock["signal"], "⚪")
            item = rumps.MenuItem(
                f"{icon} {stock['ticker']} - {stock['action']}",
                callback=None
            )
            menu_items.append(item)

        menu_items.append(rumps.separator)
        menu_items.append(rumps.MenuItem("━━━ BUY NOW ━━━", callback=None))
        for stock in PORTFOLIO["buy"]:
            icon = SIGNALS.get(stock["signal"], "⚪")
            item = rumps.MenuItem(
                f"{icon} {stock['ticker']} - {stock['name']}",
                callback=None
            )
            menu_items.append(item)

        menu_items.append(rumps.separator)
        menu_items.append(rumps.MenuItem("━━━ WATCHLIST ━━━", callback=None))
        for stock in PORTFOLIO["watch"]:
            icon = SIGNALS.get(stock["signal"], "⚪")
            item = rumps.MenuItem(
                f"{icon} {stock['ticker']} - {stock['action']}",
                callback=None
            )
            menu_items.append(item)

        menu_items.append(rumps.separator)
        menu_items.append(rumps.MenuItem("Refresh", callback=self.refresh))

        self.menu = menu_items

    @rumps.clicked("Refresh")
    def refresh(self, _):
        self.build_menu()
        rumps.notification("LaKel", "Portfolio Updated", "Signals refreshed")

if __name__ == "__main__":
    LaKelMenuBar().run()
