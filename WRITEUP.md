# FWAudit Demo and Write-up

**Name:** Maisa Aslam | **Track:** Network Defense | **Instructor:** Abdul Mannan | **Program:** Cyber Security, PNY Trainings

## 1. What I built

FWAudit is a Python command-line tool that reads a firewall rule export in CSV format and finds risky configuration before it causes harm. It checks for allow-everything rules, management ports open to the internet, rules that can never take effect, and deny rules with no logging. It saves a report with the rule number, severity, issue and evidence for every finding.

## 2. Demo

All tests were run on my own fictional lab files in `test_data/`. No real firewall, network or third-party system was scanned.

```bash
python3 main.py -i test_data/firewall_rules.csv -o audit_report.txt
```

Result on the sample export: 5 rules analysed, 4 findings (2 HIGH, 1 MEDIUM, 1 LOW).

## 3. Planted flaws checklist

The sample export `test_data/firewall_rules.csv` contains these planted flaws:

| # | Planted flaw | Rule | Expected | Found |
|---|---|---|---|---|
| 1 | RDP (3389) open to any source | 2 | HIGH | Yes |
| 2 | Deny rule with logging disabled | 3 | LOW | Yes |
| 3 | Allow rule shadowed by an earlier deny rule | 4 | MEDIUM | Yes |
| 4 | Any-to-any allow rule | 5 | HIGH | Yes |

A clean rule was not flagged: rule 1 (SSH allowed only from the internal network `192.168.1.0/24`). This shows the checks do not raise false alarms on safe configuration.

## 4. One finding explained

**Finding:** `[MEDIUM] Rule 4: Potential Shadowed Rule. Earlier rule 3 covers this rule's traffic`

```
3,10.0.0.0/8,192.168.2.30,80,tcp,deny,disabled
4,10.0.0.0/8,192.168.2.30,80,tcp,allow,enabled
```

**What was wrong:** Rule 3 denies web traffic (port 80) from `10.0.0.0/8` to `192.168.2.30`. Rule 4, below it, tries to allow exactly the same traffic. A firewall stops at the first matching rule, so rule 4 can never be reached.

**Why it is dangerous:** The administrator who wrote rule 4 believes that traffic is allowed, but it is blocked. The usual "fix" is to add a broader allow rule later, which makes the rule set wider and harder to review. The opposite case is worse: a deny rule hidden behind an earlier allow rule means traffic the administrator thinks is blocked is actually permitted.

**The fix:** Review the order. Put specific rules above general ones, decide which of the two rules is really intended, and delete the one that is dead.

## 5. Testing I did

| Test | Input | Result |
|---|---|---|
| 1 | Any-to-any allow rule | HIGH finding, as expected |
| 2 | SSH and RDP open to `any` | Two HIGH findings, as expected |
| 3 | SSH and RDP from internal networks only | No findings, as expected |
| 4 | Deny rule followed by allow for the same traffic | MEDIUM finding, as expected |
| 5 | Deny rule with logging disabled | LOW finding, as expected |
| 6 | Only safe rules | "No security findings detected", as expected |

I also confirmed that the report printed on screen matches the saved `audit_report.txt`.

## 6. Problems I ran into and fixed

While preparing the test CSV in a text editor, a stray letter was typed at the end of the file (a keyboard shortcut was typed as a plain letter) and an extra `xx` appeared at the start of the header. A header like `xxrule_id` would stop the tool from finding the `rule_id` column. I caught both by looking at the file before running the tool, removed them, and confirmed the file with `cat` before every run.

**Lesson:** Always inspect input data before trusting the output. A wrong input file gives wrong results even when the code is correct.

## 7. Limitations (honest reporting)

- It reads a simple CSV format only, not vendor-specific exports.
- Shadowed-rule detection is simplified: it compares one earlier rule with one later rule.
- Management port checks cover SSH (22) and RDP (3389).
- Severity levels are guidance labels, not proof of vulnerability.
- It is a learning prototype, not a replacement for a professional firewall review.

## 8. Defensive lesson

See [DEFENSIVE_LESSON.md](DEFENSIVE_LESSON.md): rule order and least exposure, why they matter and how to enforce them.o
