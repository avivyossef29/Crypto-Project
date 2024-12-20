# :warning: :poodle: :computer: Welcome to the POODLE attack CTF challenge :computer: :poodle: :warning:

## Introduction

This repository is a capture the flag type of game. You are an experienced hacker and you managed to perform a Man-in-the-Middle attack on an unsuspecting victim. You are now in the middle of the session between the victim and a site holding his private data (let's say a bank or something). You have the ability to force the victim to send requests to the site, modify them before they are sent and view the responses. Your mission is to find the session cookie that the victim holds which lets him access all his information.

## Background

The POODLE vulnerability (which stands for "Padding Oracle On Downgraded Legacy Encryption") was disclosed by Google on October 14, 2014. It targeted the SSL 3.0 protocol which was released back in 1996 and was still used up until 2015 when it was officially deprecated. The POODLE attack itself had many steps including a MITM, injecting a script to the user and even downgrading the security protocol to SSL 3.0 if the server already used later versions of TLS. This challenge only focuses on the cryptographic vulnerability of the protocol itself.

## Instructions

This project has a server folder and a client folder. As the attacker you are allowed to only write code in the *attacker.py* file in the client folder. Feel free to view all other folders it will help you understand how this challenge works. Below is an explanation of each file and APIs:

### ssl3.py

This is a module file created for the project that holds all the encryption functions used. It can help you see what is the process of the encryption and decryption of the messages. Here are some important notes: 
- The module uses AES-CBC with **block size 16** for encryption and for generating MACs. 

- The padding used sets the last byte of the padding as it's length and all other bytes are ignored (they are random or just the same byte repeated).

- When the server or user wish to encrypt their request they will first generate a MAC and append it to the request. Then all of that is padded and encrypted and then sent.

- When a request is being decrypted the logic is applied in reverse order. It is decrypted and the padding is removed (based on the last byte). Then the MAC is verified. If there were no errors with the padding or the MAC verification then the request is successfully received.

### server.py

This is the server that communicates with the victim. It holds the secret cookie along with the user and each request is verified to have the cookie. Requests that have wrong cookie are rejected. It has a set of keys and IVs (initialization vector) for the mac and the encryption. These are refreshed everytime a request is rejected (to simulate a connection drop in the SSL session). The endpoints in the server are not so important since all your interaction goes through the victim api.

### victim.py
This is the user you attack. All your interactions with the server go through him. He holds the cookie so only he can make calls to the server.

### victim_api.py

This is the API you are given for this challenge:

- **get_request(path, data):** This function gets a path in the url and data for the body of the request and returns the encrypted request that would be sent to the server (this is how you modify the requests)

- **send_request(request):** This function sends the request you provide to the server along with the cookie so the server will receive and try to decrypt it.

- **check_solution(cookie):** This is the last function to be called. You pass it the cookie you found and it will check if you solved the challenge.

### attacker.py

This is your script. Write your code only where it says you can. You are not allowed to add or change any imports.


## Running the Project

This project is meant to run with docker to ensure a closed independent environment. To run it just run `docker compose up -d --build`. This command will build the images of the server and client, create a private network and run the containers. If you don't use Docker Desktop you can view the logs of each container with `docker logs client_container` or `docker logs server_container`. If you need to change your code simply do `docker compose down` to shut down the running project and after you are done editing and ready to run then type again  `docker compose up -d --build`. This will rebuild the images.

You can also run it in your own environment. There is a list of dependencies in the *requirements.txt* file. You should run the server first with `python -u server.py & python -u victim.py` (in the server folder), and then run your script `python -u attacker.py` (in the client folder). The server needs to be up before the client since the client has to request the cookie form the server.  **Note that you will have to change the _SERVER_URL in the victim.py file to http://localhost:3000/ and both _SERVER_URL and _VICTIM_URL in the vicitm_api.py file to http://localhost:3000/ and http://localhost:4000/ respectively**

## Clues & Tips

My first tip to you is to read and watch a few videos on how the POODLE attack works. It is important that you understand what needs to be done for the attack to work. The next tips are hidden and feel free to reveal them if you feel stuck (recommended to reveal them in order).
The difficulty of the challenge is measured by how many tips you reveal:

- **Expert: 0 Tips** :skull:
- **Hard: 1 Tip** :crown:
- **Challenging: 2 Tips** :muscle: 
- **Intermediate: 3 Tips** :ok_hand:
- **Easy: 4 Tips** :-1:

<details style='font-weight: bold'> 
  <summary>Tip #1</summary>
   Find a way to use the fact that the last byte of the padding is not random. You can even control it.   
</details><br>

<details style='font-weight: bold'> 
  <summary>Tip #2</summary>
   You need to create a situation where you have a full block of padding when your request is sent. 
</details><br>

<details style='font-weight: bold'> 
  <summary>Tip #3</summary>
   You can see when does the server accept or refuse the request the victim sends. This can help you understand if your modified request fits the encryption protocol used. 
</details><br>

<details style='font-weight: bold'> 
  <summary>Tip #4</summary>
   Placing a block of the request as the last block of padding before the request is sent can give you specific information about the last byte of the block if the server accepts.
</details><br>

