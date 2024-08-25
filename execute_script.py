import subprocess
import os
import asyncio

async def get_result_value():
    try:
    # Run player_client.py
        current_dir = os.getcwd()
        target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'nillion-python-starter/quickstart/client_code'))

        # Determine the command to run based on the current directory
        if current_dir != target_dir:
            command = f"cd {target_dir} && python3 player_client.py"
        else:
            command = "python3 player_client.py"

        # Run the command
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        
        # Extract the value of compute_event.result.value from the output
        for line in result.stdout.split('\n'):
            if "🖥️  THE UNIFIED SYSTEM IDENTIFIER FOR HARDWARE BAN" in line:
                value = line.split()[-1]
                if value.endswith('}'):
                    value = value[:-1]
                return value
        
        # If value doesn't get returned, use this defaultr instead
        result_value= "Jinesh123"
        return result_value
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit status {e.returncode}")
        print(f"Error output: {e.stderr}")
        return "Jinesh123"


if __name__ == "__main__":
    result_value = asyncio.run(get_result_value())
    print(f"Result Value: {result_value}")