import os
import pandas as pd

def extract_data():

    # Base directory (scripts folder → go one level up)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    raw_dir = os.path.join(base_dir, "data", "raw")

    # ---------------------------------------------
    # 1. PATH TO YOUR DOWNLOADED FILE
    # ---------------------------------------------
    # ❗ Update this path to where your CSV is stored
    downloaded_file_path = r"C:\Users\bhava\Downloads\WA_Fn-UseC_-Telco-Customer-Churn.csv"

    print("📄 Loading downloaded CSV...")
    df = pd.read_csv(downloaded_file_path)

    # ---------------------------------------------
    # 2. SAVE RAW COPY INTO data/raw/
    # ---------------------------------------------
    output_path = os.path.join(raw_dir, "churn_raw.csv")

    df.to_csv(output_path, index=False)

    print(f"✅ Raw dataset saved to: {output_path}")


if __name__ == "__main__":
    extract_data()