from nada_dsl import *

def nada_main():
    PLAYER = Party(name="PLAYER")
    SECRET1 = SecretInteger(Input(name="SECRET1", party=PLAYER))
    SECRET2 = SecretInteger(Input(name="SECRET2", party=PLAYER))
    
    RESULT = SECRET1 + SECRET2 
    
    return [Output(RESULT, "RESULT", PLAYER)]