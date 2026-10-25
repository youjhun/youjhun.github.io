"""Check generated Quartz internal destinations, anchors and image resources."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Document(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.ids = set()
        self.resources = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and "internal" in attrs.get("class", "").split():
            self.resources.append(attrs.get("href", ""))
        if tag in {"img", "video", "audio", "iframe"} and attrs.get("src"):
            self.resources.append(attrs["src"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", default="public")
    root = Path(parser.parse_args().directory).resolve()
    if not root.is_dir():
        parser.error(f"missing build directory: {root}")
    documents = {
        path: Document(path.read_text()) for path in root.rglob("*.html")
    }
    errors = []
    checked = 0
    for path, document in documents.items():
        for resource in document.resources:
            url = urlsplit(resource)
            if url.scheme or url.netloc:
                continue
            url_path = unquote(url.path)
            target = (
                root / url_path.lstrip("/")
                if url_path.startswith("/")
                else path.parent / url_path
            ).resolve()
            candidates = (
                [target, Path(str(target) + ".html"), target / "index.html"]
                if url_path else [path]
            )
            found = next((item for item in candidates if item.is_file()), None)
            checked += 1
            reason = None
            if not target.is_relative_to(root):
                reason = "outside build directory"
            elif found is None:
                reason = "missing path"
            elif url.fragment and found in documents:
                if unquote(url.fragment) not in documents[found].ids:
                    reason = "missing anchor"
            if reason:
                errors.append((str(path.relative_to(root)), resource, reason))
    print(f"HTML resources checked: {checked}; errors: {len(errors)}")
    for error in errors:
        print(error)
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
