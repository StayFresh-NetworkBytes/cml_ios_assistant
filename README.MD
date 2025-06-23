# Cisco IOS Network Assistant

**DISCLAIMER** the provided scripts are a sample of what is possible for interactions between network devices, a tool like netmiko, and an LLM.  **DO NOT RUN this on a production network.  It is intended to be run in the provided CML Lab** 

This is a sample network assistant for Cisco IOS devices.  It leverages Google Gemini and the gemini-2.5-flash model to interact with network devices.  The devices are defined in a file called '.env' and match the provided CML Lab IP addresses.  The network_tools.py script contains the functions to run show commands and configuration commands.  The ios_assistant.py file contains the function calls to the network_tools.py script and the necessary config to allow your Gemini chat session.

These python scripts have been used to operate CML nodes with VRF'd management addresses.  The CML Lab has been provided with a base level config for management access to the devices.

Devices included in the .env file:

- ROUTER_IP: 172.16.1.189
- SWITCH1_IP: 172.16.1.190
- SWITCH2_IP: 172.16.1.191

Username / password for all hosts and network nodes is: netadmin / s3cr3tpw1

The username and password for all three hosts is included in the .env file.  You need to obtain a GEMINI_API key from https://aistudio.google.com/. Once obtained, add the string to your .env in the "GEMINI_API_KEY=" variable and save the file so that you can begin testing.

## Get started

Note: This lab was created with CML 2.8.1.  It will not work with versions less than this release.

Download the Gemini-LLM-Lab.yaml file from this repo.  

Import the Gemini-LLM-Lab.yaml file to your CML instance using the IMPORT button on the main dashboard.  Once imported, open the lab.

You will likely need to update the IP address of the Ubuntu host in CML.  To do so:

* Select the Ubuntu-Jumphost node.
* Select the CONFIG tab in the pop out window
* Look for ENS2, a comment says "#External LAN - Set to an available address on your personal network"
* You need to update the address, default route, and name servers under ENS2.  They are currently set to addresses in a 192.168.1.0/24 subnet
* SAVE the CONFIG when you are done making changes
* Start the lab

The CML External connector is set to bridge mode for ENS2, this allows you to get to the internet and SSH directly to the ubuntu-jumphost.  This is the preferred way to operate.  The ubuntu node will download all necessary packages and update itself using the cloud-config.  When Cloud-Config is complete you can log in and follow the instructions below.

## SSH to the Ubuntu Node

Once Ubuntu is fully booted, ssh to the host as netadmin@***your host ip*** (Ex. ssh netadmin@192.168.1.190)

**Clone this repo to the host:**
```
git clone https://github.com/StayFresh-NetworkBytes/cml_ios_assistant.git
cd cml_ios_assistant
```

**Create a python virtual environment and source it**
```
python3 -m venv .venv
source .venv/bin/activate
```

**Install the python requirements**
```
pip3 install -r requirements.txt
```

**Obtain the SSH key for the IOL router and IOL-L2 switches**
```
ssh -o StrictHostKeyChecking=accept-new netadmin@172.16.1.189
ssh -o StrictHostKeyChecking=accept-new netadmin@172.16.1.190
ssh -o StrictHostKeyChecking=accept-new netadmin@172.16.1.191
```

**Edit (vi/nano/etc) the .env file and add YOUR gemini API key after the equals sign and save**
```
GEMINI_API_KEY=
```

At this point you can run the ios_assistant.py file

```
python3 ios_assistant.py
```

## What can you do?

The assistant has been fed a prompt outline its functions.  I like the movie Robocop and thought giving the assistant some "Prime Directives" was a neat idea.  You can read the prompt below

This prompt devices 

```
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
```