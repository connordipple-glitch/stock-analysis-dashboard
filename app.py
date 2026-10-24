"""
AI-Powered Stock Analysis Dashboard
FinTech Prototype for Investment Evaluation & Financial Analysis.
"""

from datetime import datetime
import json
import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

from data.finnhub_client import FinnhubClient
from analysis.metrics import (
    extract_processed_metrics,
    assess_metric_health,
)
from analysis.evaluation_engine import evaluate_company_performance
from components.charts import (
    create_price_history_chart,
    create_rsi_chart,
    create_score_gauge,
    create_ratio_comparison_chart,
)

# Load environment variables (.env)
load_dotenv()

# Streamlit Page Configuration
st.set_page_config(
    page_title="AI Stock Analysis Dashboard | FinTech",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for polished financial dashboard styling
st.markdown(
    """
    <style>
    /* Metric Card Styling */
    .metric-container {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 14px 18px;
        border: 1px solid #e9ecef;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 12px;
    }
    .metric-title {
        font-size: 0.82rem;
        color: #6c757d;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1a252f;
        margin: 4px 0;
    }
    .metric-sub {
        font-size: 0.85rem;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 600;
    }
    .status-live {
        background-color: #d4edda;
        color: #155724;
    }
    .status-demo {
        background-color: #fff3cd;
        color: #856404;
    }
    .card-banner {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 20px 24px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def format_currency(val: float) -> str:
    """Format large numbers into Billions or Millions."""
    if val >= 1_000_000:
        return f"${val / 1_000_000:.2f}T"
    elif val >= 1_000:
        return f"${val / 1_000:.2f}B"
    return f"${val:.2f}M"


# Sidebar Configuration
st.sidebar.title("📈 FinTech Dashboard")
st.sidebar.markdown("**AI-Powered Stock Analysis**")

# API Key Handling
default_key = os.getenv("FINNHUB_API_KEY", "")
api_key_input = st.sidebar.text_input(
    "Finnhub API Key (Optional)",
    value=default_key,
    type="password",
    help="Get a free key at https://finnhub.io/register. If omitted, the dashboard automatically uses pre-packaged benchmark data.",
)

# Initialize Client
client = FinnhubClient(api_key=api_key_input.strip() if api_key_input else None)

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Stock Search")

# Quick Select Buttons
st.sidebar.markdown("<small>Quick Select Popular Tickers:</small>", unsafe_allow_html=True)
quick_cols = st.sidebar.columns(4)
selected_quick = None

with quick_cols[0]:
    if st.button("AAPL"):
        selected_quick = "AAPL"
with quick_cols[1]:
    if st.button("MSFT"):
        selected_quick = "MSFT"
with quick_cols[2]:
    if st.button("NVDA"):
        selected_quick = "NVDA"
with quick_cols[3]:
    if st.button("TSLA"):
        selected_quick = "TSLA"

quick_cols_2 = st.sidebar.columns(3)
with quick_cols_2[0]:
    if st.button("GOOGL"):
        selected_quick = "GOOGL"
with quick_cols_2[1]:
    if st.button("AMZN"):
        selected_quick = "AMZN"
with quick_cols_2[2]:
    if st.button("JPM"):
        selected_quick = "JPM"

# Ticker Text Input
if "current_ticker" not in st.session_state:
    st.session_state["current_ticker"] = "AAPL"

if selected_quick:
    st.session_state["current_ticker"] = selected_quick

ticker_input = st.sidebar.text_input(
    "Enter Ticker Symbol",
    value=st.session_state["current_ticker"],
    max_chars=10,
    help="e.g. AAPL, MSFT, GOOGL, NVDA, TSLA, AMZN, JPM",
).upper().strip()

st.session_state["current_ticker"] = ticker_input

# Chart Settings
st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Chart Settings")
chart_style = st.sidebar.radio("Price Chart Type", ["Candlestick", "Line"], index=0)
toggle_sma20 = st.sidebar.checkbox("Show 20-Day SMA", value=True)
toggle_sma50 = st.sidebar.checkbox("Show 50-Day SMA", value=True)
toggle_rsi = st.sidebar.checkbox("Show RSI (14) Oscillator", value=True)

# Project Information
st.sidebar.markdown("---")
with st.sidebar.expander("ℹ️ About This Application"):
    st.markdown(
        """
        **Assignment Project 1:**  
        *AI-Powered Stock Analysis Dashboard*  
        **FinTech Framework:** Streamlit, Plotly, Pandas  
        **API Source:** Finnhub Stock API & Benchmark Fallbacks  
        **Designed With:** Google Antigravity AI Coding Agent
        """
    )

# Main Application Logic
import re

# Clean and validate ticker format (allow letters, numbers, dot, and dash for symbols like BRK.B)
cleaned_ticker = re.sub(r"[^A-Z0-9\.\-]", "", ticker_input.upper().strip())
if not cleaned_ticker or not re.match(r"^[A-Z0-9\.\-]{1,10}$", cleaned_ticker):
    st.warning("⚠️ Please enter a valid stock ticker symbol containing only letters and standard delimiters (e.g., AAPL, MSFT, BRK.B).")
    st.stop()

ticker_input = cleaned_ticker

with st.spinner(f"Retrieving financial data and calculating metrics for {ticker_input}..."):
    stock_pkg = client.get_complete_stock_data(ticker_input)

profile = stock_pkg.get("profile", {})
quote = stock_pkg.get("quote", {})
history_df = stock_pkg.get("history", pd.DataFrame())
is_live = stock_pkg.get("is_live", False)
source_label = stock_pkg.get("source", "Data Feed")

# Extract processed metrics & evaluation
metrics = extract_processed_metrics(stock_pkg)
evaluation = evaluate_company_performance(profile, quote, metrics)

# Header / Hero Section
col_logo, col_header, col_status = st.columns([1, 6, 3])

with col_header:
    st.markdown(f"## {profile.get('name', ticker_input)} (`{ticker_input}`)")
    st.markdown(
        f"**Exchange:** {profile.get('exchange', 'N/A')} &nbsp;|&nbsp; "
        f"**Sector:** {profile.get('finnhubIndustry', 'N/A')} &nbsp;|&nbsp; "
        f"**Currency:** {profile.get('currency', 'USD')}"
    )

with col_status:
    if is_live:
        st.markdown(
            '<div style="text-align:right;"><span class="status-badge status-live">● Live Finnhub Feed</span></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div style="text-align:right;"><span class="status-badge status-demo">● Benchmark Fallback Feed</span></div>',
            unsafe_allow_html=True,
        )
    st.caption(f"Source: {source_label}")

# Price & Primary Metrics Ribbon
price_val = metrics["price"]
d_change = metrics["dollar_change"]
dp_change = metrics["percent_change"]
change_color = "green" if d_change >= 0 else "red"
change_prefix = "+" if d_change >= 0 else ""

ribbon_c1, ribbon_c2, ribbon_c3, ribbon_c4, ribbon_c5, ribbon_c6 = st.columns(6)

with ribbon_c1:
    st.metric(
        label="Latest Price",
        value=f"${price_val:,.2f}",
        delta=f"{change_prefix}${d_change:.2f} ({change_prefix}{dp_change:.2f}%)",
    )

with ribbon_c2:
    st.metric(
        label="Market Capitalization",
        value=format_currency(profile.get("marketCapitalization", 0)),
    )

with ribbon_c3:
    pe_disp = f"{metrics['pe_ratio']:.1f}x" if metrics['pe_ratio'] else "N/A"
    st.metric(label="P/E (TTM)", value=pe_disp)

with ribbon_c4:
    roe_disp = f"{metrics['roe']:.1f}%" if metrics['roe'] else "N/A"
    st.metric(label="ROE (TTM)", value=roe_disp)

with ribbon_c5:
    st.metric(
        label="52-Week Range",
        value=f"${metrics['52w_low']:.1f} - ${metrics['52w_high']:.1f}",
    )

with ribbon_c6:
    beta_disp = f"{metrics['beta']:.2f}" if metrics['beta'] else "1.00"
    st.metric(label="Beta (Risk)", value=beta_disp)

st.markdown("---")

# Main Dashboard Navigation Tabs
tab_charts, tab_ratios, tab_ai_eval, tab_profile, tab_theory = st.tabs([
    "📊 Price Action & Technicals",
    "📈 Financial Ratios & Fundamentals",
    "🤖 AI & Data-Supported Assessment",
    "🏢 Company Profile & Filing Context",
    "📚 Financial Concepts & Glossary",
])

# ----------------- TAB 1: CHARTS & TECHNICAL ANALYSIS -----------------
with tab_charts:
    st.subheader(f"Historical Price Action: {ticker_input}")

    # Plotly interactive price chart
    price_fig = create_price_history_chart(
        df=history_df,
        symbol=ticker_input,
        chart_type=chart_style,
        show_sma20=toggle_sma20,
        show_sma50=toggle_sma50,
    )
    st.plotly_chart(price_fig, use_container_width=True)

    if toggle_rsi:
        rsi_fig = create_rsi_chart(history_df)
        st.plotly_chart(rsi_fig, use_container_width=True)

    # Technical Levels Table
    st.markdown("#### Key Technical Indicators")
    tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)

    with tech_col1:
        st.info(f"**20-Day SMA:** ${metrics['sma_20']:.2f}")
    with tech_col2:
        st.info(f"**50-Day SMA:** ${metrics['sma_50']:.2f}")
    with tech_col3:
        rsi_status = "Overbought" if metrics["rsi_14"] >= 70 else ("Oversold" if metrics["rsi_14"] <= 30 else "Neutral")
        st.info(f"**14-Day RSI:** {metrics['rsi_14']:.1f} ({rsi_status})")
    with tech_col4:
        st.info(f"**52-Week Position:** {metrics['52w_position_pct']:.1f}%")

# ----------------- TAB 2: FINANCIAL RATIOS & FUNDAMENTALS -----------------
with tab_ratios:
    st.subheader("Fundamental Ratios & Financial Health")
    st.markdown(
        "Financial ratios compare critical items from financial statements "
        "(Income Statement, Balance Sheet, Cash Flow) to gauge company valuation, profitability, and solvency."
    )

    ratio_col1, ratio_col2, ratio_col3 = st.columns(3)

    # 1. Valuation Ratios
    with ratio_col1:
        st.markdown("### 🏷️ Valuation Multiples")
        pe_health = assess_metric_health("pe", metrics["pe_ratio"])
        pb_health = assess_metric_health("pb", metrics["pb_ratio"])

        st.markdown(
            f"""
            <div class="metric-container">
                <div class="metric-title">Price-to-Earnings (P/E TTM)</div>
                <div class="metric-value">{metrics['pe_ratio'] if metrics['pe_ratio'] else 'N/A'}{'x' if metrics['pe_ratio'] else ''}</div>
                <div class="metric-sub" style="color: {pe_health['badge_color']};"><b>{pe_health['status']}</b>: {pe_health['interpretation']}</div>
            </div>
            <div class="metric-container">
                <div class="metric-title">Price-to-Book (P/B)</div>
                <div class="metric-value">{metrics['pb_ratio'] if metrics['pb_ratio'] else 'N/A'}{'x' if metrics['pb_ratio'] else ''}</div>
                <div class="metric-sub" style="color: {pb_health['badge_color']};"><b>{pb_health['status']}</b>: {pb_health['interpretation']}</div>
            </div>
            <div class="metric-container">
                <div class="metric-title">Price-to-Sales (P/S TTM)</div>
                <div class="metric-value">{metrics['ps_ratio'] if metrics['ps_ratio'] else 'N/A'}{'x' if metrics['ps_ratio'] else ''}</div>
                <div class="metric-sub">Valuation multiple relative to total gross revenues.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 2. Profitability Ratios
    with ratio_col2:
        st.markdown("### 💰 Profitability & Margins")
        roe_health = assess_metric_health("roe", metrics["roe"])
        margin_health = assess_metric_health("net_margin", metrics["net_margin"])

        st.markdown(
            f"""
            <div class="metric-container">
                <div class="metric-title">Return on Equity (ROE TTM)</div>
                <div class="metric-value">{metrics['roe'] if metrics['roe'] else 'N/A'}{'%' if metrics['roe'] else ''}</div>
                <div class="metric-sub" style="color: {roe_health['badge_color']};"><b>{roe_health['status']}</b>: {roe_health['interpretation']}</div>
            </div>
            <div class="metric-container">
                <div class="metric-title">Net Profit Margin</div>
                <div class="metric-value">{metrics['net_margin'] if metrics['net_margin'] else 'N/A'}{'%' if metrics['net_margin'] else ''}</div>
                <div class="metric-sub" style="color: {margin_health['badge_color']};"><b>{margin_health['status']}</b>: {margin_health['interpretation']}</div>
            </div>
            <div class="metric-container">
                <div class="metric-title">Operating Margin</div>
                <div class="metric-value">{metrics['operating_margin'] if metrics['operating_margin'] else 'N/A'}{'%' if metrics['operating_margin'] else ''}</div>
                <div class="metric-sub">Operating income earned per dollar of revenue.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 3. Solvency & Liquidity Ratios
    with ratio_col3:
        st.markdown("### 🛡️ Solvency & Liquidity")
        de_health = assess_metric_health("debt_to_equity", metrics["debt_equity"])
        cr_health = assess_metric_health("current_ratio", metrics["current_ratio"])

        st.markdown(
            f"""
            <div class="metric-container">
                <div class="metric-title">Debt-to-Equity (D/E)</div>
                <div class="metric-value">{metrics['debt_equity'] if metrics['debt_equity'] else 'N/A'}</div>
                <div class="metric-sub" style="color: {de_health['badge_color']};"><b>{de_health['status']}</b>: {de_health['interpretation']}</div>
            </div>
            <div class="metric-container">
                <div class="metric-title">Current Ratio</div>
                <div class="metric-value">{metrics['current_ratio'] if metrics['current_ratio'] else 'N/A'}</div>
                <div class="metric-sub" style="color: {cr_health['badge_color']};"><b>{cr_health['status']}</b>: {cr_health['interpretation']}</div>
            </div>
            <div class="metric-container">
                <div class="metric-title">Beta (Systematic Risk)</div>
                <div class="metric-value">{metrics['beta']:.2f}</div>
                <div class="metric-sub">Relative volatility compared to S&P 500 index.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Benchmark Comparison Chart
    st.markdown("---")
    st.plotly_chart(
        create_ratio_comparison_chart(metrics, ticker_input),
        use_container_width=True,
    )

# ----------------- TAB 3: AI & DATA-SUPPORTED ASSESSMENT -----------------
with tab_ai_eval:
    st.subheader(f"Data-Supported Performance Assessment: {ticker_input}")

    eval_c1, eval_c2 = st.columns([1, 2])

    with eval_c1:
        # Radial Gauge Visualization
        st.plotly_chart(
            create_score_gauge(
                score=evaluation["score"],
                rating=evaluation["rating"],
                color=evaluation["color"],
            ),
            use_container_width=True,
        )

        st.markdown("#### Assessment Pillar Breakdown")
        for pillar, score in evaluation["pillars"].items():
            st.write(f"**{pillar}:** {score} / 25.0")
            st.progress(min(1.0, score / 25.0))

    with eval_c2:
        st.markdown("### 📝 Executive Financial Synthesis")
        st.info(evaluation["summary"])

        st.markdown("#### 🚀 Key Catalysts & Fundamental Strengths")
        if evaluation["strengths"]:
            for item in evaluation["strengths"]:
                st.markdown(f"- ✅ **{item}**")
        else:
            st.markdown("- *No outsized fundamental catalysts identified under current market conditions.*")

        st.markdown("#### ⚠️ Financial Risks & Monitored Headwinds")
        if evaluation["risks"]:
            for item in evaluation["risks"]:
                st.markdown(f"- ⚠️ **{item}**")
        else:
            st.markdown("- *No acute balance sheet or technical distress indicators flagged.*")

        st.markdown("#### 🎯 Decision-Making Support")
        st.success(evaluation["decision_support"])

    # Export Report Section
    st.markdown("---")
    st.subheader("📥 Export Financial Report")
    report_data = {
        "Ticker": ticker_input,
        "Name": profile.get("name"),
        "Industry": profile.get("finnhubIndustry"),
        "Timestamp": datetime.now().isoformat(),
        "Price": metrics["price"],
        "PE_Ratio": metrics["pe_ratio"],
        "PB_Ratio": metrics["pb_ratio"],
        "ROE": metrics["roe"],
        "NetMargin": metrics["net_margin"],
        "CurrentRatio": metrics["current_ratio"],
        "DebtToEquity": metrics["debt_equity"],
        "Beta": metrics["beta"],
        "Score": evaluation["score"],
        "Rating": evaluation["rating"],
        "Summary": evaluation["summary"],
    }
    report_json = json.dumps(report_data, indent=2)
    st.download_button(
        label="Download Analysis Summary (JSON)",
        data=report_json,
        file_name=f"{ticker_input}_financial_analysis.json",
        mime="application/json",
    )

# ----------------- TAB 4: COMPANY PROFILE & FILINGS -----------------
with tab_profile:
    st.subheader(f"Corporate Background & Fundamentals: {profile.get('name', ticker_input)}")

    prof_c1, prof_c2 = st.columns([1, 1])

    with prof_c1:
        st.markdown(f"**Official Website:** [{profile.get('weburl', 'N/A')}]({profile.get('weburl', '#')})")
        st.markdown(f"**Country:** {profile.get('country', 'US')}")
        st.markdown(f"**Primary Exchange:** {profile.get('exchange', 'N/A')}")
        st.markdown(f"**IPO Date:** {profile.get('ipo', 'N/A')}")
        st.markdown(f"**Phone:** {profile.get('phone', 'N/A')}")

    with prof_c2:
        shares = profile.get("shareOutstanding", 0)
        st.markdown(f"**Shares Outstanding:** {shares:,.1f} Million")
        mkt_cap = profile.get("marketCapitalization", 0)
        st.markdown(f"**Market Capitalization:** {format_currency(mkt_cap)}")
        st.markdown(f"**Dividend Yield:** {metrics.get('dividend_yield', 0.0):.2f}%")

    st.markdown("---")
    st.markdown("#### 📑 SEC Filings & Regulatory Disclosure")
    st.markdown(
        f"For comprehensive audited 10-K (Annual) and 10-Q (Quarterly) statements, "
        f"investors can inspect the SEC EDGAR company archive directly:"
    )
    sec_url = f"https://www.sec.gov/edgar/searchedgar/companysearch?companySearch={ticker_input}"
    st.markdown(f"👉 [Access Official SEC EDGAR Filings for {ticker_input}]({sec_url})")

# ----------------- TAB 5: FINANCIAL THEORY & GLOSSARY -----------------
with tab_theory:
    st.subheader("Financial Concepts, Ratios, & Mathematical Formulations")
    st.markdown(
        """
        This dashboard applies core corporate finance, quantitative equity analysis, and valuation models.
        Below are the rigorous mathematical definitions and real-world interpretations of each indicator:
        """
    )

    with st.expander("1. Price-to-Earnings Ratio (P/E)", expanded=True):
        st.latex(r"P/E = \frac{\text{Market Price Per Share}}{\text{Earnings Per Share (EPS)}}")
        st.markdown(
            """
            - **Concept:** Measures how much investors are willing to pay per dollar of current earnings.
            - **Interpretation:** A high P/E implies expectations of higher future earnings growth, or that the stock is overvalued. A low P/E may signify an undervalued value stock or fundamental distress.
            - **FinTech Application:** Used in our Valuation Pillar to assess whether market pricing aligns with earnings yield.
            """
        )

    with st.expander("2. Return on Equity (ROE)"):
        st.latex(r"ROE = \frac{\text{Net Income}}{\text{Total Shareholders' Equity}} \times 100\%")
        st.markdown(
            """
            - **Concept:** The ultimate test of financial efficiency—how effectively management converts equity capital into net profit.
            - **Interpretation:** High ROE (>15%) indicates a strong economic moat and capital compounder capability (DuPont analysis breakdown: Profit Margin × Asset Turnover × Financial Leverage).
            """
        )

    with st.expander("3. Debt-to-Equity Ratio (D/E)"):
        st.latex(r"D/E = \frac{\text{Total Short-Term \& Long-Term Debt}}{\text{Total Stockholders' Equity}}")
        st.markdown(
            """
            - **Concept:** Measures financial leverage and the proportion of capital provided by creditors versus owners.
            - **Interpretation:** Higher values (>2.0) amplify earnings during growth phases but dramatically heighten default risk during monetary tightening cycles.
            """
        )

    with st.expander("4. Relative Strength Index (RSI - 14 Days)"):
        st.latex(r"RSI = 100 - \left[ \frac{100}{1 + \frac{\text{Average Gain}}{\text{Average Loss}}} \right]")
        st.markdown(
            """
            - **Concept:** A momentum oscillator that computes the velocity of directional price changes over a 14-period window.
            - **Interpretation:** An RSI above 70 indicates an overbought condition vulnerable to mean-reversion pullbacks; an RSI below 30 signals an oversold condition.
            """
        )

    with st.expander("5. Beta Coefficient"):
        st.latex(r"\beta = \frac{\text{Covariance}(R_{\text{stock}}, R_{\text{market}})}{\text{Variance}(R_{\text{market}})}")
        st.markdown(
            """
            - **Concept:** Gauges systematic risk and price sensitivity relative to the benchmark index (e.g., S&P 500).
            - **Interpretation:** A Beta of 1.0 moves in tandem with the market. Beta > 1.0 implies heightened market sensitivity, whereas Beta < 1.0 represents a defensive asset.
            """
        )

# Footer
st.markdown("---")
st.caption(
    "AI-Powered Stock Analysis Dashboard | Built for FinTech Prototype Assignment | "
    "Data provided via Finnhub Stock API & Benchmark Fallbacks. Not financial advice."
)
