# Report template

A flexible structure, not a requirement to fill every section. It follows the structure of
the team's published studies, with a visual slot for each stage.

## Suggested page

```
# [Business subject and the concrete finding]
*Population | Study dates | Evidence date*

## Executive summary
**[One-sentence answer to the business question.]**
- The finding that most changes the decision, with its count, total and essential limit.
- Up to two more findings that change the decision.
- The decision the evidence supports, or does not support, stated plainly.

## Why this was studied
Two or three sentences: the business question and the decision it informs. Define, in
place, only the terms the summary needs.

[VISUAL 1: the comparison or journey that carries the lead finding.]

## [Finding 1 as a sentence]
Table or chart. What the numbers mean and why the business should care. Qualifications
stay attached to the claim.
**Implication:** what this means for the business, why it matters, and what happens if
nobody acts. Written as if the reader missed the point. See `plain-writing.md`.

## [Finding 2 as a sentence]
Same sequence: evidence, meaning, **Implication**. Do not repeat the summary verbatim.

[VISUAL 2, if needed.]

## Numbers not to over-read (optional)
Short bullets for figures that look like findings but cannot support a decision, each
with the reason in one line.

## What this report supports
| Decision | Rests on |
|---|---|
| Supported: ... | Finding 1 |
| Not supported yet: ... | Finding 2 |

Add a "Where it sits" column only when a roadmap item relates to a decision (`SKILL.md`).
One sentence of guardrails where a change is supported.

## How it was measured
A small table: who was included, date range, follow-up, counting unit, exclusions. Say why
important choices were made, and label any undocumented rationale as such.

## What this study does not establish
One or two sentences. Association vs cause, gaps in coverage, anything not measured.

## Sources
Numbered links to the evidence pack files, in plain words.
```

## Reading checks

- Replace jargon with plain words. The list is in `plain-writing.md`. Example: replace
  "cohort" with "group of people" (or whichever unit).
- Replace a bare percentage with the count and the total, then the percentage in brackets.
- Remove every em dash.
- Replace "the pattern is different" with what differs, when, and for whom.
- Replace "reasons are unavailable" with a bounded statement of the affected period,
  records and what could not be linked.
- Replace "extend tracking" with a precise distinction between missing source history and
  a missing transformation.
- Replace "continue TICKET-123" with the business investigation being continued.
- Avoid "X caused Y" unless a valid causal design supports it.

## Evidence handling

Keep source links short and in plain words. When an earlier study supplies a finding, name
it by subject and state its period. Do not present an earlier period as current or merge
different denominators silently. Keep query text, hashes, joins and detailed exclusions in
the evidence pack, or an appendix only when requested.

## Length check

Stay within the Profile's length, counted with `scripts/count_words.py`. If the draft is
over, follow "Shorten without changing the answer" in `SKILL.md`.

*Domain-specific example terminology does not belong in this template. Put it in the
domain context file in the analysis repository.*
