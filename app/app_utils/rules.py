"""
app/app_utils/rules.py

Extract leaf rules from:
- a fitted DecisionTreeClassifier, OR
- a fitted sklearn Pipeline containing a DecisionTreeClassifier.

Expected pipeline shape (from training):
  Pipeline(steps=[("prep", ColumnTransformer(...)), ("model", DecisionTreeClassifier(...))])
"""
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier, _tree


@dataclass(frozen=True)
class LeafRule:
    rule: str
    n_samples: int
    positive_rate: float


def _unwrap_tree_and_features(
    artifact: Union[Pipeline, DecisionTreeClassifier],
    feature_names: Optional[List[str]] = None,
) -> Tuple[DecisionTreeClassifier, List[str]]:
    """
    Return (DecisionTreeClassifier, feature_names) from a Pipeline or bare estimator.
    """
    # Bare DT
    if isinstance(artifact, DecisionTreeClassifier):
        dt = artifact
        if feature_names:
            return dt, feature_names

        names = list(getattr(dt, "feature_names_in_", []) or [])
        if names:
            return dt, names

        n_feats = int(getattr(dt, "n_features_in_", 0) or 0)
        return dt, [f"feature_{i}" for i in range(n_feats)]

    # Pipeline DT
    if not isinstance(artifact, Pipeline):
        raise TypeError(f"Unsupported artifact type: {type(artifact)}")

    if "model" not in artifact.named_steps:
        raise KeyError(
            f"Pipeline missing 'model' step. Steps: {list(artifact.named_steps.keys())}"
        )

    dt = artifact.named_steps["model"]
    if not isinstance(dt, DecisionTreeClassifier):
        raise TypeError(f"'model' step is not DecisionTreeClassifier. Got: {type(dt)}")

    if feature_names:
        return dt, feature_names

    # Prefer transformed feature names from preprocessor
    prep = artifact.named_steps.get("prep")
    if prep is not None and hasattr(prep, "get_feature_names_out"):
        try:
            names_out = prep.get_feature_names_out()
            names = [str(n) for n in names_out]
            if names:
                return dt, names
        except Exception:
            pass

    # Fallback
    names = list(getattr(dt, "feature_names_in_", []) or [])
    if names:
        return dt, names

    n_feats = int(getattr(dt, "n_features_in_", 0) or 0)
    return dt, [f"feature_{i}" for i in range(n_feats)]


def _recurse_tree(tree, feature_names: List[str], node_id: int, path: List[str], out: List[LeafRule]) -> None:
    """
    DFS traversal to collect leaf rules.
    """
    if tree.feature[node_id] != _tree.TREE_UNDEFINED:
        name = feature_names[tree.feature[node_id]]
        threshold = tree.threshold[node_id]

        left_path = path + [f"{name} <= {threshold:.4g}"]
        right_path = path + [f"{name} > {threshold:.4g}"]

        _recurse_tree(tree, feature_names, tree.children_left[node_id], left_path, out)
        _recurse_tree(tree, feature_names, tree.children_right[node_id], right_path, out)
        return

    # leaf
    value = tree.value[node_id][0]
    n = int(tree.n_node_samples[node_id])
    pos = float(value[1]) if len(value) > 1 else float(value[0])
    total = float(value.sum()) if value.sum() else 1.0
    positive_rate = pos / total

    out.append(
        LeafRule(
            rule=" AND ".join(path) if path else "(root)",
            n_samples=n,
            positive_rate=positive_rate,
        )
    )


def extract_leaf_rules(
    artifact: Union[Pipeline, DecisionTreeClassifier],
    feature_names: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Extract leaf rules from a DecisionTreeClassifier or a Pipeline containing it.

    Returns:
        DataFrame with columns: rule, n_samples, positive_rate
    """
    dt_model, names = _unwrap_tree_and_features(artifact, feature_names=feature_names)

    tree = dt_model.tree_
    rules: List[LeafRule] = []
    _recurse_tree(tree, names, 0, [], rules)

    df = pd.DataFrame([r.__dict__ for r in rules])
    df = df.sort_values(["positive_rate", "n_samples"], ascending=[False, False]).reset_index(drop=True)
    return df