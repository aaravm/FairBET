from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import requests

app = Flask(__name__)
CORS(app)  # This will allow CORS for all origins

@app.route('/run-python', methods=['GET'])
def run_python():
    python_file = './verify_id.py'

    try:
        result = subprocess.run(['python3', python_file], capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({'output': result.stdout.strip(), 'error': result.stderr.strip()}), 200
        else:
            return jsonify({'output': result.stdout, 'error': result.stderr}), result.returncode
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# NEW ROUTE TO HANDLE THE "/GET-PLAYER" REQUEST
@app.route('/get-player', methods=['GET'])
def get_player():
    try: 
        # FIXME: SET THE CORRECT URL
        response = requests.get('http://localhost:2000/player')
        
        if response.status_code == 200:
            data = response.json()
            player_alias = data.get('player_alias', 'PLAYER') # FALL BACK TO 'PLAYER' IF KEY IS MISSING
            return jsonify({'player_alias': player_alias}), 200
        else: 
            return jsonify({'error': 'Failed to retrive player alias'}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-secret', methods=['GET'])
def get_target():
    try: 
        # FIXME: SET THE CORRECT URL
        response = requests.get('http://localhost:2000/secret')
        
        if response.status_code == 200:
            
            data = response.json()
            secret_target = data.get('secret_target', 'SECRET_TARGET')
            secret_guess = data.get('secret_guess', 'SECRET_GUESS')
            
            return jsonify({'secret_target': secret_target},{'secret_guess': secret_guess}), 200
        else: 
            return jsonify({'error': 'Failed to retrive player alias'}), response.status_code
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)
