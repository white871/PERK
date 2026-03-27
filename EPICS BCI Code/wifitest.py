import paramiko
import time

HOST = "perkhost.local"   # or IP
USER = "perkhost"
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


def setup_wifi(ssh):
    print("Setting up WiFi / Hotspot...")

    NAME = "PERK_WIFI"
    PASSWORD = "perk12345"

    commands = [
        "sudo apt update",
        "sudo apt install -y network-manager",
        "sudo systemctl start NetworkManager",
        f"sudo nmcli device wifi hotspot ssid {NAME} password {PASSWORD}"
    ]

    for cmd in commands:
        out, err = run_command(ssh, cmd)
        print(out if out else err)

    print("Basic setup complete.")


def check_devices(ssh):
    print("Checking connected devices...\n")

    cmd = "ip neigh show dev wlan0"
    out, err = run_command(ssh, cmd)

    print(out)

    if err:
        print("Error:", err)
        return

    devices = []

    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 4:
            ip = parts[0]
            mac = parts[2]
            state = parts[3]
            devices.append((ip, mac, state))

    if not devices:
        print("No devices found.")
        return

    print("Connected devices:")
    for i, (ip, mac, state) in enumerate(devices, 1):
        print(f"{i}. IP: {ip} | MAC: {mac} | State: {state}")


# -----------------------------
# MENU LOOP
# -----------------------------

def menu():
    ssh = connect_ssh()
    print("Connected to Raspberry Pi.\n")

    while True:
        print("\nSelect an option:")
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