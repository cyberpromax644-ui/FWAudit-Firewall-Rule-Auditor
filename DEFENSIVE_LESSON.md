# Defensive Lesson: Rule Order and Least Exposure

**Project:** FWAudit, Firewall Rule Auditor

## The lesson in one line

A firewall stops at the **first matching rule**, so the order of the rules is part of the security policy. A rule that looks correct can do nothing at all if an earlier rule already matches the same traffic.

## What happens in practice

```
3,10.0.0.0/8,192.168.2.30,80,tcp,deny,disabled
4,10.0.0.0/8,192.168.2.30,80,tcp,allow,enabled
```

Rule 4 is never reached, because rule 3 already matched. FWAudit reports this as a **shadowed rule**.

| Case | What the administrator thinks | What really happens | Risk |
|---|---|---|---|
| Allow hidden behind a deny | "This service is allowed" | The service is blocked | Outage, then a rushed, broader "fix" |
| **Deny hidden behind an allow** | "This traffic is blocked" | The traffic is allowed | **A security control that does not exist** |
| Same action, repeated | Nothing wrong | A harmless duplicate | Clutter that hides real problems |

The second case is the dangerous one. A "default deny" rule at the bottom of the list is useless if a rule above it already allows everything.

## Why it matters

- Rule sets grow over years. Many people add rules, and nobody re-reads the whole list.
- Broad rules (any-to-any, management ports open to the internet) cancel the more careful rules placed below them.
- A deny rule without logging leaves no evidence that anything was blocked, so mistakes stay hidden.

## How to prevent it

1. **Specific above general.** Put narrow rules first and broad rules last.
2. **End with a logged default deny.** Check that nothing above it allows all traffic.
3. **Least exposure.** Never allow SSH (22) or RDP (3389) from `any`. Restrict management access to an admin network or a VPN.
4. **Turn logging on for deny rules**, so blocked traffic leaves a record.
5. **Audit after every change.** Review the rule set with a tool such as FWAudit, and remove dead and duplicate rules.
6. **Document each rule:** who asked for it, why, and when it should be reviewed.

## How FWAudit helps

FWAudit reads the rules in order, the way a firewall does, and reports:

- allow rules with unrestricted source and destination (HIGH)
- SSH or RDP open to any source (HIGH)
- shadowed rules that an earlier rule already covers (MEDIUM)
- deny rules with logging disabled (LOW)

A tool repeats this check on the whole list every time, which a person reading rules by hand cannot do reliably. It is a prototype, so the output is a starting point for a human review, not a final verdict.

## Takeaway

Security is not only about which rules exist but about the **order they are in**. Reading a rule set top to bottom, as the firewall does, is the first step of any review.

