"""
Finnhub Financial Data Client.

Handles interaction with the Finnhub REST API, response parsing, error handling,
rate limiting safeguards, and seamless fallback to benchmark data.
"""

from datetime import datetime, timedelta
import os
import time
from typing import Any, Dict, Optional
import pandas as pd
import requests

from data.sample_data import generate_synthetic_history, get_sample_data


class FinnhubClient:
    """Client for Finnhub Financial API with fallback resilience."""

    BASE_URL = "https://finnhub.io/api/v1"

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Finnhub client with API key from parameter or environment."""
        self.api_key = api_key or os.getenv("FINNHUB_API_KEY", "").strip()
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "FinTech-Stock-Analysis-Dashboard/1.0"})

    def has_api_key(self) -> bool:
        """Check if an API key is present."""
        return bool(self.api_key and len(self.api_key) > 5)

    def _get(self, endpoint: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Internal helper to execute authenticated GET requests."""
        if not self.has_api_key():
            return None

        url = f"{self.BASE_URL}{endpoint}"
        req_params = params.copy()
        req_params["token"] = self.api_key

        try:
            response = self.session.get(url, params=req_params, timeout=8)
            if response.status_code == 200:
                data = response.json()
                return data
            elif response.status_code == 429:
                # Rate limit hit (Free tier allows 30 calls/minute)
                return {"_error": "Finnhub rate limit reached (30 calls/min). Using cached fallback data."}
            elif response.status_code in (401, 403):
                return {"_error": "Invalid or unauthorized Finnhub API key. Using cached fallback data."}
            else:
                return {"_error": f"API returned status {response.status_code}."}
        except requests.exceptions.Timeout:
            return {"_error": "Finnhub API request timed out."}
        except requests.exceptions.RequestException as e:
            return {"_error": f"Network error connecting to Finnhub: {str(e)}"}

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch real-time stock quote from Finnhub.
        Returns:
            c: Current price
            d: Change
            dp: Percent change
            h: High price of the day
            l: Low price of the day
            o: Open price of the day
            pc: Previous close price
            t: Timestamp
        """
        sym = symbol.upper().strip()
        res = self._get("/quote", {"symbol": sym})
        if res and "_error" not in res and res.get("c", 0) > 0:
            return res

        fallback = get_sample_data(sym)
        return fallback["quote"]

    def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        """Fetch company profile including sector, market cap, shares outstanding."""
        sym = symbol.upper().strip()
        res = self._get("/stock/profile2", {"symbol": sym})
        if res and "_error" not in res and res.get("name"):
            return res

        fallback = get_sample_data(sym)
        return fallback["profile"]

    def get_basic_financials(self, symbol: str) -> Dict[str, Any]:
        """Fetch basic financial metrics (P/E, ROE, Debt/Equity, 52W range, Beta)."""
        sym = symbol.upper().strip()
        res = self._get("/stock/metric", {"symbol": sym, "metric": "all"})
        if res and "_error" not in res and res.get("metric"):
            return res.get("metric", {})

        fallback = get_sample_data(sym)
        return fallback["metric"]

    def get_historical_candles(
        self, symbol: str, resolution: str = "D", days: int = 365
    ) -> pd.DataFrame:
        """
        Fetch historical daily candlestick prices (OHLCV).
        If the endpoint is restricted or returns empty, synthesizes history matching the latest quote.
        """
        sym = symbol.upper().strip()
        to_ts = int(time.time())
        from_ts = int(to_ts - (days * 86400 * 1.5))  # extra buffer for weekends

        res = self._get(
            "/stock/candle",
            {"symbol": sym, "resolution": resolution, "from": from_ts, "to": to_ts},
        )

        if (
            res
            and "_error" not in res
            and res.get("s") == "ok"
            and len(res.get("c", [])) > 0
        ):
            df = pd.DataFrame({
                "Date": pd.to_datetime(res["t"], unit="s"),
                "Open": res["o"],
                "High": res["h"],
                "Low": res["l"],
                "Close": res["c"],
                "Volume": res["v"],
            })
            df.set_index("Date", inplace=True)
            df.sort_index(inplace=True)
            return df

        # Free tier candle restrictions or fallback:
        # Generate realistic GBM history anchored to the latest quote
        quote = self.get_quote(sym)
        latest_price = quote.get("c", 100.0)
        return generate_synthetic_history(sym, end_price=latest_price, days=days)

    def get_complete_stock_data(self, symbol: str) -> Dict[str, Any]:
        """
        Orchestrate retrieval of complete stock information:
        Quote, Profile, Key Financials, and Historical Candles.
        """
        sym = symbol.upper().strip()

        is_live = False
        data_source = "Demo / Benchmark Fallback Dataset"
        api_notice = None

        if self.has_api_key():
            # Try fetching live quote and profile
            quote_res = self._get("/quote", {"symbol": sym})
            profile_res = self._get("/stock/profile2", {"symbol": sym})

            if (
                quote_res
                and "_error" not in quote_res
                and quote_res.get("c", 0) > 0
                and profile_res
                and "_error" not in profile_res
                and profile_res.get("name")
            ):
                is_live = True
                data_source = "Finnhub Live Market Data API"

                # Financial metrics
                metric_res = self._get("/stock/metric", {"symbol": sym, "metric": "all"})
                metrics = metric_res.get("metric", {}) if (metric_res and "_error" not in metric_res) else {}

                # If some metrics are missing from live, merge with fallback metrics
                fallback_pkg = get_sample_data(sym)
                merged_metrics = fallback_pkg["metric"].copy()
                for k, v in metrics.items():
                    if v is not None:
                        merged_metrics[k] = v

                # History candles
                history_df = self.get_historical_candles(sym, days=365)

                return {
                    "symbol": sym,
                    "profile": profile_res,
                    "quote": quote_res,
                    "metric": merged_metrics,
                    "history": history_df,
                    "is_live": True,
                    "source": data_source,
                    "notice": None,
                }
            else:
                # Capture why API call didn't succeed
                err1 = quote_res.get("_error") if isinstance(quote_res, dict) else None
                err2 = profile_res.get("_error") if isinstance(profile_res, dict) else None
                api_notice = err1 or err2 or "No data returned for ticker. Switched to fallback."

        # Fallback dataset
        fallback_data = get_sample_data(sym)
        return {
            "symbol": sym,
            "profile": fallback_data["profile"],
            "quote": fallback_data["quote"],
            "metric": fallback_data["metric"],
            "history": fallback_data["history"],
            "is_live": False,
            "source": data_source,
            "notice": api_notice or "Running in benchmark offline mode. Provide a Finnhub API Key for live quotes.",
        }
