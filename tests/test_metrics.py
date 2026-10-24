"""
Unit Tests for Financial Metrics, Valuation Ratios, and Evaluation Engine.
"""

import unittest
import numpy as np
import pandas as pd

from analysis.metrics import (
    calculate_pe_ratio,
    calculate_pb_ratio,
    calculate_52week_range_position,
    calculate_rsi,
    assess_metric_health,
    extract_processed_metrics,
)
from analysis.evaluation_engine import evaluate_company_performance
from data.sample_data import get_sample_data, generate_synthetic_history


class TestFinancialMetrics(unittest.TestCase):
    """Test suite for financial calculations and models."""

    def test_pe_ratio_normal(self):
        """Test standard P/E ratio calculation."""
        pe = calculate_pe_ratio(150.0, 5.0)
        self.assertEqual(pe, 30.0)

    def test_pe_ratio_negative_and_none(self):
        """Test negative EPS and None handling."""
        self.assertIsNone(calculate_pe_ratio(100.0, -2.5))
        self.assertIsNone(calculate_pe_ratio(100.0, 0.0))
        self.assertIsNone(calculate_pe_ratio(100.0, None))

    def test_pb_ratio(self):
        """Test Price-to-Book calculation."""
        pb = calculate_pb_ratio(200.0, 50.0)
        self.assertEqual(pb, 4.0)
        self.assertIsNone(calculate_pb_ratio(200.0, 0.0))
        self.assertIsNone(calculate_pb_ratio(200.0, None))

    def test_52week_range_position(self):
        """Test 52-week position percentile."""
        # Midpoint
        pos_mid = calculate_52week_range_position(150.0, 100.0, 200.0)
        self.assertEqual(pos_mid, 50.0)

        # High bound
        pos_high = calculate_52week_range_position(200.0, 100.0, 200.0)
        self.assertEqual(pos_high, 100.0)

        # Low bound
        pos_low = calculate_52week_range_position(100.0, 100.0, 200.0)
        self.assertEqual(pos_low, 0.0)

    def test_rsi_calculation(self):
        """Test 14-day RSI series output bounds."""
        # Create monotonically increasing price series
        prices = pd.Series([10.0 + i * 2.0 for i in range(30)])
        rsi = calculate_rsi(prices, period=14)
        self.assertFalse(rsi.empty)
        # Monotonically increasing prices should lead to high RSI (> 70)
        self.assertGreater(float(rsi.iloc[-1]), 70.0)

    def test_assess_metric_health(self):
        """Test qualitative grading of ratios."""
        health_pe = assess_metric_health("pe", 22.0)
        self.assertEqual(health_pe["status"], "Fair Valuation")

        health_roe = assess_metric_health("roe", 32.0)
        self.assertEqual(health_roe["status"], "Exceptional")

        health_de = assess_metric_health("debt_to_equity", 0.3)
        self.assertEqual(health_de["status"], "Conservative")

    def test_sample_data_retrieval(self):
        """Verify sample data structure for pre-set and synthetic tickers."""
        aapl = get_sample_data("AAPL")
        self.assertEqual(aapl["profile"]["ticker"], "AAPL")
        self.assertIn("peTTM", aapl["metric"])
        self.assertFalse(aapl["history"].empty)

        # Arbitrary synthetic ticker
        custom = get_sample_data("CUSTOMTICKER")
        self.assertEqual(custom["profile"]["ticker"], "CUSTOMTICKER")
        self.assertGreater(custom["quote"]["c"], 0)
        self.assertFalse(custom["history"].empty)

    def test_evaluation_engine(self):
        """Verify performance assessment scoring and narrative output."""
        sample = get_sample_data("AAPL")
        metrics = extract_processed_metrics(sample)
        eval_result = evaluate_company_performance(sample["profile"], sample["quote"], metrics)

        self.assertIn("score", eval_result)
        self.assertGreaterEqual(eval_result["score"], 0)
        self.assertLessEqual(eval_result["score"], 100)
        self.assertIn("rating", eval_result)
        self.assertIn("summary", eval_result)
        self.assertTrue(len(eval_result["strengths"]) > 0)


if __name__ == "__main__":
    unittest.main()
