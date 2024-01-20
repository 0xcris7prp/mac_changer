import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()  # here parser is object $ child and can have all fuctions like it's father which is = nantr cha
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")

    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[!] Please spectify an interface, use --help for info")#code to handle error
    elif not options.new_mac:
        parser.error("[!] Please spectify new mac, use --help for info")#code to handle error
    return options
def change_mac(interface, new_mac):
    print("Changing MAC address of " + interface + " to " + new_mac)
    # Down the interface
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    # Change the MAC address
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    # Up the interface
    subprocess.call(["sudo", "ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode("utf-8")
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.strip())
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[!] Could not get mac address")

options  = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current MAC= " + str(current_mac))

change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not changed.")
