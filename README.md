# dejones.io

An atmospheric placeholder for David Jones's personal site.

## Local preview

```sh
python3 -m http.server 5050
```

Then open `http://localhost:5050`.

## Deploy

This site is configured for Firebase Hosting. Once `.firebaserc` contains the Firebase project ID:

```sh
PATH="/opt/homebrew/bin:$PATH" firebase deploy --only hosting
```

## Notes

`notes/index.html` is the index. Each note lives at `notes/<slug>/index.html`.
`notes.css` styles the reading pages; `styles.css` and `script.js` provide the shared identity and theme control.

The current notes are explicitly labelled sample copy and have `noindex` metadata. When publishing real writing, replace the samples, remove the preview notices and `noindex`, and update the matching homepage shelf and index entries. `articles.html` redirects old index and sample-fragment links.
