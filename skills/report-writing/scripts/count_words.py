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


FENCE = re.compile(r"\s*(`{3,}|~{3,})")
RULE_ROW = re.compile(r"\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)*\|?\s*$")


def visible_text(markdown):
    # Comments go first, so a fence marker inside a comment cannot hide later text.
    markdown = re.sub(r"<!--.*?-->", " ", markdown, flags=re.S)
    lines, fence = [], None
    for line in markdown.splitlines():
        opener = FENCE.match(line)
        if opener and fence is None:
            fence = opener.group(1)
            continue
        if opener and fence:
            run = opener.group(1)
            closes = run[0] == fence[0] and len(run) >= len(fence)
            if closes and not line[opener.end():].strip(" \t"):
                fence = None
                continue
        if fence or RULE_ROW.match(line) or re.match(r"\s*\[[^\]^][^\]]*\]:\s", line):
            continue
        lines.append(line)
    text = "\n".join(lines)
    text = re.sub(r"!\[[^\]]*\](\([^)]*\)|\[[^\]]*\])", " ", text)
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
