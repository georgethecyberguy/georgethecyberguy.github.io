---
group: lab
title: "picoCTF — strings it"
order: 103
year: 2026
kind: CTF
status: Solved
role: Author
stack:
  - Linux
  - strings
  - grep
summary: A General Skills challenge introducing the most fundamental static analysis move there is — extracting human-readable strings from a binary without ever executing it.
event: picoCTF 2026
category: General Skills
points: 100
---

> **Spoiler note:** This is a full walkthrough. If you want to attempt the challenge first, head to [picoCTF](https://picoctf.org) and come back.

A short, deceptively important challenge. The technique it teaches — running `strings` against a binary and grepping the output — is the *first* thing every malware analyst, reverse engineer, and forensic investigator does when they're handed an unfamiliar file. It's a beginner challenge in vocabulary; it's a daily-driver technique in practice.

## The challenge

You're given a single executable file called `strings` (yes, the same name as the tool you'll use to solve it — that's the joke). The prompt asks you to find the flag *without running the binary*.

That constraint is the entire lesson. In real incident response and malware analysis, you rarely want to execute an unknown binary blind. You inspect it statically first.

## Walkthrough

### Step 1 — Pull the file down

In the picoCTF / CyLab terminal:

```bash
wget <paste-link-here>
```

The file lands in your working directory.

### Step 2 — Run `strings` against it

`strings` is a standard Linux utility (part of the `binutils` package) that scans a binary file and prints every sequence of printable characters longer than a configurable minimum length. It doesn't execute the file — it just reads bytes and filters for anything that looks like text.

The naive first attempt:

```bash
strings strings
```

This works, but the output is enormous — thousands of lines of compiler metadata, function names, library references, and embedded text. Scrolling for a flag by eye is impractical.

### Step 3 — Pipe through `grep`

The flag follows a known format: `picoCTF{...}`. That's exactly what `grep` is for — filtering a stream of text for matching lines:

```bash
strings strings | grep picoCTF
```

The pipe (`|`) sends the output of `strings` directly into `grep`, which prints only the lines containing the literal string `picoCTF`. The flag appears on a single line, in standard format. Done.

### A note on the `-d` flag

I ran the actual command with `-d`:

```bash
strings -d strings | grep picoCTF
```

The `-d` flag tells `strings` to scan **only the initialized data sections** of the binary, rather than the entire file. For most beginner CTF challenges this doesn't change the outcome — both the headers and the data section typically contain printable text — but it's a meaningful distinction in real analysis work.

Without `-d`, `strings` reads every section of the binary, including padding, debug info, and unused regions. Output is noisier. With `-d`, you focus on the parts of the file that actually contain initialized data (hardcoded strings, error messages, embedded keys), which is usually where interesting findings live.

For this challenge, the result was the same with or without it. The habit of *thinking about which sections you're scanning* is what `-d` builds.

## Why this technique generalizes

`strings` + `grep` is the entry-level move in a much larger workflow. It's also what most real investigations begin with:

- **Malware triage.** An analyst handed an unknown sample runs `strings` against it before opening anything heavier. URLs, IP addresses, registry keys, mutex names, command-and-control beacons, and hardcoded credentials all routinely appear in the output. A 10-second `strings` pass often tells you 60% of what the malware does.
- **Forensic analysis.** Recovering text from binary blobs — memory dumps, swap files, deleted file fragments, embedded objects in document files — frequently starts with `strings`. Tools like `bulk_extractor` and `foremost` do more sophisticated versions of the same idea.
- **Reverse engineering.** Before opening a binary in Ghidra or IDA, running `strings` builds a quick map of what to expect: library calls, error messages, copyright notices. Function names embedded in symbol tables often reveal architecture before you've decompiled anything.
- **Threat hunting.** Searching files at scale for IOCs is essentially `strings` plus pattern matching, just industrialized. YARA rules — the standard for malware identification — fundamentally build on the same primitive: *what printable byte sequences exist in this file?*

The technique works because binaries are not pure machine code. They're machine code *embedded with strings* — error messages, configuration values, paths, prompts, format specifiers. As long as those strings exist, they're recoverable without executing anything.

## What this challenge teaches

- **Static analysis comes before dynamic analysis.** Look at the file before you run it. The reflex matters more than the specific tool.
- **The Unix pipeline is the analyst's microscope.** `strings | grep` is the simplest case of a pattern that scales arbitrarily — `strings | grep | sort | uniq` for deduplication, `strings | grep -E "<regex>"` for richer matching, `strings | grep | wc -l` for counting. Each layer is small; composition is what makes them powerful.
- **Flags help.** Tool flags aren't just shortcuts — they change *what* you're scanning and *how*. Reading the man page (`man strings`) on a beginner challenge pays off when you need a non-default option in a real investigation.
- **Curiosity about extra flags is a feature, not a bug.** Running `-d` "for the learning experience" is the right instinct. Build that habit on small challenges; reap it on hard ones.

A two-minute challenge. A foundational technique. Worth the writeup.
