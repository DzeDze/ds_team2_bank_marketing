import pandas as pd
from utils.data_manager import read_csv_data, save_processed_data

OUTPUT_FILE = "viz/segmentation_data.csv"
MIN_N = 200

def calc_baseline_conversion_rate(df: pd.DataFrame, target_col: str = "y") -> float:
    """
    Compute the baseline conversion rate for the full dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset containing the target column.
    target_col : str, default="y"
        Name of the target column. Assumes values are either:
        - binary numeric (0/1), or
        - strings like {"yes","no"}.

    Returns
    -------
    float
        Baseline conversion rate rounded to 4 decimals.
    """
    if target_col not in df.columns:
        raise ValueError(f"Column '{target_col}' is required to compute baseline conversion rate.")

    y = df[target_col]

    # Handle common bank dataset format: "yes"/"no"
    if y.dtype == "object":
        y = y.map({"yes": 1, "no": 0})

    baseline = y.mean()
    return round(float(baseline), 4)

def save_data(df: pd.DataFrame) -> None:
    """
    Save the segmentation output table to the processed data directory.

    Parameters
    ----------
    df : pd.DataFrame
        Segmentation results table to save.
    """
    save_processed_data(OUTPUT_FILE, df)

def evaluate_segments_full(
        data: pd.DataFrame, 
        group_vars: list[str], 
        baseline: float, 
        min_size=MIN_N,
        target_col: str = "y"
) -> pd.DataFrame:
    """Compute segment size, conversion, lift, and % customers on the full dataset.

    Parameters
    ----------
    data : pd.DataFrame
        Full dataset containing the target column.
    group_vars : list[str]
        Columns used to define segments (e.g., ["age_bucket", "loan"]).
    baseline : float
        Baseline conversion rate on the full dataset.
    min_size : int, default=MIN_N
        Minimum number of observations required for a segment to be included.
    target_col : str, default="y"
        Name of the target column.

    Returns
    -------
    pd.DataFrame
        Segment table with: n, conv, lift, pct_customers.
    """

    missing = [c for c in [*group_vars, target_col] if c not in data.columns]
    if missing:
        raise ValueError(f"Missing required column(s): {missing}")

    df = data.copy()

    # Ensure target is numeric for mean()
    if df[target_col].dtype == "object":
        df[target_col] = df[target_col].map({"yes": 1, "no": 0})

    seg = (
        df.groupby(group_vars, observed=True)
        .agg(
            n=(target_col, "size"),
            conv=(target_col, "mean"),
        )
        .reset_index()
    )

    seg["lift"] = seg["conv"] / baseline
    seg["pct_customers"] = seg["n"] / len(data) * 100

    # Minimum-size filter for reliability
    seg = seg.loc[seg["n"] >= min_size].copy()

    return seg.sort_values("lift", ascending=False)
    
def create_two_way_segmentation_table(
        df: pd.DataFrame, 
        two_way_vars: list[tuple[str, str]], 
        baseline: float, 
        min_size=MIN_N
) -> pd.DataFrame:
    """
    Create a combined two-way segmentation table for multiple variable pairs.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataset.
    two_way_vars : list[tuple[str, str]]
        List of column pairs to segment by, e.g. [("age_bucket","loan"), ...].
    baseline : float
        Baseline conversion rate used for lift calculation.
    min_size : int, default=MIN_N
        Minimum segment size threshold.

    Returns
    -------
    pd.DataFrame
        Stacked segmentation results with columns:
        segment_type, segment, n, pct_customers, conv, lift
    """

    if not two_way_vars:
        raise ValueError("two_way_vars is empty. Provide at least one (var_a, var_b) pair.")
    
    tables: list[pd.DataFrame] = []

    for a, b in two_way_vars:
        seg = evaluate_segments_full(df, [a, b], baseline, min_size=min_size)

        seg["segment"] = seg[a].astype(str) + " & " + seg[b].astype(str)
        seg["segment_type"] = f"{a} x {b}"

        tables.append(seg[["segment_type", "segment", "n", "pct_customers", "conv", "lift"]])

    return pd.concat(tables, ignore_index=True)

def save_two_way_segmentation_data(results: pd.DataFrame, output_file: str = OUTPUT_FILE) -> None:
    """
    Save the two-way segmentation results to the processed data directory.
    Parameters
    ----------
    results : pd.DataFrame
        Segmentation results table produced by `create_two_way_segmentation_table`.
    output_file : str, default=OUTPUT_FILE
        Relative path under `data/processed/` to save to.
    """
    save_processed_data(output_file, results)

def main():
    """Run two-way segmentation generation and save results for visualization."""
    data = read_csv_data("processed/processed_bank_full.csv")

    two_way_tests = [
        ("age_bucket", "loan"),
        ("age_bucket", "housing"),
        ("loan", "housing"),
        ("balance_bucket", "loan"),
        ("balance_bucket", "housing"),
        ("balance_bucket", "age_bucket"),
        ("job", "loan"),
        ("job", "housing"),
        ("marital", "loan"),
        ("marital", "housing"),
        ("education", "job"),
        ("education", "loan"),
        ("age_bucket", "marital"),
        ("age_bucket", "job"),
        ("balance_bucket", "job"),
        ("balance_bucket", "marital"),
    ]
    baseline = calc_baseline_conversion_rate(data)
    results = create_two_way_segmentation_table(data, two_way_tests, baseline)
    save_two_way_segmentation_data(results)

if __name__ == "__main__":
    main()