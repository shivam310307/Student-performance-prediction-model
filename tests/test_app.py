import os
import sys
import unittest

# Ensure root and student_performance_prediction are in path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import app

class TestStudentPerformanceApp(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_index_route(self):
        """Test home index route returns 200 OK and renders main UI."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Student Growth', response.data)

    def test_predict_route_json(self):
        """Test API prediction route with JSON payload."""
        payload = {
            "study_hours": 25,
            "attendance": 90,
            "previous_grades": 82,
            "sleep_hours": 8,
            "extracurricular_activities": "Yes",
            "parental_education": "Bachelor",
            "internet_access": "Yes",
            "family_support": "Yes"
        }
        response = self.client.post('/predict', json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('prediction', data)
        self.assertIn('confidence', data)
        self.assertIn('expected_score', data)
        self.assertIn('daily_timetable', data)

    def test_predict_route_form(self):
        """Test API prediction route with Form submission."""
        form_data = {
            "study_hours": "18",
            "attendance": "88",
            "previous_grades": "78",
            "sleep_hours": "7",
            "extracurricular_activities": "Yes",
            "parental_education": "Master",
            "internet_access": "Yes",
            "family_support": "Yes"
        }
        response = self.client.post('/predict', data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Student Growth', response.data)

if __name__ == '__main__':
    unittest.main()
