import pandas as pd

from config import DATA_INTERVAL_HOURS, PLANT_CAPACITY_MW
from logger import get_logger


logger = get_logger("performance_analysis")

INPUT_PATH = "data/raw/solar_plant_scada.csv"
OUTPUT_PATH = "data/processed/performance_analysis.csv"

DAILY_OUTPUT_PATH = "data/processed/daily_performance.csv"
MONTHLY_OUTPUT_PATH = "data/processed/monthly_performance.csv"


df = pd.read_csv(INPUT_PATH)

df["timestamp"] = pd.to_datetime(
    df["timestamp"]
)


df["expected_energy_mwh"] = (
    df["expected_power_mw"]
    * DATA_INTERVAL_HOURS
)

df["actual_energy_mwh"] = (
    df["actual_power_mw"]
    * DATA_INTERVAL_HOURS
)

df["generation_gap_mwh"] = (
    df["expected_energy_mwh"]
    - df["actual_energy_mwh"]
)


df["performance_ratio"] = (
    df["actual_energy_mwh"]
    / df["expected_energy_mwh"]
)

df["performance_ratio"] = (
    df["performance_ratio"]
    .replace([float("inf"), -float("inf")], 0)
    .fillna(0)
)


total_expected = df[
    "expected_energy_mwh"
].sum()

total_actual = df[
    "actual_energy_mwh"
].sum()

total_generation_loss = df[
    "generation_gap_mwh"
].sum()


overall_performance_ratio = (
    total_actual
    / total_expected
)


total_hours = (
    len(df)
    * DATA_INTERVAL_HOURS
)

maximum_possible_energy = (
    PLANT_CAPACITY_MW
    * total_hours
)

capacity_factor = (
    total_actual
    / maximum_possible_energy
)


plant_availability = (
    df[
        [
            "inverter_availability",
            "tracker_availability",
            "grid_availability"
        ]
    ]
    .mean(axis=1)
    .mean()
)


daily = (
    df.assign(
        date=df["timestamp"].dt.date
    )
    .groupby("date")
    .agg(
        expected_generation_mwh=(
            "expected_energy_mwh",
            "sum"
        ),
        actual_generation_mwh=(
            "actual_energy_mwh",
            "sum"
        ),
        generation_loss_mwh=(
            "generation_gap_mwh",
            "sum"
        ),
        avg_irradiance_w_m2=(
            "irradiance_w_m2",
            "mean"
        ),
        plant_availability=(
            "inverter_availability",
            "mean"
        )
    )
    .reset_index()
)


daily["performance_ratio"] = (
    daily["actual_generation_mwh"]
    / daily["expected_generation_mwh"]
)


monthly = (
    df.assign(
        month=df["timestamp"]
        .dt.to_period("M")
        .astype(str)
    )
    .groupby("month")
    .agg(
        expected_generation_mwh=(
            "expected_energy_mwh",
            "sum"
        ),
        actual_generation_mwh=(
            "actual_energy_mwh",
            "sum"
        ),
        generation_loss_mwh=(
            "generation_gap_mwh",
            "sum"
        ),
        avg_irradiance_w_m2=(
            "irradiance_w_m2",
            "mean"
        )
    )
    .reset_index()
)


monthly["performance_ratio"] = (
    monthly["actual_generation_mwh"]
    / monthly["expected_generation_mwh"]
)


df.to_csv(
    OUTPUT_PATH,
    index=False
)

daily.to_csv(
    DAILY_OUTPUT_PATH,
    index=False
)

monthly.to_csv(
    MONTHLY_OUTPUT_PATH,
    index=False
)


logger.info(
    f"Total expected generation: "
    f"{total_expected:.2f} MWh"
)

logger.info(
    f"Total actual generation: "
    f"{total_actual:.2f} MWh"
)

logger.info(
    f"Total generation loss: "
    f"{total_generation_loss:.2f} MWh"
)

logger.info(
    f"Overall performance ratio: "
    f"{overall_performance_ratio * 100:.2f}%"
)

logger.info(
    f"Capacity factor: "
    f"{capacity_factor * 100:.2f}%"
)

print("PERFORMANCE ANALYSIS")
print("=" * 40)

print(
    f"Expected generation : "
    f"{total_expected:.2f} MWh"
)

print(
    f"Actual generation   : "
    f"{total_actual:.2f} MWh"
)

print(
    f"Generation loss     : "
    f"{total_generation_loss:.2f} MWh"
)

print(
    f"Performance ratio   : "
    f"{overall_performance_ratio * 100:.2f}%"
)

print(
    f"Capacity factor     : "
    f"{capacity_factor * 100:.2f}%"
)

print(
    f"Plant availability  : "
    f"{plant_availability * 100:.2f}%"
)

print()

print(
    f"Saved to: {OUTPUT_PATH}"
)