# NetVanguard: Automated Network Diagnostic & Security Audit Tool

![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-CLI-lightgrey)

NetVanguard is a lightweight, multi-threaded CLI network diagnostic and security auditing tool written in Python. It checks host reachability, measures ICMP response latency, audits selected TCP ports concurrently, classifies exposed services by risk, and writes structured JSON Lines audit records.

## Core Capabilities

- **Host Health Diagnostics:** Performs a single ICMP echo test and records response latency.
- **Concurrent TCP Auditing:** Scans configured TCP ports in parallel with per-port timeouts.
- **Security Risk Categorization:** Flags exposed services such as FTP, HTTP, and RDP according to the local risk database.
- **Structured Operational Logging:** Appends one valid JSON object per line to `reports/audit_log.jsonl`.
- **Automation-Friendly CLI:** Supports command-line targets, configurable timeouts, custom report paths, and meaningful exit codes.

> **Scope:** NetVanguard performs basic TCP connectivity checks. It is not a vulnerability scanner or a substitute for a full security assessment. Only scan systems you own or are authorized to test.

## Critical Monitored TCP Services

| Port | Protocol | Service | Security Audit Focus |
| :--- | :--- | :--- | :--- |
| **21** | TCP | FTP | Cleartext file transfer |
| **22** | TCP | SSH | Remote administration exposure |
| **53** | TCP | DNS | Resolution service exposure |
| **80** | TCP | HTTP | Unencrypted web traffic |
| **443** | TCP | HTTPS | Secure web service |
| **3389** | TCP | RDP | Remote desktop exposure |

## Architecture

1. Resolve the target hostname to IPv4.
2. Send one ICMP echo request and record reachability/latency.
3. If reachable, scan configured TCP ports concurrently.
4. Classify open services using `config.py`.
5. Print a human-readable audit summary.
6. Append a structured JSON Lines record to the configured output file.

## Installation

```bash
git clone https://github.com/gunasheela112-lab/NetVanguard.git
cd NetVanguard
python main.py --target 192.168.1.1
```

No external Python dependencies are required.

## Usage

Interactive mode:

```bash
python main.py
```

Command-line mode:

```bash
python main.py --target 192.168.1.1
python main.py --target example.com --timeout 2
python main.py --target 192.168.1.1 --output reports/nightly.jsonl
```

## Exit Codes

| Code | Meaning |
| :--- | :--- |
| **0** | Audit completed successfully |
| **1** | Target could be resolved but was unreachable |
| **2** | Invalid input or target resolution failure |

## Testing

Run:

```bash
python -m unittest -v
```

## Project Structure

```text
NetVanguard/
├── config.py
├── main.py
├── scanner.py
├── test_scanner.py
├── requirements.txt
├── LICENSE
└── README.md
```

## License

MIT
