#!/usr/bin/env python
import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its Mac address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New Mac address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] please specify an interface, use --help for more info")
    elif not options.new_mac:
        parser.error("[-] please specify a mac, use --help for more info")
    return options

def change_mac(interface, new_mac):
    print("[+] Changing mac adress for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",ifconfig_result)  # ifconfig result with regex

    if mac_address_search_result:
        return mac_address_search_result.group(0)  # mac address print, 0 > first group or first result.
    else:
        print("[-] Could not read Mac address.")

options = get_arguments()
current_mac = get_current_mac(options.interface)
print("[+] Current Mac = " + str(current_mac))
change_mac(options.interface, options.new_mac)

current_mac=get_current_mac(options.interface)

if current_mac==options.new_mac:
    print("[+] Mac address was successfully changed to" + current_mac)
else:
    print("[-] Mac address did not get changed.")

#subprocess.call("ifconfig " + interface + "down",shell=True) Not secure.Basically, user can hijack this program and get it to execute other commands.