"""
Extract rules from a fitted DecisionTreeClassifier.
"""

from dataclasses import dataclass
from typing import List, Optional

import pandas as pd
from sklearn.tree import _tree


@dataclass(frozen=True)
class LeafRule:
    rule: str
    n_samples: int
    positive_rate: float


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
    dt_model,
    feature_names: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Extract leaf rules from a DecisionTreeClassifier.

    Args:
        dt_model: fitted sklearn DecisionTreeClassifier
        feature_names: names of features passed into the tree (required for readable rules)

    Returns:
        DataFrame with columns: rule, n_samples, positive_rate
    """
    if feature_names is None:
        # best effort: try feature_names_in_
        feature_names = list(getattr(dt_model, "feature_names_in_", []))
    if not feature_names:
        # fallback to generic names
        n_feats = int(getattr(dt_model, "n_features_in_", 0)) or 0
        feature_names = [f"feature_{i}" for i in range(n_feats)]

    tree = dt_model.tree_
    rules: List[LeafRule] = []
    _recurse_tree(tree, feature_names, 0, [], rules)

    df = pd.DataFrame([r.__dict__ for r in rules])
    df = df.sort_values(["positive_rate", "n_samples"], ascending=[False, False]).reset_index(drop=True)
    return df