from pathlib import Path

import pandas as pd

from logger import get_logger


logger = get_logger("report_generation")

PERFORMANCE_PATH = "data/processed/performance_analysis.csv"
LOSS_PATH = "data/processed/loss_summary.csv"
FINANCIAL_PATH = "data/processed/financial_impact.csv"
ANOMALY_PATH = "data/processed/anomaly_detection.csv"
FORECAST_PATH = "data/processed/forecast_metrics.csv"

OUTPUT_PATH = Path(
    "reports/plant_performance_report.md"
)


performance = pd.read_csv(
    PERFORMANCE_PATH
)

loss_summary = pd.read_csv(
    LOSS_PATH
)

financial = pd.read_csv(
    FINANCIAL_PATH
)

anomalies = pd.read_csv(
    ANOMALY_PATH
)

forecast = pd.read_csv(
    FORECAST_PATH
)


total_expected = (
    performance["expected_energy_mwh"].sum()
)

total_actual = (
    performance["actual_energy_mwh"].sum()
)

total_generation_loss = max(
    0,
    performance["generation_gap_mwh"].sum()
)


if total_expected > 0:
    overall_performance_ratio = (
        total_actual
        / total_expected
        * 100
    )
else:
    overall_performance_ratio = 0


anomaly_count = int(
    anomalies["anomaly_flag"].sum()
)


total_revenue_loss = (
    financial[
        "estimated_revenue_loss_usd"
    ].sum()
)


top_loss = (
    loss_summary
    .sort_values(
        "loss_mwh",
        ascending=False
    )
    .iloc[0]
)


report = f"""
# Solar PV Plant Performance Report

## Executive Summary

| KPI | Value |
|---|---:|
| Expected Generation | {total_expected:.2f} MWh |
| Actual Generation | {total_actual:.2f} MWh |
| Generation Loss | {total_generation_loss:.2f} MWh |
| Performance Ratio | {overall_performance_ratio:.2f}% |
| Detected Anomalies | {anomaly_count} |
| Estimated Revenue Impact | ${total_revenue_loss:,.2f} |

## Loss Breakdown

{loss_summary.to_markdown(index=False)}

## Financial Impact

{financial.to_markdown(index=False)}

## Forecast Accuracy

{forecast.to_markdown(index=False)}

## Key Finding

The largest diagnosed loss category was:

**{top_loss["loss_category"]}**

with an estimated loss of:

**{top_loss["loss_mwh"]:.2f} MWh**

## Methodology

The analysis compares actual plant generation against an expected-generation baseline and uses simulated operational signals to identify potential sources of underperformance.

An Isolation Forest model is used to flag potentially anomalous operating periods during daylight conditions.

The financial impact is estimated using the configured energy price.

The SCADA dataset is simulated for portfolio demonstration.

Loss and financial estimates are therefore illustrative and not
field-verified engineering measurements.
"""


OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)


OUTPUT_PATH.write_text(
    report,
    encoding="utf-8"
)


logger.info(
    f"Performance report generated at {OUTPUT_PATH}"
)


print(
    f"Report saved to: {OUTPUT_PATH}"
)