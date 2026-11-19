import ipaddress

MANAGEMENT_PORTS = {"22", "3389"}

def unrestricted(value):
    return value in ("any", "*", "0.0.0.0/0", "::/0")


def network_covers(earlier, later):
    if unrestricted(earlier):
        return True

    if unrestricted(later):
        return False

    try:
        first = ipaddress.ip_network(earlier, strict=False)
        second = ipaddress.ip_network(later, strict=False)

        return (
            first.version == second.version
            and second.subnet_of(first)
        )
    except ValueError:
        return earlier == later


def field_covers(earlier, later):
    return unrestricted(earlier) or earlier == later


def rule_covers(first, second):
    return (
        network_covers(first["source"], second["source"])
        and network_covers(
            first["destination"], second["destination"]
        )
        and field_covers(first["port"], second["port"])
        and field_covers(first["protocol"], second["protocol"])
    )


def audit_rules(rules):
    findings = []

    for index, rule in enumerate(rules):

        source = rule["source"]
        destination = rule["destination"]
        port = rule["port"]

        # Check 1: Any-to-any allow
        if (
            rule["action"] == "allow"
            and unrestricted(source)
            and unrestricted(destination)
        ):
            findings.append({
                "rule": rule["rule_id"],
                "severity": "HIGH",
                "issue": "Any-to-Any Allow Rule",
                "evidence": "Source and destination are unrestricted"
            })

        # Check 2: Management port exposure
        if (
            rule["action"] == "allow"
            and port in MANAGEMENT_PORTS
            and unrestricted(source)
        ):
            findings.append({
                "rule": rule["rule_id"],
                "severity": "HIGH",
                "issue": "Management Port Exposure",
                "evidence": f"Port {port} has unrestricted source"
            })

        # Check 3: Shadowed rule
        for earlier in rules[:index]:
            if rule_covers(earlier, rule):
                findings.append({
                    "rule": rule["rule_id"],
                    "severity": "MEDIUM",
                    "issue": "Potential Shadowed Rule",
                    "evidence": (
                        f"Earlier rule {earlier['rule_id']} "
                        "covers this rule's traffic"
                    )
                })
                break

        # Check 4: Deny rule logging
        if (
            rule["action"] == "deny"
            and rule["logging"] == "disabled"
        ):
            findings.append({
                "rule": rule["rule_id"],
                "severity": "LOW",
                "issue": "Logging Disabled",
                "evidence": "Deny rule has logging disabled"
            })

    return findings
