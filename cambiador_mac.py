import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest = "interface", help="Interface para cambiar interface")
    parser.add_option("-m", "--mac", dest = "new_mac", help="Nueva direccion MAC")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Por favor indicar una interfaz, utiliza --help para obtener ayuda")
    if not options.new_mac:
        parser.error("[-] Por favor indicar una nueva direccion MAC, utiliza --help para obtener ayuda")
    return options

def change_mac(interface,new_mac):
    print("[+] Cambiando Direccion MAC para "+ interface +" a " + new_mac)
    subprocess.call(["ifconfig",interface,"down"])
    subprocess.call(["ifconfig",interface,"hw","ether",new_mac])
    subprocess.call(["ifconfig",interface,"up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig",options.interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",ifconfig_result.decode('utf-8'))
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] No se pudo obtener la direccion MAC")
    return mac_address_search_result.group(0)

options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Actual MAC" + str(current_mac))

change_mac(options.interface,options.new_mac)
current_mac = get_current_mac(options.interface)

if current_mac == options.new_mac:
    print("[+] MAC cambiado correctamente a " + current_mac)
else:
    print("[-] MAC no ha sido cambiado")
