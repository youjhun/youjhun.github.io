"""[[이름]] 링크가 리디렉트 페이지나 엉뚱한 글로 빠질 수 있는 경우를 검사한다.

Quartz는 markdownLinkResolution: "shortest"로 [[이름]] 링크를 찾는다. 이름이 가리킬 수 있는 페이지가
둘 이상이면 링크가 루트의 같은 이름 페이지로 떨어진다. 그래서 다음을 막는다.
- 별칭의 마지막 부분이 어떤 글의 파일 이름과 같다 (대소문자만 다른 것, 'concepts/dtft' 같은 경로 꼴 포함)
- index가 아닌 글 두 개가 같은 파일 이름을 쓴다
- 서로 다른 글 두 개가 같은 별칭을 쓴다
사용: python3 scripts/check_aliases.py [content 폴더]
"""

import re
import sys
from collections import defaultdict
from pathlib import Path


def aliases(text):
    """front matter의 aliases를 읽는다. [a, b] 꼴과 '- a' 줄 목록 꼴을 둘 다 받는다."""
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    if not m:
        return []
    lines = m.group(1).splitlines()
    for i, line in enumerate(lines):
        key = re.match(r"aliases:\s*(.*)$", line)
        if not key:
            continue
        rest = key.group(1).strip()
        if rest.startswith("["):
            items = rest.strip("[]").split(",")
        elif rest:
            items = [rest]
        else:
            items = []
            for nxt in lines[i + 1:]:
                item = re.match(r"\s*-\s+(.*)$", nxt)
                if not item:
                    break
                items.append(item.group(1))
        return [a.strip().strip("'\"") for a in items if a.strip()]
    return []


def last_part(name):
    return re.sub(r"\s+", "-", name.rstrip("/").split("/")[-1]).lower()


root = Path(sys.argv[1] if len(sys.argv) > 1 else "content")
files = [p for p in root.rglob("*.md") if "templates" not in p.parts]
by_name = defaultdict(list)
for p in files:
    if p.stem != "index":
        by_name[p.stem.lower()].append(p)

bad = 0
for name, paths in sorted(by_name.items()):
    if len(paths) > 1:
        print(f"file name '{name}' is used by {len(paths)} files: " + ", ".join(map(str, paths)))
        bad += 1
by_alias = defaultdict(list)
for p in files:
    for alias in aliases(p.read_text(encoding="utf-8")):
        hit = by_name.get(last_part(alias))
        if hit:
            print(f"{p}: alias '{alias}' collides with {hit[0]}")
            bad += 1
        by_alias[last_part(alias)].append(p)
for alias, paths in sorted(by_alias.items()):
    if len(set(paths)) > 1:
        print(f"alias '{alias}' is used by {len(set(paths))} files: " + ", ".join(map(str, sorted(set(paths)))))
        bad += 1
print("aliases ok" if not bad else f"{bad} problem(s)")
sys.exit(1 if bad else 0)
