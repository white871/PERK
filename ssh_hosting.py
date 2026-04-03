# For UI -> Host PI connection

import paramiko 

def connect(hostname = 'perkhost.local', password = 'perk', username = 'perkhost', network = 'perknet', timeout = 10):
    client = paramiko.SSHClient()
    #client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username = username, password = password, timeout = timeout)
        client.invoke_shell()
    except paramiko.ssh_exception.SSHException as e:
        print("Bad connection")
    stdin,stdout,stderr = client.exec_command(f'sudo nmcli device wifi hotspot ssid {perknet} password perk12345 hidden yes')
    stdin,stdout,stderr = client.exec_command(f'sudo nmcli connection modify Hotspot wifi.hidden yes')
    # sudo nmcli connection down Hotspot
    # sudo nmcli connection up Hotspot
    return client

def pair(client = None, time = 10):
    if client == None:
        assert False, "No client: Use this function with a working client"
    if client.get_transport() == None
        assert False, "Client is dead! Check for connection"
     
    #stdin, stdout, sterr = ssh.exec_command(f'hostapd_cli -i wlan0 wps_pbc -p /var/run/wpa_supplicant')   
    #stdin, stdout, stderr = ssh.exec_command(f'wpa_cli -i wlan0 scan; sleep {time}; wpa_cli -i wlan0 scan_results')
    stdin,stdout,stderr = ssh.exec_command()
    #perk@perk:~ $ sudo nmcli connection delete perknet
    #'Connection 'perknet' (0ff23857-5356-456b-80a4-f84b6c8c9cae) successfully deleted.
    #perk@perk:~ $ sudo nmcli dev wifi connect perknet password perk12345

def get_clients(client = None):
    stdin, stdout, stderr = ssh.exec_command(f'ip neigh show dev wlan0 nud reachable')
    