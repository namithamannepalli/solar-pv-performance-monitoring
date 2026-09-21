import pandas as pd

from config import ENERGY_PRICE_USD_PER_MWH
from logger import get_logger


logger = get_logger("financial_impact")

INPUT_PATH = "data/processed/loss_summary.csv"
OUTPUT_PATH = "data/processed/financial_impact.csv"


loss_summary = pd.read_csv(INPUT_PATH)


loss_summary["estimated_revenue_loss_usd"] = (
    loss_summary["loss_mwh"]
    * ENERGY_PRICE_USD_PER_MWH
)


loss_summary["estimated_revenue_loss_kusd"] = (
    loss_summary["estimated_revenue_loss_usd"]
    / 1000
)


loss_summary.to_csv(
    OUTPUT_PATH,
    index=False
)


total_loss_mwh = (
    loss_summary["loss_mwh"].sum()
)

total_revenue_loss = (
    loss_summary["estimated_revenue_loss_usd"].sum()
)


logger.info(
    f"Total diagnosed loss: "
    f"{total_loss_mwh:.2f} MWh"
)

logger.info(
    f"Estimated revenue impact: "
    f"${total_revenue_loss:,.2f}"
)


print("FINANCIAL IMPACT SUMMARY")
print("=" * 40)

print(
    f"Total diagnosed loss     : "
    f"{total_loss_mwh:.2f} MWh"
)

print(
    f"Estimated revenue impact : "
    f"${total_revenue_loss:,.2f}"
)

print()

print(
    f"Saved to: {OUTPUT_PATH}"
)