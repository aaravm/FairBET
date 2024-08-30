import json
from nada_dsl import *
import os

def is_guess_in_target(array: List[SecretInteger], value: Integer) -> SecretBoolean:
    result = Integer(0)
    for element in array:
        result += (value == element).if_else(Integer(1), Integer(0))
    return (result > Integer(0))

def nada_main():
    
    user = Party(name="PLAYER")
    game = Party(name="GAME_MANAGER")
    
    secret_targets = [
        SecretInteger(Input(name=f"SECRET_TARGETS_{i}", party=game)) for i in range(5)
    ]
    
    secret_guess = SecretInteger(Input(name="SECRET_GUESS", party=user))
    
    is_present = is_guess_in_target(secret_targets, secret_guess)

    return [Output(is_present, "BET_RESULT", game)]
