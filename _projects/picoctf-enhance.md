---
title: "picoCTF — Enhance!"
order: 111
year: 2026
kind: CTF
status: Solved
role: Author
stack:
  - SVG
  - XML
  - Digital forensics

summary: A forensics-flavored challenge that hinges on a single fact — an SVG image is not a picture, it's human-readable XML markup, and the flag is sitting in its text elements.

event: picoCTF 2026
category: General Skills
points: 100

group: lab
---

> **Spoiler note:** This is a full walkthrough. If you want to attempt the challenge first, head to [picoCTF](https://picoctf.org) and come back.

A short challenge with a satisfying "oh, of course" at the center. You're handed an image and told the flag is in it. The trick is recognizing *what kind* of image it is — because an **SVG** isn't a grid of pixels like a JPEG or PNG. It's a text file. Specifically, it's XML markup describing shapes and text, which means you can read it as source instead of viewing it as a picture.

The name "Enhance!" is the joke — the old TV-detective trope of zooming infinitely into a blurry image to reveal a clue. Here you don't enhance anything. You read the source.

## The challenge

You're given an image file (an SVG) and told the flag is hidden within it. Viewing the image normally shows... an image. The flag isn't visible in the rendered picture.

## Walkthrough

### Step 1 — Open the image and view its source

Open the SVG in a new browser tab, then view the page source (`Ctrl+U`, or right-click → "View Page Source"). Because an SVG is XML, the browser will show you readable markup rather than binary gibberish.

### Step 2 — Read the text elements

Scroll through the markup toward the end. SVG renders text using `<text>` and `<tspan>` elements. Each `<tspan>` holds a chunk of text — and in this challenge, the flag is split across a series of them.

You'll notice that after each `id=tspan...` element there's a fragment of the flag. Read them in order — the first fragments spell out the familiar `picoCTF` prefix, confirming you're on the right track — and the remaining `<tspan>` contents complete the flag.

### Step 3 — Assemble the flag

Concatenate the text fragments from the `<tspan>` elements in order. That's the full flag, in standard `picoCTF{...}` format.

## Why this works — raster vs. vector

The entire challenge rests on a distinction worth knowing cold:

- **Raster images** (JPEG, PNG, GIF, BMP) store an image as a grid of pixels — a binary blob of color values. Open one in a text editor and you get unreadable binary. To hide text in a raster image you'd need steganography (encoding data in pixel values), which is a genuinely different and harder technique.
- **Vector images** (SVG) store an image as *instructions* — "draw a line here, fill this shape, place this text there" — written in XML, a plain-text markup language. Open an SVG in a text editor or "view source" and you can read every element, including any text it contains.

So the flag was never hidden in any meaningful sense. It was sitting in plain text inside a plain-text file. The only "trick" is recognizing that an `.svg` is a document you read, not just a picture you look at.

This connects directly to the lesson from the [Insp3ct0r](/projects/picoctf-insp3ct0r/) writeup: **client-visible content is readable content.** There, it was HTML/CSS/JS comments. Here, it's text elements in an XML-based image. Same principle, different file format.

## Where this matters beyond the challenge

- **SVGs are an underappreciated data-leak vector.** Because they're text, SVGs can carry comments, metadata, embedded scripts, and editor artifacts that designers never intended to ship. A logo exported from design software can contain layer names, file paths, or notes in its markup. Worth inspecting SVGs during any web assessment.
- **SVGs can carry executable script.** Unlike raster formats, SVG supports `<script>` elements, which makes them a real XSS and phishing vector when sites accept SVG uploads and serve them inline. The same "it's actually a document" property that makes this challenge trivial also makes SVG a security concern in upload-handling code.
- **File type is about format, not extension.** The real skill here is asking "what is this file actually made of?" rather than trusting the icon. A `.svg` is XML; a `.docx` is a zip archive of XML; a `.pdf` is a structured text format. Knowing what's *underneath* a file type tells you how to inspect it.

## What this challenge teaches

- **SVG is text, not pixels.** It's XML markup you can read directly. This single fact is the whole solution.
- **View source works on more than web pages.** Any text-based format — SVG, XML, JSON, HTML — is readable at the source level.
- **Raster vs. vector is a fundamental distinction.** One is a pixel grid (binary); the other is drawing instructions (text). They hide data in completely different ways.
- **Ask what a file is actually made of.** The extension is a hint, not the truth. Knowing the underlying format tells you how to inspect it.

A thirty-second solve that quietly teaches a real distinction about how images — and files in general — actually work.
