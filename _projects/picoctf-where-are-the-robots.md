---
group: lab
title: "picoCTF — Where are the robots"
order: 104
year: 2026
kind: CTF
status: Solved
role: Author
stack:
  - HTTP
  - robots.txt
  - Web reconnaissance
summary: A Web Exploitation challenge built around a critical misconception — that listing a path in robots.txt makes it private.
event: picoCTF 2026
category: Web Exploitation
points: 100
---

> **Spoiler note:** This is a full walkthrough. If you want to attempt the challenge first, head to [picoCTF](https://picoctf.org) and come back.

This is the second Web Exploitation challenge in the series, and a particularly satisfying one — because it teaches a lesson about a real, recurring failure mode in production web applications. The challenge isn't about exploiting a *bug* in `robots.txt`. It's about understanding what `robots.txt` is for and, more importantly, what it is *not* for.

## What `robots.txt` actually is

`robots.txt` is a plain text file served at the root of a web domain (e.g. `example.com/robots.txt`) that tells well-behaved web crawlers — Googlebot, Bingbot, and so on — which paths they should and shouldn't index. It's a *cooperative* protocol, defined in [RFC 9309](https://datatracker.ietf.org/doc/rfc9309/). A typical file looks like:

```
User-agent: *
Disallow: /admin/
Disallow: /private/
Allow: /
```

Critically, `robots.txt` is **not a security control**. It's a polite request to crawlers. Anyone — human or automated — can read the file, ignore its instructions, and visit every "disallowed" path directly. This challenge weaponizes that misconception.

## The challenge

You're given a URL to a small web application:

```
http://fickle-tempest.picoctf.net:<port>
```

(The hostname and port are unique to your picoCTF session.)

The challenge name (`Where are the robots`) and prompt both point at `robots.txt`. The flag is sitting on a path the site explicitly tells crawlers not to visit.

## Walkthrough

### Step 1 — Read robots.txt

Append `/robots.txt` to the URL:

```
http://fickle-tempest.picoctf.net:<port>/robots.txt
```

The response is a short text file. It includes a `Disallow:` directive listing a path the site doesn't want indexed — something like `/<some-filename>.html`.

### Step 2 — Visit the "disallowed" path directly

`robots.txt` told us where not to look. So look there:

```
http://fickle-tempest.picoctf.net:<port>/<the-disallowed-filename>
```

The page loads and renders the flag in the standard `picoCTF{...}` format. That's the challenge.

The "exploit" is doing exactly what the file told us not to do.

## Why this is more than a parlor trick

The reason `robots.txt` is one of the first things every web reconnaissance tool checks is that real developers, at real companies, *keep making the same mistake* — treating "disallowed in `robots.txt`" as if it means "private." The file becomes, in effect, a public list of paths the site owner *believes* are sensitive.

Some real-world examples worth knowing:

- **Google's own `robots.txt`** at `google.com/robots.txt` is famously long and has been the subject of recon write-ups for years. It still discloses internal-sounding paths that bug bounty hunters routinely investigate.
- **Government sites** have repeatedly exposed sensitive endpoints via `robots.txt`. The most infamous case is [the NSA's `nsa.gov/robots.txt`](https://www.nsa.gov/robots.txt), which throughout the 2010s revealed which paths the agency *didn't* want indexed — an inadvertent index of what they considered interesting.
- **Misconfigured WordPress and admin panels** are still routinely listed as `Disallow:` entries on production sites, often with no real authentication behind them.

The principle is the same one from the [Insp3ct0r](/projects/picoctf-insp3ct0r/) writeup, generalized: **anything publicly served must be assumed publicly readable.** Listing a path in `robots.txt` doesn't hide it — it *advertises* it.

The defensive posture for developers is straightforward and worth internalizing:

1. **Use `robots.txt` for what it's actually for** — telling well-behaved crawlers not to waste their crawl budget on dynamic, duplicate, or low-value pages.
2. **Use real access controls** — authentication, authorization, network policy — for anything that should not be reachable by an attacker who ignores `robots.txt`.
3. **Treat the file itself as public reconnaissance data** — never list paths there that would tip an attacker off to the existence of unauthenticated admin endpoints, backup files, or staging environments.

## Where this fits in real reconnaissance

`robots.txt` is one entry in a longer list of "low-effort, high-yield" recon endpoints every attacker checks early:

- **`/robots.txt`** — what the site doesn't want indexed.
- **`/sitemap.xml`** — what the site *does* want indexed (often an inadvertent inventory of every page).
- **`/.git/config`** — exposed when developers deploy source repositories instead of build artifacts. Disturbingly common.
- **`/.env`** — exposed when application configuration files end up web-served. Frequently contains credentials.
- **`/admin`, `/login`, `/wp-admin`, `/phpmyadmin`** — well-known administrative paths that often lack rate limiting or strong auth.
- **`/api`, `/swagger`, `/openapi.json`** — exposed API documentation that maps out the entire backend surface.

Tools like [`gobuster`](https://github.com/OJ/gobuster), [`ffuf`](https://github.com/ffuf/ffuf), and [`dirsearch`](https://github.com/maurosoria/dirsearch) automate the discovery of these paths at scale. Bug bounty programs and red teams use them constantly. Blue teams should be running them against their own perimeter, and either removing what shouldn't be there or adding actual access controls to what should.

## What this challenge teaches

- **`robots.txt` is a recon source, not a security control.** Read it on every web target; never depend on it to hide anything.
- **"Hidden" paths aren't hidden.** Any path the server will respond to is reachable, regardless of whether it appears in the site's navigation.
- **Cooperative protocols don't bind adversaries.** A standard that says "please don't" only works on parties who choose to comply.
- **Real defense lives at the server, not in markup.** If a path matters, authenticate it. If it doesn't matter, don't list it.

A challenge that takes thirty seconds to solve and points at a category of mistake that has cost real organizations real money.
