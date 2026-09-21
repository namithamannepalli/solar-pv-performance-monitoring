import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Solar PV Asset Performance",
    page_icon="☀️",
    layout="wide"
)


PERFORMANCE_PATH = (
    "data/processed/performance_analysis.csv"
)

LOSS_PATH = (
    "data/processed/loss_summary.csv"
)

FINANCIAL_PATH = (
    "data/processed/financial_impact.csv"
)

ANOMALY_PATH = (
    "data/processed/anomaly_detection.csv"
)


@st.cache_data
def load_data():

    performance = pd.read_csv(
        PERFORMANCE_PATH
    )

    losses = pd.read_csv(
        LOSS_PATH
    )

    financial = pd.read_csv(
        FINANCIAL_PATH
    )

    anomalies = pd.read_csv(
        ANOMALY_PATH
    )

    performance["timestamp"] = pd.to_datetime(
        performance["timestamp"]
    )

    anomalies["timestamp"] = pd.to_datetime(
        anomalies["timestamp"]
    )

    return (
        performance,
        losses,
        financial,
        anomalies
    )


performance, losses, financial, anomalies = (
    load_data()
)


st.title(
    "☀️ Solar PV Plant Performance Dashboard"
)

st.caption(
    "SCADA-based performance monitoring, "
    "loss diagnostics and anomaly detection"
)


st.sidebar.header("Dashboard Filters")


min_date = (
    performance["timestamp"]
    .dt.date
    .min()
)

max_date = (
    performance["timestamp"]
    .dt.date
    .max()
)


selected_dates = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


if len(selected_dates) == 2:

    start_date = selected_dates[0]
    end_date = selected_dates[1]

    filtered_performance = performance[
        (
            performance["timestamp"].dt.date
            >= start_date
        )
        &
        (
            performance["timestamp"].dt.date
            <= end_date
        )
    ].copy()

else:

    filtered_performance = performance.copy()


total_expected = (
    filtered_performance[
        "expected_energy_mwh"
    ].sum()
)


total_actual = (
    filtered_performance[
        "actual_energy_mwh"
    ].sum()
)


total_loss = max(
    0,
    total_expected - total_actual
)


if total_expected > 0:

    performance_ratio = (
        total_actual
        / total_expected
        * 100
    )

else:

    performance_ratio = 0


plant_availability = (
    filtered_performance[
        [
            "inverter_availability",
            "tracker_availability",
            "grid_availability"
        ]
    ]
    .mean(axis=1)
    .mean()
    * 100
)


col1, col2, col3, col4, col5 = (
    st.columns(5)
)


col1.metric(
    "Expected Generation",
    f"{total_expected:,.1f} MWh"
)


col2.metric(
    "Actual Generation",
    f"{total_actual:,.1f} MWh"
)


col3.metric(
    "Generation Loss",
    f"{total_loss:,.1f} MWh"
)


col4.metric(
    "Performance Ratio",
    f"{performance_ratio:.2f}%"
)


col5.metric(
    "Plant Availability",
    f"{plant_availability:.2f}%"
)


st.divider()


st.subheader(
    "Generation Performance"
)


daily = (
    filtered_performance
    .assign(
        date=filtered_performance[
            "timestamp"
        ].dt.date
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
        )
    )
    .reset_index()
)


generation_fig = px.line(
    daily,
    x="date",
    y=[
        "expected_generation_mwh",
        "actual_generation_mwh"
    ],
    markers=True,
    labels={
        "value": "Energy (MWh)",
        "variable": "Generation Type",
        "date": "Date"
    },
    title="Actual vs Expected Daily Generation"
)


st.plotly_chart(
    generation_fig,
    use_container_width=True
)


st.divider()


left, right = st.columns(2)


with left:

    st.subheader(
        "Generation Loss Breakdown"
    )

    loss_fig = px.bar(
        losses,
        x="loss_category",
        y="loss_mwh",
        labels={
            "loss_category": "Loss Category",
            "loss_mwh": "Loss (MWh)"
        },
        title="Diagnosed Energy Loss"
    )

    st.plotly_chart(
        loss_fig,
        use_container_width=True
    )


with right:

    st.subheader(
        "Financial Impact"
    )

    financial_display = financial[
        [
            "loss_category",
            "loss_mwh",
            "estimated_revenue_loss_usd"
        ]
    ].copy()

    financial_display[
        "estimated_revenue_loss_usd"
    ] = financial_display[
        "estimated_revenue_loss_usd"
    ].round(2)

    st.dataframe(
        financial_display,
        use_container_width=True,
        hide_index=True
    )


st.divider()


st.subheader(
    "Anomaly Detection"
)


anomaly_count = int(
    anomalies["anomaly_flag"].sum()
)


anomaly_col1, anomaly_col2 = (
    st.columns(2)
)


anomaly_col1.metric(
    "Detected Anomalies",
    anomaly_count
)


daytime_anomalies = anomalies[
    anomalies["anomaly_flag"] == 1
].copy()


if not daytime_anomalies.empty:

    st.dataframe(
        daytime_anomalies[
            [
                "timestamp",
                "irradiance_w_m2",
                "actual_power_mw",
                "expected_power_mw",
                "generation_gap_mwh",
                "anomaly_score"
            ]
        ]
        .sort_values(
            "anomaly_score"
        ),
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No anomalies detected."
    )


st.divider()


st.subheader(
    "Operating Conditions"
)


operating_fig = px.line(
    filtered_performance,
    x="timestamp",
    y=[
        "irradiance_w_m2",
        "actual_power_mw"
    ],
    labels={
        "value": "Value",
        "variable": "Signal",
        "timestamp": "Time"
    },
    title="Irradiance and Actual Power"
)


st.plotly_chart(
    operating_fig,
    use_container_width=True
)


st.divider()


st.subheader(
    "Loss Distribution"
)


loss_pie = px.pie(
    losses,
    names="loss_category",
    values="loss_mwh",
    title="Share of Diagnosed Loss"
)


st.plotly_chart(
    loss_pie,
    use_container_width=True
)


st.caption(
    "Data shown in this dashboard is simulated for "
    "portfolio demonstration and analytics development."
)