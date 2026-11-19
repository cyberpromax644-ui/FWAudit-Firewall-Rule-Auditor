# FWAudit - Firewall Ruleo Auditor

## Student
Maisa Aslam

## Project Description
FWAudit is a Python-based firewall rule auditing
tool that identifies common firewall configuration
weaknesses.

## Features
1. Any-to-Any Allow Detection
2. Management Port Exposure Detection
3. Shadowed Rule Detection
4. Deny Rule Logging Gap Detection
5. Automatic Audit Report Generation

## Technologies
- Kali Linux
- Python 3
- CSV
- argparse
- ipaddress

## How to Run

python3 main.py -i test_data/firewall_rules.csv -o audit_report.txt

## Output
The tool displays security findings and saves
them in audit_report.txt.

## Testing
All tests use fictional firewall rules in an
isolated lab environment.
