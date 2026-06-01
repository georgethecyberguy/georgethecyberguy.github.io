---
group: lab
title: "picoCTF — Wave a flag"
order: 100
year: 2026
kind: CTF
status: Solved
role: Author
stack:
  - Linux
  - Bash
summary: A General Skills warmup on Linux file permissions, command-line flags, and the basic "download, chmod, run" loop every CTF player needs in muscle memory.
event: picoCTF 2026
category: General Skills
points: 100
---

> **Spoiler note:** This is a full walkthrough. If you want to attempt the challenge first, head to [picoCTF](https://picoctf.org) and come back.

A short General Skills challenge that introduces three fundamentals at once: pulling files down from the web, dealing with Linux permissions, and learning to read a program's own help text. The whole thing is solvable in under a minute once the pattern clicks — which is precisely the point.

## The challenge

You're given a file named `warm` and a prompt that essentially says: *run this and find the flag.* A Linux environment is required — the picoCTF/CyLab in-browser terminal works fine, but a local Linux box or WSL is just as good.

## Walkthrough

### Step 1 — Pull the file down

In the picoCTF UI, right-click the linked file and copy the link address. Then in the terminal:

```bash
wget <paste-link-here>
```

`wget` is the canonical command-line file fetcher on Linux. The file lands in your current working directory.

### Step 2 — Try to run it

The reflexive first move is to just execute it:

```bash
./warm
```

This will fail with a `Permission denied` error. That's expected — Linux doesn't grant execute permission to downloaded files by default. It's a sensible defense against accidentally running arbitrary downloads.

### Step 3 — Set executable permission

Use `chmod` ("change mode") to give yourself permission to run the file:

```bash
chmod +x warm
```

A quick note on the common alternative: many walkthroughs reach for `chmod 777`, which grants read, write, and execute permissions to the owner, the group, *and* everyone else. It works, but it's overkill for the task at hand — you only need execute permission for yourself, which is what `+x` does. In real-world sysadmin or security work, `chmod 777` is a code smell at best and an exploitable mistake at worst. Worth building the better habit now.

If you want to read more about `chmod`, the [GeeksforGeeks `chmod` reference](https://www.geeksforgeeks.org/linux-unix/chmod-command-linux/) is a decent starting point.

### Step 4 — Run again, then read the help

```bash
./warm
```

This time it executes, and the program prints a hint pointing you toward a help flag. Re-run with `-h`:

```bash
./warm -h
```

The flag prints to the terminal, in the standard `picoCTF{...}` format.

## What this challenge teaches

Three habits worth internalizing from this one:

1. **Always check the help.** Most CLI tools — and most CTF binaries — expose useful information through `-h`, `--help`, `-?`, or by running with no arguments. It's the first thing to try, not the last.
2. **`chmod +x` over `chmod 777`.** Grant the least privilege required. The defensive instinct should be automatic, even on a CTF binary.
3. **`wget`, `chmod`, `./binary` is a pattern, not three commands.** You'll repeat it dozens of times across General Skills and Reverse Engineering challenges. Build the muscle memory now and stop thinking about it later.

A trivial flag in isolation, but the habits it builds compound across every challenge that follows.
