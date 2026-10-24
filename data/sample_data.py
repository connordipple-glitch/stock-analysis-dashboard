"""
Comprehensive Fallback & Demo Data Provider for Stock Analysis Dashboard.

This module provides high-fidelity sample data for popular tickers (AAPL, MSFT, GOOGL, NVDA, TSLA, AMZN, JPM)
and a robust synthetic generator for any custom ticker symbol. This ensures the application remains
100% operational and interactive even without an active Finnhub API key or when network limits occur.
"""

from datetime import datetime, timedelta
import math
import random
from typing import Any, Dict, List
import numpy as np
import pandas as pd

# Detailed sample company profiles, quotes, and financial metrics
SAMPLE_COMPANIES: Dict[str, Dict[str, Any]] = {
    "AAPL": {
        "profile": {
            "name": "Apple Inc.",
            "ticker": "AAPL",
            "exchange": "NASDAQ",
            "finnhubIndustry": "Technology",
            "currency": "USD",
            "country": "US",
            "marketCapitalization": 3480000.0,  # in Millions (~$3.48T)
            "shareOutstanding": 15150.0,        # in Millions
            "ipo": "1980-12-12",
            "weburl": "https://www.apple.com",
            "logo": "https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/AAPL.png",
            "phone": "14089961010",
        },
        "quote": {
            "c": 232.45,   # Current price
            "d": 2.15,     # Dollar change
            "dp": 0.9336,  # Percent change
            "h": 233.80,   # High of day
            "l": 230.12,   # Low of day
            "o": 230.50,   # Open price
            "pc": 230.30,  # Previous close
            "t": int(datetime.now().timestamp()),
        },
        "metric": {
            "peTTM": 34.20,
            "pbAnnual": 48.65,
            "psTTM": 8.95,
            "roeTTM": 154.20,
            "roaTTM": 29.80,
            "netProfitMarginTTM": 26.31,
            "operatingMarginTTM": 31.25,
            "currentRatioQuarterly": 0.98,
            "quickRatioQuarterly": 0.84,
            "totalDebt/totalEquityQuarterly": 1.45,
            "52WeekHigh": 237.23,
            "52WeekLow": 164.08,
            "beta": 1.08,
            "epsTTM": 6.80,
            "dividendYieldIndicatedAnnual": 0.44,
            "10DayAverageTradingVolume": 48.25,  # Millions
        },
        "base_price": 232.45,
        "volatility": 0.22,
    },
    "MSFT": {
        "profile": {
            "name": "Microsoft Corporation",
            "ticker": "MSFT",
            "exchange": "NASDAQ",
            "finnhubIndustry": "Technology",
            "currency": "USD",
            "country": "US",
            "marketCapitalization": 3150000.0,
            "shareOutstanding": 7430.0,
            "ipo": "1986-03-13",
            "weburl": "https://www.microsoft.com",
            "logo": "https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/MSFT.png",
            "phone": "14258828080",
        },
        "quote": {
            "c": 423.85,
            "d": -1.45,
            "dp": -0.3409,
            "h": 427.50,
            "l": 421.10,
            "o": 426.00,
            "pc": 425.30,
            "t": int(datetime.now().timestamp()),
        },
        "metric": {
            "peTTM": 35.80,
            "pbAnnual": 11.20,
            "psTTM": 12.80,
            "roeTTM": 38.50,
            "roaTTM": 19.40,
            "netProfitMarginTTM": 35.75,
            "operatingMarginTTM": 44.60,
            "currentRatioQuarterly": 1.34,
            "quickRatioQuarterly": 1.25,
            "totalDebt/totalEquityQuarterly": 0.42,
            "52WeekHigh": 468.35,
            "52WeekLow": 327.20,
            "beta": 1.15,
            "epsTTM": 11.84,
            "dividendYieldIndicatedAnnual": 0.72,
            "10DayAverageTradingVolume": 19.40,
        },
        "base_price": 423.85,
        "volatility": 0.24,
    },
    "GOOGL": {
        "profile": {
            "name": "Alphabet Inc.",
            "ticker": "GOOGL",
            "exchange": "NASDAQ",
            "finnhubIndustry": "Communication Services",
            "currency": "USD",
            "country": "US",
            "marketCapitalization": 2040000.0,
            "shareOutstanding": 12380.0,
            "ipo": "2004-08-19",
            "weburl": "https://abc.xyz",
            "logo": "https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/GOOGL.png",
            "phone": "16502530000",
        },
        "quote": {
            "c": 164.90,
            "d": 1.85,
            "dp": 1.1346,
            "h": 166.20,
            "l": 163.40,
            "o": 163.80,
            "pc": 163.05,
            "t": int(datetime.now().timestamp()),
        },
        "metric": {
            "peTTM": 21.60,
            "pbAnnual": 6.45,
            "psTTM": 6.15,
            "roeTTM": 31.40,
            "roaTTM": 21.20,
            "netProfitMarginTTM": 28.50,
            "operatingMarginTTM": 32.10,
            "currentRatioQuarterly": 2.10,
            "quickRatioQuarterly": 1.95,
            "totalDebt/totalEquityQuarterly": 0.11,
            "52WeekHigh": 191.75,
            "52WeekLow": 120.21,
            "beta": 1.05,
            "epsTTM": 7.63,
            "dividendYieldIndicatedAnnual": 0.48,
            "10DayAverageTradingVolume": 22.80,
        },
        "base_price": 164.90,
        "volatility": 0.26,
    },
    "NVDA": {
        "profile": {
            "name": "NVIDIA Corporation",
            "ticker": "NVDA",
            "exchange": "NASDAQ",
            "finnhubIndustry": "Semiconductors",
            "currency": "USD",
            "country": "US",
            "marketCapitalization": 3280000.0,
            "shareOutstanding": 24500.0,
            "ipo": "1999-01-22",
            "weburl": "https://www.nvidia.com",
            "logo": "https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/NVDA.png",
            "phone": "14084862000",
        },
        "quote": {
            "c": 133.88,
            "d": 4.12,
            "dp": 3.1751,
            "h": 135.20,
            "l": 130.40,
            "o": 130.80,
            "pc": 129.76,
            "t": int(datetime.now().timestamp()),
        },
        "metric": {
            "peTTM": 54.20,
            "pbAnnual": 42.10,
            "psTTM": 33.40,
            "roeTTM": 115.60,
            "roaTTM": 64.30,
            "netProfitMarginTTM": 55.20,
            "operatingMarginTTM": 62.40,
            "currentRatioQuarterly": 4.25,
            "quickRatioQuarterly": 3.80,
            "totalDebt/totalEquityQuarterly": 0.18,
            "52WeekHigh": 140.76,
            "52WeekLow": 39.23,
            "beta": 1.68,
            "epsTTM": 2.47,
            "dividendYieldIndicatedAnnual": 0.03,
            "10DayAverageTradingVolume": 52.10,
        },
        "base_price": 133.88,
        "volatility": 0.42,
    },
    "TSLA": {
        "profile": {
            "name": "Tesla, Inc.",
            "ticker": "TSLA",
            "exchange": "NASDAQ",
            "finnhubIndustry": "Automobiles & Components",
            "currency": "USD",
            "country": "US",
            "marketCapitalization": 710000.0,
            "shareOutstanding": 3190.0,
            "ipo": "2010-06-29",
            "weburl": "https://www.tesla.com",
            "logo": "https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/TSLA.png",
            "phone": "15125168000",
        },
        "quote": {
            "c": 222.60,
            "d": -3.80,
            "dp": -1.6784,
            "h": 227.40,
            "l": 220.10,
            "o": 226.50,
            "pc": 226.40,
            "t": int(datetime.now().timestamp()),
        },
        "metric": {
            "peTTM": 58.40,
            "pbAnnual": 10.80,
            "psTTM": 7.30,
            "roeTTM": 18.20,
            "roaTTM": 11.50,
            "netProfitMarginTTM": 12.80,
            "operatingMarginTTM": 10.40,
            "currentRatioQuarterly": 1.82,
            "quickRatioQuarterly": 1.28,
            "totalDebt/totalEquityQuarterly": 0.14,
            "52WeekHigh": 271.00,
            "52WeekLow": 138.80,
            "beta": 2.35,
            "epsTTM": 3.81,
            "dividendYieldIndicatedAnnual": 0.0,
            "10DayAverageTradingVolume": 65.40,
        },
        "base_price": 222.60,
        "volatility": 0.48,
    },
    "AMZN": {
        "profile": {
            "name": "Amazon.com, Inc.",
            "ticker": "AMZN",
            "exchange": "NASDAQ",
            "finnhubIndustry": "Consumer Discretionary",
            "currency": "USD",
            "country": "US",
            "marketCapitalization": 1960000.0,
            "shareOutstanding": 10450.0,
            "ipo": "1997-05-15",
            "weburl": "https://www.amazon.com",
            "logo": "https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/AMZN.png",
            "phone": "12062661000",
        },
        "quote": {
            "c": 187.50,
            "d": 1.20,
            "dp": 0.6441,
            "h": 189.20,
            "l": 186.10,
            "o": 186.80,
            "pc": 186.30,
            "t": int(datetime.now().timestamp()),
        },
        "metric": {
            "peTTM": 43.10,
            "pbAnnual": 8.70,
            "psTTM": 3.25,
            "roeTTM": 22.30,
            "roaTTM": 8.90,
            "netProfitMarginTTM": 7.55,
            "operatingMarginTTM": 9.02,
            "currentRatioQuarterly": 1.05,
            "quickRatioQuarterly": 0.82,
            "totalDebt/totalEquityQuarterly": 0.58,
            "52WeekHigh": 201.20,
            "52WeekLow": 118.35,
            "beta": 1.18,
            "epsTTM": 4.35,
            "dividendYieldIndicatedAnnual": 0.0,
            "10DayAverageTradingVolume": 38.60,
        },
        "base_price": 187.50,
        "volatility": 0.28,
    },
    "JPM": {
        "profile": {
            "name": "JPMorgan Chase & Co.",
            "ticker": "JPM",
            "exchange": "NYSE",
            "finnhubIndustry": "Financial Services / Banking",
            "currency": "USD",
            "country": "US",
            "marketCapitalization": 625000.0,
            "shareOutstanding": 2850.0,
            "ipo": "1969-03-05",
            "weburl": "https://www.jpmorganchase.com",
            "logo": "https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/JPM.png",
            "phone": "12122706000",
        },
        "quote": {
            "c": 218.40,
            "d": 0.85,
            "dp": 0.3907,
            "h": 219.80,
            "l": 216.50,
            "o": 217.20,
            "pc": 217.55,
            "t": int(datetime.now().timestamp()),
        },
        "metric": {
            "peTTM": 12.10,
            "pbAnnual": 1.85,
            "psTTM": 3.75,
            "roeTTM": 16.80,
            "roaTTM": 1.35,
            "netProfitMarginTTM": 32.10,
            "operatingMarginTTM": 41.50,
            "currentRatioQuarterly": 1.15,
            "quickRatioQuarterly": 1.05,
            "totalDebt/totalEquityQuarterly": 1.85,
            "52WeekHigh": 225.48,
            "52WeekLow": 137.66,
            "beta": 1.06,
            "epsTTM": 18.05,
            "dividendYieldIndicatedAnnual": 2.15,
            "10DayAverageTradingVolume": 9.40,
        },
        "base_price": 218.40,
        "volatility": 0.20,
    },
}


def generate_synthetic_history(
    symbol: str,
    end_price: float,
    annual_volatility: float = 0.25,
    days: int = 365,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate realistic historical daily stock price time series using Geometric Brownian Motion (GBM).
    The generated series ends at exactly `end_price` on the most recent trading day.
    """
    # Deterministic seed based on symbol for consistent behavior
    sym_seed = sum(ord(c) for c in symbol) + seed
    rng = np.random.default_rng(sym_seed)

    # Time parameters
    dt = 1.0 / 252.0  # Daily trading step
    annual_drift = 0.10  # Expected 10% annualized equity drift

    # Generate GBM path backwards from end_price
    daily_returns = rng.normal(
        (annual_drift - 0.5 * annual_volatility**2) * dt,
        annual_volatility * np.sqrt(dt),
        size=days,
    )

    # Cumulative multipliers
    cum_returns = np.cumprod(np.exp(daily_returns))
    # Rescale so the last price matches end_price exactly
    raw_prices = end_price * (cum_returns / cum_returns[-1])

    # Build trading dates (skipping weekends)
    today = datetime.now().date()
    dates: List[datetime] = []
    curr = today
    while len(dates) < days:
        if curr.weekday() < 5:  # Monday to Friday
            dates.append(curr)
        curr -= timedelta(days=1)
    dates.reverse()

    # Generate realistic Open, High, Low, Close, Volume
    data = []
    for i in range(days):
        close_p = round(float(raw_prices[i]), 2)
        if i == 0:
            open_p = round(close_p * (1 + rng.uniform(-0.01, 0.01)), 2)
        else:
            open_p = round(float(raw_prices[i - 1]) * (1 + rng.uniform(-0.005, 0.005)), 2)

        day_high = round(max(open_p, close_p) * (1 + abs(rng.normal(0, 0.008))), 2)
        day_low = round(min(open_p, close_p) * (1 - abs(rng.normal(0, 0.008))), 2)
        # Ensure high is strictly >= max and low is <= min
        day_high = max(day_high, open_p, close_p)
        day_low = min(day_low, open_p, close_p)

        # Realistic volume in shares
        base_vol = 25_000_000
        vol_noise = rng.lognormal(0, 0.4)
        vol = int(base_vol * vol_noise)

        data.append({
            "Date": pd.to_datetime(dates[i]),
            "Open": open_p,
            "High": day_high,
            "Low": day_low,
            "Close": close_p,
            "Volume": vol,
        })

    df = pd.DataFrame(data)
    df.set_index("Date", inplace=True)
    return df


def get_sample_data(symbol: str) -> Dict[str, Any]:
    """
    Retrieve full sample company data (profile, quote, metrics, historical df).
    If symbol is not in pre-configured list, synthesizes a realistic profile.
    """
    sym = symbol.upper().strip()

    if sym in SAMPLE_COMPANIES:
        base = SAMPLE_COMPANIES[sym]
        profile = base["profile"].copy()
        quote = base["quote"].copy()
        metric = base["metric"].copy()
        base_price = base["base_price"]
        volatility = base["volatility"]
    else:
        # Generate synthetic but reasonable company data
        seed_num = sum(ord(c) for c in sym)
        random.seed(seed_num)

        est_price = round(random.uniform(40.0, 350.0), 2)
        prev_close = round(est_price * (1 + random.uniform(-0.03, 0.03)), 2)
        dollar_chg = round(est_price - prev_close, 2)
        pct_chg = round((dollar_chg / prev_close) * 100, 4)

        profile = {
            "name": f"{sym} Corporation",
            "ticker": sym,
            "exchange": "NASDAQ",
            "finnhubIndustry": "Diversified Industries",
            "currency": "USD",
            "country": "US",
            "marketCapitalization": round(random.uniform(10000.0, 800000.0), 2),
            "shareOutstanding": round(random.uniform(500.0, 5000.0), 2),
            "ipo": "2015-05-20",
            "weburl": f"https://www.{sym.lower()}.com",
            "logo": "",
            "phone": "18005550199",
        }

        quote = {
            "c": est_price,
            "d": dollar_chg,
            "dp": pct_chg,
            "h": round(max(est_price, prev_close) * 1.015, 2),
            "l": round(min(est_price, prev_close) * 0.985, 2),
            "o": round(prev_close * 1.002, 2),
            "pc": prev_close,
            "t": int(datetime.now().timestamp()),
        }

        metric = {
            "peTTM": round(random.uniform(15.0, 45.0), 2),
            "pbAnnual": round(random.uniform(2.0, 15.0), 2),
            "psTTM": round(random.uniform(2.0, 10.0), 2),
            "roeTTM": round(random.uniform(12.0, 35.0), 2),
            "roaTTM": round(random.uniform(5.0, 18.0), 2),
            "netProfitMarginTTM": round(random.uniform(10.0, 30.0), 2),
            "operatingMarginTTM": round(random.uniform(14.0, 38.0), 2),
            "currentRatioQuarterly": round(random.uniform(1.1, 2.5), 2),
            "quickRatioQuarterly": round(random.uniform(0.9, 2.0), 2),
            "totalDebt/totalEquityQuarterly": round(random.uniform(0.2, 1.2), 2),
            "52WeekHigh": round(est_price * random.uniform(1.1, 1.35), 2),
            "52WeekLow": round(est_price * random.uniform(0.65, 0.9), 2),
            "beta": round(random.uniform(0.85, 1.45), 2),
            "epsTTM": round(est_price / random.uniform(18.0, 30.0), 2),
            "dividendYieldIndicatedAnnual": round(random.uniform(0.0, 2.5), 2),
            "10DayAverageTradingVolume": round(random.uniform(5.0, 30.0), 2),
        }
        base_price = est_price
        volatility = 0.28

    history_df = generate_synthetic_history(sym, end_price=base_price, annual_volatility=volatility)

    return {
        "symbol": sym,
        "profile": profile,
        "quote": quote,
        "metric": metric,
        "history": history_df,
        "is_fallback": True,
        "source": "Pre-packaged Financial Benchmark Dataset",
    }
