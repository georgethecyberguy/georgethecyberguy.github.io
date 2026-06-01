---
group: lab
title: "picoCTF — Tab, Tab, Attack"
order: 101
year: 2026
kind: CTF
status: Solved
role: Author
stack:
  - Linux
  - Bash
summary: A General Skills warmup on Linux filename handling and the underrated power of Tab completion.
event: picoCTF 2026
category: General Skills
points: 100
---

> **Spoiler note:** This is a full walkthrough. If you want to attempt the challenge first, head to [picoCTF](https://picoctf.org) and come back.

Another deliberately small General Skills challenge — this one built around a single foundational shell habit that shows up in every Linux interaction afterward: using `Tab` to autocomplete file names. The challenge hands you an executable with a deliberately long, awkward filename and dares you to type the whole thing manually. The shortcut, of course, is `Tab`.

## The challenge

You're given a zip file and a prompt that essentially says: *download this, unpack it, and run what's inside.* The "attack" in the name is a hint — once unzipped, you'll see why typing the binary's full name by hand would be unbearable.

## Walkthrough

### Step 1 — Pull the archive down

Right-click the linked file in the picoCTF UI, copy the link, and grab it with `wget`:

```bash
wget <paste-link-here>
```

The zip lands in your current working directory.

### Step 2 — Unzip it

```bash
unzip <filename>.zip
```

`unzip` extracts the contents. Run `ls` to see what came out — you'll find an executable with a long, intentionally awkward filename. That's the target.

### Step 3 — Run it with Tab completion

Instead of typing the entire filename, start with the first few characters and let `Tab` finish the rest:

```bash
./<first few chars><Tab>
```

The shell autocompletes the full filename. If you've typed enough to make it unambiguous, `Tab` fills it in instantly; if multiple candidates match what you've typed, press `Tab` twice to see the list and type a couple more characters to narrow it down. Hit Enter and the binary executes, printing the flag in the standard `picoCTF{...}` format.

If you hit a permissions error before it runs, you'll need `chmod +x <filename>` first — same pattern as the [Wave a flag walkthrough](/projects/picoctf-wave-a-flag/).

## Why Tab completion matters beyond convenience

It's tempting to treat Tab completion as "just a shortcut" — and for a beginner CTF, it functionally is. But it's worth being deliberate about *why* this habit matters once you're outside the playground:

- **Typo prevention.** Tab completion guarantees the filename you're acting on actually exists and is spelled correctly. Hand-typed paths are a common source of `command not found`, broken scripts, and the much more dangerous case of executing the *wrong* file with a similar name.
- **Path awareness.** When you type `mybinary<Tab>` and the shell completes it from your current directory but you expected it from `/usr/local/bin`, that's a signal worth catching. Tab completion shows you what the shell would actually run — which is how attackers exploit `$PATH` ordering with planted binaries that get picked up before the real ones (a class of attack tracked as MITRE ATT&CK [T1574.007 — Path Interception by PATH Environment Variable](https://attack.mitre.org/techniques/T1574/007/)).
- **Speed compounds.** Even setting the security framing aside, the speed difference between a competent Tab-completer and a hand-typer is enormous over a day of terminal work. Build the habit at trivial challenges; reap it at every level beyond.

## What this challenge teaches

- **Tab completion is muscle memory.** Build it on easy challenges so it's reflexive in hard ones.
- **Long filenames are a hostile environment.** Whether by accident or by adversarial design, awkward filenames discourage manual interaction. Tab completion makes that interaction cheap enough to actually do.
- **The shell will tell you what it's about to run, if you let it.** Pressing `Tab` is, in a real sense, asking the shell to confirm its interpretation before you commit to it.

Not the most technically demanding challenge in the catalog, but the habit it embeds is real.
