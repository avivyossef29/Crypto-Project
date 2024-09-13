This project demonstrates the Heartbleed vulnerability (CVE-2014-0160) through an End-to-End (E2E) attack and provides two CTF challenges. The Heartbleed vulnerability, one of the most significant security issues in internet history, allowed attackers to extract sensitive data from a server's memory by exploiting a flaw in the Heartbeat protocol of OpenSSL.

1. End-to-End Attack Demonstration
This part of the project simulates the complete attack lifecycle, demonstrating how the Heartbleed vulnerability can be exploited to extract sensitive data. It involves setting up a vulnerable SSL server, interacting with two clients, and showcasing the memory leakage attack in action.

2. CTF Challenges
Two CTF (Capture The Flag) challenges are provided in this project:

Beginner Challenge: Modify a vulnerable server code to stop the memory leak and protect against Heartbleed.
Intermediate Challenge: Fix a simulated Heartbleed vulnerability by ensuring the server validates the payload length properly before returning data to the client.
