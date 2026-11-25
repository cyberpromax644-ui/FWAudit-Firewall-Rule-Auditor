# FWAudit
## Firewall Rule Auditor

### Project Report & Technical Demonstration

---

**Project Track:** Network Defense
**Developed by:** Maisa Aslam
**Technology:** Python 3 | Tkinter | CSV | Kali Linux

---

## 1. Problem Statement

Firewalls are an important part of network security. They control incoming and outgoing network traffic through predefined rules.

However, incorrect firewall configurations can create security weaknesses. Examples include unrestricted access, exposed management services, incorrect rule ordering and disabled logging.

Manually reviewing a large set of firewall rules can be time-consuming. It can also make configuration mistakes difficult to identify.

**FWAudit addresses this problem by providing an automated way to review firewall rule exports and highlight potentially unsafe configurations.**

## 2. Project Aim

The aim of FWAudit is to develop a Python-based defensive security application that analyzes firewall rules, identifies common configuration risks and generates understandable audit results.

The application provides both a Command-Line Interface (CLI) and a Graphical User Interface (GUI).

## 3. Project Objectives

- Read firewall rules from CSV files.
- Validate the required input fields.
- Identify unrestricted allow rules.
- Detect unrestricted access to SSH and RDP management ports.
- Highlight potentially shadowed rules.
- Identify deny rules with disabled logging.
- Classify findings according to severity.
- Generate and save audit reports.
- Provide a graphical interface to review audit results.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3 | Implements the auditing logic |
| Kali Linux | Development and testing environment |
| CSV | Stores firewall rule input data |
| Tkinter | Builds the desktop GUI |
| Python CSV module | Reads structured CSV records |
| File Handling | Saves and reads audit reports |

### Why Python?

Python was selected because it provides built-in support for CSV processing, file handling and application development. Its readable syntax also makes the auditing logic easier to maintain.

### Why Tkinter?

Tkinter provides a way to build a desktop application using Python. It allows users to interact with FWAudit through buttons, tables, forms and dashboard elements instead of using only terminal commands.

## 5. Application Interfaces

FWAudit provides two ways to interact with the auditing system.

### 5.1 Command-Line Interface (CLI)

The CLI allows users to execute an audit through terminal commands.

**Purpose:**
- Run an audit using a specified CSV file.
- Display detected findings.
- Save results to a report file.

Example:

```bash
python3 main.py -i test_data/firewall_rules.csv -o audit_report.txt
```

**Command explanation:**

- `python3`: Runs the Python interpreter.
- `main.py`: Starts the main application.
- `-i`: Specifies the input file.
- `test_data/firewall_rules.csv`: Provides the firewall rule dataset.
- `-o`: Specifies the output report file.
- `audit_report.txt`: Name of the generated report.

### 5.2 Graphical User Interface (GUI)

The GUI provides a visual environment for using FWAudit.

Its main sections include:

**Dashboard**
- Displays audit statistics.
- Shows the number of rules and findings.
- Provides a summary of HIGH, MEDIUM and LOW findings.
- Displays recent audit information.

**New Audit**
- Allows the user to select a CSV file.
- Runs the firewall rule analysis.
- Displays the detected findings in a table.
- Provides report-saving functionality.

**Reports**
- Displays previously saved reports.
- Allows users to view report contents.
- Provides options to open the reports folder and delete saved reports.

**Purpose:** The GUI makes the application easier to operate and allows users to review audit information visually.

## 6. Firewall Security Checks

FWAudit performs four primary configuration checks.

### 6.1 Any-to-Any Allow Detection

This check identifies firewall rules that allow traffic from any source to any destination.

**Why is this check important?**

A firewall rule should normally allow only the traffic required for a specific purpose. An unrestricted allow rule may provide broader access than intended.

**Example configuration:**

```text
Source:      any
Destination: any
Action:      allow
```

**Potential risk:** Unnecessary network exposure.

**Severity:** HIGH

### 6.2 Management Port Exposure

This check identifies unrestricted access to commonly used management services.

FWAudit focuses on:

| Service | Port | Purpose |
|---|---:|---|
| SSH | 22 | Remote system administration |
| RDP | 3389 | Remote desktop access |

**Why is this check important?**

Management services provide administrative access. They should be restricted to authorized sources rather than being unnecessarily exposed.

**Potential risk:** Unauthorized access opportunities may increase when management services are unrestricted.

**Severity:** HIGH

### 6.3 Potentially Shadowed Rules

This check identifies a later firewall rule that may be affected by an earlier matching rule.

**Why is this check important?**

Some firewalls process rules in order. In a first-match configuration, an earlier matching rule can determine the traffic decision before a later rule is reached.

**Example:**

```text
Rule 3: Deny traffic from source A to destination B on port 80
Rule 4: Allow traffic from source A to destination B on port 80
```

Both rules describe the same traffic, but the earlier deny rule may prevent the later allow rule from taking effect.

**Potential risk:** Unexpected traffic decisions due to incorrect rule ordering.

**Severity:** MEDIUM

### 6.4 Disabled Deny Logging

This check identifies deny rules where logging is disabled.

**Why is this check important?**

Logging helps administrators review denied traffic and investigate unusual network activity.

When logging is disabled, useful information about denied connections may not be recorded.

**Potential risk:** Reduced monitoring and visibility.

**Severity:** LOW

## 7. Application Workflow

FWAudit follows these processing stages:

**Stage 1 — Input Selection**

The user provides a firewall rule CSV file.

**Stage 2 — CSV Parsing**

The parser reads the CSV records and extracts the firewall rule fields.

**Stage 3 — Input Validation**

The application checks whether the required columns are available and whether the input data is valid.

**Stage 4 — Security Analysis**

The auditing engine evaluates the firewall rules using the four implemented checks.

**Stage 5 — Risk Classification**

Detected issues are organized into HIGH, MEDIUM and LOW severity categories.

**Stage 6 — Result Display**

The findings are displayed through the CLI or GUI.

**Stage 7 — Report Generation**

The report component creates a text-based audit report that can be saved for later review.

## 8. Input File Structure

FWAudit accepts firewall rules in CSV format.

The required fields are:

```csv
rule_id,source,destination,port,protocol,action,logging
```

| Field | Explanation |
|---|---|
| `rule_id` | Identifies the firewall rule |
| `source` | Defines the traffic source |
| `destination` | Defines the traffic destination |
| `port` | Specifies the network port |
| `protocol` | Defines the protocol, such as TCP |
| `action` | Defines whether traffic is allowed or denied |
| `logging` | Indicates whether logging is enabled or disabled |

**Why CSV?**

CSV provides a simple structured format for storing and importing firewall rule information.

## 9. Practical Demonstration

The application was tested using fictional firewall rule files stored in the `test_data/` directory.

No real firewall or third-party network was scanned.

### CLI Execution

Command:

```bash
python3 main.py -i test_data/firewall_rules.csv -o audit_report.txt
```

### Sample Dataset Results

| Audit Information | Result |
|---|---:|
| Total Rules Analyzed | 5 |
| Total Findings | 4 |
| HIGH Findings | 2 |
| MEDIUM Findings | 1 |
| LOW Findings | 1 |

### Detected Configuration Issues

| Rule | Issue | Severity |
|---|---|---|
| Rule 2 | RDP open to any source | HIGH |
| Rule 3 | Deny rule with logging disabled | LOW |
| Rule 4 | Potentially shadowed allow rule | MEDIUM |
| Rule 5 | Any-to-any allow rule | HIGH |

Rule 1 was not flagged because SSH access was restricted to the internal network `192.168.1.0/24`.

## 10. Testing and Verification

Six controlled test scenarios were used to verify the auditing engine.

| Test | Scenario | Expected Result |
|---|---|---|
| T1 | Any-to-any allow | 1 HIGH finding |
| T2 | SSH and RDP open to any source | 2 HIGH findings |
| T3 | SSH and RDP restricted to internal networks | No findings |
| T4 | Earlier deny followed by matching allow | 1 MEDIUM finding |
| T5 | Deny rule with logging disabled | 1 LOW finding |
| T6 | Clean firewall rules | No findings |

**Testing Outcome:** All six scenarios produced their expected results during manual testing.

The terminal output was also compared with the generated report to verify that the displayed and saved results matched.

## 11. Challenges and Solutions

During development and testing, several practical issues were encountered.

### Challenge 1 — Incorrect CSV Header

An accidental extra character was added to the CSV header.

**Solution:** The input file was inspected and corrected before running the audit again.

### Challenge 2 — Input Data Accuracy

Incorrect or incomplete input data can affect the results of the auditing process.

**Solution:** The CSV structure and required fields were checked before testing.

### Challenge 3 — GUI Report Management

The GUI needed a way to display previously saved reports.

**Solution:** A Reports section was implemented to load report files, view their contents and manage saved reports.

## 12. Limitations

FWAudit is an educational firewall configuration auditing application.

Its current limitations are:

- Supports a defined CSV input format.
- Does not directly import every vendor-specific firewall format.
- Uses simplified comparisons for shadowed-rule detection.
- Management port checks focus on SSH and RDP.
- Severity levels are indicators for review, not proof of vulnerability.
- Results depend on the accuracy of the supplied data.
- Does not replace a complete professional firewall security assessment.

## 13. Defensive Recommendations

Based on the security checks implemented in FWAudit, the following practices are recommended:

1. Avoid unrestricted allow rules unless there is a justified requirement.
2. Restrict management ports to authorized sources.
3. Review firewall rule order to identify possible conflicts.
4. Enable logging on deny rules where appropriate.
5. Review firewall configurations regularly.
6. Follow the principle of least privilege.
7. Verify important configuration changes before applying them.

## 14. Responsible Use

FWAudit performs read-only analysis of supplied CSV files.

It does not connect to live firewall devices, modify firewall configurations, execute firewall rules or perform network attacks.

Its purpose is to support defensive learning and firewall configuration review.

## 15. Conclusion

FWAudit demonstrates how Python can be used to automate basic firewall configuration analysis.

The application combines CSV parsing, security checks, risk classification, report generation and a graphical interface in one project.

Through this project, practical experience was gained in Python programming, GUI development, input validation, defensive security concepts, testing and technical documentation.

**FWAudit — Review Firewall Rules. Identify Security Risks. Improve Network Defense.**

**Developed by Maisa Aslam**
