import os
import platform
import socket
import subprocess


def ping_host(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]
    response = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return response.returncode == 0


def scan_single_port(ip, port, open_ports):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        result = s.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        s.close()
    except Exception:
        pass
