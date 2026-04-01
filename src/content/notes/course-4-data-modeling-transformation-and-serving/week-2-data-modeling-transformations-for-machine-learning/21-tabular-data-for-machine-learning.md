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

**Modeling and Processing Tabular Data for Machine Learning**

This section covers how data engineers prepare tabular data for machine learning workflows, starting with a brief ML primer.

---


**Machine Learning Overview**

**Supervised Learning**

In supervised learning, models learn from **features** (inputs) and **labels** (outputs). When labels are categorical the task is **classification**; when labels are numerical it is **regression**.

**Unsupervised Learning**

Unsupervised learning operates without labels. Common applications include clustering and grouping records with similar features.

---


## 2.1.2 Machine Learning Lifecycle

**Machine Learning Lifecycle**

The ML lifecycle has four major stages:

- **Scoping** -- Define the project goals and success criteria.
- **Data** -- Define data requirements, establish baselines, and handle labeling and organization.
- **Algorithm Development** -- Split data into training and test sets, train several algorithms, perform error analysis via cross-validation, evaluate on the test set, and iterate by fixing data issues, adding features, or collecting more data.
- **Deployment** -- Write production software, then monitor and maintain system performance and reliability.
![](/data-engineering-specialization-website/images/d2fde354-621d-4e8b-87e0-16c05b40374a.png)

**The role of the Data Engineer in the ML/AI Team:**

Data engineers help organizations adopt a **data-centric approach** to ML by collecting high-quality data -- because "garbage in, garbage out." During deployment, they prepare and serve the data the model needs, and provide updated datasets for retraining.

---


## 2.1.3 Feature Engineering for Tabular Data

**Feature Engineering for Tabular Data**

Feature engineering is any change or preprocessing applied to raw columns, or the creation of new features. The main techniques include:

- **Handling missing values** -- Delete entire columns or rows (if no valuable data is lost), or impute missing values with summary statistics like the column mean, median, or values from similar records.
- **Feature scaling** -- Required for gradient descent algorithms to converge well, and for ML algorithms based on distance metrics. Two common types:
  - **Standardization**: subtract the mean and divide by standard deviation (result: mean=0, std=1)
  - **Min-Max scaling**: subtract the min and divide by (max - min) (result: range [0, 1])
- **Converting categorical columns into numerical ones**:
  - **One-hot encoding**: creates a binary column per category (0 or 1), which can increase dimensionality
  - **Ordinal encoding**: maps categories to integers based on ordering (e.g. basic=0, platinum=1, family=2)
  - **Hashing**: converts categories into hash values
  - **Embeddings**: dense vector representations
- **Creating new columns** by combining or modifying existing columns

---


## 2.1.4 Scikit-Learn and Pandas for Processing Tabular Data

**Scikit-Learn and Pandas for Processing Tabular Data**

```python
import pandas as pd

data = pd.read_csv("customer_churn_dataset.csv")


**get basic insights**
print(data.shape)
print(data.head())
print(data.describe())


**check nulls**
print(data.isnull().sum())
print(data[data['CustomerId'].is_null()])


**drop nulls**
data = data.dropna()


**check nulls again**
print(data.isnull().sum())


**check categorical column value counts**
for col in ['Subscription Type', 'Contract Length']:
	print(col)
	print(data[col].value_counts(normalize=True))
	print('\n')


**get features and labels**
features = data.iloc[:, 0:-1] # all columns except last
labels = data.iloc[:, -1] # customer churn column
```

Steps to prepare the data for training an ML model:

1. Split the data into training and test sets
2. Process the training/test data
   1. Standardize numerical columns
   2. One-hot encode categorical columns
3. Combine processed columns with the Customer ID into a pandas dataframe
4. Save the dataframe to a parquet file

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScalar, OneHotEncoder


**split into train/test sets**
X_train, X_test, y_train, y_test = train_test_split(features,
																										labels,
																										test_size=0.2,

```

```python
from sklearn.preprocessing import StandardScalar


**extract numerical columns																										random_state=42)**
numerical_columns = ['Age', 'Tenure', 'Usage Frequency',
										 'Payment Delay', 'Total Spend', 'Last Interaction']

X_train_numerical = X_train[numerical_columns]


**instantiate scalar**
scalar = StandardScalar()


**fit scalar: computes the mean/standard-dev of each column**
scalar.fit(X_train_numerical)


**transform scalar: uses the computed statistics to normalize the data**
x_train_scaled = scalar.transform(X_train_numerical)


**Create dataframe for scaled numerical data**
X_train_scaled_df = pd.DataFrame(data=X_train_scaled,
                                 index=X_train.index,
	                               columns=numerical_columns)
```

```python
from sklearn.preprocessing import OneHotEncoding


**extract categorical columns**
categorical_columns = ['Subscription Type', 'Contract Length']
X_train_categorical = X_train[categorical_columns]


**instantiate one hot encoder**
encoder = OneHotEncoder()


**encoder.fit: checks the unique values within each categorical column**
encoder.fit(X_train_categorical)


**encoder.transform: prepares the labels of the output columns**
X_train_encoded = encoder.transform(X_train_categorical)


**returns sparse matrix**

**print(type(X_train_encoded)) # scipy.sparse._csr.csr_matrix**


**convert one-hot encodings back to dataframe**
X_train_encoded_df = pd.DataFrame(x_train_encoded.todense(), # converts sparse matrix to dense matrix
                                  index=X_train.index,
                                  columns=encoder.get_feature_names_out()) # get feature names corresonding to column encodings

```

```python

**get final transformed dataframe**
X_train_transf = pd.concat([X_train['CustomerID'],
                            X_train_scaled_df,
                            X_train_encoded_df], axis=1)

X_train_transf.to_parquet("train.parquet")


**do the same for test set...**

**note that for test set, we do not need to re-fit scalar (it should be learned from training_set)**
```
