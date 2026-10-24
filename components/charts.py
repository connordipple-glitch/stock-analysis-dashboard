"""
Interactive Financial Visualizations using Plotly.

Provides high-resolution charts:
- Candlestick / Line price chart with SMA-20, SMA-50 overlays and Volume bars
- 14-day Relative Strength Index (RSI) momentum oscillator
- Multi-factor evaluation gauge chart
- Financial ratios benchmark comparison chart
"""

from typing import Any, Dict, Optional
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from analysis.metrics import calculate_moving_averages, calculate_rsi


def create_price_history_chart(
    df: pd.DataFrame,
    symbol: str,
    chart_type: str = "Candlestick",
    show_sma20: bool = True,
    show_sma50: bool = True,
) -> go.Figure:
    """
    Create an interactive dual-panel financial chart with price action and trading volume.
    """
    if df.empty:
        fig = go.Figure()
        fig.update_layout(title="No Historical Price Data Available")
        return fig

    # Calculate moving averages
    sma_20, sma_50 = calculate_moving_averages(df["Close"])

    # Create figure with shared x-axis (price on top, volume below)
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=(f"{symbol} Price Action", "Trading Volume"),
        row_heights=[0.75, 0.25],
    )

    # 1. Price Trace (Candlestick or Line)
    if chart_type == "Candlestick" and {"Open", "High", "Low", "Close"}.issubset(df.columns):
        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
                name="OHLC",
                increasing_line_color="#2ecc71",
                decreasing_line_color="#e74c3c",
            ),
            row=1,
            col=1,
        )
    else:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["Close"],
                mode="lines",
                name="Close Price",
                line=dict(color="#3498db", width=2),
            ),
            row=1,
            col=1,
        )

    # Moving Average Overlays
    if show_sma20:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=sma_20,
                mode="lines",
                name="SMA 20 (Short-Term)",
                line=dict(color="#f39c12", width=1.5, dash="dash"),
            ),
            row=1,
            col=1,
        )

    if show_sma50:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=sma_50,
                mode="lines",
                name="SMA 50 (Medium-Term)",
                line=dict(color="#9b59b6", width=1.8),
            ),
            row=1,
            col=1,
        )

    # 2. Volume Bar Trace
    # Color volume bars based on close >= open
    vol_colors = [
        "#2ecc71" if row["Close"] >= row["Open"] else "#e74c3c"
        for _, row in df.iterrows()
    ]

    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df["Volume"],
            name="Volume",
            marker_color=vol_colors,
            opacity=0.65,
        ),
        row=2,
        col=1,
    )

    # Layout styling
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=40, r=40, t=40, b=30),
        height=540,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        xaxis2=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=3, label="3M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(step="all", label="All"),
                ])
            ),
            type="date",
        ),
    )
    fig.update_xaxes(rangeslider_visible=False)
    fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)

    return fig


def create_rsi_chart(df: pd.DataFrame) -> go.Figure:
    """
    Create a 14-day RSI momentum oscillator chart with overbought/oversold boundaries.
    """
    if df.empty or len(df) < 15:
        fig = go.Figure()
        fig.update_layout(title="Insufficient Data for RSI Calculation")
        return fig

    rsi = calculate_rsi(df["Close"])

    fig = go.Figure()

    # RSI Line
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=rsi,
            mode="lines",
            name="RSI (14)",
            line=dict(color="#8e44ad", width=2),
        )
    )

    # Overbought reference line (70)
    fig.add_hline(
        y=70,
        line_dash="dot",
        line_color="#e74c3c",
        annotation_text="Overbought (70)",
        annotation_position="bottom right",
    )

    # Oversold reference line (30)
    fig.add_hline(
        y=30,
        line_dash="dot",
        line_color="#2ecc71",
        annotation_text="Oversold (30)",
        annotation_position="top right",
    )

    # Neutral median line (50)
    fig.add_hline(
        y=50,
        line_dash="dash",
        line_color="#bdc3c7",
    )

    fig.update_layout(
        template="plotly_white",
        title="14-Day Relative Strength Index (RSI) Momentum Indicator",
        yaxis=dict(range=[0, 100], title="RSI Value"),
        xaxis=dict(title="Date"),
        margin=dict(l=40, r=40, t=40, b=30),
        height=280,
    )
    return fig


def create_score_gauge(score: float, rating: str, color: str) -> go.Figure:
    """
    Create a modern radial gauge visualization for the composite score.
    """
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": f"<b>Overall Assessment: {rating}</b>", "font": {"size": 18}},
            number={"suffix": "/100", "font": {"size": 36, "color": color}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#bdc3c7"},
                "bar": {"color": color, "thickness": 0.28},
                "bgcolor": "white",
                "borderwidth": 1,
                "bordercolor": "#ecf0f1",
                "steps": [
                    {"range": [0, 30], "color": "#fadbd8"},
                    {"range": [30, 45], "color": "#fdebd0"},
                    {"range": [45, 65], "color": "#fcf3cf"},
                    {"range": [65, 80], "color": "#d4efdf"},
                    {"range": [80, 100], "color": "#a9dfbf"},
                ],
                "threshold": {
                    "line": {"color": color, "width": 4},
                    "thickness": 0.75,
                    "value": score,
                },
            },
        )
    )
    fig.update_layout(
        height=260,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig


def create_ratio_comparison_chart(metrics: Dict[str, Any], symbol: str) -> go.Figure:
    """
    Horizontal bar chart comparing company's ratios to market benchmark medians.
    """
    ratios = [
        "ROE (%)",
        "Net Margin (%)",
        "Operating Margin (%)",
        "Current Ratio",
        "Debt/Equity",
    ]

    company_vals = [
        metrics.get("roe") or 0.0,
        metrics.get("net_margin") or 0.0,
        metrics.get("operating_margin") or 0.0,
        (metrics.get("current_ratio") or 0.0) * 10,  # Scaled for visual balance
        (metrics.get("debt_equity") or 0.0) * 10,     # Scaled for visual balance
    ]

    # Typical S&P 500 median reference values
    benchmark_vals = [
        18.0,   # ROE
        12.0,   # Net Margin
        15.0,   # Op Margin
        14.0,   # Current Ratio 1.4 * 10
        8.0,    # Debt/Equity 0.8 * 10
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=ratios,
            x=company_vals,
            name=f"{symbol}",
            orientation="h",
            marker_color="#2980b9",
        )
    )
    fig.add_trace(
        go.Bar(
            y=ratios,
            x=benchmark_vals,
            name="S&P 500 Benchmark Median",
            orientation="h",
            marker_color="#bdc3c7",
        )
    )

    fig.update_layout(
        template="plotly_white",
        title=f"{symbol} Financial Indicators vs. Market Benchmark",
        barmode="group",
        height=320,
        margin=dict(l=40, r=40, t=40, b=30),
        xaxis=dict(title="Indicator Scale"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig
