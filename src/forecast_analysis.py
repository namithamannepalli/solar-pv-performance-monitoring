import numpy as np
import pandas as pd

from config import DAYLIGHT_IRRADIANCE_THRESHOLD
from logger import get_logger


logger = get_logger("forecast_analysis")

INPUT_PATH = "data/processed/performance_analysis.csv"
OUTPUT_PATH = "data/processed/forecast_analysis.csv"
METRICS_PATH = "data/processed/forecast_metrics.csv"


df = pd.read_csv(INPUT_PATH)

df["timestamp"] = pd.to_datetime(
    df["timestamp"]
)


df["forecast_energy_mwh"] = (
    df["expected_energy_mwh"]
)


df["forecast_error_mwh"] = (
    df["actual_energy_mwh"]
    - df["forecast_energy_mwh"]
)


df["absolute_error_mwh"] = (
    df["forecast_error_mwh"]
    .abs()
)


daytime = (
    df["irradiance_w_m2"]
    > DAYLIGHT_IRRADIANCE_THRESHOLD
)


daytime_df = df.loc[
    daytime
].copy()


mae = (
    daytime_df["absolute_error_mwh"]
    .mean()
)


rmse = np.sqrt(
    (
        daytime_df["forecast_error_mwh"]
        ** 2
    ).mean()
)


mape = (
    daytime_df["absolute_error_mwh"]
    / daytime_df["forecast_energy_mwh"]
    .replace(0, np.nan)
).mean() * 100


df.to_csv(
    OUTPUT_PATH,
    index=False
)


metrics = pd.DataFrame({
    "metric": [
        "MAE (MWh)",
        "RMSE (MWh)",
        "MAPE (%)"
    ],
    "value": [
        mae,
        rmse,
        mape
    ]
})


metrics.to_csv(
    METRICS_PATH,
    index=False
)


logger.info(
    f"Forecast MAE: {mae:.4f} MWh"
)

logger.info(
    f"Forecast RMSE: {rmse:.4f} MWh"
)

logger.info(
    f"Forecast MAPE: {mape:.2f}%"
)


print("FORECAST BASELINE ANALYSIS")
print("=" * 40)

print(
    f"MAE  : {mae:.4f} MWh"
)

print(
    f"RMSE : {rmse:.4f} MWh"
)

print(
    f"MAPE : {mape:.2f}%"
)

print()

print(
    f"Saved to: {OUTPUT_PATH}"
)

print(
    f"Saved to: {METRICS_PATH}"
)