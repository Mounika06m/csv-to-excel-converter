import argparse
import logging
import pandas as pd
import sys
import os

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def clean_data(df):
    df = df.dropna(how="all")
    df = df.fillna("N/A")
    for col in df.columns:
        try:
            df[col] = pd.to_datetime(df[col], format="mixed", dayfirst=False)
        except (ValueError, TypeError):
            pass
    return df

def convert(input_path, output_path):
    if not os.path.exists(input_path):
        logging.error(f"File not found: {input_path}")
        sys.exit(1)
    try:
        df = pd.read_csv(input_path)
        logging.info(f"Read {len(df)} rows from {input_path}")
    except Exception as e:
        logging.error(f"Failed to read CSV: {e}")
        sys.exit(1)

    df = clean_data(df)

    try:
        df.to_excel(output_path, index=False, engine="openpyxl")
        logging.info(f"Saved to {output_path}")
    except Exception as e:
        logging.error(f"Failed to write Excel: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CSV to Excel Converter")
    parser.add_argument("--input", required=True, help="Path to input CSV")
    parser.add_argument("--output", required=True, help="Path to output .xlsx")
    args = parser.parse_args()
    convert(args.input, args.output)