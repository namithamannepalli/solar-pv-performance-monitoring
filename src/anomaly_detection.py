import pandas as pd
from sklearn.ensemble import IsolationForest

from config import (
    ANOMALY_CONTAMINATION,
    DAYLIGHT_IRRADIANCE_THRESHOLD
)


INPUT_PATH = "data/processed/performance_analysis.csv"
OUTPUT_PATH = "data/processed/anomaly_detection.csv"


df = pd.read_csv(
    INPUT_PATH
)

df["timestamp"] = pd.to_datetime(
    df["timestamp"]
)


# Analyze only meaningful daylight operating periods
daytime = (
    df["irradiance_w_m2"]
    > DAYLIGHT_IRRADIANCE_THRESHOLD
)


features = [
    "irradiance_w_m2",
    "module_temperature_c",
    "expected_power_mw",
    "actual_power_mw",
    "generation_gap_mwh"
]


model = IsolationForest(
    contamination=ANOMALY_CONTAMINATION,
    random_state=42
)


df["anomaly_flag"] = 0
df["anomaly_score"] = 0.0


model.fit(
    df.loc[daytime, features]
)


predictions = model.predict(
    df.loc[daytime, features]
)

scores = model.decision_function(
    df.loc[daytime, features]
)


df.loc[daytime, "anomaly_flag"] = (
    predictions == -1
).astype(int)


df.loc[daytime, "anomaly_score"] = scores


df.to_csv(
    OUTPUT_PATH,
    index=False
)


print("ANOMALY DETECTION SUMMARY")
print("=" * 40)

print(
    f"Detected anomalies: "
    f"{df['anomaly_flag'].sum()}"
)

print(
    f"Saved to: {OUTPUT_PATH}"
)