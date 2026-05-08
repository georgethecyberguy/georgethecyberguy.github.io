---
title: SOC Automation Lab
order: 2
year: 2025
kind: Lab
status: In progress
role: Lead / sole contributor
stack:
  - Wazuh
  - TheHive
  - Shuffle SOAR
  - VirusTotal
repo: https://github.com/georgethecyberguy/Blue-Team
summary: An end-to-end automation lab — detect, alert, enrich, contain — built around Wazuh, TheHive, and Shuffle.
---

The SOC Automation Lab takes raw detection events and walks them all the way through an analyst workflow: enrichment, case creation, response playbook, and basic containment actions. It's the natural sequel to the Detection Lab — once you can detect things, the next problem is what to do with the alerts at scale.

## Pipeline

1. **Wazuh** detects a suspicious event on a monitored endpoint.
2. **Shuffle** picks up the alert via webhook and runs an enrichment workflow (IOC lookups, asset context).
3. A case is created automatically in **TheHive** with the enriched evidence attached.
4. A response playbook fires — for severity-tagged events — to take a containment action.
5. Analyst review closes the loop.

## Notes

The lab deliberately uses open-source tooling end-to-end so the entire detection-to-response chain is inspectable. It's also a useful sandbox for trying playbook patterns I wouldn't get to test in a production-shaped environment.

Writeup in progress. The repository is at [{{ page.repo | replace: "https://github.com/", "" }}]({{ page.repo }}).
