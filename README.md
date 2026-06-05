# 🇮🇳 India ESG & GHG Emissions Dashboard

> A beautiful, interactive web dashboard that visualizes India's greenhouse gas (GHG) emissions data from 2000 to 2024. Built with just **HTML + CSS + JavaScript** — no server needed, works right in your browser!

---

## 🚀 What Does This Dashboard Do?

If you're someone who cares about **climate change, sustainability, or just wants to understand India's carbon footprint**, this dashboard turns complex raw data into **beautiful, clickable charts and insights**.

### Here's what you can explore:

- **📊 Key Emissions Metrics** (5 KPI cards on top)
  - Total CO₂, Coal, Oil, Gas, Cement
  - See 24-year projections at a glance

- **📈 Interactive Line Chart — CO₂ Over Time**
  - Hover over the line to see exact values for each year
  - Toggle between different metrics like Coal, Oil, Gas, Cement
  - Turn on **annotations** to see important policy events

- **🥧 Donut Chart — Source Breakdown**
  - Visual split of where India's emissions come from
  - Coal dominates, but how much? See at a glance

- **📊 Stacked Area Chart — Emissions by Source**
  - Watch how different fuel sources grew/shrank over time
  - See Coal's massive dominance visually

- **📈 Total GHG vs CO₂ Only**
  - Compare total greenhouse gas (including Methane, N₂O) with just CO₂
  - Understand the bigger picture

- **🎯 Scope 1 / 2 / 3 Analysis**
  - **Scope 1**: Direct fossil fuel combustion (66% of total)
  - **Scope 2**: Purchased electricity & heat (23%)
  - **Scope 3**: Supply chain, logistics, cement processes (11%)

- **👤 Per Capita vs GDP Intensity**
  - Are we emitting more per person? Is GDP growing faster than emissions?
  - See the "decoupling" effect in action

- **📋 Raw Data Table**
  - See all 24 years of data in a human-readable table
  - Sort, filter, and search

- **📥 Download CSV**
  - Want the raw data for Excel/PowerBI? One click download

- **🔗 Correlation Matrix**
  - See how strongly different variables are related
  - Hover for exact Pearson correlation values

---

## 🎮 How to Use

### Option 1: Just Open It

1. **Double-click** `index.html` on your computer
2. It opens in your browser — that's it! No internet needed (except Google Fonts)

**OR visit the live version:**

```
https://your-github-username.github.io/India-ESG-GHG-Dashboard/
```

### Option 2: Deploy on GitHub Pages (Free!)

1. Fork or upload this repo to your GitHub
2. Go to **Settings → Pages**
3. Under "Source", select **Deploy from a branch → main → / (root)**
4. Click **Save** — your dashboard goes live in ~2 minutes!

---

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| **HTML5** | Structure & content |
| **CSS3** | Styling, layout, animations |
| **JavaScript** | Charts, interactivity, data processing |
| **Chart.js 4.4.1** | Beautiful, interactive charts |
| **Google Fonts** | Manrope + JetBrains Mono for typography |

**No frameworks, no build step, no server required!** Pure vanilla HTML/CSS/JS that works in any modern browser.

---

## 📊 Data Source

The data comes from **Our World in Data (OWID)** — a trusted, open-source dataset on global emissions.  
Covers **India's emissions from 2000 to 2024** across:

- CO₂ (total, coal, oil, gas, cement)
- Total GHG (CO₂ + Methane + Nitrous Oxide)
- Per capita emissions
- GDP intensity (kg CO₂ per $1000 GDP)
- Primary energy consumption

---

## ✨ Key Features

### 🎨 Clean, Modern Design
- **Sidebar navigation** — jump to any section quickly
- **KPI cards** — hover for subtle elevation
- **Year filters** — click chips to focus specific years
- **Smooth animations** — charts fade in as you scroll
- **Responsive** — works on desktop, laptop, and larger tablets

### 🎛️ Interactive Controls
- **Year chips**: Filter data by 2000, 2005, 2010, 2015, 2020, 2024
- **Metric toggles**: Switch between Total CO₂, Coal, Oil, Gas metrics
- **Annotation toggle**: See key policy events on the chart
- **Smoothing toggle**: Smooth jagged line charts for clarity
- **Chart type toggle**: Switch between Line, Area, Bar views

### 📱 Accessibility
- ARIA labels on all charts for screen readers
- High contrast color scheme
- Keyboard-navigable elements
- Responsive scaling

---

## 🧪 For Developers & Data Scientists

### File Structure

```
India-ESG-GHG-Dashboard/
├── index.html          # Main dashboard (single file, everything inside)
└── README.md           # This file
```

Yes, it's a **single HTML file**! All data, CSS, and JS are embedded.

### Built-in Data Library

The dashboard includes inline JSON data (`DATA` array) with the following fields:

```javascript
{
  year: 2000,                    // Year
  co2: 1446,                     // Total CO₂ emissions (Mt)
  coal_co2: 853.5,               // Coal CO₂
  oil_co2: 270.2,                // Oil CO₂
  gas_co2: 97.5,                 // Gas CO₂
  cement_co2: 22.8,              // Cement CO₂
  co2_per_capita: 1.36,           // tCO₂ per person
  gdp: 468206,                   // GDP (current USD, millions)
  co2_per_gdp: 3.09,             // kg CO₂ per $1000 GDP
  population: 1054500000,         // Population
  total_ghg: 3360,               // Total GHG (MtCO₂e)
  methane: 570.2,                // Methane emissions
  nitrous_oxide: 235.8,          // N₂O emissions
  primary_energy_consumption: 2.1, // Primary energy (TWh)
  share_global_co2: 5.63         // India's share of global CO₂ (%)
}
```

### Customization Tips

**Change the country?** Replace the `DATA` array with your country's OWID data.

**Want a new chart?** Add a new `<canvas>` element and call:
```javascript
new Chart(canvas, { type: 'line', data: {...} });
```

**Change colors?** Edit the `--blue`, `--teal`, `--amber` CSS variables in `:root`.

---

## 📜 License

This project uses publicly available data from Our World in Data (OWID) and is shared for **educational and informational purposes**.

The code is released under the **MIT License** — feel free to fork, modify, and use it for your own projects. We'd love a shoutout if you do! 🙌

---

## 🙋 FAQ

**Q: Why is everything in a single HTML file?**  
A: Because `index.html` + GitHub Pages = zero-cost, zero-friction deployment. No server required. Just open and it works.

**Q: Can I use this for a different country?**  
A: Absolutely! Download OWID data for your country and replace the `DATA` array inside the `<script>` tag.

**Q: What browsers are supported?**  
A: Chrome, Firefox, Safari, Edge — anything released after 2020. Chart.js 4.4.1 handles everything.

**Q: Can I download the data?**  
A: Yes! Click the **"Export CSV"** button in the top right to get the raw data as a `.csv` file.

**Q: Will the charts work without internet?**  
A: Mostly! The charts and interactivity work offline. You only need internet for Google Fonts (loads once and caches) and Chart.js CDN (you can download it and reference locally if needed).

---

## 🙏 Acknowledgements

- **Our World in Data (OWID)** — for the open-source emissions data
- **Chart.js** — for making beautiful charts with 3 lines of code
- **Google Fonts** — Manrope & JetBrains Mono
- **You** — for caring about our planet's future 🌍

---

<p align="center">
  <b>Made with 💙 for Climate Action</b><br>
  <sub>Data-driven storytelling for a sustainable future</sub>
</p>
