# FWAudit: Firewall Rule Auditor

- **Name:** Maisa Aslam
- **Instructor:** Abdul Mannan
- **Program:** Cyber Security, PNY Trainings
- **Platform:** Kali Linux, Python 3

FWAudit is a command-line tool that reads a firewall rule export (CSV), checks each rule for common configuration weaknesses, and saves a report with the rule number, severity, issue and evidence for every finding. It is read-only: it never changes a firewall or the input file.

> **Lab use only.** All tests use fictional firewall rules created for this project. No real firewall, network or third-party system was scanned.

## Why this tool

Firewall rule sets grow over time. Rules that are too broad, management ports open to the internet, rules that never take effect, and deny rules that leave no log are easy to miss when reading rules by hand. FWAudit checks them automatically and consistently.

## What it checks

| Check | What it finds | Severity |
|---|---|---|
| **Any-to-Any Allow** | An allow rule where both source and destination are unrestricted | HIGH |
| **Management Port Exposure** | SSH (22) or RDP (3389) allowed from an unrestricted source | HIGH |
| **Shadowed Rule** | A later rule that an earlier rule already covers, so it never takes effect (simplified logic) | MEDIUM |
| **Deny Logging Gap** | A deny rule with logging disabled, so blocked traffic leaves no record | LOW |

Severity is a guidance label to help a reviewer prioritise. It is not proof that a system is vulnerable.

## Project structure

```
FWAudit/
├── main.py              # command-line entry point
├── parser.py            # reads and validates the CSV
├── checks.py            # the four security checks
├── report.py            # builds and saves the text report
├── README.md
├── WRITEUP.md           # demo and write-up
├── DEFENSIVE_LESSON.md  # defensive lesson: rule order and least exposure
└── test_data/
    ├── firewall_rules.csv   # sample export
    └── tests/               # one small CSV per test case
```

## How to run

Requires Python 3. No packages need to be installed (standard library only: `csv`, `argparse`, `ipaddress`).

```bash
git clone https://github.com/cyberpromax644-ui/FWAudit-Firewall-Rule-Auditor.git
cd FWAudit-Firewall-Rule-Auditor
python3 main.py -i test_data/firewall_rules.csv -o audit_report.txt
```

| Option | Meaning |
|---|---|
| `-i` | Input CSV file with the firewall rules |
| `-o` | File where the report is saved |

## Input format

```
rule_id,source,destination,port,protocol,action,logging
1,192.168.1.0/24,192.168.2.10,22,tcp,allow,enabled
2,any,192.168.2.20,3389,tcp,allow,enabled
3,10.0.0.0/8,192.168.2.30,80,tcp,deny,disabled
4,10.0.0.0/8,192.168.2.30,80,tcp,allow,enabled
5,any,any,any,any,allow,disabled
```

`action` is `allow` or `deny`. `logging` is `enabled` or `disabled`. `source` and `destination` can be `any`, a single IP address or a CIDR range.

## Example output

```
FWAudit AUDIT REPORT
Total Rules: 5
Total Findings: 4

Rule Number: 2
Severity: HIGH
Issue: Management Port Exposure
Evidence: Port 3389 has unrestricted source

Rule Number: 3
Severity: LOW
Issue: Logging Disabled
Evidence: Deny rule has logging disabled

Rule Number: 4
Severity: MEDIUM
Issue: Potential Shadowed Rule
Evidence: Earlier rule 3 covers this rule's traffic

Rule Number: 5
Severity: HIGH
Issue: Any-to-Any Allow Rule
Evidence: Source and destination are unrestricted
```

In this sample, rule 3 (deny) comes before rule 4 (allow) for the same traffic, so rule 4 never takes effect. Rule order matters: a firewall uses the first matching rule.

## Testing

Each check was tested with a small CSV in `test_data/tests/`. The last test confirms the tool does not raise false alarms on safe rules. Full details are in [WRITEUP.md](WRITEUP.md).

| Test | Input | Expected | Result |
|---|---|---|---|
| 1 | Any-to-any allow rule | HIGH finding | Pass |
| 2 | SSH and RDP open to `any` | 2 HIGH findings | Pass |
| 3 | SSH and RDP from internal networks only | No findings | Pass |
| 4 | Deny rule followed by allow for the same traffic | MEDIUM finding | Pass |
| 5 | Deny rule with logging disabled | LOW finding | Pass |
| 6 | Safe rules only | "No security findings detected" | Pass |

## Limitations

- Reads a simple CSV format only. Vendor export formats are not supported.
- Shadowed-rule detection uses simplified logic: it compares one earlier rule with one later rule.
- Management port checks cover SSH (22) and RDP (3389).
- This is a learning prototype, not a replacement for a professional firewall review.

## Future improvements

- Support more firewall export formats
- Add unit tests and JSON output
- Cover more management ports and smarter shadowing analysis
- Summary dashboard for the report

## Defensive lesson

See [DEFENSIVE_LESSON.md](DEFENSIVE_LESSON.md): why rule order matters, how a shadowed deny rule silently leaves traffic allowed, and how to prevent it.
