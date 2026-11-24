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
DEFINITION = re.compile(r"\s*\[([^\]^][^\]]*)\]:(?:\s+(.*))?$")
DESTINATION = re.compile(r"""\s*(<[^>]*>|[^\s"'(]\S*)(\s+("[^"]*"|'[^']*'|\([^)]*\)))?\s*$""")
TITLE = re.compile(r"""\s*("[^"]*"|'[^']*'|\([^)]*\))\s*$""")


def label(name):
    return " ".join(name.lower().split())


def visible_text(markdown):
    # One pass: comment markers inside fenced code stay literal, and fence markers inside
    # a comment cannot open a code block.
    lines, definitions, fence, comment = [], set(), None, False
    tail = None  # a definition's destination or title may continue on the next line
    for line in markdown.splitlines():
        if fence:
            closer = FENCE.match(line)
            if closer and closer.group(1)[0] == fence[0] and len(closer.group(1)) >= len(fence) \
                    and not line[closer.end():].strip(" \t"):
                fence = None
            continue
        if comment:
            if "-->" not in line:
                continue
            line, comment = line.split("-->", 1)[1], False
        line = re.sub(r"<!--.*?-->", " ", line)
        if "<!--" in line:
            line, comment = line.split("<!--", 1)[0], True
        if tail == "destination" and DESTINATION.match(line):
            tail = "title" if DESTINATION.match(line).group(2) is None else None
            continue
        if tail == "title" and TITLE.match(line):
            tail = None
            continue
        tail = None
        opener = FENCE.match(line)
        if opener:
            fence = opener.group(1)
            continue
        definition = DEFINITION.match(line)
        if definition:
            definitions.add(label(definition.group(1)))
            tail = "title" if (definition.group(2) or "").strip() else "destination"
            continue
        if not RULE_ROW.match(line):
            lines.append(line)
    text = "\n".join(lines)
    text = re.sub(r"!\[[^\]]*\](\([^)]*\)|\[[^\]]*\])", " ", text)
    text = re.sub(r"!\[([^\]]*)\](?![(\[])",
                  lambda image: " " if label(image.group(1)) in definitions else image.group(0),
                  text)
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
