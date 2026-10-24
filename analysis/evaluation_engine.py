"""
AI & Data-Supported Company Performance Evaluation Engine.

Synthesizes multiple fundamental and technical dimensions:
1. Valuation attractiveness
2. Profitability and capital efficiency
3. Balance sheet solvency and liquidity
4. Price momentum and trend strength

Outputs an objective performance score (0-100), overall rating, executive summary,
key fundamental strengths, and specific risk factors.
"""

from typing import Any, Dict, List


def evaluate_company_performance(
    profile: Dict[str, Any],
    quote: Dict[str, Any],
    metrics: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Generate an evidence-based, data-supported financial evaluation.
    """
    name = profile.get("name", "The Company")
    ticker = profile.get("ticker", "TICKER")
    industry = profile.get("finnhubIndustry", "Market Sector")

    price = metrics.get("price", 0.0)
    pe = metrics.get("pe_ratio")
    pb = metrics.get("pb_ratio")
    roe = metrics.get("roe")
    margin_net = metrics.get("net_margin")
    current_ratio = metrics.get("current_ratio")
    debt_equity = metrics.get("debt_equity")
    beta = metrics.get("beta", 1.0)
    rsi = metrics.get("rsi_14", 50.0)
    pos_52 = metrics.get("52w_position_pct", 50.0)
    sma_50 = metrics.get("sma_50", price)

    strengths: List[str] = []
    risks: List[str] = []

    # 1. Valuation Pillar (0 - 25 points)
    val_score = 15.0
    if pe is not None:
        if pe < 18.0:
            val_score = 24.0
            strengths.append(f"Valuation Attractiveness: P/E ratio of {pe:.1f}x trades at a favorable discount to market multiples.")
        elif pe <= 32.0:
            val_score = 18.0
        elif pe <= 45.0:
            val_score = 12.0
            risks.append(f"Valuation Multiple: Elevated P/E of {pe:.1f}x reflects high growth expectations priced into the stock.")
        else:
            val_score = 7.0
            risks.append(f"Premium Valuation Risk: P/E of {pe:.1f}x indicates significant multiple expansion risk.")
    else:
        val_score = 10.0
        risks.append("Unprofitable or Unreported Earnings: P/E metric unavailable due to negative or zero earnings.")

    # 2. Profitability Pillar (0 - 25 points)
    prof_score = 12.0
    if roe is not None:
        if roe >= 25.0:
            prof_score += 8.0
            strengths.append(f"Elite Capital Efficiency: Return on Equity (ROE) of {roe:.1f}% indicates exceptional shareholder value generation.")
        elif roe >= 15.0:
            prof_score += 5.0
            strengths.append(f"Solid Return on Equity: ROE of {roe:.1f}% exceeds typical cost of equity hurdles.")
        elif roe >= 8.0:
            prof_score += 2.0
        else:
            prof_score -= 4.0
            risks.append(f"Sub-par Profitability: Low ROE of {roe:.1f}% reflects muted equity returns.")

    if margin_net is not None:
        if margin_net >= 20.0:
            prof_score += 5.0
            strengths.append(f"High-Margin Franchise: Net profit margin of {margin_net:.1f}% demonstrates substantial pricing power.")
        elif margin_net >= 10.0:
            prof_score += 3.0
        elif margin_net > 0:
            prof_score += 1.0
        else:
            prof_score -= 4.0
            risks.append("Operating Deficit: Negative net margin signals ongoing cash burn.")
    prof_score = max(0.0, min(25.0, prof_score))

    # 3. Solvency & Liquidity Pillar (0 - 25 points)
    solv_score = 14.0
    if debt_equity is not None:
        if debt_equity <= 0.5:
            solv_score += 6.0
            strengths.append(f"Conservative Leverage: Low Debt-to-Equity ratio ({debt_equity:.2f}) insulates the balance sheet from interest rate risk.")
        elif debt_equity <= 1.2:
            solv_score += 4.0
        elif debt_equity <= 2.2:
            solv_score += 1.0
            risks.append(f"Moderate Debt Burden: Debt-to-Equity of {debt_equity:.2f} requires steady cash generation to service liabilities.")
        else:
            solv_score -= 5.0
            risks.append(f"High Leverage Hazard: Elevated Debt-to-Equity of {debt_equity:.2f} increases financial fragility during credit contractions.")

    if current_ratio is not None:
        if current_ratio >= 1.5:
            solv_score += 5.0
            strengths.append(f"Healthy Liquidity Buffer: Current ratio of {current_ratio:.2f} confirms solid working capital cover.")
        elif current_ratio >= 1.0:
            solv_score += 2.0
        else:
            solv_score -= 4.0
            risks.append(f"Working Capital Squeeze: Current ratio of {current_ratio:.2f} indicates short-term liabilities exceed current assets.")
    solv_score = max(0.0, min(25.0, solv_score))

    # 4. Momentum & Trend Strength Pillar (0 - 25 points)
    mom_score = 12.0
    if price > sma_50:
        mom_score += 6.0
        strengths.append(f"Bullish Trend Structure: Price (\\${price:.2f}) is trading comfortably above its 50-day moving average (\\${sma_50:.2f}).")
    else:
        mom_score -= 3.0
        risks.append(f"Technical Resistance: Price (\\${price:.2f}) trades below its 50-day trendline (\\${sma_50:.2f}), suggesting intermediate consolidation.")

    if 40.0 <= rsi <= 65.0:
        mom_score += 4.0
    elif rsi > 70.0:
        risks.append(f"Overbought Oscillator: 14-day RSI of {rsi:.1f} signals potential near-term price pullback or consolidation.")
    elif rsi < 30.0:
        strengths.append(f"Oversold Condition: 14-day RSI of {rsi:.1f} indicates technical exhaustion and potential rebound zone.")

    if pos_52 >= 75.0:
        mom_score += 3.0
    elif pos_52 <= 25.0:
        mom_score -= 2.0
    mom_score = max(0.0, min(25.0, mom_score))

    # Total Composite Score
    composite_score = round(val_score + prof_score + solv_score + mom_score, 1)

    # Classification
    if composite_score >= 80:
        rating = "Strong Bullish"
        color = "#27ae60"
        sentiment = "High fundamental quality coupled with positive price momentum."
    elif composite_score >= 65:
        rating = "Bullish / Attractive"
        color = "#2ecc71"
        sentiment = "Solid fundamental foundation with balanced risk-reward profile."
    elif composite_score >= 45:
        rating = "Neutral / Hold"
        color = "#f39c12"
        sentiment = "Fair fundamentals balanced by valuation constraints or sector headwinds."
    elif composite_score >= 30:
        rating = "Cautious / Underweight"
        color = "#e67e22"
        sentiment = "Underlying pressure on margins, balance sheet leverage, or valuation multiple."
    else:
        rating = "High Risk / Avoid"
        color = "#e74c3c"
        sentiment = "Significant fundamental vulnerabilities and adverse momentum."

    # Data-supported narrative summary
    pe_text = f"P/E ratio of {pe:.1f}x" if pe else "an uncalculated P/E multiple"
    roe_text = f"ROE of {roe:.1f}%" if roe else "undisclosed ROE"
    margin_text = f"net margin of {margin_net:.1f}%" if margin_net else "operating metrics"

    summary_text = (
        f"{name} ({ticker}) currently trades at \\${price:.2f} within the {industry} sector. "
        f"Fundamentally, the company showcases a {pe_text} alongside an {roe_text} and a {margin_text}. "
        f"Its position in the 52-week corridor is at {pos_52:.1f}% with an RSI momentum index of {rsi:.1f}. "
        f"Overall, our multi-factor model assigns a score of {composite_score:.1f}/100 with a '{rating}' stance, "
        f"highlighting {len(strengths)} key financial catalysts against {len(risks)} monitored risk items."
    )

    decision_support = (
        "Suitable for medium-to-long term investors seeking exposure to "
        f"{industry}. Monitor upcoming quarterly filings for updates on gross margins and debt amortization schedules."
    )

    return {
        "score": composite_score,
        "rating": rating,
        "color": color,
        "sentiment": sentiment,
        "pillars": {
            "Valuation": round(val_score, 1),
            "Profitability": round(prof_score, 1),
            "Solvency": round(solv_score, 1),
            "Momentum": round(mom_score, 1),
        },
        "summary": summary_text,
        "strengths": strengths[:4],
        "risks": risks[:4],
        "decision_support": decision_support,
    }
