
# Solar PV Plant Performance Report

## Executive Summary

| KPI | Value |
|---|---:|
| Expected Generation | 5635.73 MWh |
| Actual Generation | 5549.16 MWh |
| Generation Loss | 86.56 MWh |
| Performance Ratio | 98.46% |
| Detected Anomalies | 81 |
| Estimated Revenue Impact | $5,115.97 |

## Loss Breakdown

| loss_category          |   loss_mwh |   loss_share_pct |
|:-----------------------|-----------:|-----------------:|
| Inverter downtime      |    9.39078 |          9.17791 |
| Tracker downtime       |    3.52117 |          3.44135 |
| Grid curtailment       |   25.0429  |         24.4753  |
| Equipment derate       |   14.1078  |         13.788   |
| Soiling                |   41.4228  |         40.4839  |
| Unexplained / residual |    8.83385 |          8.6336  |

## Financial Impact

| loss_category          |   loss_mwh |   loss_share_pct |   estimated_revenue_loss_usd |   estimated_revenue_loss_kusd |
|:-----------------------|-----------:|-----------------:|-----------------------------:|------------------------------:|
| Inverter downtime      |    9.39078 |          9.17791 |                      469.539 |                      0.469539 |
| Tracker downtime       |    3.52117 |          3.44135 |                      176.059 |                      0.176059 |
| Grid curtailment       |   25.0429  |         24.4753  |                     1252.15  |                      1.25215  |
| Equipment derate       |   14.1078  |         13.788   |                      705.389 |                      0.705389 |
| Soiling                |   41.4228  |         40.4839  |                     2071.14  |                      2.07114  |
| Unexplained / residual |    8.83385 |          8.6336  |                      441.692 |                      0.441692 |

## Forecast Accuracy

| metric     |     value |
|:-----------|----------:|
| MAE (MWh)  | 0.0267632 |
| RMSE (MWh) | 0.0967152 |
| MAPE (%)   | 2.20993   |

## Key Finding

The largest diagnosed loss category was:

**Soiling**

with an estimated loss of:

**41.42 MWh**

## Methodology

The analysis compares actual plant generation against an expected-generation baseline and uses simulated operational signals to identify potential sources of underperformance.

An Isolation Forest model is used to flag potentially anomalous operating periods during daylight conditions.

The financial impact is estimated using the configured energy price.

The SCADA dataset is simulated for portfolio demonstration.

Loss and financial estimates are therefore illustrative and not
field-verified engineering measurements.
