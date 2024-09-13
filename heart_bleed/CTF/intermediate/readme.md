Intermediate Challenge: Heartbleed Vulnerability Demonstration
Overview
This challenge demonstrates the Heartbleed vulnerability, a serious security flaw in the Heartbeat protocol that allowed attackers to extract sensitive information from memory. Your task is to modify the server code to properly handle Heartbeat requests and prevent this vulnerability.

Challenge Objective
Modify the server code: Ensure that it validates and handles Heartbeat requests correctly, preventing memory leaks.
Run the Python test script after making changes to the server code to confirm that the vulnerability has been patched.
Instructions
Step 1: Modify the Server Code
Open the server.c file.
Identify and fix the vulnerable part of the code where the server handles Heartbeat requests.
Ensure the server validates the payload length against the actual size of the data before responding, preventing memory leakage.
Step 2: Run the Test Script
After fixing the server, run the provided Python script to verify your solution:

bash
Copy code
python3 intermediate.py
If your fix is correct, the script will display Challenge Success, a famous quote related to Heartbleed, and a flag.

Hint Option
If you're unsure how to fix the vulnerability, you can run the script with the --hint option for guidance:

bash
Copy code
python3 intermediate.py --hint
Challenge Success
Upon successfully fixing the vulnerability, you will see a famous quote related to the Heartbleed bug, along with a flag to indicate your success.

