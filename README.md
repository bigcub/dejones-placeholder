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
