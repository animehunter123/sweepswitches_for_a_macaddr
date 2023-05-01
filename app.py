from flask import Flask, render_template
import os
import re

app = Flask(__name__)

agg_switches = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]
mac_regex = re.compile(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})")
workstation_list = {}

@app.route("/")
def index():
    for switch in agg_switches:
        output = os.popen(f"ssh admin@{switch} show mac-address").read()
        matches = mac_regex.findall(output)
        workstation_list[switch] = matches
    
    workstation_info = []
    for switch, workstations in workstation_list.items():
        for workstation in workstations:
            hostname = os.popen(f"nslookup {workstation}").read()
            workstation_info.append({
                "switch": switch,
                "mac_address": workstation,
                "hostname": hostname.strip(),
            })
    
    return render_template("index.html", workstation_info=workstation_info)
