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
| Length | Target 1,500 words. **Hard maximum 2,000**, tables and captions included. Do not pad to reach a number. |
| Reading time | About 10 minutes of reading plus about 2 for the visuals. 12 at most. |
| Visuals | At least `max(1, Profile minimum)`. See `references/visuals.md`. |
| Names and IDs | No ticket IDs, PR IDs, query IDs, agent names or named colleagues in the body. Use a study title or a business description. |
| Privacy | No personal identifiers, emails, sensitive free text or record-level detail |
| Plain writing | No jargon. No em dash. Counts with their total before any percentage. Every finding has an Implication that explains itself. See `references/plain-writing.md` |

Use dense, plain content. If a figure matters, say what it counts: people, accounts,
orders or events. Replace vague words with the exact observation or a plain definition.

## Tell one coherent story

Start with why the question matters and the principal finding or decision. Connect:

```
Business question -> who and what was measured -> main findings
   -> what they mean for the business -> recommendation and next step
```

- Give each finding a **specific headline**, the evidence, and an **Implication**. The
  Implication says what the finding means for the business, why it matters, and what
  happens if nobody acts. Write it as if the reader missed the point. Do not repeat the
  finding in new words.
- Prioritise three or four consequential findings. Do not reproduce every query output.
- Distinguish what happened, why it may have happened, and what action should be tested.
- State measured impact separately from potential opportunity. Never invent retained
  customers, recoverable revenue or causal lift.
- Name earlier work by subject when it supplies a finding. Do not clutter the story with
  version history.

## Explain the method without burying the finding

- Put the essential definitions before the first results table: who was included, date
  range, follow-up, counting unit and exclusions, in a small table.
- Keep essential limitations **beside the claims they affect**. Move SQL, full mappings
  and execution detail to the evidence pack and link to them.
- Say when a choice's rationale is undocumented. Label a proposed rationale as
  interpretation.

## Visuals

A table can help, but it is not a visual for the minimum. Use a chart where numbers
compare or change, and a flowchart where the report explains a journey or process. Label
population, period, unit and denominator. State whether categories overlap. Add one
sentence near each visual saying what it shows. Inspect the rendered image before
delivery. Full guidance: `references/visuals.md`.

## Finish with a decision

- Recommend only actions connected to demonstrated findings or stated uncertainties.
- Present next steps as a short prioritised table: the action, the question it answers,
  how success will be judged.
- Define what success means for the business. Do not automatically treat fewer of a
  behaviour as improvement.
- Do not invent owners, commitments, deadlines or targets.
- Close with one or two sentences on what the study **does not** establish.

## Before handing over

- Can a non-technical reader explain the question, the population, the measurement, the
  finding and the next action without opening a technical document?
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
- `references/confluence-publish.md`: publishing, images, and the fallback.
- `references/atlassian-token-setup.md`: creating and storing the personal Atlassian API
  token that route A needs.
