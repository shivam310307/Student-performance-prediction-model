# 📖 Student Performance Prediction API Documentation

Welcome to the REST API guide for the **Student Growth Companion & Performance Analyzer**.

---

## 📡 API Endpoint Overview

### 1. `GET /`
Returns the main interactive web dashboard rendering real-time performance predictions and study schedules.

### 2. `POST /predict`
Processes student feature inputs and calculates performance predictions, target requirements, confidence percentages, and study strategies.

#### Request Headers
```http
Content-Type: application/json
```

#### JSON Payload Format
```json
{
  "study_hours": 20.0,
  "attendance": 88.0,
  "previous_grades": 78.0,
  "sleep_hours": 7.5,
  "extracurricular_activities": "Yes",
  "parental_education": "Bachelor",
  "internet_access": "Yes",
  "family_support": "Yes"
}
```

#### Response Output (HTTP 200 OK)
```json
{
  "prediction": "High Potential ⭐",
  "confidence": 89.5,
  "expected_score": 84.2,
  "target_needed": 92.2,
  "score_gap": 8.0,
  "daily_timetable": [ ... ],
  "hard_work_strategy": [ ... ],
  "roadmap": [ ... ]
}
```
