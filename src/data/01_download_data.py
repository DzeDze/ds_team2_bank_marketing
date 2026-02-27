import urllib.request
import zipfile
import shutil
import tempfile
import os
import sys
import pandas as pd
from tqdm import tqdm

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DATASET_URL = "https://archive.ics.uci.edu/static/public/222/bank+marketing.zip"
OUTER_ZIP   = "bank+marketing.zip"
INNER_ZIP   = "bank-additional.zip"
TARGET_FILE = "bank-additional-full.csv"

# Resolve data/raw relative to this script's location (src/data/ -> ../../data/raw)
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR  = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", "data", "raw"))
OUTPUT_PATH = os.path.join(OUTPUT_DIR, TARGET_FILE)

# Expected shape after loading
EXPECTED_ROWS = 41_188
EXPECTED_COLS = 21


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def download(url: str, dest: str) -> None:
    """Download a URL to dest with a tqdm progress bar."""
    print(f"  Downloading {url} ...")

    with urllib.request.urlopen(url) as response:
        total_size = int(response.headers.get("Content-Length", 0))
        block_size = 8192

        with tqdm(
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            desc="  bank+marketing.zip",
            ncols=70,
        ) as bar:
            with open(dest, "wb") as f:
                while True:
                    chunk = response.read(block_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    bar.update(len(chunk))


def extract_target_csv(outer_zip_path: str, tmp_dir: str) -> str:
    """
    Unzip outer zip -> find and unzip inner zip ->return path to target CSV.
    """
    # 1. Extract outer zip
    print(f"  Extracting outer zip ...")
    with zipfile.ZipFile(outer_zip_path, "r") as z:
        z.extractall(tmp_dir)

    # 2. Locate inner zip (search recursively in case structure varies)
    inner_zip_path = None
    for root, _, files in os.walk(tmp_dir):
        for f in files:
            if f == INNER_ZIP:
                inner_zip_path = os.path.join(root, f)
                break

    if inner_zip_path is None:
        raise FileNotFoundError(
            f"Could not find '{INNER_ZIP}' inside the downloaded archive. "
            "The UCI repository structure may have changed."
        )

    # 3. Extract inner zip
    print(f"  Extracting inner zip ...")
    with zipfile.ZipFile(inner_zip_path, "r") as z:
        z.extractall(tmp_dir)

    # 4. Locate target CSV
    csv_path = None
    for root, _, files in os.walk(tmp_dir):
        for f in files:
            if f == TARGET_FILE:
                csv_path = os.path.join(root, f)
                break

    if csv_path is None:
        raise FileNotFoundError(
            f"Could not find '{TARGET_FILE}' after extraction. "
            "The UCI repository structure may have changed."
        )

    return csv_path


def validate(path: str) -> pd.DataFrame:
    """Load the CSV and assert it matches the expected shape and columns."""
    print("  Validating dataset ...")

    df = pd.read_csv(path, sep=";")

    rows, cols = df.shape

    # Shape check
    if rows != EXPECTED_ROWS or cols != EXPECTED_COLS:
        raise ValueError(
            f"Unexpected shape: got ({rows}, {cols}), "
            f"expected ({EXPECTED_ROWS}, {EXPECTED_COLS})."
        )

    # Column check
    expected_columns = [
        "age", "job", "marital", "education", "default", "housing", "loan",
        "contact", "month", "day_of_week", "duration", "campaign", "pdays",
        "previous", "poutcome", "emp.var.rate", "cons.price.idx",
        "cons.conf.idx", "euribor3m", "nr.employed", "y",
    ]
    if list(df.columns) != expected_columns:
        raise ValueError(
            f"Column mismatch.\n  Got:      {list(df.columns)}\n"
            f"  Expected: {expected_columns}"
        )

    # No fully-empty rows
    empty_rows = df.isnull().all(axis=1).sum()
    if empty_rows > 0:
        raise ValueError(f"Dataset contains {empty_rows} completely empty row(s).")

    # Target column sanity check
    target_values = set(df["y"].unique())
    if not target_values.issubset({"yes", "no"}):
        raise ValueError(f"Unexpected values in target column 'y': {target_values}")

    print(f"Shape   : {rows} rows x {cols} columns")
    print(f"Columns : all {cols} expected columns present")
    print(f"Target  : values = {sorted(target_values)}")
    print(f"Class balance:")
    for val, count in df["y"].value_counts().items():
        print(f"      {val}: {count:,}  ({count/rows*100:.1f}%)")

    return df


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("Bank Marketing Dataset — Download & Validation")
    print("=" * 60)

    # Skip download if file already exists and is valid
    if os.path.exists(OUTPUT_PATH):
        print(f"\n[INFO] File already exists at:\n  {OUTPUT_PATH}")
        print("\n[Step 1/1] Validating existing file ...")
        try:
            validate(OUTPUT_PATH)
            print("\nDataset is already present and valid. Nothing to do.")
            return
        except ValueError as e:
            print(f"\n[WARN] Existing file failed validation: {e}")
            print("  Re-downloading ...")

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"\nOutput directory : {OUTPUT_DIR}")

    with tempfile.TemporaryDirectory() as tmp_dir:
        outer_zip = os.path.join(tmp_dir, OUTER_ZIP)

        # Step 1: Download
        print("\n[Step 1/3] Downloading ...")
        download(DATASET_URL, outer_zip)

        # Step 2: Extract
        print("\n[Step 2/3] Extracting ...")
        csv_path = extract_target_csv(outer_zip, tmp_dir)
        print(f"  Found: {csv_path}")

        # Step 3: Copy to destination
        shutil.copy(csv_path, OUTPUT_PATH)
        print(f"  Saved to: {OUTPUT_PATH}")

    # Step 4: Validate
    print("\n[Step 3/3] Validating ...")
    try:
        validate(OUTPUT_PATH)
    except ValueError as e:
        print(f"\nValidation failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nDone! Dataset saved and validated successfully.")
    print(f"   Path: {OUTPUT_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    main()
