/**
 * LaKel Portfolio Tracker
 * Renders portfolio signals from config.js
 */

document.addEventListener('DOMContentLoaded', function() {
    initTracker();
});

function initTracker() {
    // Update timestamp
    updateTimestamp();

    // Render all sections
    renderStockList('holdingsList', PORTFOLIO_CONFIG.holdings);
    renderStockList('watchList', PORTFOLIO_CONFIG.watchlist);
    renderStockList('buyList', PORTFOLIO_CONFIG.buyOpportunities);
}

function updateTimestamp() {
    const el = document.getElementById('lastUpdated');
    if (el && PORTFOLIO_CONFIG.lastUpdated) {
        const date = new Date(PORTFOLIO_CONFIG.lastUpdated);
        const options = {
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        };
        el.textContent = `Updated: ${date.toLocaleDateString('en-US', options)}`;
    }
}

function renderStockList(containerId, stocks) {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (!stocks || stocks.length === 0) {
        container.innerHTML = '<div class="empty-state">No stocks</div>';
        return;
    }

    container.innerHTML = stocks.map(stock => createStockItem(stock)).join('');
}

function createStockItem(stock) {
    const pulseClass = stock.pulse ? ' pulse' : '';
    const signalClass = stock.signal || 'yellow';
    const actionClass = stock.action || 'hold';

    return `
        <div class="stock-item" data-ticker="${stock.ticker}" title="${stock.note || ''}">
            <div class="stock-signal">
                <span class="signal-dot ${signalClass}${pulseClass}"></span>
            </div>
            <div class="stock-info">
                <div class="stock-ticker">${stock.ticker}</div>
                <div class="stock-name">${stock.name}</div>
                ${stock.sector ? `<div class="stock-sector">${stock.sector}</div>` : ''}
            </div>
            <div class="stock-action ${actionClass}">${getActionLabel(stock.action)}</div>
        </div>
    `;
}

function getActionLabel(action) {
    const labels = {
        'buy': 'BUY',
        'hold': 'HOLD',
        'sell': 'SOLD',
        'watch': 'WATCH',
        'avoid': 'AVOID'
    };
    return labels[action] || action.toUpperCase();
}

// Optional: Add click handler for stock details
document.addEventListener('click', function(e) {
    const stockItem = e.target.closest('.stock-item');
    if (stockItem) {
        const ticker = stockItem.dataset.ticker;
        const note = stockItem.getAttribute('title');
        if (note) {
            // Could expand to show more details
            console.log(`${ticker}: ${note}`);
        }
    }
});

// Optional: Auto-refresh every 5 minutes
// setInterval(function() {
//     location.reload();
// }, 5 * 60 * 1000);
