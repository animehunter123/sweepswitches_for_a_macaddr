import os
import re

# IP addresses of the agg switches in the network
agg_switches = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]

# Regular expression to match MAC addresses
mac_regex = re.compile(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})")

# Dictionary to store the list of workstations connected to each switch
workstation_list = {}

# Loop through each switch and get the list of connected workstations
for switch in agg_switches:
    output = os.popen(f"ssh admin@{switch} show mac-address").read()
    matches = mac_regex.findall(output)
    workstation_list[switch] = matches

# Print the list of workstations connected to each switch
for switch, workstations in workstation_list.items():
    print(f"Workstations connected to switch {switch}:")
    for workstation in workstations:
        # Do a DNS lookup for each workstation
        hostname = os.popen(f"nslookup {workstation}").read()
        print(f"\t{workstation} ({hostname.strip()})")
