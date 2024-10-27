# Project Overview: Browser Exploit Against SSL/TLS (BEAST) and CTF Challenges

This project demonstrates the **BEAST attack** (CVE-2011-3389) through an End-to-End (E2E) attack and provides 2 Capture The Flag (CTF) challenges.
It is an attack against network vulnerabilities in TLS 1.0 and older SSL protocols, allows attackers to decrypt encrypted data (cookies) sent by client to server.

## End-to-End Attack Demonstration
This section of the project simulates a complete attack lifecycle, illustrating how the BEAST attack exploits known vulnerability of the CBC mode of operation. The demonstration involves:
- Setting up **TLS 1.0 bank server**.
- Setting up **malicious website server**.
- **Client** interacting with the malicious website.
- **MITM Attacker** performing the attack and manage to get the client's secret cookies.

## CTF Challenges

Two CTF challenges: **Beginner** and **Advanced**. Each challenge created by removing some code parts of the E2E ’Attacker’ implementation, where the Advanced challenge created by removing more parts than the Beginner.
Participants should add the missing code parts, denoted by '?'.
