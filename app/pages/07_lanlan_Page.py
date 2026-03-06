import pandas as pd
import numpy as np
from tabulate import tabulate

# ----------------------------------
# Prediction Model Comparisons
# ----------------------------------


data = {
    'Model': ['KNN (k=9)', 'Logistic Regression', 'Random Forest'],
    'Accuracy': ['89.11%', '88.34%', '89.51%'],
    'Precision': ['61.46%', '57.69%', '65.67%'],
    'Recall': ['18.46%', '1.13%', '21.56%'],
    'F1-Score': ['28.39%', '2.22%', '32.46%'],
    'Confusion Matrix': [
        [[9828, 153], [1078, 244]],
        [[9970, 11], [1307, 15]],
        [[9832, 149], [1037, 285]]
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Display the table
print("Performance Metrics Summary")
print("=" * 80)
print(df.to_string(index=False))
print("\n")

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("Prediction Page: lanlan")


