# NetVanguard: Automated Network Diagnostic & Security Audit Tool

NetVanguard is a high-performance, multi-threaded CLI network diagnostic and security auditing engine written in Python. Designed for enterprise networks and mission-critical maritime IT infrastructure, it automates host connectivity monitoring, performs transport layer security audits, and generates persistent operational incident logs.

---

## Core Capabilities

* **Automated ICMP Health Diagnostics:** Executes non-blocking reachability tests with real-time latency and packet loss verification.
* **Concurrent Transport Layer Auditing:** Utilizes multi-threading to scan mission-critical ports in parallel with zero sequential lag.
* **Security Risk Categorization:** Evaluates exposed attack surfaces and flags risks (Cleartext FTP/HTTP, exposed RDP endpoints).
* **Shift-Handover JSON Logging:** Automatically documents audit timestamps, host availability, and port exposures to persistent log files (`reports/audit_log.json`).

---

## Critical Monitored Services

| Port Number | Protocol | Service Description | Security Audit Focus |
| :--- | :--- | :--- | :--- |
| **21** | TCP | FTP | Cleartext File Transfer Audit |
| **22** | TCP | SSH | Remote Administration Access |
| **53** | UDP/TCP | DNS | Name Resolution Pipeline Health |
| **80** | TCP | HTTP | Unencrypted Web Traffic Detection |
| **443** | TCP | HTTPS | Encrypted Web Service Verification |
| **3389** | TCP | RDP | Remote Desktop Exposure Check |

---

## Architecture & Logic Flow

---

## Installation

```bash
git clone https://github.com/gunasheela112-lab/NetVanguard.git
cd NetVanguard
python main.py
No external dependencies — built entirely with Python's standard library.
Usage
Run the script and enter a target IP or hostname when prompted:
Enter Target IP or Domain: 192.168.1.1
The tool pings the host, scans critical ports concurrently, and prints a risk-tagged audit report to the console. Results are also appended to reports/audit_log.json.
Sample Output
=================================================================
 NETVANGUARD - MARITIME & ENTERPRISE AUDIT SUITE
=================================================================
Target Host : 192.168.1.1
Scan Time   : 2026-09-04 14:22:10

[*] Initiating Host Diagnostic...
[+] Host Status: ONLINE!

[*] Concurrently Auditing Critical Ports via Multi-Threading...
 - Port 21    (FTP)   : CLOSED          [SECURE] | Unencrypted File Transfer - Risk of Credential Theft
 - Port 22    (SSH)   : OPEN [ACTIVE]   [LOW RISK] | Encrypted Administrative Remote Shell
 - Port 80    (HTTP)  : OPEN [ACTIVE]   [HIGH RISK] | Cleartext Web Traffic - Recommend Enforcing HTTPS (443)

[+] Audit Complete! Log appended to reports/audit_log.json
=================================================================
