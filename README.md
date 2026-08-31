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

