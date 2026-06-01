---
group: lab
title: "picoCTF — PW Crack 2"
order: 107
year: 2026
kind: CTF
status: Solved
role: Author
stack:
  - Python
  - Hexadecimal
summary: Part 2 of picoCTF's five-part PW Crack series. The author's first attempt to hide the password — storing it as hexadecimal instead of plaintext — and why it changes nothing.
event: picoCTF 2026
category: General Skills
points: 100
---

> **Spoiler note:** This is a full walkthrough. If you want to attempt the challenge first, head to [picoCTF](https://picoctf.org) and come back.

The second entry in the **PW Crack** series, and the first where the author actually *tries* to hide the password. In [PW Crack 1](/projects/picoctf-pw-crack-1/) the password sat in the source as a plain string. Here it's stored as hexadecimal — a small obfuscation that looks like protection but provides none, because the conversion logic is right there in the script for you to read and reverse.

This is the series thesis getting its first real test: **obscuring a secret in code you control doesn't hide it.**

## The challenge

Two files, same structure as Level 1:

- `level2.py` — the password-checking, flag-decrypting script.
- `level2.flag.txt.enc` — the encrypted flag.

The difference is in how the script stores the password it's checking against.

## Walkthrough

### Step 1 — Download both files

```bash
wget <link-to-level2.py>
wget <link-to-level2.flag.txt.enc>
```

Keep them in the same directory, as before.

### Step 2 — Read the script

```bash
nano level2.py
```

(`Ctrl + X` to exit `nano` — shortcuts are on the bottom bar, `^` meaning `Ctrl`.)

### Step 3 — Spot the obfuscation

This time the password isn't a readable string. Instead, the script holds the expected value as **hexadecimal** — a sequence of hex byte values that get converted before comparison. You'll see something in the source that takes a hex representation and turns it into the actual password characters.

The "hiding" is purely cosmetic. Hexadecimal is not encryption — it's just a different *representation* of the same bytes. `0x64` is the byte `d`, `0x65` is `e`, and so on. Anyone who recognizes hex can convert it back by hand or with a one-liner.

### Step 4 — Convert the hex to the password

Once you've identified the hex values in the source, convert them to ASCII characters. The resulting four-character password is what the script expects. (Recognizing the pattern and performing the conversion is the skill here — I'm leaving the converted value out so the technique is the takeaway, not the answer.)

A quick way to convert hex to ASCII at the command line:

```bash
python3 -c "print(bytes.fromhex('<hex-here>').decode())"
```

Or do it by hand against an ASCII table for a handful of bytes — worth doing once to internalize that hex ↔ characters is a trivial, reversible mapping.

### Step 5 — Run the script and supply the password

```bash
python3 level2.py
```

Enter the converted password. The script XOR-decrypts and prints the flag in `picoCTF{...}` format.

## Why hex "hiding" fails

Hexadecimal shows up constantly in security work, and it's important to be precise about what it is and isn't:

- **Hex is encoding, not encryption.** Encoding transforms data into a different format for transport or display; it requires no key and is trivially reversible by anyone. Encryption transforms data using a secret key, and without the key the transformation can't be undone. Storing a password in hex is like writing it in a slightly different alphabet — the information is fully intact and recoverable.
- **The same applies to Base64, URL-encoding, and ROT13.** These are all *encodings*. A surprising amount of real-world "security" leans on encoding and calls it protection. Base64-encoded credentials in HTTP headers, hex-encoded config values, ROT13'd "hidden" strings — all recoverable in seconds.
- **Recognizing encodings is a core analyst skill.** A blue-teamer reading logs or malware needs to spot "that's hex," "that's Base64," "that's URL-encoded" on sight and decode it. Tools like [CyberChef](https://gchq.github.io/CyberChef/) exist precisely because chaining and reversing encodings is such a constant task.

The deeper point connects straight back to the series thesis: the author tried to hide the password by *representing it differently*. But representation isn't protection. The script has to convert the hex back to the real password in order to do its comparison — which means the conversion logic is right there, and you can run it forward yourself.

## What this challenge teaches

- **Encoding ≠ encryption.** The single most important distinction in this writeup. Hex, Base64, and URL-encoding hide nothing.
- **Recognize hex on sight.** Pairs of characters in `0-9a-f`, often prefixed `0x` or passed to a `fromhex`-style call. Spotting it is half the battle.
- **The conversion is reversible because it must be.** Any obfuscation the program itself can undo, you can undo too, by reading how the program does it.
- **The series thesis holds.** Level 1 hid nothing; Level 2 hid the password behind a different representation. Same result — visible logic, recoverable secret.

Next: PW Crack 3, where the obfuscation gets one step more involved — and falls the same way.
