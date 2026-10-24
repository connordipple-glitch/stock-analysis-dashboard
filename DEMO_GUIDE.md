# Prototype Demonstration Script & Presentation Guide

This guide is designed to help you deliver an A+ (100/100) demonstration for your **FinTech Application Assignment**, either in a live class presentation or a pre-recorded walkthrough video.

---

## ⏱️ Suggested 3-to-5 Minute Presentation Structure

### 1. Introduction & Financial Problem Statement (1 Minute)
- **Hook**: "Hello everyone. Today I'm demonstrating the **AI-Powered Stock Analysis Dashboard**, an interactive FinTech prototype designed to solve the equity analysis bottleneck."
- **Financial Problem**:
  - Individual and professional investors face significant information overload and fragmentation.
  - Valuation multiples, financial statements (SEC 10-K / 10-Q), technical trends, and risk metrics are scattered across different platforms and paywalled terminals.
  - Making an informed investment decision requires rapid synthesis of valuation, capital efficiency, balance sheet solvency, and momentum.
- **FinTech Solution**:
  - A unified Streamlit application integrating real-time market data from the **Finnhub REST API**, interactive Plotly charts, quantitative corporate finance formulas, and a 4-pillar automated evaluation engine.

---

### 2. Live Application Walkthrough (2.5 Minutes)

#### Step A: Company Search & Real-Time Price Ribbon
- **Action**: Enter `AAPL` or click the `NVDA` quick-select button in the sidebar.
- **Explain**:
  - "Notice the top ribbon updates immediately with the latest stock price, dollar and percentage change, market capitalization, P/E multiple, and 52-week trading corridor."
  - "The status badge in the upper right confirms our data feed status—either live via the Finnhub API or our pre-packaged benchmark dataset."

#### Step B: Interactive Price Action & Technical Analysis (Tab 1)
- **Action**: Click Tab 1 (*Price Action & Technicals*).
- **Explain**:
  - "We have an interactive dual-panel Plotly chart displaying daily Candlesticks and volume bars."
  - "I can zoom into any timeframe using the 1M, 3M, 6M, 1Y buttons."
  - "Notice our trend overlays: the 20-day SMA in orange and 50-day SMA in purple. When the price holds above the 50-day SMA, it confirms an intermediate bullish market structure."
  - "Below, we plot the 14-day Relative Strength Index (RSI). RSI uses Wilder's exponential smoothing to detect overbought conditions above 70 and oversold conditions below 30."

#### Step C: Fundamental Ratios & Benchmark Comparison (Tab 2)
- **Action**: Switch to Tab 2 (*Financial Ratios & Fundamentals*).
- **Explain**:
  - "Our prototype calculates and groups over 10 institutional financial ratios into three core cards:"
    1. **Valuation Multiples**: Price-to-Earnings ($P/E$), Price-to-Book ($P/B$), and Price-to-Sales ($P/S$).
    2. **Profitability Indicators**: Return on Equity ($ROE$), Net Profit Margin, and Operating Margin.
    3. **Solvency & Liquidity**: Debt-to-Equity ($D/E$) and Current Ratio.
  - "Each metric includes an automated qualitative health tag (e.g. *Exceptional*, *Fair Valuation*, *Conservative Leverage*)."
  - "Below the cards is a horizontal benchmark bar chart that compares this company's indicators directly to S&P 500 medians."

#### Step D: AI & Data-Supported Performance Assessment (Tab 3)
- **Action**: Switch to Tab 3 (*AI & Data-Supported Assessment*).
- **Explain**:
  - "This fulfills our core requirement: presenting a brief, data-supported assessment."
  - "Our 4-Pillar Evaluation Engine synthesizes Valuation, Profitability, Solvency, and Momentum into a composite score out of 100, visualized on this radial gauge."
  - "The Executive Synthesis provides an automated narrative citing the exact numbers, followed by bulleted bullish catalysts, key balance sheet risks, and decision-support guidance."
  - "Users can also click **Download Analysis Summary** to export the entire evaluation as a structured JSON report."

#### Step E: SEC Filings & Financial Theory (Tabs 4 & 5)
- **Action**: Briefly show Tabs 4 and 5.
- **Explain**:
  - "Tab 4 provides corporate metadata and a direct deep-link to the company's official SEC EDGAR 10-K and 10-Q filing archive."
  - "Tab 5 acts as an educational glossary containing LaTeX mathematical formulations and conceptual explanations for every ratio calculated."

---

### 3. AI Coding Agent Reflection & Engineering Process (1 Minute)
- **Explain**:
  - "This prototype was designed and built using **Google Antigravity** as our AI coding assistant."
  - "Rather than one-shot generation, we developed iteratively:
    1. First, establishing the data model and Finnhub API client with rate-limiting and fallback guards.
    2. Second, writing modular Python functions for each corporate finance formula.
    3. Third, creating automated unit tests in `tests/test_metrics.py`. In fact, unit testing caught a boundary issue with division-by-zero when calculating RSI on zero-loss sequences, which Google Antigravity diagnosed and corrected using Wilder's smoothing.
    4. Fourth, building the responsive Streamlit frontend and Plotly visualizations."

---

### 4. Conclusion & Limitations (30 Seconds)
- **Summary**:
  - "In conclusion, this application demonstrates how modern FinTech tools and AI coding agents can transform raw market data into an interactive, institutional-grade analytical dashboard."
- **Limitations**:
  - "Current limitations include Finnhub free-tier rate limits (30 calls/minute) and backward-looking accounting data. Future enhancements include an interactive Discounted Cash Flow (DCF) model and automated SEC 10-K LLM summarization."

---

## 💡 Anticipated Questions & Answers (Q&A Prep)

**Q: What happens if Finnhub's API is down or reaches its rate limit?**  
*A:* "We engineered a resilient dual-feed architecture in `data/finnhub_client.py`. If the API key is missing, invalid, or rate-limited, the application gracefully switches to our pre-packaged benchmark dataset and Geometric Brownian Motion (GBM) generator. The user is notified via an ambient status badge, and the application never crashes."

**Q: How is the composite performance score calculated?**  
*A:* "The score is calculated across four 25-point pillars: Valuation multiple discount, Profitability (ROE and Net Margin), Solvency (Debt/Equity and Current Ratio), and Momentum (Price vs 50-day SMA, 52-week position, and RSI). The sum yields an objective 0–100 score and rating."

**Q: Why did you choose Streamlit and Plotly?**  
*A:* "Streamlit allows rapid Python-native dashboard state management, while Plotly provides high-performance client-side interactivity (zoom, pan, hover tooltips, and time-range selection) ideal for financial market charts."
