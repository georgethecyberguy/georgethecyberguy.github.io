---
title: "picoCTF — PW Crack 1"
order: 106
year: 2026
kind: CTF
status: Solved
role: Author
stack:
  - Python
  - XOR
summary: The first of picoCTF's five-part PW Crack series. Level 1 introduces the format — a Python script that checks a password and decrypts a flag — with the password hiding in plain sight.
event: picoCTF 2026
category: General Skills
points: 100
---

> **Spoiler note:** This is a full walkthrough. If you want to attempt the challenge first, head to [picoCTF](https://picoctf.org) and come back.

This is the first entry in picoCTF's **PW Crack** series — five challenges that build on one another, each making the password harder to recover than the last. Level 1 is the gentle on-ramp: it establishes the structure you'll see throughout the series and asks only that you read the source carefully.

The series as a whole is a nicely designed lesson in *why* password handling done in client-visible code is hopeless. Each level, the author tries a slightly more sophisticated way to hide the password in the script — and each level, because the script is right there in front of you, it fails. By the end you'll have internalized the principle the hard way: **a secret embedded in code you control is not a secret.**

## The challenge

You're given two files:

- `level1.py` — a Python script that prompts for a password, and if it's correct, decrypts and prints the flag.
- `level1.flag.txt.enc` — the encrypted flag the script operates on.

The goal is to supply the correct password so the script decrypts the flag.

## Walkthrough

### Step 1 — Download both files

```bash
wget <link-to-level1.py>
wget <link-to-level1.flag.txt.enc>
```

Both files must end up in the same directory — the script reads the `.enc` file relative to where it runs.

### Step 2 — Read the script

Same instinct as every challenge before this one: read before you run.

```bash
cat level1.py
```

If you'd prefer a more readable view — especially as the scripts get longer in later levels — open it in a terminal editor:

```bash
nano level1.py
```

A quick `nano` orientation, since it traps people: the command shortcuts are listed along the bottom bar, where `^` means the `Ctrl` key. To exit, press `Ctrl + X`. You're only reading here, so if it asks to save on exit, you can decline.

### Step 3 — Understand the core logic

Two lines carry the challenge:

```python
flag_enc = open('level1.flag.txt.enc', 'rb').read()
decryption = str_xor(flag_enc.decode(), user_pw)
```

Reading these tells you exactly how the script works:

1. It opens the encrypted flag file in binary mode (`'rb'`) and reads its contents.
2. It runs an XOR operation (`str_xor`) between the encrypted data and the password you supply.

XOR is the entire cryptographic mechanism here. It's a *symmetric* operation — XORing the ciphertext with the correct key reproduces the plaintext. (This is the same symmetric-key idea introduced in the [Python Wrangling](/projects/picoctf-python-wrangling/) writeup, now visible at the code level.)

### Step 4 — Find the password

For Level 1, the password is checked against a value that's visible in the script itself. Reading the source reveals the expected password — in this instance, `691d`. There's no cracking involved yet; the "password check" is comparing your input against a string that's sitting right there in the code.

### Step 5 — Run it and supply the password

```bash
python3 level1.py
```

Enter the password when prompted. The script XOR-decrypts the flag file and prints the result in standard `picoCTF{...}` format.

## Why Level 1 is structured this way

The whole PW Crack series is a slow-motion demonstration of a single truth: **you cannot hide a password inside a program and also give someone that program.** Level 1 makes the point bluntly — the password is just *there* in the source. Later levels obscure it (encoding it, hashing it, comparing against transformed values), and each obfuscation falls because the verification logic itself is visible, and visible logic can always be run forward or reasoned backward.

This maps to a real and expensive category of mistake:

- **Hardcoded credentials in client applications** — mobile apps, desktop software, and browser JavaScript routinely ship with API keys, database passwords, or signing secrets baked in. Decompilers and `strings` recover them trivially.
- **Security through obscurity** — the belief that hiding *how* something works provides protection. It delays a determined attacker by minutes, not meaningfully at all.
- **Client-side authentication** — any check performed on the user's machine can be bypassed by the user, because the user controls the machine.

The defensive lesson, true across the whole series: **authentication and secrets belong on a server the attacker doesn't control.** A password check in code you hand to someone is theater.

## What this challenge teaches

- **Read the source.** The answer to Level 1 is simply *in the file.* The skill is the discipline of looking.
- **XOR is reversible.** Symmetric operations protect and reveal with the same key — understand this and the entire series clicks into place.
- **`nano` basics.** `Ctrl + X` to exit; shortcuts live on the bottom bar with `^` meaning `Ctrl`. Worth knowing as scripts grow.
- **Embedded secrets aren't secret.** The thesis of the whole PW Crack series, stated plainly at Level 1.

Next up: PW Crack 2, where the author starts trying to hide the password — and we watch the same principle defeat each attempt.
