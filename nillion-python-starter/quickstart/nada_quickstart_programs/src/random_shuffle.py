from nada_dsl import *
import os
import json

def load_creds(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {"PLAYERS": {}}

def nada_main():
    CRED_STORE = "../../client_code/credential_store.json"
    credentials = load_creds(CRED_STORE)
    num_parties = len(credentials['PLAYERS']) + 1
    PLAYERS = credentials['PLAYERS']
        
    parties = [Party(name=PLAYERS[player]["party_name"]) for player in PLAYERS]
    GAME_MANAGER = Party(name="GAME_MANAGER")
    UNIQUE_SECRETS = []
    
    # Generate unique random numbers using Nada's secure random number generation
    while len(UNIQUE_SECRETS) < (num_parties * 2) + 5:
        new_random_number = SecretInteger.random() % Integer(52)
        UNIQUE_SECRETS.append(new_random_number)
            
    outputs = []
    
    # Assign two random numbers to each party
    for i in range(num_parties - 1):
        outputs.append(Output(UNIQUE_SECRETS[i * 2], f"RANDOM_NUM{i+1}_1", parties[i]))
        outputs.append(Output(UNIQUE_SECRETS[(i * 2) + 1], f"RANDOM_NUM{i+1}_2", parties[i]))
    
    # Assign 5 random numbers to GAME_MANAGER
    for j in range(5):
        outputs.append(Output(UNIQUE_SECRETS[(num_parties * 2) + j], f"GAME_MANAGER_CARD{j+1}", GAME_MANAGER))

    return outputs
