import os
import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

# 1. Load dataset
DATA_PATH = "student_performance.csv"
MODEL_PATH = "model.pkl"
STATIC_DIR = "static"

os.makedirs(STATIC_DIR, exist_ok=True)
df = pd.read_csv(DATA_PATH)
print(f"Dataset loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns.")

# Define feature categories
num_features = ["study_hours", "attendance", "previous_grades", "sleep_hours"]
cat_features = ["extracurricular_activities", "parental_education", "internet_access", "family_support"]
target_col = "performance"

X = df[num_features + cat_features]
y = df[target_col].map({"Low": 0, "High": 1})

# 2. EDA & Visualizations
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

# Correlation Heatmap for numerical features
plt.figure(figsize=(8, 6))
num_df = df[num_features].copy()
num_df["performance_num"] = y
sns.heatmap(num_df.corr(), annot=True, cmap="Blues", fmt=".2f")
plt.title("Numerical Feature Correlation Matrix")
plt.tight_layout()
plt.savefig(os.path.join(STATIC_DIR, "eda_correlation.png"))
plt.close()

# Feature Distributions by Performance
plt.figure(figsize=(12, 8))
for i, feature in enumerate(num_features, 1):
    plt.subplot(2, 2, i)
    sns.boxplot(data=df, x="performance", y=feature, hue="performance", legend=False, palette="Set2")
    plt.title(f"{feature.replace('_', ' ').title()} by Performance")
plt.tight_layout()
plt.savefig(os.path.join(STATIC_DIR, "eda_distributions.png"))
plt.close()

print(f"EDA plots saved in '{STATIC_DIR}/'.")

# 3 & 6. Preprocessing Pipelines (Handling missing values, scaling & encoding)
num_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

cat_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
])

preprocessor = ColumnTransformer([
    ("num", num_pipeline, num_features),
    ("cat", cat_pipeline, cat_features)
])

# 5. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 7. Define models to train
models = {
    "Logistic Regression": LogisticRegression(random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Support Vector Machine": SVC(probability=True, random_state=42)
}

# 8. Train, Compare & Evaluate Models
results = {}
trained_pipelines = {}

print("\n" + "=" * 50)
print("MODEL TRAINING AND EVALUATION")
print("=" * 50)

for name, model in models.items():
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", model)
    ])
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    results[name] = acc
    trained_pipelines[name] = pipeline
    
    print(f"\n--- {name} ---")
    print(f"Accuracy: {acc:.4f}")
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["Low", "High"]))

# 9. Automatically choose best model
best_name = max(results, key=results.get)
best_accuracy = results[best_name]
best_pipeline = trained_pipelines[best_name]

print("=" * 50)
print(f"BEST MODEL SELECTED: {best_name} (Accuracy: {best_accuracy:.4f})")
print("=" * 50)

# 10. Save trained pipeline & metadata
model_artifacts = {
    "pipeline": best_pipeline,
    "model_name": best_name,
    "accuracy": best_accuracy,
    "num_features": num_features,
    "cat_features": cat_features
}

with open(MODEL_PATH, "wb") as f:
    pickle.dump(model_artifacts, f)

print(f"Model saved successfully to '{MODEL_PATH}'.")
