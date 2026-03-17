#!/bin/bash
# EUDAIMON LIVE TRACKER - Startup Script

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         EUDAIMON LIVE TRACKER - STARTUP                       ║"
echo "╚═══════════════════════════════════════════════════════════════╝"

# Get script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8+"
    exit 1
fi

# Install dependencies if needed
echo "📦 Checking dependencies..."
pip3 install -q -r requirements.txt

# Start the tracker
echo "🚀 Starting Eudaimon Live Tracker..."
python3 tracker_daemon.py
