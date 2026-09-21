import subprocess
import sys

from logger import get_logger


logger = get_logger("pipeline")


STEPS = [
    "src/generate_scada_data.py",
    "src/validate_scada_data.py",
    "src/performance_analysis.py",
    "src/loss_diagnostics.py",
    "src/financial_impact.py",
    "src/anomaly_detection.py",
    "src/forecast_analysis.py",
    "src/generate_report.py"
]


def run_step(script):
    logger.info(f"Starting {script}")

    try:
        subprocess.run(
            [sys.executable, script],
            check=True
        )

        logger.info(f"Completed {script}")

    except subprocess.CalledProcessError:
        logger.error(
            f"Pipeline failed while running {script}"
        )
        raise


def main():
    logger.info("Solar PV analytics pipeline started")

    for step in STEPS:
        run_step(step)

    logger.info(
        "Solar PV analytics pipeline completed successfully"
    )


if __name__ == "__main__":
    main()