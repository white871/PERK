import paramiko
import socket
import subprocess
import time

HOST = "perk.local"   # or IP
USER = "perk"
PASS = "perk"

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

def connect_wifi(ssh):
    NAME = "PERK_WIFI"
    PASSWORD = "perk12345"
    
    print(f"Connection to {NAME}")

    connect_cmd = f"sudo nmcli dev wifi connect {NAME} password {PASSWORD}"

    out, err = run_command(ssh, connect_cmd)

    print(out if out else err)

    print("Wifi connected.")

def setup_device_name():
    print("=== Device Setup ===")

    name = input("Enter a name for this Raspberry Pi (e.g. pi01): ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    # Write to file
    with open("device_id.txt", "w") as f:
        f.write(name)

    print(f"Hostname set to '{name}'")
    print("Saved to device_id.txt")

def menu():
    ssh = connect_ssh()
    print("Connected to Raspberry Pi.\n")

    while True:
        print("Select an option:")
        print("1 - Connect to WiFi / Hotspot")
        print("2 - Create Host Name File")
        print("3 - Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            connect_wifi(ssh)

        elif choice == "2":
            setup_device_name()

        elif choice == "3":
            print("Exiting...")
            ssh.close()
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    menu()