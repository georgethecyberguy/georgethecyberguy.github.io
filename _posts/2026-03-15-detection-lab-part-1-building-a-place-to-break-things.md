---
title: "Detection Lab, part 1: building a place to break things"
subtitle: How I structured the network, why I'm running Suricata and Zeek side by side, and what the SIEM split is for.
date: 2026-03-15 11:00:00 -0500
tags: [walkthrough, detection]
---

Before any of the detection content matters, you need a place to run it. This post walks through the topology and rationale behind the [Detection Lab](/projects/detection-lab/) — which sounds dull but is the single decision that ends up shaping every detection you write afterward.

## The topology, briefly

The lab sits on two virtual networks:

- An **attacker network** — a small Kali instance plus a couple of staging boxes I rotate through.
- A **defender network** — a few Windows endpoints, a domain controller, and a Linux jump host. Suricata and Zeek run inline on the egress between the two networks.

Logs flow out of the defender network into the SIEM via standard agents. There's nothing exotic here, and that's the point: I want the architecture to feel like a small enterprise edge, not a CTF challenge.

## Why Suricata *and* Zeek

The honest answer is "to compare them." Suricata fires on signatures and gives you fast, narrow alerts; Zeek records protocol-level metadata and gives you context. Running both gives you a chance to see — for the same packet capture — what each tool surfaces and what it misses.

In practice that means:

- A scripted attack sequence (e.g. a Mimikatz-style credential dump on a domain endpoint, then SMB lateral movement).
- A simultaneous Suricata alert review and Zeek log dive.
- Tuning each based on what was loud, what was quiet, and what was wrong.

## Splunk vs. Elastic

The SIEM split is the same exercise at a different layer. Both ingest the same feeds. I write the same detection logic in SPL and KQL/Lucene and watch how each platform handles the same events. The point isn't to pick a winner — both are excellent and you'll see both in the wild — it's to be fluent in both query languages.

## What's next

Part two is the detection-engineering side: writing actual content, tuning out the noise, and the awkward middle stage where every alert is either too loud or completely silent.

The repository for the lab is at [github.com/georgethecyberguy/Detection-Lab](https://github.com/georgethecyberguy/Detection-Lab) — the configs there are the ones I'm running.
