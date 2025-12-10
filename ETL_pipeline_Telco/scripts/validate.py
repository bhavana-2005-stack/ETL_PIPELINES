import os
import pandas as pd

def validate_data():

    # ----------------------------------------------------
    # PATH SETUP
    # ----------------------------------------------------
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    staged_path = os.path.join(base_dir, "data", "staged", "churn_staged.csv")

    # ----------------------------------------------------
    # LOAD STAGED DATA
    # ----------------------------------------------------
    print("📄 Loading staged dataset...")
    df = pd.read_csv(staged_path)

    print("\n🔹 Total Rows:", len(df))

    # ----------------------------------------------------
    # 1. CHECK MISSING VALUES (Critical Columns)
    # ----------------------------------------------------
    print("\n❗ Missing Values Check (Critical Columns):")
    critical_cols = ["tenure", "MonthlyCharges", "TotalCharges"]

    for col in critical_cols:
        miss = df[col].isna().sum()
        print(f"{col}: {miss} missing")

    # ----------------------------------------------------
    # 2. CHECK DUPLICATES
    # ----------------------------------------------------
    duplicates = df.duplicated().sum()
    print(f"\n🔹 Duplicate Rows: {duplicates}")

    # ----------------------------------------------------
    # 3. CHECK SEGMENT COLUMNS
    # ----------------------------------------------------
    print("\n🔹 Segment Validation:")

    valid_tenure_groups = {"New", "Regular", "Loyal", "Champion"}
    tg_invalid = df[~df["tenure_group"].isin(valid_tenure_groups)]
    print(f"Invalid tenure_group rows: {len(tg_invalid)}")

    valid_charge_segments = {"Low", "Medium", "High"}
    cs_invalid = df[~df["monthly_charge_segment"].isin(valid_charge_segments)]
    print(f"Invalid monthly_charge_segment rows: {len(cs_invalid)}")

    # ----------------------------------------------------
    # 4. CONTRACT CODE VALIDATION
    # ----------------------------------------------------
    allowed_contract_codes = {0, 1, 2}
    invalid_contract = df[~df["contract_type_code"].isin(allowed_contract_codes)]
    print(f"\nInvalid contract_type_code rows: {len(invalid_contract)}")

    # ----------------------------------------------------
    # 5. VALIDATION SUMMARY
    # ----------------------------------------------------
    print("\n============================")
    print("✅ VALIDATION SUMMARY")
    print("============================")

    print(f"Total Rows: {len(df)}")
    print(f"Missing in Critical Columns: "
          f"{sum(df[col].isna().sum() for col in critical_cols)}")
    print(f"Duplicates: {duplicates}")
    print(f"Invalid tenure_group: {len(tg_invalid)}")
    print(f"Invalid monthly_charge_segment: {len(cs_invalid)}")
    print(f"Invalid contract_type_code: {len(invalid_contract)}")

    print("\n🎉 Validation Complete!")

if __name__ == "__main__":
    validate_data()
