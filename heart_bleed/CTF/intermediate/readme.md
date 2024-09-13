# Intermediate Challenge: Heartbleed Vulnerability Demonstration

## Overview
In this challenge, you will tackle the **Heartbleed vulnerability**, a critical flaw in the Heartbeat protocol that allowed attackers to extract sensitive information from a server's memory. Your objective is to modify the server code to properly handle Heartbeat requests and prevent this vulnerability from being exploited.

## Challenge Objective
- **Modify the server code**: Ensure the server properly validates and handles Heartbeat requests, preventing memory leaks.
- **Verify your fix**: After modifying the server, run the provided Python test script to confirm that the vulnerability has been patched.

## Instructions

### Step 1: Modify the Server Code
1. Open the `server.c` file.
2. Identify the section of the code where the server handles Heartbeat requests.
3. Fix the vulnerability by ensuring the server **validates the payload length** against the actual size of the data before responding. This will prevent memory leakage and ensure the server is not vulnerable to Heartbleed exploits.

### Step 2: Run the Test Script
Once you’ve fixed the server, run the provided Python script to verify that your solution works:

```bash
python3 intermediate.py
```

## Hint Option
If you're unsure how to fix the vulnerability, you can run the script with the --hint option for guidance:

```bash
python3 intermediate.py --hint
```

## Challenge Success
Upon successfully fixing the vulnerability, you will see a famous quote related to the Heartbleed bug, along with a flag to indicate your success.

