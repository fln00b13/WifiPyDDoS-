#    Import subprocess so we can use system commands.
import subprocess

#    Import the re module so we can make use of regular expressions. 
import re

#    Python allows us to run system commands using the function 
#    provided by the subprocess module; 
#    (subprocess.run(<list of command line arguments go here>, <specify the second argument if you want to capture the output>)).
#
#    This script is a parent process that creates a child process which 
#    runs a system command and will only continue once the child process 
#    is completed. 
#
#    To save the contents that get sent to the standard output stream 
#    (the terminal), we must first specify that we want to capture the output.
#    To do this we specify the second argument as capture_output = True. 
#    This information gets stored in the stdout attribute as bytes and 
#    needs to be decoded before being used as a String in Python.
command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()

profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

wifi_list = []

if len(profile_names) != 0:
    for name in profile_names:
        wifi_profile = {}
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

for x in range(len(wifi_list)):
    print(wifi_list[x]) 