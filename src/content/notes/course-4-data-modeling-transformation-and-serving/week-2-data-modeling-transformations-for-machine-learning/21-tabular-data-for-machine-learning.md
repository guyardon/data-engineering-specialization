---
title: "2.1 ML Overview and Tabular Data"
course: "Course 4: Data Modeling, Transformation, and Serving"
courseSlug: "course-4-data-modeling-transformation-and-serving"
courseOrder: 4
week: "Week 2: Data Modeling & Transformations for Machine Learning"
weekSlug: "week-2-data-modeling-transformations-for-machine-learning"
weekOrder: 2
order: 1
notionId: "1f7969a7-aa01-8017-917c-eb29354e53f7"
---

## 2.1.1 Machine Learning Overview

This section covers how data engineers prepare tabular data for machine learning workflows.

| Learning Type | How it Works | Task Types |
|---|---|---|
| **Supervised** | Models learn from **features** (inputs) and **labels** (outputs) | Classification (categorical labels), Regression (numerical labels) |
| **Unsupervised** | Models operate without labels — discover structure in data | Clustering, dimensionality reduction, anomaly detection |

## 2.1.2 Machine Learning Lifecycle

The ML lifecycle has four major stages:

| Stage | Activities |
|---|---|
| **Scoping** | Define project goals and success criteria |
| **Data** | Define data requirements, establish baselines, handle labeling and organization |
| **Algorithm Development** | Train/test split → train models → cross-validation → error analysis → iterate |
| **Deployment** | Write production software, monitor and maintain system performance |

---

**The Data Engineer's Role in ML**

Data engineers help organizations adopt a **data-centric approach** to ML — "garbage in, garbage out." They collect high-quality data, prepare and serve data the model needs during deployment, and provide updated datasets for retraining.

## 2.1.3 Feature Engineering for Tabular Data

Feature engineering is any change or preprocessing applied to raw columns, or the creation of new features.

| Technique | Description |
|---|---|
| **Handling missing values** | Delete columns/rows if no valuable data is lost, or impute with mean, median, or similar-record values |
| **Feature scaling** | Required for gradient descent and distance-based algorithms |
| **Encoding categoricals** | Convert text categories to numbers for ML algorithms |
| **Creating new columns** | Combine or modify existing columns to create more predictive features |

---

**Feature Scaling Methods**

| Method | Formula | Result |
|---|---|---|
| **Standardization** | (x - mean) / std | Mean = 0, Std = 1 |
| **Min-Max scaling** | (x - min) / (max - min) | Range [0, 1] |

---

**Encoding Categorical Columns**

| Method | How it Works | Trade-off |
|---|---|---|
| **One-hot encoding** | Creates a binary column per category (0 or 1) | Increases dimensionality for high-cardinality columns |
| **Ordinal encoding** | Maps categories to ordered integers (e.g., basic=0, platinum=1) | Implies an ordering that may not exist |
| **Hashing** | Converts categories to hash values | Fixed output size, but collisions possible |
| **Embeddings** | Dense vector representations learned during training | Best for high-cardinality, requires neural network |

## 2.1.4 Scikit-Learn and Pandas for Processing Tabular Data

```python
import pandas as pd

data = pd.read_csv("customer_churn_dataset.csv")

# Explore the data
print(data.shape)       # (rows, columns)
print(data.head())      # first 5 rows
print(data.describe())  # summary statistics

# Check for and drop missing values
print(data.isnull().sum())
data = data.dropna()

# Inspect categorical distributions
for col in ["Subscription Type", "Contract Length"]:
    print(data[col].value_counts(normalize=True))

# Separate features and labels
features = data.iloc[:, 0:-1]  # all columns except last
labels = data.iloc[:, -1]      # churn column (target)
```

---

**Processing Pipeline**

1. Split data into training and test sets
2. Standardize numerical columns (fit on train, transform both)
3. One-hot encode categorical columns (fit on train, transform both)
4. Combine processed columns and save to Parquet

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Split into train/test sets
X_train, X_test, y_train, y_test = train_test_split(
    features, labels, test_size=0.2, random_state=42
)

# --- Standardize numerical columns ---
numerical_columns = [
    "Age", "Tenure", "Usage Frequency",
    "Payment Delay", "Total Spend", "Last Interaction"
]
scaler = StandardScaler()
scaler.fit(X_train[numerical_columns])  # learn stats from training set only

X_train_scaled = pd.DataFrame(
    scaler.transform(X_train[numerical_columns]),
    index=X_train.index,
    columns=numerical_columns
)

# --- One-hot encode categorical columns ---
categorical_columns = ["Subscription Type", "Contract Length"]
encoder = OneHotEncoder(sparse_output=False)
encoder.fit(X_train[categorical_columns])  # learn categories from training set only

X_train_encoded = pd.DataFrame(
    encoder.transform(X_train[categorical_columns]),
    index=X_train.index,
    columns=encoder.get_feature_names_out()
)

# --- Combine and save ---
X_train_final = pd.concat(
    [X_train["CustomerID"], X_train_scaled, X_train_encoded], axis=1
)
X_train_final.to_parquet("train.parquet")

# For the test set: use scaler.transform() and encoder.transform()
# Do NOT re-fit — statistics must come from the training set
```
