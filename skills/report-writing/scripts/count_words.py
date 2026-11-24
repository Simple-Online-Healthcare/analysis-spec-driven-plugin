#!/usr/bin/env python3
"""Count the words a reader sees in a markdown report. Every checker uses this one method.

Counted: headings, body text, table cells, captions, footnotes and visible link labels.
Not counted: markdown symbols, link and image targets, reference-link definitions, image
alt text, HTML tags and comments, fenced code blocks and table rule rows. Text drawn
inside a chart image is not in the file, so it is not counted; report-checker checks that
charts carry no paragraphs.

Usage: python3 count_words.py <report.md> [<more.md> ...]
"""

import re
import sys


def visible_text(markdown):
    lines, fence = [], None
    for line in markdown.splitlines():
        opener = re.match(r"\s*(`{3,}|~{3,})", line)
        if opener:
            run = opener.group(1)
            if fence is None:
                fence = run
                continue
            if run[0] == fence[0] and len(run) >= len(fence):
                fence = None
                continue
        if fence or re.match(r"\s*\|?(\s*:?-{3,}:?\s*\|?)+\s*$", line) \
                or re.match(r"\s*\[[^\]^][^\]]*\]:\s", line):
            continue
        lines.append(line)
    text = "\n".join(lines)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\](\([^)]*\)|\[[^\]]*\])", r"\1", text)
    text = re.sub(r"<[A-Za-z/!][^>]*>", " ", text)
    return text.replace("|", " ")


def count_words(markdown):
    return sum(1 for token in visible_text(markdown).split() if re.search(r"[^\W_]", token))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for path in sys.argv[1:]:
        with open(path, encoding="utf-8") as handle:
            print(f"{count_words(handle.read())} words: {path}")
