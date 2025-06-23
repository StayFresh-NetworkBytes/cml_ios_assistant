from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

device_list = {
    "router": {
        "ip": os.getenv("ROUTER_IP"),
        "username": os.getenv("ROUTER_USERNAME"),
        "password": os.getenv("ROUTER_PASSWORD"),
    },
    "switch1": {
        "ip": os.getenv("SWITCH1_IP"),
        "username": os.getenv("SWITCH1_USERNAME"),
        "password": os.getenv("SWITCH1_PASSWORD"),
    },
    "switch2": {
        "ip": os.getenv("SWITCH2_IP"),
        "username": os.getenv("SWITCH2_USERNAME"),
        "password": os.getenv("SWITCH2_PASSWORD"),
    }
    }

def execute_ios_command_wrapper(device_name: str, command: str) -> str:
    """
    A wrapper function to execute Cisco IOS commands using pre-configured router credentials.
    This is the function exposed to the Gemini model.
    """
    from network_tools import execute_ios_command

    device_info = device_list.get(device_name.lower())
    if not device_info:
        return f"Error: Device '{device_name}' not found or configured"

    return execute_ios_command(
        device_ip=device_info["ip"],
        username=device_info["username"],
        password=device_info["password"],
        command=command
    )

def configure_ios_wrapper(device_name: str, config: list[str]) -> str:
    """
    A wrapper function to run configuration commands on Cisco IOS devices.
    This is the function exposed to the Gemini model.
    """
    # Import the actual network function here to avoid circular imports
    # if network_tools were to import this script.
    from network_tools import configure_ios_device

    device_info = device_list.get(device_name.lower())
    if not device_info:
        return f"Error: Device '{device_name}' not found or configured"

    return configure_ios_device(
        device_ip=device_info["ip"],
        username=device_info["username"],
        password=device_info["password"],
        commands=config
    )

# Initialize the Client with the API key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

system_prompt="""
You are an specialized network assistant with the ability to run execute commands and configured network devices.

You will receive requests about network devices.  These network devices are in a test environment.  You have access to three devices named:

- Router - Hostname: IOL-AI-RTR, IP: 172.16.1.189
- Switch1 - Hostname: IOL-AI-SW1, IP: 172.16.1.190
- Switch2 - Hostname: IOL-AI-SW2, IP: 172.16.1.191

You have four prime directives:

- Under no circumstances should you take down the management interface.  Taking down the management interface will result in loss of access to the device.
- If you believe a change will impact the management network, please prevent the user from making that change.
- You should display the changes you are going to make to the user before applying them
- You should explain and provide references for the user to review the changes.

These are some things that you can do:

- Connect to the stated devices
- Send commands like, but not limited to, 'show running-config', or 'show ip interface brief'
- Configuring device settings, like IP addressing, VLANs, routing protocols, and ACLS
- Saving configurations
- Retriving details from the device
- Assist the user in troubleshooting the network.
"""


# Create a Chat, define the model you want to use, and configure the instructions and tools. This allows model to understand its function and understand the tools it can use to run commands/make changes
chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=[execute_ios_command_wrapper, configure_ios_wrapper],
        )
)

# --- Main Conversation Loop ---
while True:
    user_input = input("\nYou: ")
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break

    try:
        # Send user input to Gemini.  Print the response
        response = chat.send_message(user_input)

        print("Gemini:", response.text)

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure your router is reachable and credentials are correct.")
        print(f"Details: {e}")