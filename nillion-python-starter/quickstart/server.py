from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)  # This will allow CORS for all origins

@app.route('/run-python', methods=['POST'])
def run_python():
    python_file = './client_code/verify_id.py'

    try:
        result = subprocess.run(['python3', python_file], capture_output=True, text=True)
        return jsonify({'output': result.stdout, 'error': result.stderr}), result.returncode
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
