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

`notes/index.html` is the index. Each note lives off the root at `<slug>/index.html`, so it is served at `dejones.io/<slug>/`.
`notes.css` styles the reading pages; `styles.css` and `script.js` provide the shared identity and theme control.

"Practical product strategy" is published as a draft, marked with a `note-draft` tag. The other two notes are titled placeholders whose bodies read "Currently drafting." The notes keep `noindex` metadata until the writing is settled; remove it when a note is final, and update the matching homepage shelf and index entries. `articles.html` redirects old index and note-fragment links, so its slug list must track the note directories. Notes used to live at `notes/<slug>/`; those paths now hold small redirects to the new addresses.
