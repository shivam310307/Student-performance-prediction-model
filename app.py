import os
import sys
import importlib.util

# Add student_performance_prediction to Python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUB_DIR = os.path.join(BASE_DIR, 'student_performance_prediction')

if SUB_DIR not in sys.path:
    sys.path.insert(0, SUB_DIR)

# Dynamically import app from student_performance_prediction/app.py
spec = importlib.util.spec_from_file_location("student_perf_app", os.path.join(SUB_DIR, "app.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
app = module.app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
