## Usage

To do local installation, you have 3 different options:

### Option 1: Use Gitpod
To run using gitpod, search this:
```
https://gitpod.io/new/#https://github.com/aaravm/eth-watchdog
```
### Option 2: Use Docker
To run using docker:
Step 1: Building the containers
```
docker build -t nillion-python-starter .
```
Step 2: Run the Docker Container:
```
docker run -it nillion-python-starter
```
To run the servers:
```
docker build -f Dockerfile.flask -t flask-app .
docker run -p 5000:5000 flask-app
```

### Option 3: Build Locally
To run locally:

Step 1: Clone the Repository
Step 2: open the nillion-python-starter folder using:
```
cd nillion-python-starter/
```

Step 3: Install Nillion and its dependencies:
```bash
curl https://nilup.nilogy.xyz/install.sh | bash
```
```
nilup install latest 
nilup use latest 
nilup init
```
For telemetry analysis of wattelk address
```
nilup instrumentation enable --wallet <your-eth-wallet-address>
```

Install minimum python version
```
python3 --version
python3 -m pip --version
```

Create and activate virtual environment
```
python3 -m venv .venv
source .venv/bin/activate
```

Install the requirements from .txt file in root
```
pip install --upgrade -r requirements.txt
```

For compiling the nada file, run this in the same dir as nada.toml
```
nada build
```

Spinning up local devnet 
```
nillion-devnet
```

To run the client-code, go the respective directory and run: 
```
python3 <client-code>.py
```
