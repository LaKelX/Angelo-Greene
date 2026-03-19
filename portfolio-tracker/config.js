/**
 * LaKel Portfolio Configuration
 *
 * UPDATE THIS FILE to change your portfolio signals.
 *
 * Signal Types:
 *   "green"  = BUY  (strong conviction, entry point)
 *   "yellow" = HOLD (maintain position, don't add)
 *   "red"    = SELL/AVOID (exit or stay away)
 *
 * Action Types:
 *   "buy"   = Active buy signal
 *   "hold"  = Maintain current position
 *   "sell"  = Exit position
 *   "watch" = On radar, waiting for entry
 */

const PORTFOLIO_CONFIG = {
    // Last updated timestamp
    lastUpdated: "2026-02-22T18:00:00Z",

    // =============================================
    // CURRENT HOLDINGS
    // Stocks you currently own
    // =============================================
    holdings: [
        {
            ticker: "ASX",
            name: "ASE Technology",
            sector: "Semis",
            signal: "yellow",
            action: "hold",
            note: "Wait for NVDA Feb 25"
        },
        {
            ticker: "AMSC",
            name: "American Superconductor",
            sector: "Grid Tech",
            signal: "yellow",
            action: "hold",
            note: "Microsoft interest, superconductors"
        }
    ],

    // =============================================
    // WATCHLIST
    // Stocks you're tracking for potential entry
    // =============================================
    watchlist: [
        {
            ticker: "VRT",
            name: "Vertiv Holdings",
            sector: "Power",
            signal: "yellow",
            action: "watch",
            note: "ATH, wait for $115-120 pullback"
        },
        {
            ticker: "ASML",
            name: "ASML Holding",
            sector: "Semis",
            signal: "yellow",
            action: "watch",
            note: "EUV monopoly, wait for weakness"
        },
        {
            ticker: "MP",
            name: "MP Materials",
            sector: "Materials",
            signal: "yellow",
            action: "watch",
            note: "Only US rare earth, $18-20 entry"
        },
        {
            ticker: "AVAV",
            name: "AeroVironment",
            sector: "Defense",
            signal: "yellow",
            action: "watch",
            note: "If Iran talks fail Thursday"
        }
    ],

    // =============================================
    // BUY OPPORTUNITIES
    // Active buy signals
    // =============================================
    buyOpportunities: [
        {
            ticker: "LEU",
            name: "Centrus Energy",
            sector: "Nuclear",
            signal: "green",
            action: "buy",
            note: "$900M DOE contract, HALEU monopoly",
            pulse: true
        },
        {
            ticker: "DDOG",
            name: "Datadog",
            sector: "Cloud",
            signal: "green",
            action: "buy",
            note: "RSI 16.9, extremely oversold",
            pulse: true
        },
        {
            ticker: "CCJ",
            name: "Cameco",
            sector: "Uranium",
            signal: "green",
            action: "buy",
            note: "Top miner, Westinghouse stake"
        }
    ],

    // =============================================
    // RECENTLY EXITED
    // Stocks you've sold (for reference)
    // =============================================
    recentlyExited: [
        {
            ticker: "PWR",
            name: "Quanta Services",
            sector: "Grid",
            signal: "red",
            action: "sell",
            note: "Sold - overbought after earnings"
        },
        {
            ticker: "PPTA",
            name: "Perpetua Resources",
            sector: "Materials",
            signal: "red",
            action: "sell",
            note: "Sold - position closed"
        }
    ]
};

// Export for use in tracker.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PORTFOLIO_CONFIG;
}
