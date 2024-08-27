from nada_dsl import *

def nada_main():
    user = Party(name="User")
    game = Party(name="Game Manager")
    a = SecretInteger(Input(name="secret_guess", party=user))
    b = SecretInteger(Input(name="secret_target", party=game))

    result = a == b

    return [Output(result, "is_same_num", game)]