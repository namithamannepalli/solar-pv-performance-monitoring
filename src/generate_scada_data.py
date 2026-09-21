import numpy as np
import pandas as pd


PLANT_CAPACITY_MW = 10
DATA_FREQUENCY = "15min"
SIMULATION_DAYS = 90


timestamps = pd.date_range(
    start="2026-01-01",
    periods=SIMULATION_DAYS * 96,
    freq=DATA_FREQUENCY
)

hours = np.asarray(
    timestamps.hour + timestamps.minute / 60,
    dtype=float
)

solar_angle = np.pi * (hours - 6) / 12

irradiance = np.where(
    (hours >= 6) & (hours <= 18),
    np.sin(solar_angle),
    0
)

irradiance = np.maximum(irradiance, 0)

# Add realistic day-to-day weather variation
rng = np.random.default_rng(42)

daily_weather_factor = rng.uniform(
    0.75,
    1.05,
    size=SIMULATION_DAYS
)

weather_factor = np.repeat(daily_weather_factor, 96)

irradiance_w_m2 = (
    1000
    * irradiance
    * weather_factor
)

irradiance_w_m2 = np.clip(
    irradiance_w_m2,
    0,
    1000
)


# Ambient temperature
day_of_year = np.asarray(
    timestamps.dayofyear,
    dtype=float
)
ambient_temperature_c = (
    28
    + 6 * np.sin(2 * np.pi * (day_of_year - 30) / 365)
    + 4 * np.sin(2 * np.pi * (hours - 6) / 24)
)


# Module temperature
module_temperature_c = (
    ambient_temperature_c
    + 20 * (irradiance_w_m2 / 1000)
)


# Expected power generation
temperature_coefficient = 0.004

temperature_loss = (
    1
    - temperature_coefficient
    * np.maximum(module_temperature_c - 25, 0)
)

expected_power_mw = (
    PLANT_CAPACITY_MW
    * (irradiance_w_m2 / 1000)
    * temperature_loss
)

expected_power_mw = np.clip(
    expected_power_mw,
    0,
    PLANT_CAPACITY_MW
)


# Equipment availability
inverter_availability = np.ones(len(timestamps))
tracker_availability = np.ones(len(timestamps))
grid_availability = np.ones(len(timestamps))

grid_curtailment = np.zeros(len(timestamps))


# Actual power initially equals expected power
actual_power_mw = expected_power_mw.copy()


# Introduce inverter downtime
inverter_start = 1500
inverter_end = 1530

inverter_availability[inverter_start:inverter_end] = 0
actual_power_mw[inverter_start:inverter_end] = 0


# Introduce tracker downtime
tracker_start = 4000
tracker_end = 4040

tracker_availability[tracker_start:tracker_end] = 0
actual_power_mw[tracker_start:tracker_end] *= 0.35


# Introduce grid curtailment
curtailment_start = 5500
curtailment_end = 5560

grid_curtailment[curtailment_start:curtailment_end] = 1
actual_power_mw[curtailment_start:curtailment_end] *= 0.60


# Introduce equipment derating
derate_start = 7000
derate_end = 7080

actual_power_mw[derate_start:derate_end] *= 0.75


# Introduce gradual soiling
soiling_start = 7500

soiling_factor = np.ones(len(timestamps))

soiling_factor[soiling_start:] = np.linspace(
    1.0,
    0.88,
    len(timestamps) - soiling_start
)

actual_power_mw *= soiling_factor


# Add small measurement noise
noise = rng.normal(
    0,
    0.02,
    size=len(timestamps)
)

actual_power_mw += noise

actual_power_mw = np.clip(
    actual_power_mw,
    0,
    PLANT_CAPACITY_MW
)


# Create SCADA dataframe
scada_data = pd.DataFrame({
    "timestamp": timestamps,
    "irradiance_w_m2": irradiance_w_m2,
    "ambient_temperature_c": ambient_temperature_c,
    "module_temperature_c": module_temperature_c,
    "expected_power_mw": expected_power_mw,
    "actual_power_mw": actual_power_mw,
    "inverter_availability": inverter_availability,
    "tracker_availability": tracker_availability,
    "grid_availability": grid_availability,
    "grid_curtailment": grid_curtailment
})


# Save dataset
output_path = "data/raw/solar_plant_scada.csv"

scada_data.to_csv(
    output_path,
    index=False
)

print("SCADA dataset generated successfully.")
print(f"Records: {len(scada_data)}")
print(f"Saved to: {output_path}")