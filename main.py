import json
import os
import queue
import threading
from datetime import datetime

from scanner import ping_host, scan_single_port

PORT_SECURITY_DB = {
    21: {
        "service": "FTP",
        "risk": "HIGH",
        "detail": "Unencrypted File Transfer - Risk of Credential Theft",
    },
    22: {
        "service": "SSH",
        "risk": "LOW",
        "detail": "Encrypted Administrative Remote Shell",
    },
    53: {
        "service": "DNS",
        "risk": "MEDIUM",
        "detail": "Core Resolution Pipeline - Verify Recursion Settings",
    },
    80: {
        "service": "HTTP",
        "risk": "HIGH",
        "detail": "Cleartext Web Traffic - Recommend Enforcing HTTPS (443)",
    },
    443: {
        "service": "HTTPS",
        "risk": "LOW",
        "detail": "Encrypted Secure Web Service",
    },
    3389: {
        "service": "RDP",
        "risk": "CRITICAL",
        "detail": "Exposed Remote Desktop Endpoint - Target for Brute-force",
    },
}


def run_audit(target):
    print("\n" + "=" * 65)
    print(" NETVANGUARD - MARITIME & ENTERPRISE AUDIT SUITE ")
    print("=" * 65)
    print(f"Target Host : {target}")
    print(f"Scan Time   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print("[*] Initiating Host Diagnostic...")
    if not ping_host(target):
        print("[-] Target Offline / Unreachable.")
        print("[*] Performing Auto-Triage: Check Local Gateway & ISP/VSAT.\n")
        return
    print("[+] Host Status: ONLINE!\n")

    print("[*] Concurrently Auditing Critical Ports via Multi-Threading...")

    result_queue = queue.Queue()
    threads = []

    for port in PORT_SECURITY_DB.keys():
        t = threading.Thread(
            target=scan_single_port, args=(target, port, result_queue)
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    open_ports = []
    while not result_queue.empty():
        open_ports.append(result_queue.get())

    audit_summary = []
    for port, meta in PORT_SECURITY_DB.items():
        is_open = port in open_ports
        status = "OPEN [ACTIVE]" if is_open else "CLOSED"
        risk_tag = f"[{meta['risk']} RISK]" if is_open else "[SECURE]"
        line = f" - Port {port:<5} ({meta['service']:<5}) : {status:<15} {risk_tag} | {meta['detail']}"
        print(line)
        audit_summary.append(
            {
                "port": port,
                "service": meta["service"],
                "status": status,
                "risk": meta["risk"] if is_open else "NONE",
            }
        )

    # Shift-Handover JSON Export
    os.makedirs("reports", exist_ok=True)
    report_data = {
        "target": target,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "audit_results": audit_summary,
    }
    with open("reports/audit_log.json", "a") as f:
        f.write(json.dumps(report_data, indent=2) + "\n")

    print("\n[+] Audit Complete! Log appended to reports/audit_log.json")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    target_ip = input("Enter Target IP or Domain: ")
    run_audit(target_ip)
  
