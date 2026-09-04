import os
import platform
import queue
import socket
import subprocess


def ping_host(host: str) -> bool:
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]
    response = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return response.returncode == 0


def def scan_single_port(ip: str, port: int, result_queue: queue.Queue) -> None:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        result = s.connect_ex((ip, port))
        if result == 0:
            result_queue.put(port)
        s.close()
    except Exception:
        pass
