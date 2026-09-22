# NetVanguard: Automated Network Diagnostic & Security Audit Tool

![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-CLI-lightgrey)

NetVanguard is a lightweight, multi-threaded CLI network diagnostic and security auditing tool written in Python. It checks host reachability, measures ICMP response latency, audits selected TCP ports concurrently, classifies exposed services by risk, and writes structured JSON Lines audit records.

## Core Capabilities

- **Host Health Diagnostics:** Performs a single ICMP echo test and records response latency.
- **Concurrent TCP Auditing:** Scans configured TCP ports in parallel with per-port timeouts.
- **Clear Port Statuses:** Reports ports as `open`, `closed`, `filtered`, or `error`.
- **Security Risk Categorization:** Flags exposed services such as FTP, HTTP, and RDP according to the local risk database.
- **Structured Logging:** Appends one valid JSON object per line to the configured report.
- **Scan Summary:** Records the number of ports scanned, open ports, and total scan duration.
- **Automation-Friendly CLI:** Supports command-line targets, configurable timeouts, custom report paths, and meaningful exit codes.

> **Scope:** NetVanguard performs basic TCP connectivity checks. It is not a vulnerability scanner or a substitute for a full security assessment. Only scan systems you own or are authorized to test.

## Monitored TCP Services

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
2. Send one ICMP echo request and record reachability and latency.
3. If reachable, scan the configured TCP ports concurrently.
4. Classify open services using `config.py`.
5. Print a human-readable audit summary.
6. Append a JSON Lines record containing the scan results and summary.

## Installation

Clone the repository and move into the project directory:

`git clone https://github.com/gunasheela112-lab/NetVanguard.git`

`cd NetVanguard`

No external Python packages are required because NetVanguard uses Python's standard library.

## Usage

### Interactive Mode

Run:

`python main.py`

The program will ask for the target IP address or domain.

### Command-Line Mode

Run NetVanguard by providing the target directly:

`python main.py --target 192.168.1.1`

You can also specify a custom TCP timeout:

`python main.py --target example.com --timeout 2`

To save the report to a custom location:

`python main.py --target 192.168.1.1 --output reports/nightly.jsonl`

The default report is saved to `reports/audit_log.jsonl`.

Each scan is stored as one JSON object per line, making the report easy to append to and process later.

## Exit Codes

| Code | Meaning |
| :--- | :--- |
| **0** | Audit completed successfully |
| **1** | Target could be resolved but was unreachable |
| **2** | Invalid input or target resolution failure |

## Testing

Run the complete test suite with:

`python -m unittest -v`

The tests cover host reachability, hostname resolution, TCP port states, timeout handling, socket errors, and report generation.

GitHub Actions also runs the test suite automatically when changes are pushed or pull requests are created.

## Project Structure

`NetVanguard/`

`├── .github/`

`│   └── workflows/`

`│       └── tests.yml`

`├── config.py`

`├── main.py`

`├── scanner.py`

`├── test_scanner.py`

`├── requirements.txt`

`├── LICENSE`

`└── README.md`

## License

MIT
