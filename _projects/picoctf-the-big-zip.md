---
title: "picoCTF — The Big Zip"
order: 112
year: 2026
kind: CTF
status: Solved
role: Author
stack:
  - Linux
  - grep
  - unzip

summary: A General Skills challenge on searching at scale — when a zip explodes into thousands of files, you don't look through them, you let grep sweep the whole tree at once.

event: picoCTF 2026
category: General Skills
points: 100

group: lab
---

> **Spoiler note:** This is a full walkthrough. If you want to attempt the challenge first, head to [picoCTF](https://picoctf.org) and come back.

A short challenge that teaches one of the most useful commands you'll run as an analyst: **recursive grep**. You're handed a zip file that unpacks into a sprawling directory tree of files, with the flag buried somewhere inside one of them. Opening files one at a time is hopeless. The move is to search the entire tree in a single command.

This is the same instinct as the [strings it](/projects/picoctf-strings-it/) challenge — *let the tool do the searching* — scaled up from one binary to a whole directory structure.

## The challenge

You're given a file named `the-big-zip`. Unzipping it produces a large number of files and folders. The flag is in one of them. The challenge is finding it without manually inspecting thousands of files.

## Walkthrough

### Step 1 — Download the file

```bash
wget <link-to-the-big-zip>
```

### Step 2 — Unzip it

```bash
unzip the-big-zip.zip
```

Watch a torrent of filenames scroll by as it extracts. This is the point of the challenge — far too many files to check by hand. It unpacks into a directory (something like `the-big-unzip/`).

### Step 3 — Search the whole tree with recursive grep

Instead of opening files, search all of them at once:

```bash
grep -r "picoCTF" the-big-unzip/
```

The `-r` flag is the key. It stands for **recursive** — it tells `grep` to descend into the directory and search *every file in every subfolder* beneath it, rather than searching a single file. One command sweeps the entire tree.

`grep` prints every line matching `picoCTF`, prefixed with the path of the file it found it in. Since the flag follows the `picoCTF{...}` format, searching for `picoCTF` surfaces it directly — along with the exact file it was hiding in.

The flag appears in the output in standard format. Done.

## Understanding `grep -r`

It's worth being precise about what `-r` does, because recursive search is a daily tool in real work:

- **Plain `grep "pattern" file.txt`** searches a single named file.
- **`grep -r "pattern" directory/`** searches *every file under that directory*, recursing into all subdirectories automatically. You don't have to name the files — you point it at the top of the tree and it handles the rest.

A few related flags worth knowing, because they turn `grep -r` from a blunt instrument into a precise one:

- **`grep -r -l "pattern" dir/`** — `-l` lists only the *filenames* that contain a match, not the matching lines. Useful when you want to know *which* file, not *what* matched.
- **`grep -r -i "pattern" dir/`** — `-i` makes the search case-insensitive.
- **`grep -r -n "pattern" dir/`** — `-n` includes the line number of each match.
- **`grep -r -E "regex" dir/`** — `-E` enables extended regular expressions for richer pattern matching.

For this challenge, plain `-r` with the literal string `picoCTF` is enough. But the same command with a regex is how you'd hunt for IP addresses, email patterns, API keys, or any other signature across a large codebase or evidence set.

## Where this matters beyond the challenge

Recursive search across a directory tree is constant in security work:

- **Log analysis.** Searching a directory of log files for an IOC — an attacker IP, a suspicious user agent, a known-bad domain — is `grep -r` against a log directory. It's often the first move in an investigation.
- **Source code review.** Hunting for hardcoded secrets, dangerous function calls, or a specific string across an entire codebase is recursive grep (and tools like `ripgrep` are faster, grep-compatible versions built exactly for this).
- **Incident response triage.** When handed a directory of collected evidence, sweeping it for known indicators before doing anything else is standard practice.
- **Configuration auditing.** Finding every config file that contains a particular insecure setting across a sprawling system is, again, recursive grep.

The challenge is trivial. The command is one you'll type thousands of times.

## What this challenge teaches

- **`grep -r` searches a whole directory tree.** Point it at the top, and it recurses into everything below. No need to name files.
- **Search at scale instead of looking by hand.** The moment there are too many files to eyeball, that's the cue to let the tool sweep them.
- **Know grep's useful flags.** `-l` for filenames, `-i` for case-insensitive, `-n` for line numbers, `-E` for regex. Small additions, big precision gains.
- **This is real-world tradecraft.** Log hunting, code review, IR triage, config audits — recursive grep underlies all of them.

A thirty-second solve that hands you a command you'll use for the rest of your career.
