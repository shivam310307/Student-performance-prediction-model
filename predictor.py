import joblib
import pandas as pd

model = joblib.load("student_score_predictor.pkl")

study_hours = float(input("Weekly Study Hours: "))
attendance = float(input("Attendance Percentage: "))
participation = float(input("Class Participation: "))

sample = pd.DataFrame({
    "weekly_self_study_hours":[12],
    "attendance_percentage":[50],
    "class_participation":[3.5]
})

prediction = model.predict(sample)

print(f"\nPredicted Total Score: {prediction[0]:.2f}")