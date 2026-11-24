---
name: report-writing
description: "How analyses are written up for this team. Use when: drafting, revising or publishing an analytical report, executive study, research synthesis, interpretation of results, methodological review or stakeholder write-up; adding charts or flowcharts to a report; publishing a report to Confluence. Triggers: write the report, draft the study, executive summary, write up findings, report, publish to Confluence, add a chart, add a flowchart, plain English, explain results."
tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "AskUserQuestion"]
---

# Report Writing

Reports are read mostly by people who are not analysts or engineers. Anyone should be
able to read one and understand it. That is the standard everything below serves.

> **Authority:** `AGENTS.md` §6, §7, §10 and §12 are blocking. This skill explains how to
> meet them. The Profile sets the length, minimum visuals and publishing route.

This is writing and communication guidance. It does not replace a governed metric
definition, a source restriction or an explicit instruction.

## Scale to the question

- Narrow question: a short, direct answer with the number, its definition and its date.
  Do not turn it into a report.
- Full study: the structure in `references/report-template.md`.
- Natural, direct language is fine in conversation and implementation instructions. The
  formal voice below is for reports.

## Deliver the requested stage

Honour the stage the user asked for: explain, review, draft, revise or publish.

- Draft in chat when review is requested. Do not create or update Confluence, Jira or
  repository files outside the analysis folder without explicit permission.
- Answer methodology questions before rewriting when the user wants point-by-point review.
- When publishing: search for the existing page first and reuse it. Never create numbered
  duplicates. See `references/confluence-publish.md`.

## Standards

| Standard | Rule |
|----------|------|
| Reader | An intelligent executive without analytics or engineering knowledge |
| Voice | Third person: "The study found...", "Customers...", "The next step is...". No "I", "we", "you", assistant narration or comments about how the report was produced |
| Reading level | Plain English at about a tenth-grade level. Short sentences. Define unfamiliar terms at first use. |
| Length | The Profile's length, counted with `scripts/count_words.py` (`python3 scripts/count_words.py <report>`). Do not pad to reach a number. |
| Reading time | The Profile's reading time. |
| Visuals | At least `max(1, Profile minimum)`. See `references/visuals.md`. |
| Names and IDs | No ticket IDs, PR IDs, query IDs, agent names or named colleagues in the body. Use a study title or a business description. |
| Privacy | No personal identifiers, emails, sensitive free text or record-level detail |
| Plain writing | No jargon. No em dash. Counts with their total before any percentage. Every finding has an Implication that explains itself. See `references/plain-writing.md` |

Use dense, plain content. If a figure matters, say what it counts: people, accounts,
orders or events. Replace vague words with the exact observation or a plain definition.

## Tell one coherent story

Lead with the finding that most changes the decision the report informs. State its scale
and essential qualification. Use magnitude to distinguish otherwise similarly relevant
findings, not as the sole ranking criterion. If the evidence supports a recommendation,
make it explicit in the opening. The lead may be a large problem, a smaller confirmed
failure, or evidence that a proposed change is not justified.

The opening holds a short answer to the business question, up to three findings that
change the decision, and the decision the evidence supports with its essential limit.
Then connect:

```
Business question -> who and what was measured -> main findings
   -> what they mean for the business -> what this report supports
```

- Give each finding a **specific headline**, the evidence, and an **Implication**
  (`references/plain-writing.md` §4).
- Prioritise three or four consequential findings. Do not reproduce every query output.
- A finding that only warns against over-reading a number goes in a short "numbers not to
  over-read" section, unless the warning itself changes the decision.
- Give each defined term the shortest familiar label that keeps what was measured, and use
  it the same way in every heading, table and chart (`references/plain-writing.md` §2).
- Distinguish what happened, why it may have happened, and what action should be tested.
- State measured impact separately from potential opportunity. Never invent retained
  customers, recoverable revenue or causal lift.
- Name earlier work by subject when it supplies a finding. Do not clutter the story with
  version history.

## Explain the method without burying the finding

- Define only what the opening needs, in place, in plain words. Put the full method table
  (who was included, date range, follow-up, counting unit, exclusions) after the findings.
- Keep essential limitations **beside the claims they affect**, and say what each one
  prevents and does not prevent: "This prevents estimating recoverable revenue, but does
  not prevent investigating the payment process." Move SQL, full mappings and execution
  detail to the evidence pack and link to them.
- Say when a choice's rationale is undocumented. Label a proposed rationale as
  interpretation.

## Shorten without changing the answer

Cutting words must not change the apparent certainty, feasibility or recommended
decision. Before cutting, for each headline and each decision, keep:

- the evidence that supports it, and the evidence that qualifies or challenges it;
- a newer period or subset with usable data, when it changes what can be done;
- any earlier work that already answers a question the report would otherwise leave open.

Move the rest to the pack.

## Visuals

A table can help, but it is not a visual for the minimum. Use a chart where numbers
compare or change, and a flowchart where the report explains a journey or process. The
image holds a title, subtitle, axis labels, legend and data labels; definitions and
caveats go in the sentence beside it. Inspect the rendered image before delivery. Full
guidance: `references/visuals.md`.

## Finish with what this report supports

Close with a short table of **decisions, not tasks**: what the evidence supports now, and
what it does not support. Columns: the decision, the finding it rests on, and where it
sits on the roadmap.

- **Where it sits:** if the Profile names a **Roadmap location**, use the items recorded
  in `methodology.md` during Frame and write one
  of: covered by `<item>` (the item names this exact work), related, not covered by
  `<item>`, not scheduled. If the roadmap was not read, write "roadmap not checked".
- **Open questions.** Include an unresolved question only when its answer could change
  the conclusion, the recommended action or its scope. Explain what it prevents deciding,
  usually in a sentence beside the affected finding or decision. Do not turn it into an
  automatic follow-up task. If it prevents the main conclusion, say the evidence cannot
  settle it; if answering it is in the agreed scope, the analysis is not complete. A
  question that would not change the decision stays in the pack, not the report.
- Add one sentence of guardrails where a change is supported, for example which harms to
  watch when judging it. Do not automatically treat fewer of a behaviour as improvement.
- Name no owners, leads or teams as decision makers, and invent no commitments,
  deadlines or targets (`AGENTS.md` §7).
- Close with one or two sentences on what the study **does not** establish.

## Before handing over

- Executive read: does the report pass the six questions in `agents/report-checker.md`,
  step 1?
- Does every measured value trace to its cited saved results version, and every design
  date to methodology or executed SQL?
- Is the report within the length cap, with the minimum visuals rendered and inspected?
- Are jargon, repeated disclaimers, ticket IDs and unsupported recommendations removed?
- Does every percentage have its count and total beside it, and is there no em dash?
- Do you have permission to publish?

Delegate the mechanical checks to `report-checker` and the language checks to
`writing-checker`.

## References

- `references/plain-writing.md`: the plain-words list, counts before percentages, how to
  write the Implication, punctuation and tone.
- `references/report-template.md`: the report structure.
- `references/visuals.md`: charts, flowcharts, rendering and inspection.
- `scripts/count_words.py`: the one word count every checker uses.
- `references/confluence-publish.md`: publishing, images, and the fallback.
- `references/atlassian-token-setup.md`: creating and storing the personal Atlassian API
  token that route A needs.
