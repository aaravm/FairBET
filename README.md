# FairBET: A Casino Game Prioritizing User Trust and Data Privacy
A decentralized roulette platform focused on ensuring fair play, privacy, and trust using Nillion and Sign protocol. 
There are 2 parts to this projects:
1. Securely play roulette and other casino games, with all computations happening securely and privately on Nillion
2. Securely storing the hash of hardware ID of a user, so that banned user can't play from the same device

## Usage:
On information on how to use this repository locally, check [docs](./docs/usage.md)

## Motivation
The online casino industry has grown significantly, attracting millions of users worldwide. However, with real money at stake, concerns about fairness and cheating often arise. 
Users may worry whether the games are manipulated or if their personal data is secure. Similarly, game developers face the challenge of ensuring trust in their platforms while combating potential hackers and cheaters.

## System Architecture

## Features
To address these concerns, we introduce FairBET, a casino platform built with Nillion and Sign Protocol to enhance data privacy and foster trust. Currently, we offer two games: Roulette and Blackjack. Below are the key features we’ve integrated to ensure a fair and secure experience.

Roulette Game
In FairBET’s roulette, we’ve utilized Nillion to safeguard the user’s betting information. Here’s how it works:

 - A user’s bet remains completely private, stored on Nillion’s decentralized network, inaccessible to anyone—including game administrators.
Once the roulette wheel generates a result, it is sent to Nillion, which privately computes whether the user won or lost.
The result is returned securely, without exposing any sensitive data. This ensures that neither the game makers nor external actors can influence the outcome, promoting fairness and transparency.
Blackjack Game
In FairBET’s blackjack, we address the common concern that the deck may be manipulated or that cards could be unfairly swapped:

 - We store the state of the card deck on Nillion. After every move, the platform verifies whether there has been any tampering with the deck.
Additionally, Sign Protocol ensures that a user’s cards remain unchanged during gameplay. After each move, an attestation is generated, linking the current card sequence to the previous one. This cryptographic validation prevents any malicious activity from altering the cards, maintaining fairness throughout the game.
Security Features Beyond the Games

- To further enhance platform security, we’ve implemented a ban functionality for user misconduct in the chatroom. If a user misbehaves, they receive up to three warnings. After that:<br>
The system generates an attestation using Sign Protocol and permanently bans the user, preventing further logins.