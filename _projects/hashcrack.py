#!/usr/bin/env python3
"""
hashcrack - a small, educational password hash cracker.

Supports dictionary (wordlist) and brute-force attacks against common
unsalted and salted hash types. Built as a learning tool to demonstrate
how the attacks behind picoCTF's PW Crack series scale in practice.

NOT a replacement for hashcat or John the Ripper. This is a clear,
readable reference implementation, not a performance-tuned cracker.

Author: George Hall
License: MIT
"""

import argparse
import hashlib
import itertools
import string
import sys
import time

# --------------------------------------------------------------------
# Hash type support
# --------------------------------------------------------------------
# Map each supported algorithm to its hashlib constructor and the
# length (in hex characters) of its output. The length lets us
# auto-detect the likely algorithm from a bare hash string.
HASH_TYPES = {
    "md5":     {"fn": hashlib.md5,    "hexlen": 32},
    "sha1":    {"fn": hashlib.sha1,   "hexlen": 40},
    "sha256":  {"fn": hashlib.sha256, "hexlen": 64},
    "sha512":  {"fn": hashlib.sha512, "hexlen": 128},
}

# Multiple algorithms can share a digest length (none of the above do,
# but SHA-2 variants can collide with other families). When a length is
# ambiguous we return all candidates and let the user disambiguate.
LENGTH_TO_TYPES = {}
for name, meta in HASH_TYPES.items():
    LENGTH_TO_TYPES.setdefault(meta["hexlen"], []).append(name)


def detect_hash_type(target_hash):
    """Guess the algorithm(s) from the hash length. Returns a list."""
    candidates = LENGTH_TO_TYPES.get(len(target_hash), [])
    return candidates


def compute_hash(algorithm, candidate, salt="", salt_position="prefix"):
    """
    Hash a candidate password with the given algorithm, optionally
    applying a salt before or after the password.
    """
    if salt:
        if salt_position == "prefix":
            data = salt + candidate
        else:  # suffix
            data = candidate + salt
    else:
        data = candidate

    fn = HASH_TYPES[algorithm]["fn"]
    return fn(data.encode("utf-8", errors="ignore")).hexdigest()


# --------------------------------------------------------------------
# Attack modes
# --------------------------------------------------------------------
def dictionary_attack(target_hash, algorithm, wordlist_path,
                      salt="", salt_position="prefix", verbose=False):
    """
    Try each word in the wordlist. Returns the matching password, or
    None if exhausted with no match.
    """
    target_hash = target_hash.lower()
    tried = 0
    start = time.time()

    try:
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                candidate = line.rstrip("\n\r")
                if not candidate:
                    continue
                tried += 1
                if compute_hash(algorithm, candidate, salt, salt_position) == target_hash:
                    elapsed = time.time() - start
                    if verbose:
                        print(f"[+] Match after {tried} candidates "
                              f"in {elapsed:.2f}s ({tried/elapsed:,.0f}/s)")
                    return candidate
                if verbose and tried % 100000 == 0:
                    print(f"[*] {tried:,} candidates tried...")
    except FileNotFoundError:
        sys.exit(f"[!] Wordlist not found: {wordlist_path}")

    return None


def brute_force_attack(target_hash, algorithm, charset, max_length,
                       salt="", salt_position="prefix", verbose=False):
    """
    Try every combination of characters in `charset` up to `max_length`.
    Exhaustive but exponential — practical only for short passwords.
    """
    target_hash = target_hash.lower()
    tried = 0
    start = time.time()

    for length in range(1, max_length + 1):
        if verbose:
            space = len(charset) ** length
            print(f"[*] Trying length {length} "
                  f"({space:,} combinations)...")
        for combo in itertools.product(charset, repeat=length):
            candidate = "".join(combo)
            tried += 1
            if compute_hash(algorithm, candidate, salt, salt_position) == target_hash:
                elapsed = time.time() - start
                if verbose:
                    print(f"[+] Match after {tried:,} candidates "
                          f"in {elapsed:.2f}s")
                return candidate

    return None


# --------------------------------------------------------------------
# Charset helpers for brute-force mode
# --------------------------------------------------------------------
CHARSETS = {
    "digits":   string.digits,
    "lower":    string.ascii_lowercase,
    "upper":    string.ascii_uppercase,
    "alpha":    string.ascii_letters,
    "alnum":    string.ascii_letters + string.digits,
    "all":      string.ascii_letters + string.digits + string.punctuation,
}


# --------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------
def build_parser():
    p = argparse.ArgumentParser(
        prog="hashcrack",
        description="A small educational password hash cracker "
                    "(dictionary and brute-force modes).",
        epilog="Example: hashcrack 5f4dcc3b5aa765d61d8327deb882cf99 "
               "-w rockyou.txt",
    )
    p.add_argument("hash", help="the target hash to crack")
    p.add_argument("-a", "--algorithm",
                   choices=list(HASH_TYPES.keys()),
                   help="hash algorithm (auto-detected from length if omitted)")
    p.add_argument("-w", "--wordlist",
                   help="path to a wordlist for a dictionary attack")
    p.add_argument("-b", "--brute-force", action="store_true",
                   help="enable brute-force mode")
    p.add_argument("-c", "--charset", default="alnum",
                   choices=list(CHARSETS.keys()),
                   help="character set for brute-force (default: alnum)")
    p.add_argument("-m", "--max-length", type=int, default=4,
                   help="max password length for brute-force (default: 4)")
    p.add_argument("-s", "--salt", default="",
                   help="salt value, if the hash is salted")
    p.add_argument("--salt-position", choices=["prefix", "suffix"],
                   default="prefix",
                   help="where the salt is applied (default: prefix)")
    p.add_argument("-v", "--verbose", action="store_true",
                   help="show progress and timing")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    target = args.hash.strip().lower()

    # Resolve algorithm: explicit flag, or auto-detect from length.
    if args.algorithm:
        algorithm = args.algorithm
    else:
        candidates = detect_hash_type(target)
        if not candidates:
            sys.exit(f"[!] Could not auto-detect hash type for a "
                     f"{len(target)}-character hash. Specify with -a.")
        if len(candidates) > 1:
            sys.exit(f"[!] Ambiguous hash length. Candidates: "
                     f"{', '.join(candidates)}. Specify with -a.")
        algorithm = candidates[0]
        if args.verbose:
            print(f"[*] Auto-detected algorithm: {algorithm}")

    # Must pick at least one mode.
    if not args.wordlist and not args.brute_force:
        sys.exit("[!] Choose an attack: -w <wordlist> and/or -b "
                 "(brute-force).")

    result = None

    # Dictionary first — it's faster and more likely to succeed.
    if args.wordlist:
        if args.verbose:
            print(f"[*] Dictionary attack with {args.wordlist}...")
        result = dictionary_attack(
            target, algorithm, args.wordlist,
            args.salt, args.salt_position, args.verbose)

    # Fall back to brute-force if requested and dictionary missed.
    if result is None and args.brute_force:
        if args.verbose:
            print(f"[*] Brute-force: charset='{args.charset}', "
                  f"max_length={args.max_length}...")
        result = brute_force_attack(
            target, algorithm, CHARSETS[args.charset], args.max_length,
            args.salt, args.salt_position, args.verbose)

    # Report.
    if result is not None:
        print(f"\n[+] CRACKED: {target} ({algorithm}) = {result}")
        return 0
    else:
        print(f"\n[-] No match found for {target} ({algorithm}).")
        return 1


if __name__ == "__main__":
    sys.exit(main())
