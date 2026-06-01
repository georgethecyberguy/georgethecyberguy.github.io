---
group: lab
title: "picoCTF — PW Crack 5"
order: 110
year: 2026
kind: CTF
status: Solved
role: Author
stack:
  - Python
  - MD5
  - Rainbow tables

summary: Part 5 of 5 — the finale of picoCTF's PW Crack series, where the attack moves off your own machine entirely and onto a precomputed hash-lookup service.

event: picoCTF 2026
category: General Skills
points: 100
---

> **Spoiler note:** This is a full walkthrough. If you want to attempt the challenge first, head to [picoCTF](https://picoctf.org) and come back.

The finale of the **PW Crack** series. [Level 4](/projects/picoctf-pw-crack-4/) had you write a loop to test a hundred candidates yourself. Level 5 takes the dictionary attack to its logical endpoint: instead of generating and hashing candidates locally, you hand the target hash to a service that has *already* hashed billions of common passwords and stored the results for instant lookup. No loop, no code edit — just a precomputed table doing in milliseconds what would take your laptop a long while.

This level introduces **rainbow tables** (and their practical cousins, hash-lookup databases), and in doing so completes the series' argument about why fast, unsalted hashing is a dead end for password storage.

## The challenge

The usual files:

- `level5.py` — the password-checking, flag-decrypting script. Unlike Level 4, you won't modify it.
- `level5.hash.bin` — the file holding the target hash.
- the encrypted flag.

This time the candidate list isn't small enough to loop, and isn't given to you at all. The hash itself is the only lead.

## Walkthrough

### Step 1 — Download the files

```bash
wget <links-to-the-files>
```

### Step 2 — Extract the hash from the binary

The hash lives in `level5.hash.bin`. To read a binary file cleanly, use `bvi` — a binary-aware version of the `vi` editor, better suited to `.bin` files than plain `vi`:

```bash
bvi level5.hash.bin
```

(In `bvi`, `:q` then Enter quits.)

Inside, you'll find a 32-character hexadecimal string — the MD5 signature again, same as [Level 3](/projects/picoctf-pw-crack-3/).

### Step 3 — Look the hash up

Here's the new tactic. Rather than cracking the hash with your own dictionary loop, submit it to a precomputed lookup service like [CrackStation](https://crackstation.net/):

- Copy the MD5 hash out of the file.
- **Watch for stray spaces or formatting** when you paste — a hash with embedded whitespace won't match anything. Strip it down to the clean 32 hex characters.
- Submit it.

If the underlying password is a common one (and in this challenge it is), CrackStation returns the plaintext instantly. It can do this because it has *already* hashed enormous wordlists and stored hash→plaintext mappings — so "cracking" becomes a simple database lookup.

### Step 4 — Run the script with the recovered password

```bash
python3 level5.py
```

Enter the recovered password when prompted. The script decrypts and prints the flag in standard `picoCTF{...}` format.

## Rainbow tables and lookup services — the concept

Level 5's tactic rests on a time-memory tradeoff that's worth understanding precisely:

- **Doing it live (Level 4 style):** hash each candidate at attack time and compare. Costs computation every single attack.
- **Precomputing (Level 5 style):** hash a massive wordlist *once*, store the results, and thereafter just *look up* any target hash. Costs storage instead of repeated computation.

A **rainbow table** is a space-optimized version of that precomputed store — it uses clever chaining to shrink the storage needed while still allowing fast reversal. Services like CrackStation use large lookup databases (and rainbow-table techniques) so that any hash of a previously-seen password resolves instantly.

Two defensive consequences flow directly from this, and they're the payoff of the whole series:

- **This is exactly why salting exists.** A *salt* is a unique random value added to each password before hashing. It means identical passwords produce *different* hashes, which defeats precomputed tables entirely — an attacker can't precompute against a salt they've never seen. Every modern password store salts. MD5 as used in this challenge does not, which is precisely why CrackStation can resolve it.
- **This is why fast hashes are the wrong tool.** MD5 and SHA-1 were built to be fast. For password storage you want the *opposite* — deliberately slow, salted algorithms (bcrypt, scrypt, Argon2) that make both live cracking and precomputation prohibitively expensive.

## The series, in retrospect

Five challenges, one argument, escalating each time. Lined up, the arc is the whole lesson:

1. **[PW Crack 1](/projects/picoctf-pw-crack-1/) — plaintext.** The password sat in the source as a readable string. Hiding nothing.
2. **[PW Crack 2](/projects/picoctf-pw-crack-2/) — encoding.** The password was stored as hexadecimal. *Encoding is not encryption* — trivially reversible, so still hiding nothing.
3. **[PW Crack 3](/projects/picoctf-pw-crack-3/) — hashing + small dictionary.** A one-way MD5 hash you *can't* reverse — but with a short candidate list, you hash each guess forward and match. Hashing protects against reversal, not guessing.
4. **[PW Crack 4](/projects/picoctf-pw-crack-4/) — automation.** A hundred candidates, too many by hand, so you write the loop. The dictionary attack scales by code, not effort.
5. **PW Crack 5 — precomputation.** The candidate set is effectively "every common password ever," precomputed by someone else. A lookup, not a loop.

The throughline: **a secret embedded in, or verified by, code and data the attacker controls is not a secret.** Each level tried a more sophisticated way to protect the password — plaintext, then encoding, then hashing, then hashing against larger and larger spaces — and each fell, because the protection always lived somewhere the attacker could see or compute against. The only real defenses (salting, slow hashing, server-side verification) are precisely the ones that move the secret or the work *out of the attacker's reach* — and none of those appear in the PW Crack scripts, by design.

That's a genuinely good security education compressed into five short challenges. Understanding *why* each level falls is worth far more than the five flags.

## What this challenge teaches

- **Precomputation beats live computation when storage is cheap.** Rainbow tables and lookup databases turn cracking into a lookup.
- **Salting defeats precomputation.** Unique per-password salts make precomputed tables useless. Their absence here is why the lookup works.
- **Fast hashes are wrong for passwords.** Use slow, salted algorithms (bcrypt, scrypt, Argon2) for storage.
- **Watch your formatting.** A hash with stray whitespace matches nothing. Small detail, total failure if missed.

With that, the PW Crack series is complete — five levels, one durable lesson about how passwords actually fail.
