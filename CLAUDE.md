# Project context

This repository contains the temporary landing page for `dejones.io`, David
Jones's personal site. It is intentionally a small, atmospheric, dependency-free
static site rather than a framework application.

## What is here

- `index.html` contains the page structure and the inline SVG landscape.
- `styles.css` contains the complete visual system, responsive layout, light and
  dark themes, and scene animations.
- `script.js` handles the saved colour theme and subtle pointer parallax.
- `notes/index.html` lists the notes. Each note lives off the root at
  `<slug>/index.html`, so its address is `dejones.io/<slug>/`. The old
  `notes/<slug>/` paths are redirects to those addresses. `notes.css` styles
  these reading pages.
- `projects/index.html` lists David's tools and experiments. It uses the
  notes index's page shell and list styles, with each project's domain as its
  label. A project without an address yet is listed without a link. The page
  is live, but its header link is hidden on every page until David has a
  stronger portfolio; add `<a href="/projects/">Projects</a>` back between
  Notes and About when he asks.
- `about/index.html` is the About page, in the note layout, with a drawing of a
  window sill holding a candle and a potted plant, between two small wall
  shelves of books that carry the drawing towards the margins. It is a focused
  still life with no location, deliberately not a scene or an element borrowed
  from one.
  The light follows the theme: the sun is in the window by day, and at night
  the moon is out and the candle is lit. The text is David's own; limit edits to
  grammar and cohesion.
- `favicon.svg` is the site icon.
- `firebase.json` configures Firebase Hosting. The root-relative static assets
  also work when the repository is served by GitHub Pages.

There is no build step, package manager, or automated test suite. `tools/`
holds two small scripts that regenerate search and sharing metadata; the
site itself runs without them.

## Product and design intent

Preserve the quiet, editorial feel: warm natural colours, restrained typography,
and a hand-illustrated landscape. The page should stay lightweight and should not
gain a frontend framework without a clear reason.

When changing the scene, keep both themes coherent. Treat accessibility and
reduced motion as requirements: retain semantic labels, keyboard focus styles,
and the `prefers-reduced-motion` behaviour. Check narrow mobile layouts as well as
desktop layouts.

Keep the scenes light to run, especially on phones. Only the scene on show
animates: a rule in `styles.css` pauses every animation in the hidden scenes.
Avoid `feGaussianBlur` and CSS `filter` on anything that moves, or that sits
under something that moves, because the blur is then recomputed every frame.
Draw soft glows, mists and hazes as shapes filled with a feathered radial
gradient instead, and let a slow drift over a blurred shape use `steps()`
timing so that it repaints a few times a second rather than every frame.

For now the reduced-motion rules are turned off at David's request, so the
animations play on his phone, which has reduced motion switched on. Each one is
commented out and marked `REDUCED-MOTION-OFF` in `styles.css` and `script.js`.
Leave them off until he asks for them back, but still write reduced-motion rules
for new animation and comment them out with the same marker.

## Header

Every page shares one header. Places (Notes and About; Projects is hidden for
now) are text links in
`.site-nav`, with `aria-current` marking the current section; a note marks Notes.
The round buttons are kept for LinkedIn and the scene and theme controls, so add
new sections as words rather than more circles. On phones the section links take
the tagline's place beneath the name.

## Notes and articles

The notes index and every note share one page shell: the site header, the
decorative landscape band (`.notes-landscape`), a centred 720px column, and the
footer. A note's prose sits inside that column at about 65 characters a line.
Keep the index and the notes identical in these respects, so that moving between
them does not shift the layout. There is no templating, so a new note starts as a
copy of an existing note page, and is then added to the list in
`notes/index.html`, to the slug list in `articles.html`, and, if it should be
featured, to the shelf on the homepage. Then refresh its search and sharing
metadata and its shared image, as described under Search and sharing.

A note that is published but still being refined carries a `note-draft` tag above
its title, and "· Draft" after its category in the notes list and on the
homepage shelf. Remove all three when the note is final.

A note with no content yet, whose notes are still being gathered, carries the
same tag reading "Collating", and "· Collating" in the same two places. Change
all three to Draft once writing starts.

`example/` is an unlisted reference note with sample text. It shows the
reading layout at full length and the inline-drawing pattern below. Leave it
out of the notes list, and keep invented text out of David's real notes.

### Drawings in a note

A note can borrow an element from a scene to carry a point, as the example's
moored boat does. Use a `<figure class="note-figure">` holding an inline SVG,
with a short `figcaption` that states the point. Give the SVG `role="img"` and an
`aria-label` that describes the picture. Reuse the scene's own class names
(`boat`, `buoy`, and so on) and colour variables, so that the drawing follows the
theme and inherits the scene's animation. Then:

- Wrap anything that animates in an outer group that positions it. A CSS
  animation replaces an element's `transform` attribute, so the drawing would
  jump to the scene's coordinates.
- Scene colours were chosen to stand against a sky, not against the paper. Check
  pale fills, such as sails, against the light paper, and dark ones against the
  dark paper. Outline pale shapes faintly. Draw lines such as ropes in
  `--reading-muted`, which reads in both themes.
- Fade the edges into the page with a mask rather than drawing a box.
- Check both themes, a phone width, and reduced motion.

## Search and sharing

Every page carries a generated block between `<!-- meta -->` and
`<!-- /meta -->` before `</head>`: the canonical address, robots, Open Graph
and Twitter tags, and JSON-LD (Person and WebSite on the homepage, BlogPosting
on notes, Blog on the notes page, ProfilePage on About, with breadcrumbs). The
header is an h-card, each note an h-entry, and the notes page an h-feed.
`sitemap.xml`, `robots.txt` and the Atom feed `feed.xml` are generated too.
Don't edit any of these by hand. After adding a note or changing a page's
title or description, run both, with the local server running:

```sh
python3 tools/update-meta.py
./tools/render-social.sh
```

The first rewrites the tags, sitemap and feed from the pages themselves. It
keeps each page's published and modified dates in its block, and moves the
modified date only when the page's words change. The second renders the
1200 × 630 shared images into `og/` from `tools/social-card.html`, which takes
a page's title, description and first drawing, and the homepage's from the
landscape itself; it also renders `apple-touch-icon.png`.

Projects and the example note are live but kept out of search (`HIDDEN` in
the script); the 404 page and the old `notes/<slug>/` redirects carry their own
noindex.

## Analytics

Google Analytics (GA4, `G-NBVH23JQKN`) is included in the `<head>` of the
homepage and every note page. The snippet loads the tag only when the page is
served from `dejones.io`, so local development never reaches the reports. A new
page that copies an existing note keeps the snippet; a page written from
scratch needs it added.

## Working locally

Run a static server from the repository root:

```sh
python3 -m http.server 5050
```

Then open `http://localhost:5050`. Before handing off a visual change, check:

- light and dark themes;
- desktop and mobile viewport widths;
- the theme preference after a reload;
- the browser console for errors; and
- the reduced-motion experience when animation code changes.

## Deployment

The live site is served by GitHub Pages, so publishing means committing and
pushing to GitHub. Firebase Hosting is configured to publish the repository root. Once
`.firebaserc` contains the intended Firebase project ID, deploy with:

```sh
PATH="/opt/homebrew/bin:$PATH" firebase deploy --only hosting
```

Stylesheets and the script are linked with a version query (`styles.css?v=9`,
`notes.css?v=3`, `script.js?v=3`). Bump it on every page when a change to the CSS or script must reach
visitors together with new HTML, so a cached file cannot break the page.

Do not commit Firebase caches, debug logs, or local machine files. Do not put
secrets or environment-specific project IDs in this document.
