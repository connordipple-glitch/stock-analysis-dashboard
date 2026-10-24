"""
Financial Ratio & Quantitative Indicator Calculations.

Implements core corporate finance formulas and quantitative indicators:
- Valuation (P/E, P/B, P/S)
- Profitability (ROE, ROA, Net Margin, Operating Margin)
- Solvency & Liquidity (Debt-to-Equity, Current Ratio)
- Market & Risk Indicators (Beta, 52W Range, RSI-14, Moving Averages)
"""

from typing import Any, Dict, Optional, Tuple
import numpy as np
import pandas as pd


def calculate_pe_ratio(price: float, eps: Optional[float]) -> Optional[float]:
    """
    Calculate Price-to-Earnings (P/E) Ratio.
    Formula: Share Price / Earnings Per Share (EPS).
    A core valuation metric representing the dollar amount an investor can expect to invest
    in a company to receive one dollar of that company’s earnings.
    """
    if eps is None or eps <= 0:
        return None
    return round(price / eps, 2)


def calculate_pb_ratio(price: float, book_value_per_share: Optional[float]) -> Optional[float]:
    """
    Calculate Price-to-Book (P/B) Ratio.
    Formula: Share Price / Book Value Per Share.
    Compares a company's market value to its net asset value (book value).
    """
    if book_value_per_share is None or book_value_per_share <= 0:
        return None
    return round(price / book_value_per_share, 2)


def calculate_52week_range_position(current_price: float, low_52w: float, high_52w: float) -> float:
    """
    Calculate where the current stock price sits within its 52-week trading corridor (0% to 100%).
    Formula: ((Current - 52W Low) / (52W High - 52W Low)) * 100.
    """
    if high_52w <= low_52w:
        return 50.0
    pos = ((current_price - low_52w) / (high_52w - low_52w)) * 100.0
    return round(max(0.0, min(100.0, pos)), 2)


def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate the Relative Strength Index (RSI) technical momentum oscillator.
    Formula: RSI = 100 - (100 / (1 + RS))
    where RS = Average Gain / Average Loss over the specified period.
    Values >= 70 indicate overbought conditions; <= 30 indicate oversold conditions.
    When average loss is zero, RSI = 100. When average gain is zero, RSI = 0.
    """
    delta = series.diff()
    gain = delta.clip(lower=0.0)
    loss = -1.0 * delta.clip(upper=0.0)

    avg_gain = gain.rolling(window=period, min_periods=period).mean().copy()
    avg_loss = loss.rolling(window=period, min_periods=period).mean().copy()

    # Wilder's smoothing for subsequent values
    for i in range(period, len(series)):
        prev_gain = avg_gain.iloc[i - 1]
        prev_loss = avg_loss.iloc[i - 1]
        if not np.isnan(prev_gain) and not np.isnan(gain.iloc[i]):
            avg_gain.iloc[i] = (prev_gain * (period - 1) + gain.iloc[i]) / period
        if not np.isnan(prev_loss) and not np.isnan(loss.iloc[i]):
            avg_loss.iloc[i] = (prev_loss * (period - 1) + loss.iloc[i]) / period

    rsi = pd.Series(50.0, index=series.index)
    for i in range(period, len(series)):
        g = avg_gain.iloc[i]
        l = avg_loss.iloc[i]
        if np.isnan(g) or np.isnan(l):
            rsi.iloc[i] = 50.0
        elif l == 0.0 and g > 0.0:
            rsi.iloc[i] = 100.0
        elif g == 0.0:
            rsi.iloc[i] = 0.0
        else:
            rs = g / l
            rsi.iloc[i] = round(100.0 - (100.0 / (1.0 + rs)), 2)

    return rsi


def calculate_moving_averages(series: pd.Series) -> Tuple[pd.Series, pd.Series]:
    """
    Compute 20-day (short-term) and 50-day (medium-term) Simple Moving Averages.
    """
    sma_20 = series.rolling(window=20).mean()
    sma_50 = series.rolling(window=50).mean()
    return sma_20, sma_50


def assess_metric_health(name: str, value: Optional[float]) -> Dict[str, str]:
    """
    Provide institutional financial interpretation and grading for a calculated ratio.
    Returns:
        status: "Excellent" | "Good" | "Fair" | "Elevated" | "High Risk" | "N/A"
        color: hex color or Streamlit style
        interpretation: analytical commentary
    """
    if value is None or np.isnan(value):
        return {
            "status": "N/A",
            "badge_color": "gray",
            "interpretation": "Data not available or metric not applicable.",
        }

    if name == "pe":
        if value < 0:
            return {"status": "Unprofitable", "badge_color": "#e74c3c", "interpretation": "Negative earnings (net loss). High risk."}
        elif value < 15:
            return {"status": "Value / Undervalued", "badge_color": "#27ae60", "interpretation": "Trades below broader market average P/E multiples."}
        elif value <= 30:
            return {"status": "Fair Valuation", "badge_color": "#2980b9", "interpretation": "Reasonably aligned with historical S&P 500 medians."}
        elif value <= 50:
            return {"status": "Growth Premium", "badge_color": "#f39c12", "interpretation": "Priced with high growth expectations; sensitive to earnings misses."}
        else:
            return {"status": "High Premium", "badge_color": "#e67e22", "interpretation": "Very high valuation multiple; requires sustained hyper-growth."}

    elif name == "pb":
        if value < 1.0:
            return {"status": "Below Book Value", "badge_color": "#27ae60", "interpretation": "Trading at a discount to net tangible asset value."}
        elif value <= 5.0:
            return {"status": "Healthy / Typical", "badge_color": "#2980b9", "interpretation": "Standard capitalization for capital-light or established firms."}
        else:
            return {"status": "Intangible-Heavy", "badge_color": "#8e44ad", "interpretation": "High multiple reflecting significant IP, goodwill, or high ROE."}

    elif name == "roe":
        if value >= 25.0:
            return {"status": "Exceptional", "badge_color": "#27ae60", "interpretation": "World-class capital allocation and shareholder return generation."}
        elif value >= 15.0:
            return {"status": "Strong", "badge_color": "#2ecc71", "interpretation": "Outperforms average corporate cost of equity."}
        elif value >= 8.0:
            return {"status": "Moderate", "badge_color": "#f39c12", "interpretation": "Acceptable profitability, near average equity hurdle rates."}
        else:
            return {"status": "Weak", "badge_color": "#e74c3c", "interpretation": "Sub-par return on shareholder equity capital."}

    elif name == "current_ratio":
        if value >= 2.0:
            return {"status": "Very Liquid", "badge_color": "#27ae60", "interpretation": "Ample short-term assets to cover obligations twice over."}
        elif value >= 1.2:
            return {"status": "Adequate", "badge_color": "#2980b9", "interpretation": "Healthy working capital and short-term solvency."}
        elif value >= 1.0:
            return {"status": "Tight", "badge_color": "#f39c12", "interpretation": "Modest liquidity buffer; monitor working capital cycles."}
        else:
            return {"status": "Deficit", "badge_color": "#e74c3c", "interpretation": "Current liabilities exceed current assets. Liquidity watch needed."}

    elif name == "debt_to_equity":
        if value <= 0.5:
            return {"status": "Conservative", "badge_color": "#27ae60", "interpretation": "Pristine balance sheet with minimal leverage."}
        elif value <= 1.5:
            return {"status": "Manageable", "badge_color": "#2980b9", "interpretation": "Balanced capital structure utilizing modest leverage."}
        elif value <= 2.5:
            return {"status": "Elevated", "badge_color": "#f39c12", "interpretation": "Significant debt burden; sensitive to interest rate fluctuations."}
        else:
            return {"status": "High Leverage", "badge_color": "#e74c3c", "interpretation": "Heavily leveraged; solvency risk during macroeconomic downturns."}

    elif name == "net_margin":
        if value >= 20.0:
            return {"status": "High Margin", "badge_color": "#27ae60", "interpretation": "Wide economic moat with strong pricing power."}
        elif value >= 10.0:
            return {"status": "Healthy", "badge_color": "#2980b9", "interpretation": "Solid operational efficiency and bottom-line conversion."}
        elif value > 0:
            return {"status": "Thin Margin", "badge_color": "#f39c12", "interpretation": "Modest margin; vulnerable to input cost inflation."}
        else:
            return {"status": "Operating Loss", "badge_color": "#e74c3c", "interpretation": "Negative profit margin. Cash burn rate is critical."}

    elif name == "beta":
        if value < 0.8:
            return {"status": "Low Volatility", "badge_color": "#27ae60", "interpretation": "Defensive stock; moves less than the broader market."}
        elif value <= 1.2:
            return {"status": "Market Correlated", "badge_color": "#2980b9", "interpretation": "Volatility closely mirrors the S&P 500 index."}
        else:
            return {"status": "High Volatility", "badge_color": "#e67e22", "interpretation": "Aggressive swings; significantly amplified beta movements."}

    return {"status": "Neutral", "badge_color": "#7f8c8d", "interpretation": "Standard corporate baseline."}


def extract_processed_metrics(data_package: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract, compute, and normalize all required ratios and metrics from the raw data package.
    """
    quote = data_package.get("quote", {})
    metric = data_package.get("metric", {})
    history = data_package.get("history", pd.DataFrame())

    current_price = float(quote.get("c", 0.0))
    eps = metric.get("epsTTM")
    pe_raw = metric.get("peTTM") or calculate_pe_ratio(current_price, eps)
    pb_raw = metric.get("pbAnnual")
    ps_raw = metric.get("psTTM")
    roe_raw = metric.get("roeTTM")
    roa_raw = metric.get("roaTTM")
    margin_net = metric.get("netProfitMarginTTM")
    margin_op = metric.get("operatingMarginTTM")
    current_ratio = metric.get("currentRatioQuarterly")
    debt_equity = metric.get("totalDebt/totalEquityQuarterly")
    beta = metric.get("beta", 1.0)
    dividend_yield = metric.get("dividendYieldIndicatedAnnual", 0.0)

    # 52-Week Range
    low_52 = metric.get("52WeekLow") or (history["Low"].min() if not history.empty else current_price * 0.7)
    high_52 = metric.get("52WeekHigh") or (history["High"].max() if not history.empty else current_price * 1.3)
    pos_52 = calculate_52week_range_position(current_price, float(low_52), float(high_52))

    # RSI & Moving Averages from historical data
    rsi_val = 50.0
    sma_20_val = current_price
    sma_50_val = current_price

    if not history.empty and len(history) >= 20:
        close_series = history["Close"]
        rsi_series = calculate_rsi(close_series)
        rsi_val = round(float(rsi_series.iloc[-1]), 2)
        sma20_s, sma50_s = calculate_moving_averages(close_series)
        sma_20_val = round(float(sma20_s.iloc[-1]), 2)
        sma_50_val = round(float(sma50_s.dropna().iloc[-1]), 2) if not sma50_s.dropna().empty else current_price

    return {
        "price": current_price,
        "dollar_change": float(quote.get("d", 0.0)),
        "percent_change": float(quote.get("dp", 0.0)),
        "pe_ratio": pe_raw,
        "pb_ratio": pb_raw,
        "ps_ratio": ps_raw,
        "roe": roe_raw,
        "roa": roa_raw,
        "net_margin": margin_net,
        "operating_margin": margin_op,
        "current_ratio": current_ratio,
        "debt_equity": debt_equity,
        "beta": beta,
        "dividend_yield": dividend_yield,
        "52w_low": float(low_52),
        "52w_high": float(high_52),
        "52w_position_pct": pos_52,
        "rsi_14": rsi_val,
        "sma_20": sma_20_val,
        "sma_50": sma_50_val,
    }
