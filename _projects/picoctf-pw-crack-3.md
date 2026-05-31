---
title: "picoCTF — PW Crack 3"
order: 108
year: 2026
kind: CTF
status: Solved
role: Author
stack:
  - Python
  - MD5
  - Dictionary attack

summary: Part 3 of picoCTF's five-part PW Crack series — the turning point, where the password is protected by a one-way hash and the attack shifts from decoding to cracking.

event: picoCTF 2026
category: General Skills
points: 100
---

> **Spoiler note:** This is a full walkthrough. If you want to attempt the challenge first, head to [picoCTF](https://picoctf.org) and come back.

This is the pivot point of the **PW Crack** series. [Level 1](/projects/picoctf-pw-crack-1/) hid the password in plain sight; [Level 2](/projects/picoctf-pw-crack-2/) hid it behind a reversible hex encoding. Both fell to *reading and reversing* the source. Level 3 changes the game: the password is now protected by a **one-way hash**, which can't be reversed at all. The attack has to change with it — from decoding to **cracking**.

If the first two levels were about recognizing that encoding isn't protection, this one is about understanding what real protection (hashing) looks like, and why even that fails when the candidate set is small and known.

## The challenge

Three files this time:

- `level3.py` — the script, which contains a *list of possible passwords*.
- `level3.hash.bin` — a file holding the target hash.
- `level3.flag.txt.enc` — the encrypted flag.

The script checks a supplied password by hashing it and comparing against a stored target. The work is figuring out *which* of the candidate passwords produces the matching hash.

## Walkthrough

### Step 1 — Download the files

```bash
wget <link-to-level3.py>
wget <link-to-level3.hash.bin>
wget <link-to-level3.flag.txt.enc>
```

### Step 2 — Read the script

```bash
cat level3.py
```

Two things stand out. First, there's a **list of candidate passwords** right in the source — a small set of possible values. Second, the verification works by *hashing* the input and comparing it to a stored hash, rather than comparing the password directly.

### Step 3 — Inspect the hash file

The target hash lives in `level3.hash.bin`. To look inside a binary-ish file, open it in an editor like `vi`:

```bash
vi level3.hash.bin
```

(In `vi`, type `:q!` and press Enter to quit without saving.)

The contents turn out to be **Base64-encoded**. Running it through [CyberChef](https://gchq.github.io/CyberChef/) — decoding the Base64 — reveals a 32-character hexadecimal string. That length and character set is the signature of an **MD5 hash**.

### Step 4 — Recognize the wall (and the way around it)

Here's the key realization, and the reason this level matters: **an MD5 hash is one-way.** Unlike the hex in Level 2, you cannot mathematically reverse it to recover the original password. Decoding gets you nothing further. The hash is the destination, not a disguise.

So the approach inverts. Instead of working *backward* from the hash, you work *forward* from the candidates:

1. Take each candidate password from the list in the script.
2. Hash it with MD5.
3. Compare the result to the target hash.
4. The candidate whose hash matches *is* the password.

You're not breaking the hash — you're guessing inputs, hashing each guess, and checking for a match. This works because the real password is somewhere in that candidate list; you just have to find which one.

### Step 5 — Run the attack

The script can do this loop itself once you understand its structure. Running it:

```bash
python3 level3.py
```

It iterates the candidate list, hashes each, finds the one matching the target, and uses it to decrypt the flag — printed in standard `picoCTF{...}` format. (If you're reproducing the comparison manually, the pattern is `hashlib.md5(candidate.encode()).hexdigest()` against the decoded target — but the method is the takeaway, not the matching value.)

## Dictionary attack vs. brute-force — the distinction matters

It's tempting to call this "brute-forcing the password," but it's worth being precise, because the vocabulary is meaningful in security work:

- **Dictionary attack** (what this level is): you test a *known, finite list* of candidate passwords. Fast, because the list is small. Effective only when the real password is *in* the list. The PW Crack 3 candidate list is the "dictionary."
- **Brute-force attack:** you generate *every possible* string — `a`, `b`, ... `aa`, `ab`, and so on — up to some length. Guaranteed to find the password eventually, but exponentially expensive as length grows. You'd use this only when you have no candidate list to work from.

This level is firmly a dictionary attack, and that's the more *realistic* of the two — real-world password cracking overwhelmingly uses dictionaries (and dictionaries augmented with rules: appending years, swapping letters for numbers, etc.), because humans pick predictable passwords. Pure brute-force is the last resort.

## How this maps to real cracking

The loop you ran here — hash each candidate, compare to target — is *exactly* what professional cracking tools do, just at enormous scale:

- **[Hashcat](https://hashcat.net/hashcat/)** and **[John the Ripper](https://www.openwall.com/john/)** hash millions to billions of candidates per second (GPU-accelerated), comparing against stolen hash dumps.
- **Real attacks target leaked hash databases.** When a service is breached and its password hashes leak, attackers run dictionary and brute-force attacks offline against those hashes to recover plaintext passwords.
- **This is why MD5 is broken for passwords.** MD5 is fast — which is great for checksums and terrible for password storage, because "fast to hash" means "fast to crack." Modern password storage uses deliberately *slow*, salted algorithms (bcrypt, scrypt, Argon2) specifically to make this attack expensive. The defensive lesson: never store passwords with a fast general-purpose hash like MD5 or SHA-1.

The series thesis evolves here. Levels 1 and 2 showed that *obscuring* a secret fails. Level 3 shows that even *properly hashing* a secret fails when the input space is small and known — because hashing protects against reversal, not against guessing.

## What this challenge teaches

- **Hashes are one-way; encodings are two-way.** You can decode Base64 or hex back to the original. You cannot decode a hash. This is the single most important distinction in the whole series.
- **When you can't reverse, you guess forward.** Hash your candidates and compare. That's cracking.
- **Dictionary attack ≠ brute-force.** Know the difference and use the right word.
- **Fast hashes are bad for passwords.** MD5's speed is exactly what makes it crackable. Real systems use slow, salted hashes by design.

Next: PW Crack 4 and 5, where the candidate lists grow and the attack scales — same forward-guessing method, larger haystack.
