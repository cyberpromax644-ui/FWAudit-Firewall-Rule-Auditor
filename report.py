from datetime import datetime

def generate_report(findings, total_rules, output_file):

    lines = [
        "===================================",
        "       FWAudit AUDIT REPORT",
        "===================================",
        f"Date: {datetime.now()}",
        f"Total Rules: {total_rules}",
        f"Total Findings: {len(findings)}",
        "-----------------------------------"
    ]

    if not findings:
        lines.append("No security findings detected.")

    for item in findings:
        lines.extend([
            f"Rule Number: {item['rule']}",
            f"Severity: {item['severity']}",
            f"Issue: {item['issue']}",
            f"Evidence: {item['evidence']}",
            "-----------------------------------"
        ])

    report = "\n".join(lines)

    print(report)

    with open(output_file, "w") as file:
        file.write(report)

    print(f"\nReport saved to: {output_file}")
