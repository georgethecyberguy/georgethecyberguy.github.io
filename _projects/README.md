# hashcrack

A small, readable password hash cracker in Python — supporting dictionary
and brute-force attacks against common hash types, with salt support and
automatic algorithm detection.

Built as an educational tool: a clear reference implementation of the
attacks behind picoCTF's PW Crack series, scaled into something usable.
It is **not** a replacement for [hashcat](https://hashcat.net/hashcat/) or
[John the Ripper](https://www.openwall.com/john/) — those are
GPU-accelerated and orders of magnitude faster. This prioritizes clarity
over speed.

## Features

- **Multiple hash types:** MD5, SHA-1, SHA-256, SHA-512.
- **Automatic algorithm detection** from hash length (override with `-a`).
- **Dictionary attack:** test each entry in a wordlist.
- **Brute-force attack:** exhaustively try combinations from a chosen
  character set up to a maximum length.
- **Salt support:** prefix or suffix salts.
- **Progress and timing** with `-v`.

## Usage

```bash
# Dictionary attack (algorithm auto-detected from hash length)
python3 hashcrack.py 0d107d09f5bbe40cade3de5c71e9e9b7 -w wordlist.txt

# Force a specific algorithm
python3 hashcrack.py <hash> -a sha256 -w wordlist.txt

# Brute-force, digits only, up to 4 characters
python3 hashcrack.py <hash> -b -c digits -m 4

# Dictionary first, then brute-force if it misses
python3 hashcrack.py <hash> -w wordlist.txt -b -c alnum -m 4

# Salted hash (salt prepended to the password)
python3 hashcrack.py <hash> -w wordlist.txt -s mysalt --salt-position prefix

# Verbose output (progress + timing)
python3 hashcrack.py <hash> -w wordlist.txt -v
```

## Options

| Flag | Description |
| --- | --- |
| `hash` | The target hash to crack (positional). |
| `-a`, `--algorithm` | Hash algorithm. Auto-detected from length if omitted. |
| `-w`, `--wordlist` | Path to a wordlist for a dictionary attack. |
| `-b`, `--brute-force` | Enable brute-force mode. |
| `-c`, `--charset` | Character set for brute-force: `digits`, `lower`, `upper`, `alpha`, `alnum`, `all`. Default `alnum`. |
| `-m`, `--max-length` | Max password length for brute-force. Default `4`. |
| `-s`, `--salt` | Salt value, if the hash is salted. |
| `--salt-position` | `prefix` or `suffix`. Default `prefix`. |
| `-v`, `--verbose` | Show progress and timing. |

## A note on brute-force cost

Brute-force is exponential. The number of combinations is
`charset_size ^ length`. With the full character set (~94 printable
characters), brute-forcing even a 6-character password is over 600 billion
combinations — impractical for this tool. Brute-force here is meant for
short passwords and to *demonstrate why length matters* far more than
complexity for password strength.

## Why this exists

Working through picoCTF's PW Crack series, the same technique kept
recurring: hash each candidate, compare to the target. Levels 3 and 4
made me write that loop by hand. This tool generalizes that loop into
something reusable, and along the way demonstrates the concepts that make
the attack work — and the defenses (salting, slow hashing) that defeat it.

The full writeup is at
[georgethecyberguy.github.io/projects/hashcrack](https://georgethecyberguy.github.io/projects/hashcrack/).

## Ethics

This tool is for cracking hashes you are **authorized** to crack — your
own, CTF challenges, and systems you have explicit permission to test.
Using it against systems or data you don't own or have permission to test
is illegal. Don't.

## License

MIT
