import os
import pandas as pd

def transform_data():

    # ----------------------------------------------------
    # PATH SETUP
    # ----------------------------------------------------
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    raw_path = os.path.join(base_dir, "data", "raw", "churn_raw.csv")
    staged_path = os.path.join(base_dir, "data", "staged", "churn_staged.csv")

    # ----------------------------------------------------
    # LOAD RAW DATA
    # ----------------------------------------------------
    print("📄 Loading raw dataset...")
    df = pd.read_csv(raw_path)

    # ----------------------------------------------------
    # ✔ CLEANING TASKS
    # ----------------------------------------------------

    # Convert TotalCharges to numeric (spaces → NaN)
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    # Fill missing numeric values with median
    numeric_cols = ["tenure", "MonthlyCharges", "TotalCharges"]
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    # Fill missing categorical values with "Unknown"
    cat_cols = df.select_dtypes(include=["object"]).columns
    for col in cat_cols:
        df[col] = df[col].fillna("Unknown")

    # ----------------------------------------------------
    # ✔ FEATURE ENGINEERING
    # ----------------------------------------------------

    # 1. tenure_group
    def tenure_group(t):
        if t <= 12:
            return "New"
        elif t <= 36:
            return "Regular"
        elif t <= 60:
            return "Loyal"
        else:
            return "Champion"

    df["tenure_group"] = df["tenure"].apply(tenure_group)

    # 2. monthly_charge_segment
    def charge_segment(m):
        if m < 30:
            return "Low"
        elif m <= 70:
            return "Medium"
        else:
            return "High"

    df["monthly_charge_segment"] = df["MonthlyCharges"].apply(charge_segment)

    # 3. has_internet_service
    df["has_internet_service"] = df["InternetService"].map({
        "DSL": 1,
        "Fiber optic": 1,
        "No": 0
    }).fillna(0)

    # 4. is_multi_line_user
    df["is_multi_line_user"] = df["MultipleLines"].apply(lambda x: 1 if x == "Yes" else 0)

    # 5. contract_type_code
    df["contract_type_code"] = df["Contract"].map({
        "Month-to-month": 0,
        "One year": 1,
        "Two year": 2
    }).fillna(-1)

    # ----------------------------------------------------
    # ✔ DROP UNNEEDED COLUMNS
    # ----------------------------------------------------
    df.drop(["customerID", "gender"], axis=1, inplace=True)

    # ----------------------------------------------------
    # SAVE STAGED OUTPUT
    # ----------------------------------------------------
    df.to_csv(staged_path, index=False)
    print(f"✅ Transformed dataset saved to: {staged_path}")


if __name__ == "__main__":
    transform_data()