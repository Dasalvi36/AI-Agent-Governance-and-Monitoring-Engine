import time
import requests

API_URL = "http://127.0.0.1:8000/action"

def send_action(action_type, target):
    payload = {
        "action_type": action_type,
        "target": target
    }
    response = requests.post(API_URL, json=payload)
    print("Sent:", payload, "→ Response:", response.json())

def main():
    # Simulated sequence of actions
    actions = [
        ("read_file", "logs.txt"),
        ("read_file", "config.json"),
        ("write_file", "output.txt"),
        ("write_file", "secrets.txt"),
        ("run_command", "ls -la"),
        ("run_command", "rm -rf /"),
    ]

    for action_type, target in actions:
        send_action(action_type, target)
        time.sleep(1)  # wait 1 second between actions

if __name__ == "__main__":
    main()
