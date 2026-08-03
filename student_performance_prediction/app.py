import pickle
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Load trained model artifacts
try:
    with open("model.pkl", "rb") as f:
        artifacts = pickle.load(f)
    model_pipeline = artifacts["pipeline"]
    model_name = artifacts["model_name"]
    model_accuracy = artifacts["accuracy"]
except Exception as e:
    model_pipeline, model_name, model_accuracy = None, "Not Loaded", 0.0

@app.route("/")
def index():
    return render_template(
        "index.html",
        model_name=model_name,
        model_accuracy=round(model_accuracy * 100, 1)
    )

@app.route("/predict", methods=["POST"])
def predict():
    if not model_pipeline:
        return jsonify({"error": "Model not trained yet. Run train.py first."}), 400

    data = request.get_json() if request.is_json else request.form

    input_data = {
        "study_hours": float(data.get("study_hours", 15)),
        "attendance": float(data.get("attendance", 80)),
        "previous_grades": float(data.get("previous_grades", 75)),
        "sleep_hours": float(data.get("sleep_hours", 7)),
        "extracurricular_activities": data.get("extracurricular_activities", "No"),
        "parental_education": data.get("parental_education", "Bachelor"),
        "internet_access": data.get("internet_access", "Yes"),
        "family_support": data.get("family_support", "Yes")
    }

    df_input = pd.DataFrame([input_data])

    prediction_idx = model_pipeline.predict(df_input)[0]
    probabilities = model_pipeline.predict_proba(df_input)[0]

    result_en = "High Potential ⭐" if prediction_idx == 1 else "Needs Growth 📈"
    result_hi = "उच्च क्षमता (High Potential ⭐)" if prediction_idx == 1 else "सुधार की आवश्यकता (Needs Growth 📈)"
    confidence = round(float(probabilities[prediction_idx]) * 100, 1)

    # Calculate expected score % in upcoming exam & target score needed
    base_score = (
        0.35 * input_data["previous_grades"] +
        0.30 * input_data["attendance"] +
        0.20 * (input_data["study_hours"] / 35.0 * 100.0) +
        0.05 * (input_data["sleep_hours"] / 10.0 * 100.0) +
        (3.0 if input_data["family_support"] == "Yes" else 0.0) +
        (2.5 if input_data["extracurricular_activities"] == "Yes" else 0.0) +
        (2.0 if input_data["internet_access"] == "Yes" else 0.0)
    )
    expected_score = round(min(98.5, max(40.0, base_score)), 1)
    target_needed = 84.0
    score_gap = round(max(0.0, target_needed - expected_score), 1)

    # Percentages for Progress Bar Comparison vs Ideal Benchmark
    study_pct = round(min(100.0, (input_data["study_hours"] / 30.0) * 100.0), 1)
    attend_pct = round(input_data["attendance"], 1)
    grades_pct = round(input_data["previous_grades"], 1)
    sleep_pct = round(min(100.0, (input_data["sleep_hours"] / 8.0) * 100.0), 1)

    # SMART METHOD FRAMEWORK DATA
    smart_method_en = {
        "specific": f"Target Predicted Score: {expected_score}% (Goal: {target_needed}%)",
        "measurable": f"Track 15-20 weekly study hours & {int(attend_pct)}% attendance",
        "achievable": "Follow step-by-step 30-day 4-week improvement roadmap",
        "relevant": "Focus on past exam papers and foundational concept revision",
        "time_bound": "30-day exam countdown + maintain 7-8 hours nightly sleep"
    }

    smart_method_hi = {
        "specific": f"लक्ष्य अनुमानित अंक: {expected_score}% (लक्ष्य: {target_needed}%)",
        "measurable": "साप्ताहिक 15-20 घंटे अध्ययन और 85%+ उपस्थिति मापें",
        "achievable": "चरणबद्ध 30-दिवसीय 4-सप्ताह रोडमैप का पालन करें",
        "relevant": "पुराने प्रश्न पत्रों और कमजोर विषयों के पुनरीक्षण पर ध्यान दें",
        "time_bound": "30-दिवसीय परीक्षा उल्टी गिनती + प्रतिदिन 7-8 घंटे नींद"
    }

    profile_summary_en = {
        "study": f"Study Time: {int(study_pct)}% of recommended weekly routine.",
        "attendance": f"Class Participation: Excellent ({int(attend_pct)}%).",
        "grades": f"Academic Performance: Solid foundation ({int(grades_pct)}%).",
        "sleep": f"Sleep & Rest: Healthy ({input_data['sleep_hours']} hrs)."
    }

    profile_summary_hi = {
        "study": f"अध्ययन समय: अनुशंसित दिनचर्या का {int(study_pct)}%।",
        "attendance": f"कक्षा भागीदारी: उत्कृष्ट ({int(attend_pct)}%)।",
        "grades": f"शैक्षणिक प्रदर्शन: मजबूत आधार ({int(grades_pct)}%)।",
        "sleep": f"नींद और आराम: स्वस्थ ({input_data['sleep_hours']} घंटे)।"
    }

    focus_areas_en = [
        "Increase study consistency by 30–45 minutes/day",
        "Improve revision and past paper practice before exams",
        "Maintain 7–8 hours of consistent nightly sleep"
    ]
    focus_areas_hi = [
        "प्रतिदिन अध्ययन में 30-45 मिनट की निरंतरता बढ़ाएं",
        "परीक्षा से पहले पुनरीक्षण और पुराने प्रश्न पत्रों का अभ्यास करें",
        "प्रतिदिन 7-8 घंटे की नियमित नींद बनाए रखें"
    ]

    positives_en = []
    positives_hi = []
    improvements_en = []
    improvements_hi = []

    if input_data["attendance"] >= 80:
        positives_en.append(f"Class Participation: Excellent ({int(input_data['attendance'])}%)")
        positives_hi.append(f"कक्षा भागीदारी: उत्कृष्ट ({int(input_data['attendance'])}%)")
    else:
        improvements_en.append(f"Class Participation: Below optimal ({int(input_data['attendance'])}%)")
        improvements_hi.append(f"कक्षा भागीदारी: कम ({int(input_data['attendance'])}%)")

    if input_data["sleep_hours"] >= 7:
        positives_en.append(f"Sleep & Rest: Healthy ({input_data['sleep_hours']} hrs/night)")
        positives_hi.append(f"नींद और आराम: स्वस्थ ({input_data['sleep_hours']} घंटे)")
    else:
        improvements_en.append(f"Sleep Duration: Below 7 hrs ({input_data['sleep_hours']} hrs/night)")
        improvements_hi.append(f"नींद की अवधि: 7 घंटे से कम ({input_data['sleep_hours']} घंटे)")

    if prediction_idx == 1:
        ai_coach_en = f"Your class participation ({int(input_data['attendance'])}%) and study routine give you a solid foundation! If you add 45 minutes of daily practice, your predicted score could reach {min(98.0, round(expected_score + 5.5, 1))}%. Keep pushing!"
        ai_coach_hi = f"आपकी कक्षा भागीदारी ({int(input_data['attendance'])}%) और अध्ययन अभ्यास आपको एक मजबूत आधार दे रहे हैं! यदि आप प्रतिदिन 45 मिनट अभ्यास जोड़ते हैं, तो आपका स्कोर {min(98.0, round(expected_score + 5.5, 1))}% तक पहुंच सकता है!"
    else:
        ai_coach_en = f"Don't worry—you have great potential! By boosting your weekly study hours by just 4-5 hours and keeping class participation high, you can increase your score to around {round(expected_score + 10.5, 1)}% in your upcoming exam!"
        ai_coach_hi = f"चिंता न करें—आपमें अपार क्षमता है! यदि आप अपनी साप्ताहिक पढ़ाई में 4-5 घंटे बढ़ाएँ और कक्षा उपस्थिति अच्छी रखें, तो आपका स्कोर आने वाली परीक्षा में {round(expected_score + 10.5, 1)}% तक पहुंच सकता है!"

    roadmap_en = [
        {"week": "Week 1", "task": "Daily Study Booster (+45 mins/day) & Set Goal Tracker"},
        {"week": "Week 2", "task": "Solve Past Exam Papers & Review Core Weak Topics"},
        {"week": "Week 3", "task": "Conduct Timed Practice Tests & Teacher Consultation"},
        {"week": "Week 4", "task": "Final Mock Exam & Pre-Exam Relaxation Routine"}
    ]
    roadmap_hi = [
        {"week": "सप्ताह 1", "task": "दैनिक अध्ययन में 45 मिनट की वृद्धि और लक्ष्य निर्धारण"},
        {"week": "सप्ताह 2", "task": "पुराने प्रश्न पत्र हल करें और कमजोर विषयों का पुनरीक्षण करें"},
        {"week": "सप्ताह 3", "task": "समयबद्ध मॉक टेस्ट और शिक्षकों से परामर्श लें"},
        {"week": "सप्ताह 4", "task": "अंतिम अभ्यास परीक्षा और शांत दिमाग से दोहराव करें"}
    ]

    teacher_exp_en = "Provide structured study schedules and remedial practice for weak topics."
    teacher_exp_hi = "व्यवस्थित अध्ययन समय-सारणी और कमजोर विषयों के लिए अभ्यास प्रदान करें।"

    response = {
        "prediction": result_en,
        "prediction_hi": result_hi,
        "confidence": confidence,
        "expected_score": expected_score,
        "target_needed": target_needed,
        "score_gap": score_gap,
        "study_pct": study_pct,
        "attend_pct": attend_pct,
        "grades_pct": grades_pct,
        "sleep_pct": sleep_pct,
        "smart_method": smart_method_en,
        "smart_method_hi": smart_method_hi,
        "profile_summary": profile_summary_en,
        "profile_summary_hi": profile_summary_hi,
        "focus_areas": focus_areas_en,
        "focus_areas_hi": focus_areas_hi,
        "positives": positives_en,
        "positives_hi": positives_hi,
        "improvements": improvements_en,
        "improvements_hi": improvements_hi,
        "ai_coach": ai_coach_en,
        "ai_coach_hi": ai_coach_hi,
        "roadmap": roadmap_en,
        "roadmap_hi": roadmap_hi,
        "teacher_explanation": teacher_exp_en,
        "teacher_explanation_hi": teacher_exp_hi,
        "model_used": model_name,
        "input_features": input_data
    }

    if request.is_json:
        return jsonify(response)

    return render_template(
        "index.html",
        prediction_res=response,
        model_name=model_name,
        model_accuracy=round(model_accuracy * 100, 1)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
