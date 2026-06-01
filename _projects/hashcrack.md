---
title: "hashcrack — a Python hash cracker"
order: 1
year: 2026
kind: Tool
status: Complete
role: Author
repo: https://github.com/georgethecyberguy/hashcrack
stack:
  - Python
  - hashlib
  - argparse

summary: A small, readable password hash cracker supporting dictionary and brute-force attacks across MD5/SHA family hashes, with salt support and automatic algorithm detection. The tool the PW Crack series was quietly teaching me to build.

group: tool
---

The [PW Crack series](/projects/picoctf-pw-crack-1/) kept circling the same primitive: hash each candidate password, compare to the target, repeat. [Level 3](/projects/picoctf-pw-crack-3/) introduced it; [Level 4](/projects/picoctf-pw-crack-4/) made me write the loop by hand. The obvious next step was to generalize that loop into something reusable — a proper command-line tool. So I built one.

`hashcrack` is a small, deliberately readable password hash cracker. It is **not** trying to compete with [hashcat](https://hashcat.net/hashcat/) or [John the Ripper](https://www.openwall.com/john/) — those are GPU-accelerated and millions of times faster. This is a clear reference implementation that demonstrates *how* the attacks work, prioritizing legibility over raw speed.

## What it does

- **Four hash types:** MD5, SHA-1, SHA-256, SHA-512.
- **Automatic algorithm detection** by hash length — a 32-char hash is assumed MD5, 64-char is SHA-256, and so on, with a manual override for ambiguous cases.
- **Dictionary attack:** test every entry in a wordlist.
- **Brute-force attack:** exhaustively generate combinations from a chosen character set up to a max length.
- **Salt support:** prefix or suffix, since real systems salt their hashes.
- **Progress and timing** output, including a candidates-per-second rate.

## Design decisions worth noting

A few choices in the build that reflect deliberate thinking rather than just "make it work":

**Auto-detection by length, with a safe fallback.** Hash length is a reliable first guess at algorithm, so the tool detects it automatically for convenience. But length isn't *always* unique across hash families, so the code keeps a length-to-algorithms map and refuses to guess when a length is ambiguous — it asks the user to specify rather than silently picking wrong. Failing loudly beats failing silently.

**Dictionary before brute-force.** When both modes are enabled, the tool always runs the dictionary attack first. This mirrors real-world practice: the overwhelming majority of crackable passwords fall to a wordlist, and a dictionary pass is cheap compared to exponential brute-force. Brute-force is the fallback, not the opener.

**Salt position as an explicit option.** Salting isn't a single thing — implementations differ on whether the salt goes before or after the password. Rather than assume, the tool exposes `--salt-position` so it can match whichever scheme the target used.

**Clean failure modes.** Missing wordlist, no attack mode chosen, unrecognizable hash length — each exits with a clear message and a non-zero status code, so the tool behaves correctly in scripts and pipelines, not just interactively.

## What I learned building it

- **`argparse` for real CLIs.** Moving past `sys.argv` hacking to a proper argument parser with help text, choices validation, and defaults. The difference between a script and a tool is largely its interface.
- **`itertools.product` for brute-force.** Generating every combination of a character set up to length *n* is a one-liner with `itertools.product(charset, repeat=n)` — far cleaner than nested loops, and it makes the exponential cost visible in the code itself.
- **Why salting works, from the attacker's side.** Implementing salt support made the defense concrete: a unique salt per password means a precomputed table (like the one [PW Crack 5](/projects/picoctf-pw-crack-5/) exploited) is useless, because the attacker would have to rebuild the entire table for every distinct salt.
- **Why fast hashes are the wrong choice for passwords.** The verbose mode prints a candidates-per-second rate. Watching MD5 chew through tens of thousands of candidates per second on a *single CPU core* drives home why MD5 and SHA-1 are unfit for password storage, and why slow, salted algorithms (bcrypt, scrypt, Argon2) exist.

## Usage

```bash
# Dictionary attack, algorithm auto-detected
python3 hashcrack.py 0d107d09f5bbe40cade3de5c71e9e9b7 -w wordlist.txt

# Brute-force, digits only, up to 4 chars
python3 hashcrack.py <hash> -b -c digits -m 4

# Salted hash
python3 hashcrack.py <hash> -w wordlist.txt -s mysalt --salt-position prefix
```

Full documentation and the source are in the [repository]({{ page.repo }}).

## Ethics

The tool is for hashes you're **authorized** to crack — your own, CTF challenges, and systems you have explicit permission to test. Running it against anything else is illegal. The README says the same thing, more bluntly.

## What's next

Natural extensions, if I come back to it: support for salted-hash formats that store the salt inline (like `$1$salt$hash`), a rules engine for dictionary mutations (append digits, swap letters for numbers — the things that make real dictionary attacks effective), and multiprocessing to use more than one core. Each is a contained, well-scoped improvement — good candidates for incremental commits rather than a rewrite.
