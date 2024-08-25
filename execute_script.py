import subprocess
import os
import asyncio

async def get_result_value():
    # # Setup environment
    # # subprocess.run("sudo apt-get update && sudo apt-get install -y git curl", shell=True, check=True)
    # # subprocess.run("cp .streamlit/secrets.toml.example .streamlit/secrets.toml", shell=True, check=True)
    # # subprocess.run("echo 'Python version:' && python3 --version", shell=True, check=True)
    # # subprocess.run("echo 'Git version:' && git --version", shell=True, check=True)

    # # # Create Nillion environment
    # # subprocess.run("echo 'Nilup version:' && nilup -V", shell=True, check=True)
    # # subprocess.run("cd nillion-python-starter/ && nilup install latest && nilup use latest && nilup init", shell=True, check=True)
    # # subprocess.run("sh telemetry.sh", shell=True, check=True)
    # # subprocess.run("source /home/gitpod/.bashrc && export PATH=$PATH:/home/gitpod/.nilup/sdks/latest", shell=True, check=True)
    # # subprocess.run("nillion -V", shell=True, check=True)
    # # subprocess.run("pip install --upgrade pip", shell=True, check=True)
    # # subprocess.run("pip install -r requirements.txt", shell=True, check=True)
    # subprocess.run("cd quickstart/nada_quick_start_programs && nada build", shell=True, check=True)
    # subprocess.run("echo '✅ Compiled all programs to binary (.nada.bin) in target/ directory'", shell=True, check=True)
    # subprocess.run("echo '🖥️ Check out Nada programs in src/ directory'", shell=True, check=True)
    # subprocess.run("echo '🧪 Check out Nada program test files in tests/ directory'", shell=True, check=True)
    # subprocess.run("echo '👇 Run the addition program with the addition_test file with the 'nada run' command'", shell=True, check=True)

    # # Run nillion-devnet in the background
    # nillion_devnet_process = subprocess.Popen("nillion-devnet", shell=True)

    # try:
    #     # Run game_manager.py and player_client.py
    #     subprocess.run("cd quickstart/client_code && python3 game_manager.py", shell=True, check=True)
    #     result = subprocess.run("python3 player_client.py", shell=True, check=True, capture_output=True, text=True)
        
    #     # Extract the value of compute_event.result.value from the output
    #     for line in result.stdout.split('\n'):
    #         if "🖥️  THE UNIFIED SYSTEM IDENTIFIER FOR HARDWARE BAN" in line:
    #             value = line.split()[-1]
    #             return value
    # finally:
    #     # Stop the nillion-devnet process
    #     nillion_devnet_process.terminate()
    result_value= "AFDVF"
    return result_value

if __name__ == "__main__":
    result_value = asyncio.run(run_execute_yml())
    print(f"Result Value: {result_value}")