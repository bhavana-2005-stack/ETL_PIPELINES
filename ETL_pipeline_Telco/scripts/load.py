import os
import pandas as pd
import time
from supabase import create_client, Client

# ----------------------------------------------------
# CONFIG: Supabase (FILL THESE)
# ----------------------------------------------------
SUPABASE_URL="https://mwqgjwirrsauufbihoyq.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im13cWdqd2lycnNhdXVmYmlob3lxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NTMzMDEwMywiZXhwIjoyMDgwOTA2MTAzfQ.3LtVF_1ZYyMjC_EMRPJjqk6MYg4oexfa0J3o9q12aGo"
TABLE_NAME="telco_churn2"

# ----------------------------------------------------
# BATCH SETTINGS
# ----------------------------------------------------
BATCH_SIZE = 200
RETRY_COUNT = 3
RETRY_DELAY = 2  # seconds


def load_to_supabase():
    # ----------------------------------------------------
    # PATH SETUP
    # ----------------------------------------------------
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    staged_path = os.path.join(base_dir, "data", "staged", "churn_staged.csv")

    # ----------------------------------------------------
    # LOAD TRANSFORMED CSV
    # ----------------------------------------------------
    print("📄 Loading transformed dataset...")
    df = pd.read_csv(staged_path)

    # Keep only the columns required for Supabase table
    required_columns = [
        "tenure",
        "MonthlyCharges",
        "TotalCharges",
        "Churn",
        "InternetService",
        "Contract",
        "PaymentMethod",
        "tenure_group",
        "monthly_charge_segment",
        "has_internet_service",
        "is_multi_line_user",
        "contract_type_code"
    ]

    df = df[required_columns]

    # Replace NaN with None
    df = df.where(pd.notnull(df), None)

    # ----------------------------------------------------
    # CONNECT TO SUPABASE
    # ----------------------------------------------------
    print("🔗 Connecting to Supabase...")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    print(f"✅ Using existing Supabase table: {TABLE_NAME}")

    # ----------------------------------------------------
    # INSERT IN BATCHES
    # ----------------------------------------------------
    print(f"🚀 Loading data into Supabase in batches of {BATCH_SIZE}...")

    total_rows = len(df)

    for start in range(0, total_rows, BATCH_SIZE):
        end = min(start + BATCH_SIZE, total_rows)
        batch = df.iloc[start:end].to_dict(orient="records")

        attempt = 0
        while attempt < RETRY_COUNT:
            try:
                supabase.table(TABLE_NAME).insert(batch).execute()
                print(f"✅ Inserted rows {start} to {end - 1}")
                break
            except Exception as e:
                attempt += 1
                print(f"❌ Error inserting batch {start}-{end-1}, attempt {attempt}: {e}")
                time.sleep(RETRY_DELAY)

        else:
            print(f"⚠️ Failed to insert batch {start}-{end-1} after {RETRY_COUNT} attempts")

    print("🎉 Data load complete!")


if __name__ == "__main__":
    load_to_supabase()
