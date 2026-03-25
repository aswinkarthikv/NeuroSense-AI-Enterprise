import os
import sys

# Ensure the root dir is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app

app = create_app()

if __name__ == '__main__':
    # Run the Waitress or Flask dev server
    print("==================================================")
    print("🚀 DOCTOR LOGIN: doctor@neurosense.com")
    print("🔑 PASSWORD: doctor123")
    print("==================================================")
    print("Starting NeuroSense AI Enterprise Edition...")
    app.run(host='0.0.0.0', port=5000, debug=True)
