from nada_dsl import *
import os
import json
import random

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
    UNIQUE_CARDS = []
    UNIQUE_SECRETS = []
    
    
    while len(UNIQUE_CARDS) < (num_parties * 2) + 5:
        random_number = random.randint(0, 51)
        # new_random_number = SecretInteger.random() % Integer(52)
        if random_number not in UNIQUE_CARDS:
            new_random_number = SecretInteger(Input(name=f"random_{random_number}", party=GAME_MANAGER))
            UNIQUE_CARDS.append(random_number)
            UNIQUE_SECRETS.append(new_random_number)
            
            
    outputs = []
    
    # ASSIGN TWO RANDOM NUMBERS IN THE NAME OF EACH PARTY 
    for i in range(num_parties - 1):
        outputs.append(Output(UNIQUE_SECRETS[i * 2], f"RANDOM_NUM{i+1}_1", parties[i]))
        outputs.append(Output(UNIQUE_SECRETS[(i * 2) + 1], f"RANDOM_NUM{i+1}_2", parties[i]))
    
    # ASSIGN 5 RANDOM NUMBERS TO GAME_MANAGER
    for j in range(5):
        outputs.append(Output(UNIQUE_SECRETS[(num_parties * 2) + j], f"GAME_MANAGER_CARD{j+1}", GAME_MANAGER))

    return outputs
