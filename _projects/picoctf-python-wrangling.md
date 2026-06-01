---
group: lab
title: "picoCTF — Python Wrangling"
order: 105
year: 2026
kind: CTF
status: Solved
role: Author
stack:
  - Python
  - Linux
summary: A General Skills challenge that's really about reading an unfamiliar script before running it, and understanding symmetric encryption from the user's side.
event: picoCTF 2026
category: General Skills
points: 100
---

> **Spoiler note:** This is a full walkthrough. If you want to attempt the challenge first, head to [picoCTF](https://picoctf.org) and come back.

The first Python challenge in the series, and a step up in substance from the earlier warmups. You're given three files and a script you've never seen, and the path to the flag runs through *understanding what the script does before you run it*. That habit — read first, execute second — is the same instinct the [strings it](/projects/picoctf-strings-it/) challenge built, applied here to source code instead of a binary.

## The challenge

You're given three files:

- `ende.py` — a Python script you'll need to read and understand.
- `flag.txt.en` — an encrypted file (the `.en` suffix is a hint).
- `pw.txt` (named `password.txt` in some variants) — a password.

The goal is to recover the plaintext flag. The script is the tool that does it; the work is figuring out *how to invoke it correctly*.

## Walkthrough

### Step 1 — Download all three files

In the picoCTF / CyLab terminal, grab each file with `wget`:

```bash
wget <link-to-ende.py>
wget <link-to-flag.txt.en>
wget <link-to-password-file>
```

### Step 2 — Ask the script what it does

Before reading the source, run the script with no useful arguments to see if it self-documents:

```bash
python3 ende.py
```

It prints usage information — it can **encrypt** and **decrypt**. Useful, but not the full picture.

### Step 3 — Read the source

This is the actual challenge. Don't run an unfamiliar script blind — read it:

```bash
cat ende.py
```

Reading through the script reveals the important detail: when decrypting, it expects to operate on a specific input file. Depending on the variant, it either hardcodes a filename or takes one as an argument. The key insight from reading the source is understanding *which file it wants and what flag invokes decrypt mode*.

This step is the whole point of the challenge. The flag isn't gated behind a clever trick — it's gated behind whether you bothered to understand the tool before using it.

### Step 4 — Stage the encrypted file

The script operates on a particular filename. To feed it the encrypted flag, make a copy with the name the script expects:

```bash
cp flag.txt.en pole.txt
```

A note on `cp` vs `mv`: `cp` *copies* the file, leaving the original `flag.txt.en` in place. `mv` would *rename* it, removing the original. Either works here, but `cp` is the safer habit — it preserves your original data in case you need to start over. When you're manipulating files during an investigation, defaulting to non-destructive operations is a good reflex.

### Step 5 — Read the password

The decrypt operation needs the password. Print it and keep it handy:

```bash
cat pw.txt
```

### Step 6 — Decrypt

Run the script in decrypt mode against the staged file:

```bash
python3 ende.py -d pole.txt
```

The `-d` flag is the script's own decrypt mode (defined in `ende.py` itself — not a system flag like in some other challenges). The script prompts for the password; supply the one from `pw.txt`. The flag prints in standard `picoCTF{...}` format.

## What this challenge is actually about

On the surface this is "run a Python script." Underneath, it's three transferable skills:

**Reading code before executing it.** You were handed an unfamiliar script. The correct move was to `cat` it and understand its behavior before depending on it. In a security context this is non-negotiable — running unknown code blind is how analysts get compromised. The same `python3 ende.py` you ran could, in a malicious file, have done anything. Reading first is the safety habit.

**Understanding symmetric encryption from the outside.** `ende.py` encrypts and decrypts with the same password — that's *symmetric* encryption. The same secret protects and reveals the data. You didn't need to understand the cipher internals to use it, but the challenge quietly introduces the concept: one key, two operations, and the security rests entirely on keeping the key (here, `pw.txt`) secret. The whole challenge is a lesson in why "the password was sitting in a file right next to the encrypted data" is a catastrophic real-world mistake.

**The file-staging mindset.** The script wanted a specific input. Rather than editing the script, you adapted the *environment* to fit the tool — copying the encrypted file to the name the script expected. That's a small instance of a recurring pattern: when a tool has assumptions, you often satisfy the assumptions rather than rewrite the tool.

## What this challenge teaches

- **Read unfamiliar scripts before running them.** `cat` first, execute second. Always.
- **Self-documenting tools exist.** Running a script with no args (or `-h`) often reveals its interface before you read a line of source.
- **`cp` is non-destructive; `mv` is not.** Default to `cp` when you might need the original back.
- **Symmetric encryption is only as strong as key secrecy.** A password stored next to the ciphertext provides no protection at all — which is the entire (deliberate) joke of this challenge.

A genuine step up from the pure-warmup challenges, and a good on-ramp to the Python work ahead.
