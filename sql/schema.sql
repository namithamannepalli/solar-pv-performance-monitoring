CREATE TABLE IF NOT EXISTS solar_scada (
    timestamp TIMESTAMP PRIMARY KEY,
    irradiance_w_m2 DOUBLE PRECISION,
    ambient_temperature_c DOUBLE PRECISION,
    module_temperature_c DOUBLE PRECISION,
    expected_power_mw DOUBLE PRECISION,
    actual_power_mw DOUBLE PRECISION,
    inverter_availability DOUBLE PRECISION,
    tracker_availability DOUBLE PRECISION,
    grid_availability DOUBLE PRECISION,
    grid_curtailment DOUBLE PRECISION,
    equipment_derate_factor DOUBLE PRECISION,
    soiling_factor DOUBLE PRECISION
);


CREATE TABLE IF NOT EXISTS plant_performance (
    timestamp TIMESTAMP PRIMARY KEY,
    expected_energy_mwh DOUBLE PRECISION,
    actual_energy_mwh DOUBLE PRECISION,
    generation_gap_mwh DOUBLE PRECISION,
    performance_ratio DOUBLE PRECISION
);


CREATE INDEX IF NOT EXISTS idx_solar_scada_timestamp
ON solar_scada(timestamp);