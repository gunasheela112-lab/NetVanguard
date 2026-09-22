import platform
import queue
import socket
import subprocess
import time
from typing import Optional


def ping_host(host: str, timeout: float = 2.0) -> bool:
    """Return True when the host responds to a single ICMP echo request."""
    return ping_host_diagnostic(host, timeout)["reachable"]


def ping_host_diagnostic(host: str, timeout: float = 2.0) -> dict:
    """Run a single ping and return reachability plus latency/error details."""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    timeout = max(float(timeout), 0.1)
    command = ["ping", param, "1", host]

    if platform.system().lower() == "windows":
        command.extend(["-w", str(int(timeout * 1000))])
    else:
        command.extend(["-W", str(max(1, int(timeout)))])

    started = time.perf_counter()
    try:
        response = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout + 1,
            text=True,
            check=False,
        )
    except (subprocess.TimeoutExpired, OSError) as exc:
        return {"reachable": False, "latency_ms": None, "error": str(exc)}

    latency_ms = round((time.perf_counter() - started) * 1000, 2)
    return {
        "reachable": response.returncode == 0,
        "latency_ms": latency_ms if response.returncode == 0 else None,
        "error": None if response.returncode == 0 else response.stderr.strip() or "Host did not respond",
    }


def resolve_host(host: str) -> Optional[str]:
    """Resolve a hostname to an IPv4 address."""
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return None


def scan_single_port(host: str, port: int, result_queue: queue.Queue, timeout: float = 1.0) -> None:
    """Scan one TCP port and place a structured result in the queue."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(max(float(timeout), 0.1))
    try:
        result = sock.connect_ex((host, port))
        result_queue.put({
            "port": port,
            "status": "open" if result == 0 else "closed",
            "error": None,
        })
    except (OSError, socket.timeout) as exc:
        result_queue.put({"port": port, "status": "error", "error": str(exc)})
    finally:
        sock.close()
