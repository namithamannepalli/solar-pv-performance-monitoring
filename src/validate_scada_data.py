import pandas as pd


INPUT_PATH = "data/raw/solar_plant_scada.csv"
OUTPUT_PATH = "data/processed/validation_report.csv"


df = pd.read_csv(INPUT_PATH)

df["timestamp"] = pd.to_datetime(df["timestamp"])


validation_results = []


def add_check(check_name, invalid_count):
    validation_results.append({
        "check": check_name,
        "invalid_records": invalid_count,
        "status": "PASS" if invalid_count == 0 else "FAIL"
    })


# Missing values
missing_count = df.isnull().sum().sum()
add_check("Missing values", missing_count)


# Duplicate timestamps
duplicate_count = df["timestamp"].duplicated().sum()
add_check("Duplicate timestamps", duplicate_count)


# Irradiance
invalid_irradiance = (
    (df["irradiance_w_m2"] < 0)
    | (df["irradiance_w_m2"] > 1200)
).sum()

add_check("Irradiance range", invalid_irradiance)


# Expected power
invalid_expected_power = (
    (df["expected_power_mw"] < 0)
    | (df["expected_power_mw"] > 10)
).sum()

add_check("Expected power range", invalid_expected_power)


# Actual power
invalid_actual_power = (
    (df["actual_power_mw"] < 0)
    | (df["actual_power_mw"] > 10)
).sum()

add_check("Actual power range", invalid_actual_power)


# Availability
availability_columns = [
    "inverter_availability",
    "tracker_availability",
    "grid_availability"
]

for column in availability_columns:

    invalid_values = (
        (df[column] < 0)
        | (df[column] > 1)
    ).sum()

    add_check(
        f"{column} range",
        invalid_values
    )


# Grid curtailment
invalid_curtailment = (
    (df["grid_curtailment"] < 0)
    | (df["grid_curtailment"] > 1)
).sum()

add_check(
    "Grid curtailment range",
    invalid_curtailment
)


# Timestamp frequency
time_difference = df["timestamp"].diff().dropna()

unexpected_intervals = (
    time_difference != pd.Timedelta(minutes=15)
).sum()

add_check(
    "Timestamp interval",
    unexpected_intervals
)


# Create validation report
validation_report = pd.DataFrame(validation_results)


# Save report
validation_report.to_csv(
    OUTPUT_PATH,
    index=False
)


print("SCADA validation completed.")
print()
print(validation_report.to_string(index=False))
print()
print(f"Report saved to: {OUTPUT_PATH}")