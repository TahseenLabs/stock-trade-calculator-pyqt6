# Stock Trade Profit Calculator

A desktop app built with **Python** and **PyQt6** that lets you calculate the profit or loss from buying and selling stocks on specific dates. Select a stock, pick your buy and sell dates from a calendar, set a quantity — and the app instantly shows your purchase total, sell total, profit, or loss.

---

## Screenshots

### Main Interface
> Full view of the app showing stock selection, dual calendars, and live-updating totals.

![Main Interface](docs/screenshots/main-interface.png)

### Stock Dropdown
> Dropdown populated with all available stocks from the dataset (Amazon, Apple, Bitcoin, Tesla and more).

![Stock Selection](docs/screenshots/stock-selection.png)

### Selection Summary & Totals
> Live summary of current selections with automatically calculated purchase total, sell total, profit and loss.

![Summary and Totals](docs/screenshots/summary-totals.png)

---

## Project Structure

```
stock-trade-calculator/
├── StockTradeCalculator.py     # Main application, all UI and calculation logic
└── Stock_Market_Dataset.csv    # Historical stock price data (CSV)
```

---

## Requirements

- Python 3.8+
- PyQt6

Install dependencies:

```bash
pip install PyQt6
```

---

## How to Run

Make sure `Stock_Market_Dataset.csv` is in the same directory as the script, then:

```bash
python StockTradeCalculator.py
```

---

## How It Works

1. **Select a stock** from the dropdown (e.g. Apple, Tesla, Bitcoin, S&P 500).
2. **Set a quantity** using the spin box (1–10,000 shares/units).
3. **Pick a purchase date** and a **sell date** using the two calendar widgets.
4. The app **instantly calculates** and displays:
   - Purchase Total
   - Sell Total
   - Profit (if sell > buy)
   - Loss (if sell < buy)

All values update in real time as you change any input, no button press needed.

---

## Features

- **Live-updating summary**: selected stock, quantity, and both dates are reflected in a summary box as you change them
- **Dual calendar pickers**: buy and sell dates default to a sensible range based on the dataset
- **Profit/Loss display**: only the relevant figure shows a non-zero value, keeping the display clean
- **CSV-driven data**: stock prices are loaded directly from `Stock_Market_Dataset.csv`, making it easy to swap in different data

---

## Available Stocks

The dataset includes historical prices for: Amazon, Apple, Berkshire, Bitcoin, Copper, Crude Oil, Ethereum, Gold, Google, Meta, Microsoft, Nasdaq 100, Natural Gas, Netflix, Nvidia, Platinum, S&P 500, Silver, Tesla.

---

## Built With

- [Python](https://www.python.org/)
- [PyQt6](https://pypi.org/project/PyQt6/), GUI framework
- `QComboBox`, `QSpinBox`, `QCalendarWidget`, `QGridLayout`, `QLabel`
