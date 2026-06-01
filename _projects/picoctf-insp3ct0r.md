---
group: lab
title: "picoCTF — Insp3ct0r"
order: 102
year: 2026
kind: CTF
status: Solved
role: Author
stack:
  - HTML
  - CSS
  - JavaScript
summary: A beginner Web Exploitation challenge on browser DevTools, page source inspection, and the surprisingly common practice of leaving secrets in client-side code.
event: picoCTF 2026
category: Web Exploitation
points: 100
---

> **Spoiler note:** This is a full walkthrough. If you want to attempt the challenge first, head to [picoCTF](https://picoctf.org) and come back.

The first Web Exploitation challenge in this series — and a textbook one. The challenge name `Insp3ct0r` is the entire hint: open the browser Inspector and look at the source. The flag is split into three segments, each one hiding in plain sight in a different client-side asset.

This is a beginner challenge, but the lesson generalizes far beyond CTFs. Client-side source code is *not* a hiding place. Anything served to a browser is, by definition, readable by anyone who knows where to look — and that "anyone" includes attackers running automated reconnaissance against real production sites every day.

## The challenge

You're given a URL to a small static-looking webpage:

```
http://fickle-tempest.picoctf.net:<port>
```

(The hostname and port are unique to your picoCTF session.)

The page itself is short and intentionally innocuous. The prompt tells you to find the flag — which is split across the page's HTML, CSS, and JavaScript.

## Walkthrough

### Step 1 — Open DevTools

In any modern browser, press `F12` (or `Ctrl+Shift+I` on Windows / `Cmd+Option+I` on macOS). The DevTools panel opens with the Elements tab selected by default — this shows the live DOM of the page.

For a cleaner full-page view, you can also right-click anywhere on the page and choose **"View Page Source"** (or `Ctrl+U`). That opens the raw HTML as the server actually sent it, without any DOM modifications made by JavaScript. For a static challenge like this, either approach surfaces the same content.

### Step 2 — Find segment 1 in the HTML

Scroll through the HTML in either view. The first segment of the flag is sitting in an HTML comment — something like:

```html
<!-- piece of the flag: picoCTF{tHi5_- ... -->
```

HTML comments are completely invisible in the rendered page but plainly visible in source. Score the first third of the flag.

### Step 3 — Pivot to the linked assets

Near the top of the source, you'll see two references that immediately stand out:

```html
<link rel="stylesheet" type="text/css" href="mycss.css">
<script type="text/javascript" src="myjs.js"></script>
```

These are external assets — separate files the browser fetches alongside the HTML. Each one is just as readable as the HTML itself; you only need to know where to look. Navigate to each in the browser:

```
http://fickle-tempest.picoctf.net:<port>/mycss.css
http://fickle-tempest.picoctf.net:<port>/myjs.js
```

### Step 4 — Find segment 2 in the CSS

Open `mycss.css`. Scroll to the bottom. A CSS comment sits there:

```css
/* Part 2 of flag: <segment> */
```

CSS comments use `/* ... */` syntax, and like HTML comments they're never rendered on the page — they only exist in the source. Second third collected.

### Step 5 — Find segment 3 in the JavaScript

Open `myjs.js`. The third segment is sitting in a JavaScript comment, either `// single-line` or `/* multi-line */` format depending on how the challenge author wrote it.

Concatenate the three segments — in order: HTML, CSS, JavaScript — into the canonical `picoCTF{...}` format. Submit.

## Why this challenge matters

The Insp3ct0r challenge is trivial. The class of mistake it represents is not.

Real-world examples of secrets-in-client-side-code are *abundant*:

- **API keys in JavaScript bundles.** Developers paste a secret into `config.js` for "just testing" and the file ships to production. Automated scrapers like [TruffleHog](https://github.com/trufflesecurity/trufflehog) and [gitleaks](https://github.com/gitleaks/gitleaks) find these constantly — including on real corporate sites, not just CTFs.
- **Hidden admin endpoints.** A comment in HTML reading `<!-- TODO: remove /admin-debug before launch -->` is, in essence, a treasure map for an attacker. Bug bounty reports are full of these.
- **Stack traces and framework versions.** Many frameworks leak their exact version in HTML meta tags, response headers, or commented-out boilerplate. An attacker who knows you're running `<framework> v2.3.1` can immediately search public CVE databases for known exploits.
- **Source maps in production.** Modern build tools often emit `.map` files that reverse-engineer minified JavaScript back to readable code, complete with comments and developer notes. Production deploys regularly ship them by accident.

The defensive principle is straightforward: **anything served to a browser must be assumed public.** Authentication, authorization, and secrets all belong on the server, never in client-side code. This is a recurring failure mode in real cloud and web applications, and it's the reason "view source" is still a meaningful reconnaissance step in 2026.

## What this challenge teaches

- **DevTools is the lowest-friction recon tool there is.** Open it on every web challenge before doing anything else.
- **HTML, CSS, and JavaScript comments are all visible.** Different syntax (`<!-- -->`, `/* */`, `//`) but identical visibility.
- **Linked assets are first-class targets.** Anything referenced by `href`, `src`, or `link` is just another URL you can visit directly.
- **Client-side is public-side.** A useful slogan to make permanent. If you're holding it in JavaScript, an attacker can read it. Treat the browser as hostile.

The challenge takes two minutes. The mental model it builds — *check the source, then check what the source points to, then check what those things point to* — is the foundation of everything in Web Exploitation that comes after.
