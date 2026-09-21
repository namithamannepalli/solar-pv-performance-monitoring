import pandas as pd


def test_energy_conversion():
    data = pd.DataFrame({
        "power_mw": [10, 5, 0]
    })

    energy = (
        data["power_mw"] * 0.25
    )

    assert energy.tolist() == [
        2.5,
        1.25,
        0.0
    ]


def test_performance_ratio():
    expected = 100
    actual = 90

    performance_ratio = (
        actual / expected
    )

    assert performance_ratio == 0.9


def test_capacity_factor():
    actual_energy = 2160
    plant_capacity = 10
    total_hours = 2160

    capacity_factor = (
        actual_energy
        / (plant_capacity * total_hours)
    )

    assert capacity_factor == 0.1