import os
import pandas as pd
import matplotlib.pyplot as plt
from supabase import create_client
from dotenv import load_dotenv

# ---------------------------------------------
# CONNECT TO SUPABASE
# ---------------------------------------------
def connect_supabase():
    load_dotenv()

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise Exception("❌ Missing SUPABASE_URL or SUPABASE_KEY in .env")

    print("🔗 Connecting to Supabase...")
    return create_client(url, key)


# ---------------------------------------------
# MAIN ANALYSIS FUNCTION
# ---------------------------------------------
def analyze_data():
    supabase = connect_supabase()

    print("📥 Fetching table from Supabase...")
    response = supabase.table("telco_churn2").select("*").execute()
    data = response.data

    if not data:
        raise Exception("❌ No data found in Supabase table.")

    df = pd.DataFrame(data)

    print(f"📌 Loaded {len(df)} rows from Supabase")

    # ---------------------------------------------
    # METRICS
    # ---------------------------------------------

    churn_percentage = (df["Churn"].value_counts(normalize=True) * 100).round(2)

    avg_monthly_by_contract = (
        df.groupby("Contract")["MonthlyCharges"].mean().round(2)
    )

    customer_segments = df["tenure_group"].value_counts()

    internet_dist = df["InternetService"].value_counts()

    # Pivot Table FIXED (no customerID)
    churn_pivot = df.pivot_table(
        index="tenure_group",
        columns="Churn",
        aggfunc="size",
        fill_value=0
    )

    # ---------------------------------------------
    # CREATE OUTPUT DIRECTORY
    # ---------------------------------------------
    out_dir = os.path.join("..", "data", "processed")
    os.makedirs(out_dir, exist_ok=True)

    # ---------------------------------------------
    # SAVE CSV SUMMARY
    # ---------------------------------------------
    summary = {
        "churn_percentage": churn_percentage.to_dict(),
        "avg_monthly_by_contract": avg_monthly_by_contract.to_dict(),
        "customer_segments": customer_segments.to_dict(),
        "internet_service_distribution": internet_dist.to_dict(),
        "churn_vs_tenure_group": churn_pivot.to_dict()
    }

    summary_path = os.path.join(out_dir, "analysis_summary.csv")
    pd.DataFrame(dict([(k, pd.Series(v)) for k, v in summary.items()])).to_csv(summary_path)

    print(f"📄 Analysis summary saved to: {summary_path}")

    # ---------------------------------------------
    # VISUALIZATIONS
    # ---------------------------------------------
    print("📊 Generating charts...")

    # 1. Churn rate by Monthly Charge Segment
    plt.figure(figsize=(8, 5))
    df.groupby("monthly_charge_segment")["Churn"].value_counts(normalize=True).unstack().plot(kind="bar")
    plt.title("Churn Rate by Monthly Charge Segment")
    plt.xlabel("Monthly Charge Segment")
    plt.ylabel("Rate")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "churn_rate_by_monthly_charge_segment.png"))
    plt.close()

    # 2. Histogram of TotalCharges
    plt.figure(figsize=(8, 5))
    df["TotalCharges"].hist(bins=30)
    plt.title("Histogram of Total Charges")
    plt.xlabel("Total Charges")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "total_charges_histogram.png"))
    plt.close()

    # 3. Bar plot of Contract types
    plt.figure(figsize=(8, 5))
    df["Contract"].value_counts().plot(kind="bar")
    plt.title("Contract Type Distribution")
    plt.xlabel("Contract Type")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "contract_type_distribution.png"))
    plt.close()

    print(f"📂 All charts saved inside: {out_dir}")
    print("🎉 Analysis Complete!")


# ---------------------------------------------
# RUN
# ---------------------------------------------
if __name__ == "__main__":
    analyze_data()
