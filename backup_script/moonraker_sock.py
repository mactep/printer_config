import socket
import os
import json
import subprocess
import sys

# Define the path to the Unix socket and the script to trigger
SOCK_PATH = os.path.expanduser('~/printer_data/comms/moonraker.sock')
SYNC_SCRIPT = '/home/orangepi/git-sync.sh'

def run_sync_script():
    """
    Executes the git-sync.sh shell script.
    """
    print("--- Triggering git-sync.sh script ---")
    try:
        # We use subprocess.run to execute the shell script
        # The 'check=True' argument will raise an exception if the script fails
        # 'shell=True' is used to execute the command via the shell
        result = subprocess.run(
            [SYNC_SCRIPT],
            check=True,
            capture_output=True,
            text=True,
            shell=True
        )
        print("Script output:")
        print(result.stdout)
        print("--- Script completed successfully ---")
    except subprocess.CalledProcessError as e:
        print(f"Error: The script '{SYNC_SCRIPT}' failed with exit code {e.returncode}")
        print(f"Error output:\n{e.stderr}", file=sys.stderr)
    except FileNotFoundError:
        print(f"Error: The script '{SYNC_SCRIPT}' was not found. Please check the path.")
    except Exception as e:
        print(f"An unexpected error occurred while running the script: {e}")

def main():
    """
    Connects to the Moonraker Unix socket and listens for a specific update.
    """
    if not os.path.exists(SOCK_PATH):
        print(f"Error: The socket file was not found at {SOCK_PATH}.")
        print("Please ensure that the Moonraker service is running.")
        sys.exit(1)

    print(f"Connecting to Moonraker socket at {SOCK_PATH}...")
    try:
        # Create a Unix domain socket
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(SOCK_PATH)
            print("Successfully connected to the socket.")
            
            # Continuously read from the socket
            buffer = ""
            while True:
                # Read data in chunks
                data = s.recv(4096)
                if not data:
                    print("Connection closed by the server.")
                    break
                
                # Decode the data and append to the buffer
                buffer += data.decode('utf-8')
                
                # The messages are separated by the ETX character (0x03)
                messages = buffer.split('\x03')
                buffer = messages.pop() # Keep the last (incomplete) message in the buffer

                for msg in messages:
                    if msg.strip():
                        try:
                            # Parse the JSON message
                            message = json.loads(msg)
                            
                            # Check for the specific "notify_klippy_ready" method
                            if message.get("method") == "notify_klippy_ready":
                                print("\nDetected 'notify_klippy_ready' event.")
                                run_sync_script()
                                # You can exit after triggering, or continue listening
                                # If you want to continue listening for other events, remove this line:
                                # sys.exit(0)
                                
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON: {e}")
                            print(f"Faulty data: {msg}")
    
    except ConnectionRefusedError:
        print(f"Error: Connection refused. Is Moonraker running and listening on {SOCK_PATH}?")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
