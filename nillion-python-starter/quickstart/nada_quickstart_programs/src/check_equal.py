from nada_dsl import *

def nada_main():
    user = Party(name="PLAYER")
    game = Party(name="GAME_MANAGER")
    a = SecretInteger(Input(name="SECRET_GUESS", party=user))
    b = SecretInteger(Input(name="SECRET_TARGET", party=game))

    result = a == b

    return [Output(result, "IS_SAME_NUM", game)]