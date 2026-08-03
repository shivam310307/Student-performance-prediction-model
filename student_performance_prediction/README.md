# Student Performance Prediction

An end-to-end Machine Learning web application designed to predict whether a student will achieve **High** or **Low** academic performance based on study habits, attendance, past academic history, lifestyle metrics, and family support factors.

---

## 📌 Project Overview

This project provides a complete machine learning solution featuring:
- Automated dataset processing and missing value imputation.
- Feature scaling for numerical data & one-hot encoding for categorical attributes using `scikit-learn` ColumnTransformers.
- Multi-model evaluation across **Logistic Regression**, **Random Forest**, **Decision Tree**, and **Support Vector Machine (SVM)** algorithms.
- Automatic selection and serialization (`pickle`) of the top-performing model.
- A modern, responsive Flask dashboard built with **Bootstrap 5** and **Chart.js** for real-time inference and metric profiling.

---

## 📁 Project Structure

```text
student_performance_prediction/
├── app.py                  # Flask web application & REST API
├── train.py                # ML pipeline: loading, preprocessing, model training & evaluation
├── model.pkl               # Serialized best-performing ML model pipeline
├── student_performance.csv  # Dataset containing student feature records
├── requirements.txt        # Python dependency specifications
├── README.md               # Project documentation
├── static/                 # Generated EDA visualization charts
│   ├── eda_correlation.png
│   └── eda_distributions.png
└── templates/
    └── index.html          # Responsive Bootstrap dashboard UI
```

---

## 📊 Dataset Description

The dataset (`student_performance.csv`) consists of 1,000 student records with 8 key predictive features:

| Feature | Type | Description |
| :--- | :--- | :--- |
| `study_hours` | Numerical | Weekly study time in hours (1 – 35) |
| `attendance` | Numerical | Class attendance percentage (50% – 100%) |
| `previous_grades` | Numerical | Previous exam score percentage (40% – 100%) |
| `sleep_hours` | Numerical | Average sleep per night in hours (4 – 10) |
| `extracurricular_activities` | Categorical | Participation in extracurriculars (`Yes` / `No`) |
| `parental_education` | Categorical | Parent education level (`High School`, `Bachelor`, `Master`, `Doctorate`) |
| `internet_access` | Categorical | Home internet availability (`Yes` / `No`) |
| `family_support` | Categorical | Family academic support (`Yes` / `No`) |
| **`performance`** | **Target** | Academic outcome (`High` / `Low`) |

---

## ⚙️ Machine Learning Workflow

1. **Data Loading**: Loads raw dataset and handles missing entries using `SimpleImputer`.
2. **Preprocessing**: 
   - Numerical attributes: Median imputation + `StandardScaler`.
   - Categorical attributes: Most-frequent imputation + `OneHotEncoder`.
3. **Train-Test Split**: Stratified 80-20 train-test split for balanced representation.
4. **Model Comparison**:
   - Logistic Regression
   - Random Forest Classifier
   - Decision Tree Classifier
   - Support Vector Classifier (SVC)
5. **Model Persistence**: Saves the winning scikit-learn `Pipeline` to `model.pkl`.

### Model Performance Summary

| Model Algorithm | Accuracy | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: | :---: |
| **Logistic Regression** *(Best)* | **87.5%** | **0.87** | **0.88** | **0.88** |
| Support Vector Machine (SVM) | 87.0% | 0.86 | 0.88 | 0.87 |
| Random Forest | 86.5% | 0.89 | 0.84 | 0.86 |
| Decision Tree | 76.5% | 0.81 | 0.70 | 0.75 |

---

## 🚀 Installation & Running

### 1. Prerequisites
Ensure Python 3.9+ is installed on your system.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Train the Model
To re-run data preprocessing, EDA chart generation, and model training:
```bash
python train.py
```

### 4. Launch the Web Application
Start the local Flask web server:
```bash
python app.py
```

Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 🖼️ Dashboard & UI Screenshots

*(Place screenshots of the EduPredict web dashboard here)*

- **Input Form**: Range sliders for study hours, attendance, previous grades, and sleep.
- **Prediction Card**: Displays prediction class (`High` / `Low`), confidence percentage, and key predictive factors.
- **Radar Profiling**: Interactive Chart.js radar comparing student parameters against high-performer benchmarks.
