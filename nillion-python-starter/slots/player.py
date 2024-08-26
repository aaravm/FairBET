import asyncio
import os
import py_nillion_client as nillion


from py_nillion_client import NodeKey, UserKey
from dotenv import load_dotenv
from nillion_python_helpers import get_quote_and_pay, create_nillion_client, create_payments_config

from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey


async def main():
    PROGRAM_NAME="main"
    PROGRAM_PATH = f"../nada_quickstart_programs/target/{PROGRAM_NAME}.nada.bin"

    # GET NILLION-DEVNET CREDENTIALS
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    grpc_endpoint = os.getenv("NILLION_NILCHAIN_GRPC")
    chain_id = os.getenv("NILLION_NILCHAIN_CHAIN_ID")
    
    # CREATE THE PAYMENTS CONFIG, SET UP NILLION WALLET etc.
    payments_config = create_payments_config(chain_id, grpc_endpoint)
    payments_client = LedgerClient(payments_config)
    payments_wallet = LocalWallet(
        PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
        prefix="nillion",
    )

    # TODO: replace seed with id received from frontend
    seed = "PLAYER"
    user_key = UserKey.from_seed(seed)
    node_key = NodeKey.from_seed(seed)
    player = create_nillion_client(user_key, node_key)

    receipt_store_program = await get_quote_and_pay(
        player,
        nillion.Operation.store_program(PROGRAM_PATH),
        payments_wallet,
        payments_client,
        cluster_id,
    )

    # TODO: Get secret_guess and secret_target from frontend
    secret_guess=10
    secret_target=10

    result= nillion.NadaValues(
        {
            "secret_guess": nillion.SecretInteger(secret_guess),
            "secret_target": nillion.SecretInteger(secret_target)
        }
    )
    print(result)

if __name__ == "__main__":
    asyncio.run(main()) 