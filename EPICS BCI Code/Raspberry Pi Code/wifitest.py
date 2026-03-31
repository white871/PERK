import paramiko
from scp import SCPClient
import socket
import time

HOST = "perkhost.local"   # or IP
USER = "perkhost"
PASS = "perk"

CLIENT_USER = "perk"
CLIENT_PASS = "perk"

def connect_ssh():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username=USER, password=PASS)
    return ssh


def run_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode()
    error = stderr.read().decode()
    return output, error


def setup_wifi(ssh):
    print("Setting up WiFi / Hotspot...")

    NAME = "PERK_WIFI"
    PASSWORD = "perk12345"

    cmd = f"sudo nmcli device wifi hotspot ssid {NAME} password {PASSWORD}"
    
    out, err = run_command(ssh, cmd)
    print(out if out else err)

    print("Basic setup complete.")


def check_devices(ssh):
    print("Checking connected devices...\n")

    cmd = "ip neigh show dev wlan0"
    out, err = run_command(ssh, cmd)

    if err:
        print("Error:", err)
        return

    ips = []

    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 4 and parts[-1] == "REACHABLE":
            ips.append(parts[0])

    if not ips:
        print("No devices found.")
        return

    print("Requesting device identities...\n")

    devices = []

    for ip in ips:
        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, username=CLIENT_USER, password=CLIENT_PASS, timeout=2)

            scp = SCPClient(client.get_transport())
                
            # Download a file
            scp.get('device_id.txt', f"{ip}_name.txt")
            scp.close()

            # read it
            with open(f"{ip}_name.txt", "r") as f:
                name = f.read().strip()

            devices.append((name, ip))

            client.close()
        except Exception:
            # ignore devices that don't respond
            continue

    if not devices:
        print("No Raspberry Pis responded.")
        return

    print("Connected Raspberry Pis:")
    for i, (name, ip) in enumerate(devices, 1):
        print(f"{i}. {name} → {ip}")

# -----------------------------
# MENU LOOP
# -----------------------------

def menu():
    ssh = connect_ssh()
    print("Connected to Raspberry Pi.\n")

    while True:
        print("Select an option:")
        print("1 - Setup WiFi / Hotspot")
        print("2 - Check connected devices")
        print("3 - Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            setup_wifi(ssh)

        elif choice == "2":
            check_devices(ssh)

        elif choice == "3":
            print("Exiting...")
            ssh.close()
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    menu()