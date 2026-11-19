import argparse
from parser import parse_rules
from checks import audit_rules
from report import generate_report


def main():

    parser = argparse.ArgumentParser(
        description="FWAudit Firewall Rule Auditor"
    )

    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Firewall CSV file"
    )

    parser.add_argument(
        "-o", "--output",
        default="audit_report.txt",
        help="Output report file"
    )

    args = parser.parse_args()

    try:
        rules = parse_rules(args.input)

        findings = audit_rules(rules)

        generate_report(
            findings,
            len(rules),
            args.output
        )

    except (OSError, ValueError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()

