"""
src/pipelines/train_models.py

Trains and saves:
- Decision Tree pipeline (explainable rules)
- Logistic Regression pipeline (ranking)

Saves artifacts under artifacts/models/.
"""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier

from config import CFG
from utils.data_manager import read_csv_data
from utils.preprocessing import ensure_target_numeric

def make_preprocess(X: pd.DataFrame) -> ColumnTransformer:
    """
    ColumnTransformer:
    - categorical -> OneHotEncoder(handle_unknown="ignore")
    - numeric -> passthrough
    """
    cat_cols = X.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
    num_cols = X.select_dtypes(include=["number"]).columns.tolist()

    return ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols),
            ("num", "passthrough", num_cols),
        ],
        remainder="drop",
    )

def save_joblib(obj, path: Path) -> None:
    """
    Save joblib artifact, ensuring directories exist.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(obj, path)

def train_decision_tree_pipeline(df: pd.DataFrame) -> Pipeline:
    """
    Decision tree pipeline for explainability.
    """
    features = list(CFG.MODEL_FEATURES)
    X = df[features].copy()
    y = df[CFG.TARGET_COL].astype(int)

    X_train, _, y_train, _ = train_test_split(
        X,
        y,
        test_size=CFG.TEST_SIZE,
        random_state=CFG.RANDOM_STATE,
        stratify=y,
    )

    pipe = Pipeline(
        steps=[
            ("prep", make_preprocess(X_train)),
            ("model", DecisionTreeClassifier(
                max_depth=3,
                min_samples_leaf=CFG.MIN_SEGMENT_N,
                random_state=CFG.RANDOM_STATE,
            )),
        ]
    )
    pipe.fit(X_train, y_train)
    return pipe

def train_logistic_regression_pipeline(df: pd.DataFrame) -> Pipeline:
    """
    Logistic regression pipeline for ranking / deployment scoring.
    """
    features = list(CFG.MODEL_FEATURES)
    X = df[features].copy()
    y = df[CFG.TARGET_COL].astype(int)

    X_train, _, y_train, _ = train_test_split(
        X,
        y,
        test_size=CFG.TEST_SIZE,
        random_state=CFG.RANDOM_STATE,
        stratify=y,
    )

    pipe = Pipeline(
        steps=[
            ("prep", make_preprocess(X_train)),
            ("model", LogisticRegression(max_iter=2000)),
        ]
    )
    pipe.fit(X_train, y_train)
    return pipe

def main() -> None:
    """
    Train both pipelines and save joblibs.
    """
    df = read_csv_data((CFG.PROCESSED_DATA_REL + "/" + CFG.PROCESSED_BANK_REL))
    df = ensure_target_numeric(df, CFG.TARGET_COL)

    dt_pipe = train_decision_tree_pipeline(df)
    lr_pipe = train_logistic_regression_pipeline(df)

    save_joblib(dt_pipe, CFG.DT_PIPELINE_PATH)
    save_joblib(lr_pipe, CFG.LR_PIPELINE_PATH)


if __name__ == "__main__":
    main()