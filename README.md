# eth-watchdog

Needed commands: 
Note: You won't need to run this, if you are using gitpod
To run using gitpod, search this:
```
https://gitpod.io/new/#https://github.com/aaravm/eth-watchdog
```
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

# casino
casino game with Nodejs/Express, ReactJs/Redux and HTML Canvas\
You can play roulette, blackjack, slots, craps, poker (5 card draw and Texas Hold'em), keno and bet on races

## Screenshot00 - The Splash screen
![Image 0](./server/images/00.png)

## Screenshot01 - The Salon
![Image 1](./server/images/01.png)

## Screenshot02 - Roulette wheel and panel user
![Image 2](./server/images/02.png)

## Screenshot03 - Roulette board and panel chat
![Image 3](./server/images/03.png)

## Screenshot04 - Poker Texas hold'em
![Image 4](./server/images/04.png)