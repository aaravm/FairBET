from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import requests

app = Flask(__name__)
CORS(app)  # This will allow CORS for all origins
data_store = []
secret_target=-1
secret_guess=-1
hardware_id=-1

@app.route('/set-secret-guess', methods=['POST'])
def set_data_guess():
    global secret_guess
    # Get the JSON data from the request
    data = request.get_json()
    # Store the data in the in-memory list
    secret_guess=data.get('guess', -1)
    return jsonify({"message": "Data received successfully", "data": secret_guess}),200

@app.route('/set-secret-target', methods=['POST'])
def set_data_target():
    global secret_target
    # Get the JSON data from the request
    data = request.get_json()
    # Store the data in the in-memory list
    secret_target=data.get('target', -1)
    return jsonify({"message": "Data received successfully", "data": secret_target}),200

@app.route('/set-secret-hardawre-id', methods=['POST'])
def set_hardware_id():
    global hardware_id
    # Get the JSON data from the request
    data = request.get_json()

    # Store the data in the in-memory list
    hardware_id=data.get('hardware_id', -1)
    return jsonify({"message": "Data received successfully", "data": hardware_id}),200

@app.route('/get-secret-target', methods=['GET'])
def get_secret_target():
    return jsonify({'output': secret_target}), 200

@app.route('/get-secret-guess', methods=['GET'])
def get_secret_guess():
    return jsonify({'output': secret_guess}), 200

@app.route('/get-hardware-id', methods=['GET'])
def get_hardware_id():
    return jsonify({'output': hardware_id}), 200

@app.route('/run-python', methods=['GET'])
def run_python():
    python_file = './verify_id.py'
    param1 = request.args.get('username')

    try:
        result = subprocess.run(['python3', python_file, param1], capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({'output': result.stdout.strip(), 'error': result.stderr.strip()}), 200
        else:
            return jsonify({'output': result.stdout, 'error': result.stderr}), result.returncode
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/get-result', methods=['GET'])
def get_result():
    python_file = './return_slots.py'
    try:
        result = subprocess.run(['python3', python_file], capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({'output': result.stdout.strip(), 'error': result.stderr.strip()}), 200
        else:
            return jsonify({'output': result.stdout.strip(), 'error': result.stderr}), result.returncode
    except Exception as e:
        return jsonify({'error': str(e)}), 500  
    
@app.route('/set-user', methods=['POST'])
def set_user():
    
    python_file = './setuser.py'
    param1 = request.args.get('username')

    try:
        result = subprocess.run(['python3', python_file,param1], capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({'output': result.stdout.strip(), 'error': result.stderr.strip()}), 200
        else:
            return jsonify({'output': result.stdout, 'error': result.stderr}), result.returncode
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# NEW ROUTE TO HANDLE THE "/GET-PLAYER" REQUEST
# TODO: REDUNDANT CODE


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
    
@app.route('/get-bets', methods=['GET'])
def get_bets():
    try:
        # FIXME: SET THE CORRECT URL
        response = requests.get('http://localhost:2000/get-bets')
        
        if response.status_code == 200:
            data = response.json()
            bets = response['bets']
            
            bets = ["LOW", "HIGH", "RED", "BLACK", "ODD", "EVEN"]            
            return jsonify({'bets': bets}), 200
        else: 
            return jsonify({'error': 'Failed to retrieve the bets'}), response.status_code
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)
