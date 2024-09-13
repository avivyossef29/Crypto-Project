# Project Overview: Heartbleed Vulnerability Exploit and CTF Challenges

This project demonstrates the **Heartbleed vulnerability** (CVE-2014-0160) through an End-to-End (E2E) attack and provides two Capture The Flag (CTF) challenges. The Heartbleed vulnerability, regarded as one of the most severe security flaws in internet history, allowed attackers to extract sensitive information from a server's memory by exploiting a flaw in the Heartbeat protocol of OpenSSL.

## End-to-End Attack Demonstration
This section of the project simulates a complete attack lifecycle, illustrating how the Heartbleed vulnerability can be exploited to extract sensitive data. The demonstration involves:
- Setting up a **vulnerable SSL server**.
- Interacting with **two clients**.
- Showcasing the **memory leakage attack** in action, revealing how attackers could extract data from server memory.

## CTF Challenges

Two CTF challenges are designed for participants to both exploit and secure systems affected by the Heartbleed vulnerability:

### Beginner Challenge
- **Objective**: Modify the vulnerable server code to stop the memory leak and protect against the Heartbleed vulnerability.
- **Task**: Ensure that the server properly handles Heartbeat requests and prevents memory leaks.

### Intermediate Challenge
- **Objective**: Fix a simulated Heartbleed vulnerability by ensuring that the server properly validates the payload length before returning data to the client.
- **Task**: Modify the server code to patch the vulnerability and test it with the provided Python script to verify that the fix is effective.
