# LaKel Portfolio Tracker

A live portfolio signal tracker with red/yellow/green indicators.

## Files

| File | Purpose |
|------|---------|
| `index.html` | Full sidebar tracker |
| `widget.html` | Minimal embeddable widget |
| `style.css` | Full tracker styles |
| `config.js` | **YOUR PORTFOLIO DATA** |
| `tracker.js` | Rendering logic |

---

## Quick Start

### Option 1: Local Preview
```bash
cd portfolio-tracker
open index.html
```

### Option 2: GitHub Pages (Recommended)
1. Push this folder to your GitHub repo
2. Go to repo Settings → Pages
3. Set Source to "main" branch, folder "/portfolio-tracker"
4. Your tracker will be live at: `https://lakelx.github.io/LaKel/portfolio-tracker/`

---

## How to Update Your Portfolio

Edit `config.js` and change the stocks:

```javascript
holdings: [
    {
        ticker: "ASX",
        name: "ASE Technology",
        sector: "Semis",
        signal: "green",    // green, yellow, or red
        action: "buy",      // buy, hold, sell, watch
        note: "Your note here"
    }
]
```

### Signal Colors
- **green** = BUY (active buy signal, good entry)
- **yellow** = HOLD (maintain position, don't add)
- **red** = SELL/AVOID (exit or stay away)

### Action Labels
- **buy** = Active buy
- **hold** = Keep position
- **sell** = Exit
- **watch** = On radar

---

## Embedding on Another Page

### As an iframe:
```html
<iframe
    src="https://lakelx.github.io/LaKel/portfolio-tracker/widget.html"
    width="300"
    height="400"
    frameborder="0">
</iframe>
```

### As a sidebar:
```html
<div style="position: fixed; right: 0; top: 0; height: 100vh; width: 320px;">
    <iframe src="..." width="100%" height="100%" frameborder="0"></iframe>
</div>
```

---

## Customization

### Add pulsing effect to urgent buys:
```javascript
{
    ticker: "LEU",
    signal: "green",
    pulse: true  // adds pulsing glow
}
```

### Change colors in CSS:
```css
:root {
    --gold: #d4a855;
    --green: #3fb950;
    --yellow: #d29922;
    --red: #f85149;
}
```

---

## Deployment to GitHub Pages

```bash
cd /Users/angelogreene/Desktop/LaKel
git add portfolio-tracker/
git commit -m "Add portfolio tracker widget"
git push origin main
```

Then enable GitHub Pages in your repo settings.

---

*LaKel Capital - Hardware-Focused Investment Fund*
