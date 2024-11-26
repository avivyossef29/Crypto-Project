# :computer: :warning: :poodle: Welcome to the POODLE attack CTF challenge :poodle: :warning: :computer:

## Introduction

This repository is a capture the flag type of game. You are an experienced hecker and you managed to preform a Man-in-the-Middle attack on an unsuspecting victim. You are now in the middle of the session between the victim and a site holding his private data (let's say a bank or something). You have the ability to force the victim to send api calls the site, modify them before they are sent and veiw the responses. Your mission is to find the session cookie that the victim holds which lets him access all his information.

## Backgrond

The POODLE vulnerability (which stands for "Padding Oracle On Downgraded Legacy Encryption") was disclosed by Google on October 14, 2014. It targeted the SSL 3.0 protocol which was released back in 1996 and waws still used up until 2015 when it was officially deprecated. The POODLE attack itself had many steps including a MITM, injecting a script to the user and even downgrading the security protocol to SSL 3.0 if the server already used later versions of TLS. This challenge only focuses on the cryptographic vulnerability of the protocol itself.

## Instructions

This project has a server folder and aclient folder. As the attacker you are allowed to only write code in the attacker.py file in the client folder.


## Running the Project


## Clues & Tips

My first tip to you is to read and watch a few videos on how the POODLE attack works. It is important that you understand what needs to be done for the attack to work. The next tips are hidden and feel free to reveal them if you feel stuck.
The difficulty of the challenge is measured by how many tips you reveal:

- **Expert: 0 Tips** :skull:
- **Hard: 1 Tip** :muscle:
- **Intermediate: 2 Tips** :ok_hand:
- **Easy: 3 Tips** :-1:

<details style='font-weight: bold'> 
  <summary>Tip #1</summary>
   A1: JavaScript 
</details><br>

<details style='font-weight: bold'> 
  <summary>Tip #2</summary>
   A1: JavaScript 
</details><br>

<details style='font-weight: bold'> 
  <summary>Tip #3</summary>
   A1: JavaScript 
</details><br>

<details style='font-weight: bold'> 
  <summary>Tip #4</summary>
   A1: JavaScript 
</details><br>

