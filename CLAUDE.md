# Project context

This repository contains the temporary landing page for `dejones.io`, David
Jones's personal site. It is intentionally a small, atmospheric, dependency-free
static site rather than a framework application.

## What is here

- `index.html` contains the page structure and the inline SVG landscape.
- `styles.css` contains the complete visual system, responsive layout, light and
  dark themes, and scene animations.
- `script.js` handles the saved colour theme and subtle pointer parallax.
- `favicon.svg` is the site icon.
- `firebase.json` configures Firebase Hosting. The root-relative static assets
  also work when the repository is served by GitHub Pages.

There is no build step, package manager, or automated test suite.

## Product and design intent

Preserve the quiet, editorial feel: warm natural colours, restrained typography,
and a hand-illustrated landscape. The page should stay lightweight and should not
gain a frontend framework without a clear reason.

When changing the scene, keep both themes coherent. Treat accessibility and
reduced motion as requirements: retain semantic labels, keyboard focus styles,
and the `prefers-reduced-motion` behaviour. Check narrow mobile layouts as well as
desktop layouts.

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

Firebase Hosting is configured to publish the repository root. Once
`.firebaserc` contains the intended Firebase project ID, deploy with:

```sh
PATH="/opt/homebrew/bin:$PATH" firebase deploy --only hosting
```

Do not commit Firebase caches, debug logs, or local machine files. Do not put
secrets or environment-specific project IDs in this document.
