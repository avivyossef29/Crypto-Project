import subprocess
import time
import argparse

# Function to run shell commands
def run_command(command, capture_output=False):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=capture_output)
        return result.stdout.strip() if capture_output else None
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(e)
        return None

# Function to build and run the server
def build_and_run_server():
    print("Building the server Docker image...")
    build_cmd = "docker build -t openssl-heartbleed-server ./server_c"
    run_command(build_cmd)

    print("Running the server container...")
    run_server_cmd = "docker run --rm -d -p 443:443 --name heartbleed-server openssl-heartbleed-server"
    run_command(run_server_cmd)
    time.sleep(5)  # Allow the server to start

# Function to build and run the client
def build_and_run_client(server_ip):
    print("Building the client Docker image...")
    build_cmd = "docker build -t openssl-heartbleed-test ./client"
    run_command(build_cmd)

    print("Running the client to test the server...")
    run_client_cmd = f"docker run --rm openssl-heartbleed-test {server_ip}"
    client_output = run_command(run_client_cmd, capture_output=True)
    return client_output

# Main logic for checking challenge success or failure
def check_challenge_result(client_output, show_hint):
    if "Server is vulnerable to heartbleed" in client_output:
        print("Challenge Failed! The server is vulnerable to Heartbleed!")
        if show_hint:
            print("Hint: Make sure the server checks the payload length before returning data. The vulnerability occurs when the server returns more data than the client requests!")
    else:
        print("Challenge Success! The server is not vulnerable.")
        print("Flag: CTF_FLAG{Heartbleed_Patched_Successfully}")
        print("Famous Quote: 'The bug that broke the internet.' - on Heartbleed, a vulnerability affecting millions of websites and services.'")

# Main function
def main():
    # Add argument parsing for the hint option
    parser = argparse.ArgumentParser(description="Automate Heartbleed challenge")
    parser.add_argument('--hint', action='store_true', help="Show a hint if the challenge fails")
    args = parser.parse_args()

    # Step 1: Build and run the server
    build_and_run_server()

    # Step 2: Build and run the client, passing the server IP (localhost in this case)
    server_ip = "172.17.0.2"
    client_output = build_and_run_client(server_ip)

    # Step 3: Check the result and print the challenge outcome
    if client_output:
        check_challenge_result(client_output, args.hint)

    # Step 4: Clean up and stop the server container
    print("Stopping the server container...")
    stop_server_cmd = "docker stop heartbleed-server"
    run_command(stop_server_cmd)

if __name__ == "__main__":
    main()
