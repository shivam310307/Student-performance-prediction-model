import os
import sys

# Add root directory and student_performance_prediction to Python path for serverless deployment
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(base_dir, 'student_performance_prediction'))

from app import app
