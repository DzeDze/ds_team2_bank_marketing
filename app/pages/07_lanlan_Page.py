import pandas as pd
import numpy as np
from tabulate import tabulate

# ----------------------------------
# Prediction Model Comparisons
# ----------------------------------


data = {
    'Model': ['KNN (k=51)', 'Logistic Regression', 'Random Forest'],
    'Accuracy': ['88.81%', '88.32%', '89.43%'],
    'Precision': ['77.67%', '53.57%', '64.53%'],
    'Recall': ['6.05%', '1.13%', '21.33%'],
    'AUC': ['0.7610', '0.7322', '0.7905'],
    'Confusion Matrix': [
        [[9958, 23], [1242, 80]],      
        [[9979, 2], [1320, 2]],        
        [[9826, 155], [1040, 282]]
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



