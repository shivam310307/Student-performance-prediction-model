# 🎓 Student Performance Prediction & AI Growth Companion

An end-to-end Machine Learning web application designed to predict student academic outcomes (**High Potential** or **Needs Growth**) based on study habits, attendance, past academic performance, and sleep schedules.

Features an **Exam Ready Hub** with a 30-Day Step-by-Step Preparation Roadmap, Personalized Daily Student Timetable, and Scientifically-Backed Hard Work Strategies.

---

## 📌 Project Overview

This project provides a complete machine learning solution featuring:
- **Automated Dataset Processing**: Missing value imputation, standard scaling, and one-hot encoding using `scikit-learn` ColumnTransformers.
- **Multi-Model Evaluation**: Evaluated across **Logistic Regression**, **Random Forest**, **Decision Tree**, and **Support Vector Machine (SVM)** algorithms.
- **Automatic Model Selection**: Automatically selects and serializes (`pickle`) the top-performing model (**87.5% accuracy**).
- **Exam Ready Hub**: Personalized 30-day preparation roadmap, daily student timetable based on study and sleep hours, and hard work strategies.
- **Bilingual UI**: Complete English & Hindi language switcher.
- **Cloud Ready**: Configured for 1-click deployment on **Vercel** and **Render**.

---

## 📁 Repository Structure

```text
├── README.md               # Project documentation (displayed on GitHub main page)
├── app.py                  # Main Flask application launcher & REST API
├── Procfile                # WSGI configuration for Render / Railway (web: gunicorn app:app)
├── vercel.json             # Serverless deployment configuration for Vercel
├── requirements.txt        # Python dependency specifications
├── .gitignore              # Git ignore configuration
└── student_performance_prediction/
    ├── app.py              # Core Flask application logic & route handlers
    ├── train.py            # ML pipeline: data loading, preprocessing, model training & evaluation
    ├── model.pkl           # Serialized best-performing ML model pipeline
    ├── student_performance.csv  # Dataset containing 1,000 student feature records
    ├── static/             # Generated EDA visualization charts
    │   ├── eda_correlation.png
    │   └── eda_distributions.png
    └── templates/
        └── index.html      # Modern Bootstrap 5 dashboard UI with Exam Ready Hub
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

## ⚙️ Model Comparison & Performance

| Model Algorithm | Accuracy | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: | :---: |
| **Logistic Regression** *(Best)* | **87.5%** | **0.87** | **0.88** | **0.88** |
| Support Vector Machine (SVM) | 87.0% | 0.86 | 0.88 | 0.87 |
| Random Forest | 86.5% | 0.89 | 0.84 | 0.86 |
| Decision Tree | 76.5% | 0.81 | 0.70 | 0.75 |

---

## 🚀 Running Locally

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. (Optional) Re-train the Machine Learning Model
To re-run data preprocessing, generate EDA charts, and export `model.pkl`:
```bash
python student_performance_prediction/train.py
```

### 3. Launch the Web Application
```bash
python app.py
```

Open your browser and navigate to **`http://localhost:5000`** (or `http://127.0.0.1:5000`).

---

## ☁️ Cloud Deployment

- **Vercel**: Import the GitHub repo (`shivam310307/Student-performance-prediction-model`) into Vercel. It automatically uses `vercel.json` for 1-click deployment.
- **Render**: Create a new Web Service on Render, select this repo, and use Start Command: `gunicorn app:app`.
