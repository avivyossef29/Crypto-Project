# Heartbleed Vulnerability Exploit - Beginner Challenge

## Overview
In this challenge, you need to craft a Heartbeat request that exploits the Heartbleed vulnerability.

## Instructions
1. Modify the fields of HEARTBEAT_REQUEST_HEX in the script to create a malicious request.
2. Run the script. If it prints `Success`, you have exploited the vulnerability and retrieved the flag.

## How to Run
```bash
python3 exploit_heartbleed.py

## Hint
if you need help understanding the vulnerability, run the script with the --hint option for guidance:

```bash
python3 exploit_heartbleed.py --hint
