import numpy as np
import pandas as pd

from logger import get_logger


logger = get_logger("loss_diagnostics")

INPUT_PATH = "data/processed/performance_analysis.csv"
OUTPUT_PATH = "data/processed/loss_diagnostics.csv"
SUMMARY_PATH = "data/processed/loss_summary.csv"


df = pd.read_csv(INPUT_PATH)

df["timestamp"] = pd.to_datetime(
    df["timestamp"]
)


df["gross_generation_loss_mwh"] = (
    df["expected_energy_mwh"]
    - df["actual_energy_mwh"]
).clip(lower=0)


df["inverter_loss_mwh"] = (
    df["expected_energy_mwh"]
    * (1 - df["inverter_availability"])
)


df["tracker_loss_mwh"] = (
    df["expected_energy_mwh"]
    * (1 - df["tracker_availability"])
    * 0.65
)


df["grid_curtailment_loss_mwh"] = (
    df["expected_energy_mwh"]
    * df["grid_curtailment"]
    * 0.40
)


df["equipment_derate_loss_mwh"] = (
    df["expected_energy_mwh"]
    * (1 - df["equipment_derate_factor"])
)


df["soiling_loss_mwh"] = (
    df["expected_energy_mwh"]
    * (1 - df["soiling_factor"])
)


loss_columns = [
    "inverter_loss_mwh",
    "tracker_loss_mwh",
    "grid_curtailment_loss_mwh",
    "equipment_derate_loss_mwh",
    "soiling_loss_mwh"
]


df["diagnosed_loss_before_scaling_mwh"] = (
    df[loss_columns].sum(axis=1)
)


scale_factor = np.where(
    df["diagnosed_loss_before_scaling_mwh"] > 0,
    np.minimum(
        1,
        df["gross_generation_loss_mwh"]
        / df["diagnosed_loss_before_scaling_mwh"]
    ),
    0
)


for column in loss_columns:
    df[column] = (
        df[column]
        * scale_factor
    )


df["diagnosed_loss_mwh"] = (
    df[loss_columns].sum(axis=1)
)


df["residual_loss_mwh"] = (
    df["gross_generation_loss_mwh"]
    - df["diagnosed_loss_mwh"]
).clip(lower=0)


def classify_loss(row):

    if row["inverter_loss_mwh"] > 0:
        return "Inverter downtime"

    if row["tracker_loss_mwh"] > 0:
        return "Tracker downtime"

    if row["grid_curtailment_loss_mwh"] > 0:
        return "Grid curtailment"

    if row["equipment_derate_loss_mwh"] > 0:
        return "Equipment derate"

    if row["soiling_loss_mwh"] > 0:
        return "Soiling"

    if row["residual_loss_mwh"] > 0:
        return "Unexplained / residual"

    return "No material loss"


df["primary_loss_category"] = (
    df.apply(
        classify_loss,
        axis=1
    )
)


summary = pd.DataFrame({
    "loss_category": [
        "Inverter downtime",
        "Tracker downtime",
        "Grid curtailment",
        "Equipment derate",
        "Soiling",
        "Unexplained / residual"
    ],
    "loss_mwh": [
        df["inverter_loss_mwh"].sum(),
        df["tracker_loss_mwh"].sum(),
        df["grid_curtailment_loss_mwh"].sum(),
        df["equipment_derate_loss_mwh"].sum(),
        df["soiling_loss_mwh"].sum(),
        df["residual_loss_mwh"].sum()
    ]
})


total_loss = summary[
    "loss_mwh"
].sum()


if total_loss > 0:
    summary["loss_share_pct"] = (
        summary["loss_mwh"]
        / total_loss
        * 100
    )
else:
    summary["loss_share_pct"] = 0


df.to_csv(
    OUTPUT_PATH,
    index=False
)

summary.to_csv(
    SUMMARY_PATH,
    index=False
)


logger.info(
    "Loss diagnostics completed successfully"
)

logger.info(
    f"Total diagnosed loss: "
    f"{summary['loss_mwh'].sum():.2f} MWh"
)


print("LOSS DIAGNOSTICS")
print("=" * 40)

for _, row in summary.iterrows():

    print(
        f"{row['loss_category']:<25}"
        f"{row['loss_mwh']:>10.2f} MWh"
    )

print()

print(
    f"Saved to: {OUTPUT_PATH}"
)

print(
    f"Saved to: {SUMMARY_PATH}"
)