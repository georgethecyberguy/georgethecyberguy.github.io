---
group: lab
title: Detection Lab
order: 1
year: 2025
kind: Lab
status: Ongoing
role: Lead / sole contributor
stack:
  - Wireshark
  - Suricata
  - Zeek
  - Splunk
  - Elastic
repo: https://github.com/georgethecyberguy/Detection-Lab
summary: A self-built detection environment for practicing SIEM implementation, log analysis, and network-based attack detection.
---

The Detection Lab is the foundation project for everything else on the blue-team side. It pairs a small attacker network with a defender network running Suricata and Zeek for traffic analysis, with logs forwarded into a SIEM (Splunk for one branch of the lab, Elastic for another) so I can compare alert fidelity and tuning between platforms.

## What's inside

- A simple two-network topology that mirrors a small enterprise edge.
- Suricata and Zeek deployed inline on the egress segment.
- Splunk and Elastic instances ingesting parallel feeds for direct comparison.
- Detection content built around common adversary techniques — credential dumping, lateral movement, basic C2 beacons.

## Why it exists

Reading detection theory is useful. Watching the same packet capture light up two different SIEMs differently is *educational.* The lab gave me a place to actually see what tuning means in practice — and to break my own detections on purpose.

See the [GitHub repository]({{ page.repo }}) for the configs and setup notes.
