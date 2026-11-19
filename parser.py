import csv

REQUIRED_FIELDS = {
    "rule_id", "source", "destination",
    "port", "protocol", "action", "logging"
}

def parse_rules(filename):
    rules = []

    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)

        if not REQUIRED_FIELDS.issubset(reader.fieldnames or []):
            raise ValueError("Invalid CSV columns")

        for row in reader:
            rule = {
                key: value.strip().lower()
                for key, value in row.items()
            }

            if rule["action"] not in ("allow", "deny"):
                raise ValueError("Invalid action")

            rules.append(rule)

    return rules
