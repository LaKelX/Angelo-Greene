import Cocoa

// ============================================
// CONFIGURATION - EDIT YOUR TICKERS HERE
// ============================================

let holdingTickers = ["ASX", "AMSC"]
let watchlistTickers = ["LEU", "DDOG", "CCJ", "VRT", "AVAV", "ASML", "MP"]

// Signal thresholds
let RSI_OVERSOLD: Double = 30.0      // Below = GREEN (BUY)
let RSI_OVERBOUGHT: Double = 70.0    // Above = RED (SELL/AVOID)
// Between = YELLOW (HOLD/WATCH)

// Refresh interval in seconds
let REFRESH_INTERVAL: TimeInterval = 300 // 5 minutes

// ============================================
// DATA MODELS
// ============================================

struct StockData {
    let ticker: String
    var price: Double = 0.0
    var change: Double = 0.0
    var changePercent: Double = 0.0
    var rsi: Double = 50.0
    var signal: Signal = .yellow

    var formattedPrice: String {
        return String(format: "$%.2f", price)
    }

    var formattedChange: String {
        let sign = changePercent >= 0 ? "+" : ""
        return String(format: "%@%.2f%%", sign, changePercent)
    }
}

enum Signal: String {
    case green = "🟢"
    case yellow = "🟡"
    case red = "🔴"

    static func fromRSI(_ rsi: Double) -> Signal {
        if rsi < RSI_OVERSOLD { return .green }
        if rsi > RSI_OVERBOUGHT { return .red }
        return .yellow
    }
}

// ============================================
// API FETCHER
// ============================================

class StockFetcher {
    static let shared = StockFetcher()

    // Using Yahoo Finance API (free, no key required)
    func fetchQuote(ticker: String, completion: @escaping (StockData?) -> Void) {
        let urlString = "https://query1.finance.yahoo.com/v8/finance/chart/\(ticker)?interval=1d&range=1mo"
        guard let url = URL(string: urlString) else {
            completion(nil)
            return
        }

        var request = URLRequest(url: url)
        request.setValue("Mozilla/5.0", forHTTPHeaderField: "User-Agent")

        URLSession.shared.dataTask(with: request) { data, response, error in
            guard let data = data, error == nil else {
                completion(nil)
                return
            }

            do {
                if let json = try JSONSerialization.jsonObject(with: data) as? [String: Any],
                   let chart = json["chart"] as? [String: Any],
                   let results = chart["result"] as? [[String: Any]],
                   let result = results.first,
                   let meta = result["meta"] as? [String: Any],
                   let indicators = result["indicators"] as? [String: Any],
                   let quotes = indicators["quote"] as? [[String: Any]],
                   let quote = quotes.first {

                    let currentPrice = meta["regularMarketPrice"] as? Double ?? 0.0
                    let previousClose = meta["chartPreviousClose"] as? Double ?? currentPrice
                    let change = currentPrice - previousClose
                    let changePercent = previousClose > 0 ? (change / previousClose) * 100 : 0

                    // Calculate RSI from closing prices
                    let closes = quote["close"] as? [Double?] ?? []
                    let validCloses = closes.compactMap { $0 }
                    let rsi = self.calculateRSI(prices: validCloses)

                    var stockData = StockData(ticker: ticker)
                    stockData.price = currentPrice
                    stockData.change = change
                    stockData.changePercent = changePercent
                    stockData.rsi = rsi
                    stockData.signal = Signal.fromRSI(rsi)

                    completion(stockData)
                    return
                }
            } catch {
                print("JSON parse error: \(error)")
            }
            completion(nil)
        }.resume()
    }

    // RSI Calculation (14-period)
    func calculateRSI(prices: [Double], period: Int = 14) -> Double {
        guard prices.count > period else { return 50.0 }

        var gains: [Double] = []
        var losses: [Double] = []

        for i in 1..<prices.count {
            let change = prices[i] - prices[i-1]
            if change > 0 {
                gains.append(change)
                losses.append(0)
            } else {
                gains.append(0)
                losses.append(abs(change))
            }
        }

        // Use last 'period' values
        let recentGains = Array(gains.suffix(period))
        let recentLosses = Array(losses.suffix(period))

        let avgGain = recentGains.reduce(0, +) / Double(period)
        let avgLoss = recentLosses.reduce(0, +) / Double(period)

        if avgLoss == 0 { return 100.0 }

        let rs = avgGain / avgLoss
        let rsi = 100.0 - (100.0 / (1.0 + rs))

        return rsi
    }
}

// ============================================
// MENU BAR APP
// ============================================

class AppDelegate: NSObject, NSApplicationDelegate {
    var statusItem: NSStatusItem!
    var refreshTimer: Timer?
    var holdings: [StockData] = []
    var watchlist: [StockData] = []
    var lastUpdate: Date = Date()

    func applicationDidFinishLaunching(_ notification: Notification) {
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)

        if let button = statusItem.button {
            button.title = "◈ LaKel ⏳"
        }

        // Initial fetch
        refreshData()

        // Auto-refresh timer
        refreshTimer = Timer.scheduledTimer(withTimeInterval: REFRESH_INTERVAL, repeats: true) { [weak self] _ in
            self?.refreshData()
        }
    }

    func refreshData() {
        DispatchQueue.main.async {
            if let button = self.statusItem.button {
                button.title = "◈ LaKel ⏳"
            }
        }

        let allTickers = holdingTickers + watchlistTickers
        let group = DispatchGroup()

        var newHoldings: [StockData] = []
        var newWatchlist: [StockData] = []

        for ticker in allTickers {
            group.enter()
            StockFetcher.shared.fetchQuote(ticker: ticker) { data in
                if let data = data {
                    if holdingTickers.contains(ticker) {
                        newHoldings.append(data)
                    } else {
                        newWatchlist.append(data)
                    }
                }
                group.leave()
            }
        }

        group.notify(queue: .main) { [weak self] in
            guard let self = self else { return }

            // Sort by ticker
            self.holdings = newHoldings.sorted { $0.ticker < $1.ticker }
            self.watchlist = newWatchlist.sorted { $0.ticker < $1.ticker }
            self.lastUpdate = Date()

            // Update menu bar title with buy signal count
            let buySignals = (self.holdings + self.watchlist).filter { $0.signal == .green }.count
            if buySignals > 0 {
                self.statusItem.button?.title = "◈ LaKel 🟢\(buySignals)"
            } else {
                self.statusItem.button?.title = "◈ LaKel"
            }

            self.setupMenu()
        }
    }

    func setupMenu() {
        let menu = NSMenu()

        // Header with last update time
        let formatter = DateFormatter()
        formatter.dateFormat = "h:mm a"
        let timeStr = formatter.string(from: lastUpdate)
        let header = NSMenuItem(title: "Last Update: \(timeStr)", action: nil, keyEquivalent: "")
        header.attributedTitle = NSAttributedString(string: "Last Update: \(timeStr)", attributes: [.foregroundColor: NSColor.secondaryLabelColor, .font: NSFont.systemFont(ofSize: 11)])
        menu.addItem(header)

        menu.addItem(NSMenuItem.separator())

        // Holdings Section
        addSectionHeader(menu: menu, title: "━━━ HOLDINGS ━━━")
        for stock in holdings {
            addStockItem(menu: menu, stock: stock, showPrice: true)
        }

        menu.addItem(NSMenuItem.separator())

        // Buy Signals (green RSI < 30)
        let buySignals = watchlist.filter { $0.signal == .green }
        if !buySignals.isEmpty {
            addSectionHeader(menu: menu, title: "━━━ BUY SIGNALS ━━━")
            for stock in buySignals {
                addStockItem(menu: menu, stock: stock, showPrice: true)
            }
            menu.addItem(NSMenuItem.separator())
        }

        // Watchlist
        let watchItems = watchlist.filter { $0.signal != .green }
        if !watchItems.isEmpty {
            addSectionHeader(menu: menu, title: "━━━ WATCHLIST ━━━")
            for stock in watchItems {
                addStockItem(menu: menu, stock: stock, showPrice: true)
            }
            menu.addItem(NSMenuItem.separator())
        }

        // Actions
        let refreshItem = NSMenuItem(title: "🔄 Refresh Now", action: #selector(refreshAction), keyEquivalent: "r")
        refreshItem.target = self
        menu.addItem(refreshItem)

        let quitItem = NSMenuItem(title: "Quit LaKel", action: #selector(NSApplication.terminate(_:)), keyEquivalent: "q")
        menu.addItem(quitItem)

        statusItem.menu = menu
    }

    func addSectionHeader(menu: NSMenu, title: String) {
        let item = NSMenuItem(title: title, action: nil, keyEquivalent: "")
        item.attributedTitle = NSAttributedString(string: title, attributes: [
            .foregroundColor: NSColor(red: 0.83, green: 0.66, blue: 0.33, alpha: 1.0),
            .font: NSFont.boldSystemFont(ofSize: 12)
        ])
        menu.addItem(item)
    }

    func addStockItem(menu: NSMenu, stock: StockData, showPrice: Bool) {
        let signal = stock.signal.rawValue
        let rsiStr = String(format: "RSI:%.0f", stock.rsi)

        var title = "\(signal) \(stock.ticker)"
        if showPrice {
            title += "  \(stock.formattedPrice)  \(stock.formattedChange)  (\(rsiStr))"
        }

        let item = NSMenuItem(title: title, action: nil, keyEquivalent: "")

        // Color based on change
        var color = NSColor.labelColor
        if stock.changePercent > 0 {
            color = NSColor(red: 0.25, green: 0.73, blue: 0.31, alpha: 1.0)
        } else if stock.changePercent < 0 {
            color = NSColor(red: 0.97, green: 0.32, blue: 0.29, alpha: 1.0)
        }

        item.attributedTitle = NSAttributedString(string: title, attributes: [
            .foregroundColor: color,
            .font: NSFont.monospacedSystemFont(ofSize: 12, weight: .regular)
        ])

        menu.addItem(item)
    }

    @objc func refreshAction() {
        refreshData()
    }
}

// ============================================
// LAUNCH
// ============================================

let app = NSApplication.shared
let delegate = AppDelegate()
app.delegate = delegate
app.setActivationPolicy(.accessory)
app.run()
