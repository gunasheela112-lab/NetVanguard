import argparse
import json
import os
import queue
import threading
import time
from datetime import datetime, timezone

from config import PORT_SECURITY_DB
from scanner import ping_host_diagnostic, resolve_host, scan_single_port


def run_audit(target: str, timeout: float = 1.0, output: str = "reports/audit_log.jsonl") -> int:
    """Run a network audit and return a process-friendly exit code."""
    started_at = datetime.now(timezone.utc)
    start_time = time.perf_counter()
    print("\n" + "=" * 65)
    print(" NETVANGUARD - MARITIME & ENTERPRISE AUDIT SUITE ")
    print("=" * 65)
    print(f"Target Host : {target}")
    print(f"Scan Time   : {started_at.astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')}\n")

    resolved_ip = resolve_host(target)
    if not resolved_ip:
        print("[-] Unable to resolve target host.")
        return 2

    print(f"[*] Resolved Target: {resolved_ip}")
    print("[*] Initiating Host Diagnostic...")
    ping_result = ping_host_diagnostic(target, timeout)
    if not ping_result["reachable"]:
        print("[-] Target Offline / Unreachable.")
        if ping_result["error"]:
            print(f"    Reason: {ping_result['error']}")
        print("[*] Performing Auto-Triage: Check Local Gateway & ISP/VSAT.\n")
        return 1

    print(f"[+] Host Status: ONLINE! ({ping_result['latency_ms']} ms)\n")
    print("[*] Concurrently Auditing Critical TCP Ports via Multi-Threading...")

    result_queue = queue.Queue()
    threads = []
    for port in PORT_SECURITY_DB:
        thread = threading.Thread(
            target=scan_single_port,
            args=(resolved_ip, port, result_queue, timeout),
            daemon=True,
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    results_by_port = {}
    while not result_queue.empty():
        result = result_queue.get()
        results_by_port[result["port"]] = result

    audit_summary = []
    open_count = 0
    for port, meta in PORT_SECURITY_DB.items():
        result = results_by_port.get(port, {"status": "error", "error": "No scanner result"})
        is_open = result["status"] == "open"
        if is_open:
            open_count += 1
        status = "OPEN [ACTIVE]" if is_open else result["status"].upper()
        risk_tag = f"[{meta['risk']} RISK]" if is_open else "[SECURE]"
        print(
            f" - Port {port:<5} ({meta['service']:<5}) : "
            f"{status:<15} {risk_tag} | {meta['detail']}"
        )
        audit_summary.append({
            "port": port,
            "service": meta["service"],
            "status": result["status"],
            "risk": meta["risk"] if is_open else "NONE",
            "error": result["error"],
        })

    duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
    report_data = {
        "target": target,
        "resolved_ip": resolved_ip,
        "timestamp": started_at.isoformat(),
        "duration_ms": duration_ms,
        "summary": {"ports_scanned": len(PORT_SECURITY_DB), "open_ports": open_count},
        "host": {"status": "online", "latency_ms": ping_result["latency_ms"]},
        "audit_results": audit_summary,
    }

    os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
    with open(output, "a", encoding="utf-8") as report_file:
        report_file.write(json.dumps(report_data) + "\n")

    print(f"\n[+] Audit Complete! {open_count} open port(s) found in {duration_ms} ms.")
    print(f"[+] Log appended to {output}")
    print("=" * 65 + "\n")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="NetVanguard - Network Diagnostic & Security Audit Tool"
    )
    parser.add_argument("-t", "--target", help="Target IP address or domain to audit")
    parser.add_argument("--timeout", type=float, default=1.0, help="TCP scan timeout in seconds (default: 1.0)")
    parser.add_argument("-o", "--output", default="reports/audit_log.jsonl", help="JSON Lines report path")
    return parser


if __name__ == "__main__":
    args = build_parser().parse_args()
    target = args.target or input("Enter Target IP or Domain: ").strip()

    if not target:
        print("[-] No target provided. Please enter a valid IP or domain.")
        raise SystemExit(2)

    if args.timeout <= 0:
        print("[-] Timeout must be greater than zero.")
        raise SystemExit(2)

    raise SystemExit(run_audit(target, args.timeout, args.output))
