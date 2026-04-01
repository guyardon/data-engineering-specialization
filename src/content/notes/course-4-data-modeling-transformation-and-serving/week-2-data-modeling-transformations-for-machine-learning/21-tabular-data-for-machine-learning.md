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

## Modeling and Processing Tabular Data for Machine Learning

---

### Machine Learning Overview

**Supervised Learning**

- Learn from features and labels
- Types of labels:
- Categorical - Classification Models
- Numerical - Regression Models
**Unsupervised Learning**

- No Labels
- E.g. clustering and grouping similar features
---

### Machine Learning Lifecycle

- **Scoping**
- Defining Project
- **Data **
- Defining data and establishing baseline
- Labeling and organizing data
- **Algorithm Development**
- Select and train the model
  - Split the data into training and test sets
  - Use training set to train several ML algorithms
- Perform error analysis
  - Select the best model through cross validation
  - Evaluate the model performance using the test set
- Feedback to data stage
  - Fix something in the collected data
  - Add more features
  - Collect more data
- **Deployment**
- Write software to deploy in production
- Monitor and Maintain
  - Check to make sure the system's performance is good and reliable
![](/data-engineering-specialization-website/images/d2fde354-621d-4e8b-87e0-16c05b40374a.png)

The role of the Data Engineer in the ML/AI Team:

- Help the organization adopt a data centric approach to ML
- Enhance the ML system by collecting high quality data
- "Garbage in, garbage out"
- How a data engineer can help in the ML deployment phase:
- Prepare and serve the data that is needed for the deployed model
- Serve an updated set of data to re-train and update the model
---

### Feature Engineering for Tabular Data

Feature engineering Any change or preprocessing done to a raw column and any creation of new features, for example:

- **Handling missing values**
- Delete the entire column or row (if there's no risk of losing valuable data)
- Impute the missing values with summary statistics (e.g. column mean/median/ or values from a similar record)
- **Feature scaling**
- Features need to be scaled for gradient descent algorithms to converge well
- Features also need to be scaled when ML algorithms are based on distance metrics
- Types:
  - Standardization (subtract mean and divide standard deviation). Result: column has mean=0 and standard deviation=1
  - Min-Max scaling (subtract min and divide by max-min). Result: column has minimum=0 and maximum=1
- **Converting categorical columns into numerical ones**
- Types:
  - One-hot encoding (convert categorical columns into into several columns (one column per category). The values are either 0 or 1. Can increase the number of columns in the dataset
  - Ordinal Encoding: (convert categorical column into integer column, based on the ordering of the categories). For example, converting account types: basic=0, platinum=1, family=2.
  - Hashing: converting categories into a hash values
  - Embeddings 
- **Creating new columns by combining or modifying existing columns**
---

### Scikit-Learn and Pandas for Processing Tabular Data

```python
import pandas as pd

data = pd.read_csv("customer_churn_dataset.csv")

# get basic insights
print(data.shape)
print(data.head())
print(data.describe())

# check nulls
print(data.isnull().sum())
print(data[data['CustomerId'].is_null()])

# drop nulls
data = data.dropna()

# check nulls again
print(data.isnull().sum())

# check categorical column value counts
for col in ['Subscription Type', 'Contract Length']:
	print(col)
	print(data[col].value_counts(normalize=True))
	print('\n')
	
# get features and labels
features = data.iloc[:, 0:-1] # all columns except last
labels = data.iloc[:, -1] # customer churn column
```

Steps to prepare the data for training an ML model:

1. Split the data into training and test sets
2. Process the training/test data
1. Standardize numerical columns
2. One hot encoding for categorical columns
3. Combine processed columns with the Customer ID into a pandas dataframe
4. Save the dataframe to a parquet file

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScalar, OneHotEncoder

# split into train/test sets
X_train, X_test, y_train, y_test = train_test_split(features, 
																										labels, 
																										test_size=0.2, 
                                           
```

```python
from sklearn.preprocessing import StandardScalar

# extract numerical columns																										random_state=42)
numerical_columns = ['Age', 'Tenure', 'Usage Frequency',
										 'Payment Delay', 'Total Spend', 'Last Interaction']

X_train_numerical = X_train[numerical_columns]

# instantiate scalar
scalar = StandardScalar()

# fit scalar: computes the mean/standard-dev of each column
scalar.fit(X_train_numerical)

# transform scalar: uses the computed statistics to normalize the data
x_train_scaled = scalar.transform(X_train_numerical)

# Create dataframe for scaled numerical data
X_train_scaled_df = pd.DataFrame(data=X_train_scaled,
                                 index=X_train.index,
	                               columns=numerical_columns)
```

```python
from sklearn.preprocessing import OneHotEncoding

# extract categorical columns	                                                
categorical_columns = ['Subscription Type', 'Contract Length']
X_train_categorical = X_train[categorical_columns]

# instantiate one hot encoder
encoder = OneHotEncoder()

# encoder.fit: checks the unique values within each categorical column
encoder.fit(X_train_categorical)

# encoder.transform: prepares the labels of the output columns
X_train_encoded = encoder.transform(X_train_categorical) 

# returns sparse matrix
# print(type(X_train_encoded)) # scipy.sparse._csr.csr_matrix

# convert one-hot encodings back to dataframe
X_train_encoded_df = pd.DataFrame(x_train_encoded.todense(), # converts sparse matrix to dense matrix
                                  index=X_train.index,
                                  columns=encoder.get_feature_names_out()) # get feature names corresonding to column encodings

```

```python
# get final transformed dataframe
X_train_transf = pd.concat([X_train['CustomerID'],
                            X_train_scaled_df,
                            X_train_encoded_df], axis=1)
                            
X_train_transf.to_parquet("train.parquet")  

# do the same for test set...
# note that for test set, we do not need to re-fit scalar (it should be learned from training_set)                                              
```
