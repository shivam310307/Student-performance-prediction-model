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

def generate_performance_payload(input_data, prediction_idx=1, probabilities=[0.15, 0.85]):
    study_hours = input_data["study_hours"]
    attendance = input_data["attendance"]
    previous_grades = input_data["previous_grades"]
    sleep_hours = input_data["sleep_hours"]
    extracurricular = input_data["extracurricular_activities"]
    internet = input_data["internet_access"]
    support = input_data["family_support"]

    result_en = "High Potential ⭐" if prediction_idx == 1 else "Needs Growth 📈"
    result_hi = "उच्च क्षमता (High Potential ⭐)" if prediction_idx == 1 else "सुधार की आवश्यकता (Needs Growth 📈)"
    confidence = round(float(probabilities[prediction_idx]) * 100, 1)

    base_score = (
        0.35 * previous_grades +
        0.30 * attendance +
        0.20 * (study_hours / 35.0 * 100.0) +
        0.05 * (sleep_hours / 10.0 * 100.0) +
        (3.0 if support == "Yes" else 0.0) +
        (2.5 if extracurricular == "Yes" else 0.0) +
        (2.0 if internet == "Yes" else 0.0)
    )
    expected_score = round(min(98.5, max(40.0, base_score)), 1)
    target_needed = 85.0 if expected_score < 80 else min(98.0, round(expected_score + 8.0, 1))
    score_gap = round(max(0.0, target_needed - expected_score), 1)

    daily_study = round(study_hours / 7.0, 1)

    # 1. Customized Daily Time Table
    sleep_bed_time = "10:30 PM" if sleep_hours >= 7.5 else "11:30 PM"
    daily_timetable_en = [
        {"time": "06:30 AM - 07:15 AM", "activity": "🌅 Morning Active Recall & Formulas", "detail": "Review key formulas, flashcards, and summary notes with a fresh mind."},
        {"time": "07:15 AM - 08:15 AM", "activity": "🍳 Healthy Breakfast & Prep", "detail": "Nutritious breakfast, hydration, and organizing your study materials."},
        {"time": "08:30 AM - 02:30 PM", "activity": "🏫 Active Class Participation", "detail": f"Attend classes actively to maintain your {int(attendance)}% participation benchmark."},
        {"time": "03:00 PM - 04:30 PM", "activity": "📚 Core Subject Study Session", "detail": f"Dedicated deep work study block. Part of your daily {daily_study} hrs study plan."},
        {"time": "04:30 PM - 05:30 PM", "activity": "⚽ Rest, Refresh & Physical Break", "detail": "Outdoor walk, sport, or relaxation to reset mental focus."},
        {"time": "05:30 PM - 07:00 PM", "activity": "📝 Past Papers & Problem Solving", "detail": "Solve previous year exam papers under timed practice without looking at answers."},
        {"time": "07:00 PM - 08:00 PM", "activity": "🧠 Error Notebook & Spaced Repetition", "detail": "Review your Zero-Error Log notebook and re-attempt missed questions."},
        {"time": "08:00 PM - 09:00 PM", "activity": "🥗 Dinner & Relaxation", "detail": "Enjoy a balanced meal and unwind with family."},
        {"time": "09:00 PM - 09:45 PM", "activity": "📅 Light Revision & Goal Setting", "detail": "Plan your top 3 study goals for tomorrow and pack your bag."},
        {"time": f"{sleep_bed_time} - 06:30 AM", "activity": "😴 Memory Consolidation Sleep", "detail": f"Guarantees {sleep_hours} hours of restorative sleep required for memory retention."}
    ]

    daily_timetable_hi = [
        {"time": "06:30 AM - 07:15 AM", "activity": "🌅 सुबह का पुनरीक्षण एवं सूत्र", "detail": "ताज़ा दिमाग से मुख्य सूत्रों, फ्लैशकार्ड और नोट्स का पुनरीक्षण।"},
        {"time": "07:15 AM - 08:15 AM", "activity": "🍳 पौष्टिक नाश्ता और तैयारी", "detail": "पौष्टिक नाश्ता करें और अध्ययन सामग्री व्यवस्थित करें।"},
        {"time": "08:30 AM - 02:30 PM", "activity": "🏫 सक्रिय कक्षा उपस्थिति", "detail": f"कक्षा में ध्यान दें और {int(attendance)}% उपस्थिति बनाए रखें।"},
        {"time": "03:00 PM - 04:30 PM", "activity": "📚 मुख्य विषय अध्ययन सत्र", "detail": f"गहन अध्ययन ब्लॉक। दैनिक {daily_study} घंटे योजना का भाग।"},
        {"time": "04:30 PM - 05:30 PM", "activity": "⚽ विश्राम, खेल-कूद एवं ताज़गी", "detail": "मानसिक ऊर्जा रीचार्ज करने के लिए शारीरिक गतिविधि या विश्राम।"},
        {"time": "05:30 PM - 07:00 PM", "activity": "📝 अभ्यास सत्र (पुराने प्रश्न पत्र)", "detail": "बिना उत्तर देखे पुराने परीक्षा प्रश्न पत्र और अभ्यास सेट हल करें।"},
        {"time": "07:00 PM - 08:00 PM", "activity": "🧠 त्रुटि नोटबुक एवं पुनरावृत्ति", "detail": "त्रुटि नोटबुक का पुनरीक्षण करें और कठिन विषयों का आत्म-परीक्षण करें।"},
        {"time": "08:00 PM - 09:00 PM", "activity": "🥗 रात्रि भोजन एवं परिवार समय", "detail": "संतुलित भोजन करें और परिवार के साथ तनावमुक्त समय बिताएं।"},
        {"time": "09:00 PM - 09:45 PM", "activity": "📅 हल्का पुनरीक्षण और कल के लक्ष्य", "detail": "कल के 3 मुख्य लक्ष्य तय करें और बैग तैयार करें।"},
        {"time": f"{sleep_bed_time} - 06:30 AM", "activity": "😴 स्मृति सुदृढ़ीकरण नींद", "detail": f"स्मृति मजबूत करने के लिए आवश्यक {sleep_hours} घंटे की गहरी नींद लें।"}
    ]

    # 2. How to Work Hard & Smart Strategy
    hard_work_strategy_en = [
        {"icon": "bi-fire", "color": "text-danger", "heading": "The 50/10 Pomodoro Focus Method", "desc": "Study with 100% intense focus for 50 minutes, then take a 10-minute phone-free break. 4 cycles = 3.3 hours of super-productive study!"},
        {"icon": "bi-lightning-charge-fill", "color": "text-warning", "heading": "Active Recall Over Passive Reading", "desc": "Never just re-read textbooks. Close the book, write down what you remembered, and solve problems from memory. This builds 3x stronger exam retention."},
        {"icon": "bi-journal-code", "color": "text-primary", "heading": "The Zero-Error Log Notebook", "desc": "Maintain a dedicated error log notebook. Whenever you solve a question incorrectly, write it down and re-attempt it every 3 days until zero mistakes remain."},
        {"icon": "bi-graph-up-arrow", "color": "text-success", "heading": f"Bridge the Score Gap ({score_gap}%)", "desc": f"Your current predicted score is {expected_score}% against target {target_needed}%. Adding just 30–45 minutes of daily practice will easily bridge this gap!"},
        {"icon": "bi-shield-check", "color": "text-purple", "heading": "Consistency Beats Late-Night Cramming", "desc": "Daily 2-hour consistent revision is 10x more effective than an all-nighter before the exam. Stick to your timetable and maintain your sleep schedule!"}
    ]

    hard_work_strategy_hi = [
        {"icon": "bi-fire", "color": "text-danger", "heading": "50/10 पोमोडोरो एकाग्रता तकनीक", "desc": "50 मिनट बिना किसी भटकाव (बिना फोन) के ध्यान केंद्रित करें, फिर 10 मिनट का ब्रेक लें। 4 चक्र = 3.3 घंटे का अत्यंत उत्पादक अध्ययन!"},
        {"icon": "bi-lightning-charge-fill", "color": "text-warning", "heading": "सक्रिय स्मरण (Active Recall) बनाम निष्क्रिय पढ़ना", "desc": "केवल किताबें न पढ़ें। किताब बंद करें और जो याद है उसे लिखें। इससे परीक्षा में 3 गुना बेहतर स्मरण शक्ति मिलती है।"},
        {"icon": "bi-journal-code", "color": "text-primary", "heading": "शून्य-त्रुटि नोटबुक (Error Log Notebook)", "desc": "एक अलग नोटबुक बनाएं। जब भी कोई प्रश्न गलत हो, उसे लिखें और हर 3 दिन में दोबारा हल करें जब तक गलती शून्य न हो जाए।"},
        {"icon": "bi-graph-up-arrow", "color": "text-success", "heading": f"अंक अंतर दूर करें ({score_gap}%)", "desc": f"आपका अनुमानित अंक {expected_score}% और लक्ष्य {target_needed}% है। प्रतिदिन केवल 30-45 मिनट का अभ्यास जोड़कर इस अंतर को आसानी से पार करें!"},
        {"icon": "bi-shield-check", "color": "text-purple", "heading": "निरंतरता रात भर रटने से बेहतर है", "desc": "प्रतिदिन 2 घंटे का निरंतर अध्ययन परीक्षा की रात जागने से 10 गुना अधिक प्रभावी है। अपनी समय-सारणी का पालन करें!"}
    ]

    # 3. 4-Week Exam Preparation Roadmap
    roadmap_en = [
        {"week": "Week 1", "phase": "Foundations & Weak Area Mapping", "task": f"Identify top 3 weak subjects, create Error Log notebook, and establish a daily {daily_study} hr study routine."},
        {"week": "Week 2", "phase": "Active Recall & High-Yield Practice", "task": "Solve chapter-wise numericals and conceptual questions using the 50/10 Pomodoro method without looking at solutions."},
        {"week": "Week 3", "phase": "Timed Past Exam Papers", "task": f"Attempt 3-5 full-length past exam papers under strict time limits to reach {target_needed}% accuracy."},
        {"week": "Week 4", "phase": "Final Speed Mocks & Exam Mindset", "task": f"Review Error Notebook, take final mock tests, maintain {sleep_hours} hrs sleep nightly, and stay completely calm."}
    ]

    roadmap_hi = [
        {"week": "सप्ताह 1", "phase": "मूल बातें एवं कमजोर क्षेत्र पहचान", "task": f"3 सबसे कमजोर विषयों की पहचान करें, त्रुटि नोटबुक बनाएं और दैनिक {daily_study} घंटे का अध्ययन शुरू करें।"},
        {"week": "सप्ताह 2", "phase": "सक्रिय स्मरण एवं मुख्य अभ्यास", "task": "बिना उत्तर देखे 50/10 पोमोडोरो तकनीक का उपयोग करके अध्याय-वार प्रश्न हल करें।"},
        {"week": "सप्ताह 3", "phase": "समयबद्ध पुराने प्रश्न पत्र", "task": f"{target_needed}% सटीकता प्राप्त करने के लिए सख्त समय सीमा के साथ 3-5 पिछले वर्षों के प्रश्न पत्र हल करें।"},
        {"week": "सप्ताह 4", "phase": "अंतिम मॉक टेस्ट और आत्मविश्वास", "task": f"त्रुटि नोटबुक का पुनरीक्षण करें, अंतिम मॉक टेस्ट दें, {sleep_hours} घंटे की नींद लें और शांत रहें।"}
    ]

    # S.M.A.R.T Framework
    smart_method_en = {
        "specific": f"Target Predicted Score: {expected_score}% (Goal Target: {target_needed}%)",
        "measurable": f"Track {study_hours} weekly study hours & {int(attendance)}% attendance",
        "achievable": "Follow the step-by-step 30-day preparation roadmap and daily timetable",
        "relevant": "Focus on high-yield exam papers, error notebook, and active recall",
        "time_bound": f"30-day exam countdown + maintain {sleep_hours} hours nightly sleep"
    }

    smart_method_hi = {
        "specific": f"लक्ष्य अनुमानित अंक: {expected_score}% (लक्ष्य अंक: {target_needed}%)",
        "measurable": f"साप्ताहिक {study_hours} घंटे अध्ययन और {int(attendance)}%+ उपस्थिति मापें",
        "achievable": "चरणबद्ध 30-दिवसीय तैयारी रोडमैप और दैनिक समय-सारणी का पालन करें",
        "relevant": "मुख्य परीक्षा प्रश्नों, त्रुटि नोटबुक और सक्रिय स्मरण पर ध्यान केंद्रित करें",
        "time_bound": f"30-दिवसीय परीक्षा उल्टी गिनती + प्रतिदिन {sleep_hours} घंटे नींद"
    }

    # Focus Areas
    focus_areas_en = [
        f"Increase study consistency by 30–45 minutes/day (Daily target: {daily_study} hrs)",
        "Improve active recall practice using past year exam papers",
        f"Maintain a consistent {sleep_hours} hrs/night sleep schedule"
    ]
    focus_areas_hi = [
        f"प्रतिदिन अध्ययन में 30-45 मिनट की निरंतरता बढ़ाएं (दैनिक लक्ष्य: {daily_study} घंटे)",
        "पुराने परीक्षा प्रश्न पत्रों का उपयोग करके सक्रिय स्मरण बढ़ाएं",
        f"नियमित {sleep_hours} घंटे/रात की नींद का पालन करें"
    ]

    if prediction_idx == 1:
        ai_coach_en = f"Awesome work! With an expected score of {expected_score}%, you have high potential! Follow your daily timetable and work hard on your error log to achieve {target_needed}%+!"
        ai_coach_hi = f"शानदार! {expected_score}% के अनुमानित अंक के साथ, आपमें उच्च क्षमता है! अपनी दैनिक समय-सारणी का पालन करें और {target_needed}%+ प्राप्त करने के लिए कठिन परिश्रम करें!"
    else:
        ai_coach_en = f"You have strong growth potential! Your current baseline is {expected_score}%. By adding 30-45 mins of daily active recall and following your timetable, you can achieve {target_needed}%!"
        ai_coach_hi = f"आपमें सुधार की अपार क्षमता है! आपका वर्तमान आधार {expected_score}% है। प्रतिदिन 30-45 मिनट का सक्रिय अभ्यास जोड़कर आप {target_needed}% प्राप्त कर सकते हैं!"

    return {
        "prediction": result_en,
        "prediction_hi": result_hi,
        "confidence": confidence,
        "expected_score": expected_score,
        "target_needed": target_needed,
        "score_gap": score_gap,
        "study_pct": round(min(100.0, (study_hours / 30.0) * 100.0), 1),
        "attend_pct": round(attendance, 1),
        "grades_pct": round(previous_grades, 1),
        "sleep_pct": round(min(100.0, (sleep_hours / 8.0) * 100.0), 1),
        "smart_method": smart_method_en,
        "smart_method_hi": smart_method_hi,
        "focus_areas": focus_areas_en,
        "focus_areas_hi": focus_areas_hi,
        "ai_coach": ai_coach_en,
        "ai_coach_hi": ai_coach_hi,
        "roadmap": roadmap_en,
        "roadmap_hi": roadmap_hi,
        "daily_timetable": daily_timetable_en,
        "daily_timetable_hi": daily_timetable_hi,
        "hard_work_strategy": hard_work_strategy_en,
        "hard_work_strategy_hi": hard_work_strategy_hi,
        "model_used": model_name,
        "input_features": input_data
    }

@app.route("/")
def index():
    default_input = {
        "study_hours": 15.0,
        "attendance": 85.0,
        "previous_grades": 75.0,
        "sleep_hours": 7.0,
        "extracurricular_activities": "No",
        "parental_education": "Bachelor",
        "internet_access": "Yes",
        "family_support": "Yes"
    }
    default_payload = generate_performance_payload(default_input, 1, [0.15, 0.85])
    return render_template(
        "index.html",
        prediction_res=default_payload,
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

    prediction_idx = int(model_pipeline.predict(df_input)[0])
    probabilities = model_pipeline.predict_proba(df_input)[0]

    response = generate_performance_payload(input_data, prediction_idx, probabilities)

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

