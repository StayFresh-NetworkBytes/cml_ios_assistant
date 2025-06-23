# network_tools.py
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import os
from dotenv import load_dotenv


# Load environment variables from a .env file
load_dotenv()

def get_device_connection(host, username, password, secret=None):
    """
    Establishes a Netmiko connection to a Cisco IOS device.
    Returns a Netmiko ConnectHandler object if successful, None otherwise.
    """
    device = {
        'device_type': 'cisco_ios',
        'host': host,
        'username': username,
        'password': password,
        'secret': secret, # Enable secret if needed
    }
    try:
        net_connect = ConnectHandler(**device)
        return net_connect
    except NetmikoTimeoutException:
        print(f"Error: Connection to {host} timed out. Check IP, port, and reachability.")
        return None
    except NetmikoAuthenticationException:
        print(f"Error: Authentication failed for {host}. Check username and password.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred connecting to {host}: {e}")
        return None

def execute_ios_command(device_ip: str, username: str, password: str, command: str, secret: str = None) -> str:
    """
    Executes a single show or operational command on a Cisco IOS device and returns the output.
    This function is designed to be called by an AI model.

    Args:
        device_ip (str): The IP address of the Cisco IOS device.
        username (str): The username for SSH access.
        password (str): The password for SSH access.
        command (str): The Cisco IOS command to execute (e.g., "show ip int brief").
        secret (str, optional): The enable secret password if needed for privilege escalation.

    Returns:
        str: The command output from the device, or an error message if the operation fails.
    """
    net_connect = get_device_connection(device_ip, username, password, secret)
    if net_connect:
        try:
            output = net_connect.send_command(command)
            return output
        except Exception as e:
            return f"Error executing command '{command}' on {device_ip}: {e}"
        finally:
            net_connect.disconnect()
    else:
        return f"Could not establish connection to {device_ip} to execute command '{command}'."

def configure_ios_device(device_ip: str, username: str, password: str, commands: list[str], secret: str = None) -> str:
    """
    Applies a list of configuration commands to a Cisco IOS device.
    This function is designed to be called by an AI model.

    Args:
        device_ip (str): The IP address of the Cisco IOS device.
        username (str): The username for SSH access.
        password (str): The password for SSH access.
        commands (list[str]): A list of Cisco IOS configuration commands (e.g., ["interface Loopback0", "ip address 1.1.1.1 255.255.255.255"]).
        secret (str, optional): The enable secret password if needed for privilege escalation.

    Returns:
        str: The output of the configuration commands, or an error message if the operation fails.
    """
    net_connect = get_device_connection(device_ip, username, password, secret)
    if net_connect:
        try:
            output = net_connect.send_config_set(commands)
            return output
        except Exception as e:
            return f"Error applying configuration on {device_ip}: {e}"
        finally:
            net_connect.disconnect()
    else:
        return f"Could not establish connection to {device_ip} to apply configuration."

if __name__ == "__main__":
    # This block is for testing your Netmiko functions independently
    # Replace with your router's actual details
    ROUTER_IP = os.getenv("ROUTER_IP")
    ROUTER_USERNAME = os.getenv("ROUTER_USERNAME")
    ROUTER_PASSWORD = os.getenv("ROUTER_PASSWORD")

    print(f"--- Testing 'execute_ios_command' on {ROUTER_IP} ---")
    output = execute_ios_command(ROUTER_IP, ROUTER_USERNAME, ROUTER_PASSWORD, "show ip interface brief")
    print(output)

    # We are focusing on 'show' commands, so you can comment out the config test
    # print(f"\n--- Testing 'configure_ios_device' on {ROUTER_IP} (creating a loopback) ---")
    # config_commands = [
    #     "interface Loopback99",
    #     "description Test_Loopback_by_Gemini",
    #     "ip address 192.168.99.1 255.255.255.0",
    #     "no shutdown"
    # ]
    # output = configure_ios_device(ROUTER_IP, ROUTER_USERNAME, ROUTER_PASSWORD, config_commands, ROUTER_SECRET)
    # print(output)

    print("\n--- Testing complete for network_tools.py ---")