# BEAST - Beginner & Advanced Challenges

## Overview
Each challenge created by removing some code parts of the E2E ’Attacker’ implementation, where the Advanced
challenge created by removing more parts than the Beginner.
Thus, you should start with the Advanced challenge, and only if you can’t solve it try the esaier ’Beginner’ challenge.
## Instructions
1. Complete the missing code parts denoted in ’ ?’. Notice that each ’ ?’ might be more than 1 line of code.
2. Run the script. If it prints the client's cookie, you have exploited the vulnerability and retrieved the flag.

## How to Run
As the CTF created from the E2E attack, it has the same design.
You should act in accordance with the instructions detailed in the README.md file of the E2E attack,
under the **Setup** section, **but instead of** running the original attacker image you need to run the following commands:

### Build and Run the Attacker

1. Navigate to the relevant CTF challenge directory (beginner or advanced).

2. Build the Docker image for the attacker:
   ```sh
   docker build -t attacker_ctf_image .
   ```

3. Run the CTF attacker container:
   ```sh
   docker run --rm -t --network=host attacker_ctf_image
   ```

To sum up, the steps are:
- Use 4 different terminals for the bank server, malicious server, client and attacker_ctf.
### Build and Run the Bank server
### Build and Run the Malicious server
### Build and Run the Attacker
Run the updated commands above.
### Build and Run the Client

## Hints
Any hints, if exist, will appear in a remark adjacent to the relevant missing code part.
