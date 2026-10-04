#!/usr/bin/env python3
"""Keeps the site's search and sharing metadata in step with its pages.

Run from the repository root after adding a note or changing a page's title
or description:

    python3 tools/update-meta.py

It reads each page's own <title>, description, heading and notes-list entry,
and writes:

- a block of canonical, Open Graph, Twitter and JSON-LD tags before </head>,
  between <!-- meta --> and <!-- /meta -->;
- microformats (h-card, h-entry, h-feed) in the existing markup;
- sitemap.xml, robots.txt and feed.xml.

Publication dates come from git the first time a page is seen, and are then
kept in the page's block. The modified date only moves when the page's main
content changes, so rerunning the script never makes every page look new.
Run tools/render-social.sh as well when a page's shared image should change.
"""

import hashlib
import html
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

SITE = "https://dejones.io"
NAME = "David Jones"
TAGLINE = "Product Thinking, Product Practice"
LINKEDIN = "https://www.linkedin.com/in/dejones/"
PERSON = f"{SITE}/#person"
WEBSITE = f"{SITE}/#website"
BLOG = f"{SITE}/notes/#blog"
ROOT = Path(__file__).resolve().parent.parent

# Pages that are live but kept out of search for now.
HIDDEN = {"projects", "example"}


def git_date(path, first):
    args = ["git", "log", "--format=%aI", "--", str(path)]
    if first:
        args[2:2] = ["--follow", "--diff-filter=A"]
    out = subprocess.run(args, cwd=ROOT, capture_output=True, text=True).stdout.split()
    return (out[-1] if first else out[0]) if out else None


def iso(value):
    return datetime.fromisoformat(value).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def text(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def notes_list():
    """The notes in the order the notes page lists them, with their labels."""
    index = (ROOT / "notes/index.html").read_text()
    notes = []
    for href, category, title, summary in re.findall(
        r'href="/([^"/]+)/"><span class="note-number">\d+</span><div><span class="note-category">([^<]*)</span>'
        r'<h2[^>]*>(.*?)</h2><p[^>]*>(.*?)</p>', index):
        section, _, status = category.partition(" · ")
        notes.append({"slug": href, "section": section, "status": status, "title": text(title), "summary": text(summary)})
    return notes


def pages():
    found = [{"slug": "", "kind": "home"}, {"slug": "notes", "kind": "notes"}, {"slug": "about", "kind": "about"},
             {"slug": "projects", "kind": "projects"}, {"slug": "example", "kind": "note"}]
    found += [dict(note, kind="note") for note in notes_list()]
    for page in found:
        page["path"] = ROOT / (f"{page['slug']}/index.html" if page["slug"] else "index.html")
        page["url"] = f"{SITE}/{page['slug']}/" if page["slug"] else f"{SITE}/"
        page["indexed"] = page["slug"] not in HIDDEN
    return found


def person():
    return {
        "@type": "Person", "@id": PERSON, "name": NAME, "url": f"{SITE}/",
        "description": "Designs and builds software products for the gaming industry.",
        "homeLocation": {"@type": "Place", "name": "Manchester, United Kingdom"},
        "sameAs": [LINKEDIN],
    }


def breadcrumbs(page, title):
    trail = [("Home", f"{SITE}/")]
    if page["kind"] == "note":
        trail.append(("Notes", f"{SITE}/notes/"))
    if page["kind"] != "home":
        trail.append((title, page["url"]))
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": n, "name": name, "item": url} for n, (name, url) in enumerate(trail, 1)]}


def graph(page, title, description, image, published, modified, all_notes):
    nodes = [person()]
    if page["kind"] == "home":
        nodes.append({"@type": "WebSite", "@id": WEBSITE, "url": f"{SITE}/", "name": NAME, "description": TAGLINE,
                      "inLanguage": "en-GB", "publisher": {"@id": PERSON}})
        nodes.append({"@type": "WebPage", "@id": f"{SITE}/#webpage", "url": f"{SITE}/", "name": title,
                      "description": description, "isPartOf": {"@id": WEBSITE}, "about": {"@id": PERSON},
                      "primaryImageOfPage": image, "inLanguage": "en-GB"})
        return nodes
    if page["kind"] == "note":
        article = {"@type": "BlogPosting", "@id": f"{page['url']}#article", "headline": title, "description": description,
                   "url": page["url"], "mainEntityOfPage": page["url"], "image": image,
                   "datePublished": published, "dateModified": modified, "author": {"@id": PERSON},
                   "publisher": {"@id": PERSON}, "isPartOf": {"@id": BLOG}, "inLanguage": "en-GB"}
        if page.get("section"):
            article["articleSection"] = page["section"]
        if page.get("status"):
            article["creativeWorkStatus"] = page["status"]
        nodes.insert(0, article)
    elif page["kind"] == "notes":
        nodes.insert(0, {"@type": "Blog", "@id": BLOG, "url": page["url"], "name": title, "description": description,
                         "author": {"@id": PERSON}, "publisher": {"@id": PERSON}, "inLanguage": "en-GB", "image": image,
                         "blogPost": [{"@type": "BlogPosting", "@id": f"{n['url']}#article", "headline": n["title"],
                                       "url": n["url"], "datePublished": n["published"]} for n in all_notes]})
    elif page["kind"] == "about":
        nodes.insert(0, {"@type": "ProfilePage", "url": page["url"], "name": title, "description": description,
                         "mainEntity": {"@id": PERSON}, "dateModified": modified, "inLanguage": "en-GB"})
    else:
        nodes.insert(0, {"@type": "CollectionPage", "url": page["url"], "name": title, "description": description,
                         "author": {"@id": PERSON}, "inLanguage": "en-GB"})
    nodes.append(breadcrumbs(page, title))
    return nodes


def main_content(source):
    body = re.sub(r"<!-- meta -->.*?<!-- /meta -->", "", source, flags=re.S)
    body = re.sub(r'<p class="note-entry" hidden>.*?</p>', "", body, flags=re.S)
    match = re.search(r"<main.*?</main>", body, re.S)
    # The words alone, so that markup the script adds never counts as a change.
    words = " ".join(text(match.group(0) if match else body).split())
    return hashlib.sha1(words.encode()).hexdigest()[:12]


def stored(source, key):
    match = re.search(rf"<!-- {key}: ([^ ]+) -->", source)
    return match.group(1) if match else None


def microformats(page, source, published, modified):
    # The header's identity link is a representative h-card on every page.
    source = re.sub(r'<a class="identity"', '<a class="identity h-card"', source)
    source = source.replace("<strong>David Jones</strong>", '<strong class="p-name">David Jones</strong>')
    source = re.sub(r"<small>(Product Thinking, Product Practice · Manchester, UK)</small>", r'<small class="p-note">\1</small>', source)
    source = re.sub(r'(href="https://www\.linkedin\.com/in/dejones/"\s+target="_blank"\s+rel=")noopener(")', r"\1noopener me\2", source)
    source = re.sub(r'<html lang="en">', '<html lang="en-GB">', source)
    if page["kind"] == "note":
        source = re.sub(r"<article>", '<article class="h-entry">', source, count=1)
        source = re.sub(r'(<header class="note-title">.*?)<h1>', r'\1<h1 class="p-name">', source, count=1, flags=re.S)
        source = source.replace('<div class="note-prose">', '<div class="note-prose e-content">', 1)
        entry = (f'<p class="note-entry" hidden><a class="u-url" href="{page["url"]}">{page["url"]}</a> '
                 f'<time class="dt-published" datetime="{published}">{published[:10]}</time> '
                 f'<time class="dt-updated" datetime="{modified}">{modified[:10]}</time> '
                 f'<a class="p-author h-card" href="{SITE}/">{NAME}</a></p>')
        source = re.sub(r'\n      <p class="note-entry" hidden>.*?</p>', "", source, flags=re.S)
        source = re.sub(r'(<header class="note-title">)', rf"\1\n      {entry}", source, count=1)
    if page["kind"] == "notes":
        source = source.replace('<main class="notes-index" id="content">', '<main class="notes-index h-feed" id="content">', 1)
        source = source.replace('<li><a class="note-index-link" href=', '<li class="h-entry"><a class="note-index-link u-url" href=')
        source = re.sub(r'(class="note-index-link u-url"[^>]*>.*?)<h2>(.*?)</h2><p>', r'\1<h2 class="p-name">\2</h2><p class="p-summary">', source)
    return source


def update_page(page, all_notes):
    source = page["path"].read_text()
    # A new note starts as a copy of another, so its stored dates are only
    # trusted when the block was written for this page.
    if f'<link rel="canonical" href="{page["url"]}">' not in source:
        source = re.sub(r"<!-- (published|modified|content): [^ ]+ -->\n?", "", source)
    title = text(re.search(r"<title>(.*?)</title>", source, re.S).group(1))
    if page["kind"] != "home":
        title = title.removesuffix(f" — {NAME}")
    description = html.unescape(re.search(r'<meta\s+name="description"\s+content="([^"]*)"', source).group(1))
    content = main_content(source)
    now = datetime.now(timezone.utc).isoformat()
    # A note may first have lived at notes/<slug>/, before notes moved to the root.
    first_seen = [git_date(page["path"], True)]
    if page["kind"] == "note":
        first_seen.append(git_date(ROOT / "notes" / page["slug"] / "index.html", True))
    first_seen = [datetime.fromisoformat(d) for d in first_seen if d]
    published = stored(source, "published") or iso((min(first_seen) if first_seen else datetime.now(timezone.utc)).isoformat())
    previous = stored(source, "content")
    if previous == content:
        modified = stored(source, "modified")
    elif previous is None:
        modified = iso(git_date(page["path"], False) or now)
    else:
        modified = iso(now)
    page.update(published=published, modified=modified, title=title, description=description)

    image_name = "home" if page["kind"] == "home" else page["slug"]
    image_url = f"{SITE}/og/{image_name}.jpg"
    image_alt = f"{title}, by {NAME}" if page["kind"] != "home" else f"{NAME}: a roulette table beneath a chandelier in a Mayfair gaming room"
    image = {"@type": "ImageObject", "url": image_url, "width": 1200, "height": 630}
    og_type = "article" if page["kind"] == "note" else ("profile" if page["kind"] == "about" else "website")

    tags = [
        f"<!-- published: {published} -->", f"<!-- modified: {modified} -->", f"<!-- content: {content} -->",
        f'<link rel="canonical" href="{page["url"]}">',
        '<meta name="robots" content="index, follow, max-image-preview:large">' if page["indexed"] else '<meta name="robots" content="noindex">',
        f'<meta name="author" content="{NAME}">',
        f'<link rel="alternate" type="application/atom+xml" title="Notes by {NAME}" href="/feed.xml">',
        '<link rel="apple-touch-icon" href="/apple-touch-icon.png">',
        f'<meta property="og:site_name" content="{NAME}">',
        '<meta property="og:locale" content="en_GB">',
        f'<meta property="og:type" content="{og_type}">',
        f'<meta property="og:title" content="{html.escape(title)}">',
        f'<meta property="og:description" content="{html.escape(description)}">',
        f'<meta property="og:url" content="{page["url"]}">',
        f'<meta property="og:image" content="{image_url}">',
        '<meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{html.escape(image_alt)}">',
    ]
    if og_type == "article":
        tags += [f'<meta property="article:published_time" content="{published}">',
                 f'<meta property="article:modified_time" content="{modified}">',
                 f'<meta property="article:author" content="{SITE}/about/">']
        if page.get("section"):
            tags.append(f'<meta property="article:section" content="{html.escape(page["section"])}">')
    if og_type == "profile":
        tags += ['<meta property="profile:first_name" content="David">', '<meta property="profile:last_name" content="Jones">']
    tags += [
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{html.escape(title)}">',
        f'<meta name="twitter:description" content="{html.escape(description)}">',
        f'<meta name="twitter:image" content="{image_url}">',
        f'<meta name="twitter:image:alt" content="{html.escape(image_alt)}">',
        '<script type="application/ld+json">' + json.dumps(
            {"@context": "https://schema.org", "@graph": graph(page, title, description, image, published, modified, all_notes)},
            ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>",
    ]
    block = "<!-- meta -->\n" + "\n".join(tags) + "\n<!-- /meta -->\n"

    # Earlier hand-written tags give way to the block.
    source = re.sub(r"\n?<!-- meta -->.*?<!-- /meta -->\n?", "\n", source, flags=re.S)
    source = re.sub(r'\s*<meta\s+property="og:[^"]+"\s+content="[^"]*"\s*/?>', "", source)
    source = re.sub(r'<meta name="robots" content="noindex">', "", source)
    source = microformats(page, source, published, modified)
    source = re.sub(r"\n?\s*</head>", "\n" + block + "</head>", source, count=1)
    page["path"].write_text(source)


def write_sitemap(all_pages):
    urls = "".join(f"  <url><loc>{p['url']}</loc><lastmod>{p['modified'][:10]}</lastmod></url>\n" for p in all_pages if p["indexed"])
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /tools/\n\nSitemap: {SITE}/sitemap.xml\n")


def write_feed(notes):
    entries = "".join(
        f"""  <entry>
    <title>{html.escape(n['title'])}</title>
    <link href="{n['url']}"/>
    <id>{n['url']}</id>
    <published>{n['published']}</published>
    <updated>{n['modified']}</updated>
    <summary>{html.escape(n['description'])}</summary>
    {f'<category term="{html.escape(n["section"])}"/>' if n.get('section') else ''}
  </entry>
""" for n in notes)
    updated = max(n["modified"] for n in notes)
    (ROOT / "feed.xml").write_text(f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en-GB">
  <title>Notes by {NAME}</title>
  <subtitle>{TAGLINE}</subtitle>
  <link href="{SITE}/feed.xml" rel="self"/>
  <link href="{SITE}/notes/"/>
  <id>{SITE}/notes/</id>
  <updated>{updated}</updated>
  <author><name>{NAME}</name><uri>{SITE}/</uri></author>
  <icon>{SITE}/favicon.svg</icon>
{entries}</feed>
""")


def main():
    all_pages = pages()
    notes = [p for p in all_pages if p["kind"] == "note" and p["indexed"]]
    # Notes first, so the notes page can list them with their dates.
    for page in sorted(all_pages, key=lambda p: p["kind"] != "note"):
        update_page(page, notes)
    write_sitemap(all_pages)
    write_feed(notes)
    for page in all_pages:
        print(f"{'indexed' if page['indexed'] else 'hidden ':8} {page['published'][:10]} {page['modified'][:10]}  {page['url']}")


if __name__ == "__main__":
    main()
