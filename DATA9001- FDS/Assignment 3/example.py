import pandas as pd
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load the breast cancer dataset
cancer = load_breast_cancer()
X, y = cancer.data, cancer.target
data = pd.DataFrame(X, columns=cancer.feature_names)
data["target"] = y

# Add some invalid data (NaN values)
data.loc[5:10, "mean radius"] = np.nan
data.loc[15:20, "mean texture"] = np.nan

print("Original DataFrame with Invalid Data:")
print(data.head(20))

# Remove rows with missing values
# data.fillna(data.mean(), inplace=True)
data.dropna(inplace=True)

# Feature scaling
scaler = StandardScaler()
data[cancer.feature_names] = scaler.fit_transform(data[cancer.feature_names])

print("\nDataFrame after Preprocessing:")
print(data.head(20))


# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    data[cancer.feature_names], data["target"], test_size=0.2, random_state=42
)

X_train = np.ascontiguousarray(X_train)
X_test = np.ascontiguousarray(X_test)

# Define classifiers
classifiers = {
    "K-Nearest Neighbors": KNeighborsClassifier(),
    "Naive Bayes": GaussianNB(),
    "Decision Tree": DecisionTreeClassifier(),
}

# Train and evaluate classifiers
for name, clf in classifiers.items():
    # Train the classifier
    clf.fit(X_train, y_train)

    # Predict the labels for the test set
    y_pred = clf.predict(X_test)

    # Evaluate the model
    print(f"\n{name} - Model Evaluation:")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
