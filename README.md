# 🎓 Student Growth Companion & Performance Prediction AI

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3.0-orange.svg)
![Build Status](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-purple.svg)

An AI-powered web application and student growth companion that predicts academic performance, estimates target scores, and generates personalized daily study timetables, exam strategy guides, and 30-day preparation roadmaps.

---

## 🌟 Key Features

* **🤖 Machine Learning Prediction Engine**: Trained on student academic data using Scikit-Learn pipelines with feature scaling and categorical encoding.
* **📊 Dual Language AI Growth Companion (English & Hindi)**:
  * Personalized 24-hour Daily Study Timetable tailored to sleep and study hours.
  * 50/10 Pomodoro Focus Method & Active Recall Strategies.
  * Zero-Error Log Notebook guidance to bridge score gaps.
  * 4-Week Exam Countdown Preparation Roadmap.
* **⚡ Modern Responsive UI**: Built with Bootstrap 5, glassmorphism cards, interactive tabs, progress bars, and instant prediction visualization.
* **🧪 Comprehensive Unit Test Suite**: Includes automated test coverage for Flask HTTP routes, form handling, and JSON API payloads.

---

## 🛠️ Project Architecture

```
Student Performance Analyzer/
├── app.py                            # Root Flask application launcher
├── vercel.json                       # Vercel Serverless Deployment Config
├── requirements.txt                  # Python dependencies
├── Procfile                          # Gunicorn web server process configuration
├── student_performance_prediction/
│   ├── app.py                        # Core Flask routing & AI payload generator
│   ├── train.py                      # Model training & EDA visualization script
│   ├── model.pkl                     # Serialized Scikit-Learn ML pipeline
│   ├── student_performance.csv       # Training dataset
│   ├── templates/
│   │   └── index.html                # Responsive web interface
│   └── static/                       # Correlation heatmaps & feature plots
└── tests/
    ├── __init__.py
    └── test_app.py                   # Automated unit test suite
```

---

## 🚀 Getting Started

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/shivam310307/Student-performance-prediction-model.git
cd Student-performance-prediction-model
pip install -r requirements.txt
```

### 2. Run the Web Application Locally

```bash
python app.py
```

Open your browser and navigate to:
👉 **`http://localhost:5000`** or **`http://127.0.0.1:5000`**

### 3. Run Automated Unit Tests

```bash
python -m unittest discover -s tests
```

---

## ☁️ Deployment

This project is pre-configured for free cloud deployment on **Vercel** or **Render**:

* **Vercel**: Pre-configured via `vercel.json` (`@vercel/python` serverless runner).
* **Render**: Procfile configured with `gunicorn app:app`.

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).
