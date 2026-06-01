---
group: lab
title: "picoCTF — PW Crack 4"
order: 109
year: 2026
kind: CTF
status: Solved
role: Author
stack:
  - Python
  - Dictionary attack
  - Loops

summary: Part 4 of picoCTF's five-part PW Crack series — the same hash-checking problem as Level 3, but with a hundred candidates instead of a handful, forcing you to stop guessing manually and write the loop yourself.

event: picoCTF 2026
category: General Skills
points: 100
---

> **Spoiler note:** This is a full walkthrough. If you want to attempt the challenge first, head to [picoCTF](https://picoctf.org) and come back.

The fourth entry in the **PW Crack** series, and the one where you cross a meaningful line: from *running* a cracking routine to *writing* one. [Level 3](/projects/picoctf-pw-crack-3/) introduced the dictionary attack with a small candidate list you could almost eyeball. Level 4 hands you **a hundred candidates** — too many to try by hand — so the only sane approach is to let Python do the iterating. The concept is identical; the scale forces better technique.

## The challenge

The familiar trio of files:

- `level4.py` — the script, this time containing a list of 100 possible passwords (`pos_pw_list`).
- The hash/encrypted-flag files the script checks against.

The script has a password-check function but doesn't loop over the candidates for you. Your job is to add that loop.

## Walkthrough

### Step 1 — Download the files

```bash
wget <links-to-the-files>
```

### Step 2 — Open the script for editing

```bash
nano level4.py
```

(`Ctrl + O` then Enter to save in `nano`; `Ctrl + X` to exit.)

Unlike the earlier levels, you're not just reading this one — you're modifying it. The script provides a `pos_pw_list` (the 100 candidates) and a check function, but leaves the iteration to you.

### Step 3 — Add the loop (what I did)

My first working version passed the candidate list into the check function and looped over it by index:

```python
def level_4_pw_check(pos_pw_list):
    for i in range(1, 100):
        user_pw = pos_pw_list[i]
        # ... existing hash-and-compare logic runs against user_pw ...

level_4_pw_check(pos_pw_list)
```

This ran, found the matching candidate, and decrypted the flag. Challenge solved.

### Step 4 — The better pattern (and why)

The version above works *for this challenge*, but it has a latent bug worth understanding, because it's exactly the kind of off-by-one error that bites you on real code:

`range(1, 100)` produces the numbers `1, 2, ... 99`. That means:

- **It skips index `0`** — the *first* candidate in the list is never checked.
- **If the list has exactly 100 items (indices `0`–`99`), it never checks index `99`'s neighbor correctly** — `range(1,100)` stops at 99, so the last index reached is 99, but index 0 is missed entirely.

It worked only because the correct password happened to sit somewhere in indices 1–99. If the answer had been the very first entry, this loop would have silently failed to find it.

The robust pattern is to let Python iterate the list directly, without hand-managing indices at all:

```python
def level_4_pw_check(pos_pw_list):
    for user_pw in pos_pw_list:
        # ... existing hash-and-compare logic runs against user_pw ...

level_4_pw_check(pos_pw_list)
```

Iterating `for user_pw in pos_pw_list` walks *every* element, start to finish, with no off-by-one risk and no dependence on knowing the list's exact length. If you do need the index for some reason, `for i, user_pw in enumerate(pos_pw_list)` gives you both safely. And if you must use `range`, `range(len(pos_pw_list))` covers the whole list regardless of size.

The lesson: **prefer iterating the collection over iterating a hardcoded number range.** Hardcoding `100` couples your loop to an assumption about the data that can silently break. Iterating the list itself is shorter, safer, and self-adjusting.

### Step 5 — Run it

```bash
python3 level4.py
```

The loop walks the candidates, hashes each, finds the match, and decrypts the flag in standard `picoCTF{...}` format.

## Why this level matters

Levels 1–3 were about *recognizing* what kind of protection you were facing (plaintext, encoding, hashing). Level 4 is the first that demands you *build the tool*. That shift — from consumer of a script to author of one — is the single most valuable jump in the series, because automation is the entire game in real password cracking:

- **Scale is the whole point.** A human can try five passwords. A loop tries a hundred instantly; a real tool like [Hashcat](https://hashcat.net/hashcat/) tries billions. The technique you wrote here is the same one those tools industrialize.
- **The candidate list is the "dictionary."** This is still a dictionary attack — you're testing a known, finite set. Level 4 just makes the set big enough that manual checking stops being viable, which is the realistic case.
- **Correct iteration is a security skill, not just a coding nicety.** An off-by-one that skips a candidate means a real cracking tool would *miss the password and report failure* even though the answer was right there. Iterating completely and correctly is the difference between "no match found" and "cracked."

This is also a natural seed for an original project: the loop you wrote here, generalized into a small standalone Python tool that takes a hash and a wordlist and reports the match, would be a genuinely useful portfolio piece — and a clean demonstration that you can write security tooling, not just solve puzzles.

## What this challenge teaches

- **Automate the moment manual stops scaling.** A hundred candidates is the cue to write a loop.
- **Iterate the collection, not a magic number.** `for x in list` over `for i in range(1, 100)`. Avoids off-by-one bugs and adapts to any list size.
- **`enumerate` when you need the index too.** Safer than hand-managing `range(len(...))`.
- **The dictionary attack scales by code, not by effort.** Same method as Level 3, more candidates, zero additional manual work once the loop exists.

Next: PW Crack 5, the finale — where the candidate set grows again and the series thesis reaches its conclusion.
