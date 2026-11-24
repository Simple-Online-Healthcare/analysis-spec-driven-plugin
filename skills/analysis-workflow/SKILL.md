---
name: analysis-workflow
description: "The data analysis workflow for this team. Use when: asked to analyse something, answer a business question with data, investigate a metric or behaviour, compare periods or groups, build an evidence pack, replicate or verify an earlier analysis, or write up findings. Triggers: analysis, analyse, analyze, investigate, study, why did, what happened to, compare periods, evidence pack, replay, re-run analysis, verify analysis, discovery."
tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "AskUserQuestion", "Task"]
---

# Analysis Workflow

An analysis here goes: pin the question, settle the method with the user one decision at
a time, run saved SQL, prove it re-runs, write for non-technical readers, get an
independent review, hand over by PR.

> **Authority:** `AGENTS.md` at the repo root holds the mandatory, blocking rules and the
> **Analysis Profile**. This skill points to them rather than restating them.

The evidence is committed. The agreed design lives in `methodology.md` inside the
analysis folder, so a re-run knows exactly what was agreed. Decisions that explain a
specific line of SQL live in a comment next to that line.

| Intent | Route |
|--------|-------|
| New analysis | All phases |
| Narrow factual question ("how many X last week") | Answer briefly with the number, its definition and its date. If the number may support a decision, also save the query and its result as a minimal pack (`AGENTS.md` §1). A throwaway curiosity needs no pack. |
| Re-run or verify an earlier analysis | Start at **Verify** on the existing pack |
| Report only, from existing verified results | Start at **Write** |
| Review an existing pack or report | Start at **Review** |

---

## Start

0. **First time on this machine or in this repo?** If `AGENTS.md` is missing, the
   Profile's role or tools have not been checked, or the user says they have just
   installed the plugin, run the `analysis-setup` skill first. Come back here when it
   reports that setup is complete.
1. Get the ticket ID from the Profile's **ticketing** system, if there is one. Check for
   an existing analysis folder or open PR for it.
2. Read the **domain context** file named in the Profile. These hold the definitions of
   record. Do not redefine them.
3. Look for earlier analyses of the same subject in the evidence repo. Name any that
   supply a finding; reuse their saved results where the period and definition still
   apply. Do not rebuild data that already exists.
4. Branch from the Profile's **base branch**:
   `git checkout <base> && git pull && git checkout -b <ticket-or-slug>`.
   If the working tree is dirty, stash first and say so.
5. Create the analysis folder from the Profile's **folder pattern**
   (`analyses/<dd-mm-yy>-<slug>/`).

---

## Frame

Do this yourself, in the main thread. Pin down, with the user where needed:

- **The decision** the analysis informs, who will make it, and the alternatives being
  considered.
- **What the analysis must settle:** the question it has to answer for the decision,
  what evidence would change the recommendation, and what is out of scope. A finished
  report answers this as far as the evidence permits.
- **The reader.** Assume non-technical unless told otherwise.
- **The stage requested:** explain, draft, publish. Honour it. Do not publish when asked
  to draft.
- **What "no change" would mean.** If every plausible result leads to the same action,
  say so and ask whether the analysis is worth running.
- **Ground the question.** Inspect connected records and models before asserting what
  they contain. Use dbt to read model definitions, fields and lineage; use the repo for
  specifications and earlier evidence; run read-only **exploratory** warehouse queries
  only for what the design needs. A file being in a repo does not mean it is in the dbt catalogue.
- **Roadmap.** If the Profile names a **Roadmap location**, record in `methodology.md`
  the name and exact wording of any item that covers or relates to this question.

Write the question, decision, alternatives, what must be settled, scope, reader and stage
at the top of `methodology.md`.

---

## Design

Turn what Frame left open into decisions, **one question at a time**, each with a
recommendation. This is where the approach is chosen. The **analysis queries** that
produce reported numbers do not run until the design is agreed. Read-only exploratory
queries that inform a decision (for example, row counts under each option, or checking
what a field contains) are fine at this stage. Cite them as evidence in the question, and
rerun anything you later report as a saved, commented statement in Run.

**Which questions.** Only ones whose answer changes what gets measured or shown. Skip
anything a definition of record or an earlier analysis already settles, and say which one
settled it. Ask the questions other answers depend on first: population before outcome,
unit before denominator.

The topics to cover, as they apply (see `references/method-rules.md`):
- population, inclusion dates and exclusions
- unit of analysis and denominator
- time anchor, observation cutoff and follow-up length per horizon
- outcome definitions and whether they overlap
- comparison groups and whether they are like for like
- how missing data and unknown values are treated
- the **visual brief**: what picture answers the question (see below)
- small-count handling

**What a question must contain.** The user has not seen your Frame work. Each question
stands on its own:

- **Decision:** what is being chosen, in one line.
- **Why it matters:** what changes in the result depending on the answer.
- **Evidence:** the definition, file, table or query you found, with numbers.
- **Options:** two to four, each with its concrete consequence.
- **Recommendation:** one option, and why.

Ask with `ask_user_question`, recommended option first. Carry each answer forward **in
the user's words**. Do not widen it. If an answer reopens an earlier one, say so and
re-ask that one.

If a fact needed for a decision is owned by someone else and there is no evidence to base
a recommendation on, do not invent one. Ask who owns it.

**The visual brief.** Before the analysis queries, decide what the report needs to show
and which visual shows it (see `report-writing/references/visuals.md`). At least
`max(1, Profile minimum)`. A comparison over time or between groups suggests a chart;
a journey or a process suggests a flowchart. List what data each visual needs so the
queries produce it.

**The agreed design.** When nothing left would change what is measured, write it in your
reply and save it in `methodology.md`:

- **Decisions:** each with its answer.
- **Population and definitions:** who, when, unit, denominator, follow-up, cutoff.
- **Done when:** the checks that prove the work, each marked **Objective** (checkable
  against ground truth or a recomputation) or **Needs-human** (a judgement).
- **Visual brief:** each visual and the data it needs.
- **Risks and known limits** from Frame.

This design is what `method-reviewer` and `replay-verifier` check against.

---

## Run

Follow `references/evidence-pack.md` for the file shapes.

- Run the queries. Save each statement **exactly as executed** to `<topic>.sql`, with
  intent comments per `AGENTS.md` §9. Share a base CTE across related queries in
  `study_base.sql`.
- Save each result to `<topic>_results.json`: aggregates only, with schema, row counts,
  query ID, SHA-256 of the SQL body, and the cutoff. No personal or record-level data.
- Record source **freshness** at run time and the code or definition revision used.
- Record every scratch object created and keep it in the user's scratch schema.
- Build the visuals **from the saved results**, never from numbers typed by hand.
- Maintain `evidence_index.md` as you go: artifact, what it establishes, execution
  boundary (what was and was not run).

If a query fails or the result surprises you, say so and re-check the design before
continuing. Do not quietly adjust a definition to get a cleaner number.

---

## Verify

Delegate to `replay-verifier` with the analysis folder and the agreed design. It returns
the per-result and overall verdicts defined in `agents/replay-verifier.md`, **Verdict
rules**. Use that shared contract, including its precedence and verification gate.

- **MATCH:** continue.
- **MISMATCH / CHECK FAILED:** diagnose, repair using the verifier's **Repair** rule, and
  re-verify. Neither can be accepted as it stands. Source movement alone does not justify
  NOT REPLAYABLE, and changing a recorded hash alone does not repair provenance.
- **MATCH (partial) / NOT RUN:** finish the omitted replay or recover the missing
  metadata. Do not advance these as verified results.
- **NOT REPLAYABLE:** perform the verifier's fallback checks. Missing results prevent
  recomputation; missing SQL/base prevents fingerprinting. Record unavailable checks and
  affected claims, but restore missing files before handover. Only the complete-pack,
  unrecoverable-source case can pass `AGENTS.md` §8.

`final_verification.md` records what was checked, what was not, and what remains limited.
Never mark a result verified from reading the SQL alone.

---

## Write

Follow `report-writing` and `AGENTS.md` §12. Write the report from verified results only.
Use plain words, give counts before percentages, never use an em dash, and write each
Implication so it makes sense to someone who missed the point of the finding.

- Lead with the finding that most changes the decision (`report-writing`, "Tell one
  coherent story").
- Prioritise three or four consequential findings, each with an **Implication** line.
- Every measured value comes from its cited saved results version; design dates come
  from methodology or executed SQL. Every visual is rendered and inspected.
- State the population, definitions and limits beside the claims they affect.
- End with "What this report supports" and a short statement of what the study does
  **not** establish.
- Save to `executive_study.md`. Detail goes in the pack with links, not in the body. If
  the report is rewritten after verification, keep the new report and its charts in a
  `report/` subfolder so the verified files stay unchanged. Record the current report's
  path in `evidence_index.md`.

---

## Review

Delegate in parallel to:

- `method-reviewer`: the design and SQL against the method rules.
- `report-checker`: executive read, word count, visuals, traceability, claim meaning,
  decision use and reader-facing content.
- `writing-checker`: grammar, flow, tone, ease of understanding and the writing rules in
  `AGENTS.md` §12. Give it the current report and `methodology.md`.

All are independent: they have not seen your reasoning, which is the point. Each owns its
area, cites the rule behind each issue, and returns High, Medium and Low issues.
`report-checker` and `writing-checker` also return the SHA-256 of the files they checked.
Record the verdicts and hashes in `evidence_index.md`.

- Interactive: walk the High and Medium issues with the user, offering a specific fix for
  each.
  - `report-checker` and `writing-checker` **High** issues must be fixed. They cannot be
    declined or recorded as limits, because `AGENTS.md` §6 and §12 are blocking.
  - `method-reviewer` **High** issues are fixed, or the user explicitly accepts them. An
    accepted High issue is recorded in `final_verification.md` under "Accepted by user",
    with the reason, and is stated beside the claim it affects (`AGENTS.md` §5).
  - Medium issues may be declined by the user.
- Treat Low findings and suggestions as optional. Chasing every finding adds defensive
  caveats for cases that cannot happen.
- Record each issue not fixed in `evidence_index.md` under "Known limits".

**Rounds.** On a re-review, give each checker its previous issue list. After two automatic
rounds, stop rewriting and show the user what remains, grouped as blocking (High),
required (Medium) and optional (Low), with any place two checkers contradict each other.
Remaining High issues still block (`AGENTS.md` §8).

**Recheck in proportion to the edit.** A wording change needs `report-checker` (meaning,
executive read) and `writing-checker`. A chart change needs `report-checker` (visuals). A
method or result change needs `method-reviewer`, `replay-verifier` and `report-checker`.
Punctuation alone does not need the warehouse re-run.

---

## Hand over

1. Check `git status`. Stage only this analysis: the pack, the visuals and the report. No
   scratch files, no record-level extracts.
2. Commit with the ticket ID if there is one. Push the branch and open a PR to the base
   branch. The body carries: the question, the agreed design, the verification result,
   the known limits, and the visuals as images.
3. Publish to Confluence **only with explicit permission**, following
   `report-writing/references/confluence-publish.md`. Before publishing, confirm the
   report and chart hashes still match the recorded review, and that no placeholder or
   local file link remains in the page. Draft first, reuse the existing
   page, never create numbered duplicates. Complete its **After publishing** step so
   the committed pack and PR both link to the page.
4. Update the ticket. **Never merge.**

---

## Interactive only (v1)

The human touchpoints are the Design questions, Needs-human checks, High and Medium review
issues, and the PR. Do not add approval gates between phases. Scheduled or unattended mode
is not supported in v1: an unattended run cannot answer Design questions.

---

## What good looks like

**A Design question that works:**

> **Decision:** which customers count as "repeat buyers" for the study population.
> **Why it matters:** sets the denominator for every outcome rate in the report.
> **Evidence:** the definition of record counts a repeat buyer from the second order; the
> order history includes customers whose first order was before the study window (query
> in `study_base.sql`, row counts shown for each option below).
> **Options:** (a) first order inside the window: `<N_a>` customers, matches the earlier
> period's rule; (b) first order at any time: `<N_b>` customers, mixes older groups.
> **Recommendation:** (a), so both periods use the same entry rule.

**A question that does not work:** "Which customers should we include?" There is no
evidence, no consequence and no recommendation, so the user has to redo the Frame work to
answer it.

**A PR body:** the question; the agreed design; each Done-when check with its result;
verification verdicts using the replay-verifier contract, with limits; known limits;
links to the report and the visuals.

*(`<N_a>` and `<N_b>` are placeholders: a real question quotes real numbers from a saved
query.)*

---

## References

- `references/method-rules.md`: the method rules in detail.
- `references/evidence-pack.md`: file shapes and what each must contain.
- `../analysis-setup/SKILL.md`: first-time setup for a new teammate.
- `../report-writing/SKILL.md`: how the report is written.
