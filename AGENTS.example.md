# AGENTS.md: Mandatory Rules for Analyses

> **Authority:** This is the highest-authority file for analysis work. Every agent, skill
> and sub-agent MUST obey these rules. They are **blocking**: if an analysis violates a
> rule below, do not proceed. Fix it or stop and surface it to the user.
>
> - **AGENTS.md (this file)** = mandatory, blocking rules.
> - **`analysis-workflow` skill** = the workflow that orchestrates *how* work happens.
> - **`report-writing` skill** = how a report is written and presented.
> - **Sub-agents** (`/agents`) = isolated checks that run within that workflow.
>
> Subjective quality (tone, emphasis, clarity of one paragraph) is **not** enforced here.
> That is the job of the `report-checker`, `writing-checker` and `method-reviewer`
> agents. This file holds only the objective, checkable rules.

---

## Analysis Profile (team-specific configuration)

> **This block is the only team-specific part of the file.** Every numbered rule below is
> generic and refers to these values by name. To adapt this plugin to another team or
> domain, change this block, not the rules. Copy this file to the root of your analysis
> repository as `AGENTS.md` and edit the values.

| Parameter | Value |
|-----------|-------|
| Evidence repository | `analytics` |
| Analysis folder pattern | `analyses/<dd-mm-yy>-<slug>/` |
| Base branch | `main` |
| Domain context location | `context/<domain>.md` in the evidence repository. Holds links to the definitions of record. The plugin never stores domain definitions. |
| Report destination | Confluence space `DT` (Data Team). Parent page per study series. |
| Naming conventions | **Repository:** `analytics` (GitHub `<org>/analytics`), base branch `main`; never `analytics-pipelines` (dbt) or another team's repo. **Branch:** `<TICKET>-<slug>` from `main`. **Folder:** `analyses/<dd-mm-yy>-<slug>/`, dated the day the analysis starts, slug in lowercase words joined by hyphens. **Confluence:** space `DT` (Data Team), never `DATA`; folder `Analysis` under the space home; page title states the question in plain words (for example "Kin conversion: why it fell, and what commitment plans did"), no dates, ticket IDs or version numbers; one page per study, reused on re-runs. |
| Data sources | Prefer semantic views, then dbt models, then raw tables. Say in `methodology.md` when a fallback was used and why. Problems with a source are fixed in its model documentation (raise a ticket), not recorded as local notes in the pack. |
| Experiment method | Lives in the `cro-squad` plugin. Call `$cro-experiment-analysis` for any experiment result; it health-checks first and labels each result as the standard route (pre-built results with the settings configured in Statsig) or a custom route with health warnings. Both plugins must be installed. |
| Confluence base URL | `https://<your-site>.atlassian.net/wiki` |
| Image publishing | Route A (the agent uploads the picture for you; tested; token held as a per-user Cortex secret named `ATLASSIAN_API_TOKEN`). Fallback: route B (manual drag-in). See `report-writing/references/confluence-publish.md`. |
| Ticketing | Jira project `DATA`. Ticket IDs go in commits, PRs and `methodology.md`, never in the report body. |
| Warehouse and role | Snowflake, the user's own read-only analyst role. Each person runs analyses under their own login. No shared automated account is used yet. |
| Scratch location | A private working area that only the person can write to, such as their own personal schema. Name the exact pattern for your warehouse. |
| Length | Target 1,500 words for the main report. Hard maximum 2,000 words. Counted only with the `report-writing` skill's `scripts/count_words.py`; that script defines what counts. This row is the only place the limit is set. |
| Reading time | Up to about 10 minutes of reading plus about 2 for the visuals. 12 minutes at most. |
| Minimum visuals | 1 per report (a chart or a flowchart; a table alone does not count) |
| Chart tooling | Python standard library builds SVG; `rsvg-convert` converts to PNG, or headless Chrome at 2x where `rsvg-convert` is not installed. Flowcharts: mermaid via `npx`, or the same SVG approach. |
| Roadmap location | Optional. Where the team's roadmap lives, for example a Confluence page. Leave out if analyses are often not roadmap work; reports then show no roadmap column. |
| Small-count handling | Decided per analysis in the Design phase and recorded in `methodology.md`. |
| Sensitive data rule | No personal identifiers, emails, free text or record-level health detail in reports, results files or skill resources. Saved results are aggregates only. |
| PR template | The evidence repository's template if it has one, otherwise the summary below in the workflow skill |

---

## 1. Evidence pack (blocking)

Every analysis that produces a number someone may act on has an evidence pack in the
analysis folder named by the Profile.

- Each reported result has its SQL, its saved aggregate result, and a place in
  `evidence_index.md`.
- SQL is saved exactly as executed, with brief intent comments.
- The pack is saved to the repository through a pull request. Working files that are not
  evidence are not saved.

**Fail if:** a measured value in the report cannot be traced to its cited saved result
version and the SQL that produced it. Study-period and design dates trace to
`methodology.md` or the executed SQL instead.

*Why: a number without its method cannot be re-run or defended.*

---

## 2. Reproducibility (blocking)

- Record the **cutoff**: the date and time after which nothing was counted. Say whether
  records at the cutoff itself were counted, and give the timezone. Also record how fresh
  each source was when the query ran.
- Pin the code revision or definition version used where one applies.
- Record the query IDs and a SHA-256 code for each executed SQL body (a short code that
  changes if the text changes).
- Say plainly if the sources were read at different moments rather than all at once.

**Fail if:** the pack gives no cutoff, or claims reproducibility it cannot support.

---

## 3. Read-only and safe (blocking)

- Analyses read from sources. They do not write to production objects.
- Use only the role named in the Profile. Before the first query, run
  `USE SECONDARY ROLES NONE` to switch off every other role you hold. If you skip this,
  a second role, such as an administrator's, can quietly add the right to change data.
- Scratch tables (temporary working tables) go only in the scratch location named in the
  Profile, and are named in `evidence_index.md`.
- No personal identifiers or record-level detail in saved results, reports or logs.

**Fail if:** any production object is changed, or personal data reaches a committed file.

---

## 4. Definitions of record (blocking)

- Use the definitions named in the domain context file. Do not redefine a measure.
- If this analysis needs a different definition, state the difference and why in
  `methodology.md` and flag it to the user. Do not silently choose.
- Keep a business rule, a grouping assigned by a model, an observed record, a hypothesis
  and an unverified assumption separate and labelled.

**Fail if:** a term is used with a meaning that conflicts with the definition of record,
without saying so.

---

## 5. Method (blocking)

The rules in `skills/analysis-workflow/references/method-rules.md` are binding. In short:

- State who was counted, the start and end dates, how long each person was watched, the
  date each person's clock starts from, what one row of the count stands for, and the
  total each result is measured against.
- Compare like with like.
- When an outcome is missing for a person, keep that person in the total.
- Do not say one thing caused another unless the design proves it.
- Before saying a measure rose or fell, check mix (channel, new against repeat, subscription
  against one-time purchase, drug or category) and seasonality (weekly and monthly cycles),
  and record both in `methodology.md`.
- An experiment result comes through `$cro-experiment-analysis`, health first. A custom route
  is agreed in Design and its warnings sit beside the number in the report.

**Fail if:** the `method-reviewer` returns a High issue that has not been fixed or
explicitly accepted by the user.

---

## 6. Report standard (blocking)

- Written for a non-technical reader. Anyone should be able to read the report and
  understand it.
- At least the Profile's minimum number of **visuals**, and never fewer than one. Each is
  rendered and inspected.
- Within the Profile's **length**, counted with the shared word counter.
- No ticket IDs, named colleagues, query IDs or personal identifiers in the body.
- Passes the **executive read**: a reader given only the report and its charts can say
  what is happening, how big it is, what decision the evidence supports and why.
- Follows the writing style in §12.

**Fail if:** the `report-checker` returns any High issue that has not been fixed.

---

## 7. Causation and claims (blocking)

- Do not claim a cause without a design that supports it. Describe an association as an
  association.
- Keep measured impact separate from potential opportunity. Never invent recovered
  revenue, retained customers or an improvement that was not measured.
- Recommend only actions connected to demonstrated findings or stated uncertainties.
- A label, headline or chart title claims no more than was measured. A missing record is
  reported as missing, not as a confirmed failure.
- A report names no owners, leads or teams as decision makers, even as proposals.
  Ownership belongs in the planning document.
- A roadmap item "covers" a question only when it names that exact work. Otherwise say
  "related, not covered", or say nothing about the roadmap. Write that work will be done
  only when a delivery commitment is recorded.

**Fail if:** the report states or implies an effect, certainty, owner or commitment the
evidence does not establish.

---

## 8. Pull request gate (blocking)

Before a PR can merge:
- Every pack file exists and `evidence_index.md` is complete.
- `replay-verifier` meets the verification gate in `agents/replay-verifier.md`,
  **Verdict rules**, including its gate scope and verified-replacement requirements.
  Every result version is accounted for; superseded failures retain their verdict and
  correction history. Only MATCH, or NOT REPLAYABLE due to
  demonstrably unrecoverable sources with a complete pack and passing fallback checks,
  can pass. Failed, partial, unrun or uncheckable verification blocks the merge. Record
  every unavailable check and affected claim in `final_verification.md`; recording a
  missing file does not waive the complete-pack requirement.
- The Review phase has no open High issues. A `method-reviewer` High issue is closed by a
  fix or by the user's explicit acceptance, recorded in `final_verification.md`
  (see §5). A `report-checker` or `writing-checker` High issue is closed only by a fix.
- Each `report-checker` and `writing-checker` result names the SHA-256 of the report,
  chart and `methodology.md` files it checked, and those match the files being handed
  over. A later edit needs the matching recheck.
- The user has approved the report.

**Fail if:** any of the above is not met. The workflow never merges a PR.

---

## 9. Inline comments for non-obvious SQL (blocking)

SQL that is **intentional but not self-evident** MUST carry a brief comment stating the
intent: why, not a restatement of the syntax. At minimum, comment:

- the **time boundary** and why it is inclusive or exclusive;
- a **filter that encodes a business rule**;
- a **join type** chosen to control rows, and NULL handling on join keys;
- **deduplication**: the partition and order, and why;
- `COALESCE` or any NULL substitution that changes the meaning;
- an intentional **fan-out** (one row matching many rows, which makes counts grow);
- **first-event** selection rules.

**Fail if:** any construct above is present with deliberate-but-implicit intent and no
comment.

---

## 10. Publication (blocking)

- Draft in chat or in the pack first. Do not create or update a Confluence page, Jira
  ticket or repository file outside the analysis folder without explicit permission.
- Search before creating a page. Reuse the existing page. Never create numbered
  duplicates.
- Never merge a PR.

---

## 11. Explicitly forbidden

- Reporting a number that has no saved evidence.
- Redefining a measure of record silently.
- Writing to production objects.
- Personal or record-level data in committed files.
- Illustrative numbers presented as results.
- Ticket IDs or colleague names in a reader-facing report.
- Jargon, an em dash, or a percentage with no count beside it, in anything written for a
  reader (§12).
- Skipping the Verify phase because the SQL "looks right".
- Using an experiment result before its health (sample ratio mismatch, missing events,
  completion, power) is known, or reporting a custom experiment analysis without its
  warnings.

---

## 12. Writing style (blocking)

This applies to everything written for a person to read: reports, methodology notes, PR
descriptions, Confluence pages, ticket comments and replies in chat. Write so that a
non-technical colleague and a technical colleague both understand it on the first read.

- **No jargon.** Jargon is any word or short phrase that only a specialist would know.
  It is prohibited. Use the plain word instead. If a technical term cannot be avoided,
  explain it in brackets the first time it appears. Common swaps are listed in
  `skills/report-writing/references/plain-writing.md`.
- **Explain the implication.** Under every finding, write an **Implication** that says what
  the finding means for the business and what happens if nobody acts, or which decision it
  changes. Write it as if the reader missed why the finding matters. Do not repeat the
  finding in new words.
- **Counts before percentages.** Give the real number and the total it comes from, for
  example "412 of 1,830 customers". A count shows the whole group. A percentage hides how
  many people stand behind it. A percentage may follow in brackets. Never give one alone.
- **No em dash.** Never use the em dash (the long dash that joins two phrases). It is a
  clear sign of machine-written text. Use a full stop, a comma, a colon or brackets.
- **Plain sentences.** Short sentences, one idea each, in the active voice. Say what a
  number counts: people, accounts, orders or events.

**Fail if:** the `writing-checker` returns any High issue that has not been fixed.

*Why: a finding that only an analyst can read does not change a decision.*
