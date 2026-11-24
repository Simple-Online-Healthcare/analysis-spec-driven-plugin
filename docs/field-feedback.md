# Field Feedback: Real-World Failures

> Canonical log of observed behaviour during analyses. Each entry says what was seen,
> where, and which plugin files were changed to prevent it happening again. Rules in this
> plugin should trace back to an entry here. Add to this file whenever real use surfaces a
> problem, and make the fix in the same PR.

---

## How to add an entry

1. Give it a heading with a short title and the month.
2. List **Observations**: what was seen, with evidence. Do not paste personal or
   record-level data.
3. State the **Correct pattern**.
4. Add a **Plugin actions taken** table: file, change.
5. If something is **untested or open**, say so under "Open".

---

## Starting findings before the first release (November 2026)

Recorded from the team's published studies and from setting up this plugin.
These are observed conditions, not failures of an earlier version of the plugin.
Study-specific figures are kept in the team's private analysis repository, not here.

### Observations

1. **Evidence was mixed with unrelated work.** Analysis folders sat in the dbt
   repository's specs directory beside many unrelated feature specs, and Confluence pages
   linked straight to those paths.
2. **No standard way to decide what to analyse.** Each study chose its population,
   follow-up and outcomes in conversation. The reasoning lived in the methodology file
   written afterwards, not in an agreed design written first.
3. **A published study had no visual.** It was text and tables only, although it explains
   a multi-step journey to a mostly non-technical readership.
4. **Reader-facing text named ticket IDs.** One published guide lists ticket IDs in its
   source notes, which the team's own writing rules forbid.
5. **Length drifted.** One executive study went over the word limit at independent review
   and had to be cut at proofreading. The cap was applied late and by hand.
6. **Re-running was hard.** Several saved result sets could not be replayed against
   moved sources. The team worked around it by recovering query history, hashes and
   execution ledgers after the fact.
7. **The Atlassian MCP cannot upload attachments.** An image on a page needs a media ID
   from an uploaded file, so there is no one-step way to add a chart.
8. **An existing chart is correct but not plain English.** The saved chart renders
   cleanly, but its subtitle and axis use statistical terms that a non-technical reader
   would not follow. (Seen when testing the SVG to PNG route.)

### Correct pattern

- A committed, standard evidence pack per analysis, in the analysis repository.
- The agreed design is written **before** analysis queries run, including a visual brief;
  read-only exploratory queries may inform it.
- Word count, visual count and reader-facing content are checked mechanically by an
  independent agent, not left to proofreading.
- Replay is attempted in the Verify phase. When it is impossible, the pack says why and
  what was recomputed instead.
- Images are generated from saved results and published through a route that works
  (upload by REST, or manual drag-in).

### Plugin actions taken

| File | Change |
|------|--------|
| `skills/analysis-workflow/SKILL.md` | Frame, Design (with a visual brief), Run, Verify, Write, Review, Hand over |
| `skills/analysis-workflow/references/evidence-pack.md` | Standard pack shape, based on the existing studies |
| `skills/analysis-workflow/references/method-rules.md` | Generic method rules taken from the team's writing conventions |
| `skills/report-writing/` | 1,500-word target and 2,000 hard maximum; at least one visual; plain-English test |
| `agents/report-checker.md` | Counts words, visuals and traceability; flags ticket IDs and identifiers |
| `agents/replay-verifier.md` | MATCH / MISMATCH / NOT REPLAYABLE, with recomputation fallback |
| `agents/method-reviewer.md` | Independent review of the design and SQL |
| `skills/report-writing/references/confluence-publish.md` | Two image routes (REST upload and manual drag-in) |
| `skills/report-writing/references/confluence-publish.md` | Route A confirmed: use `cortex secret run --map`, `?status=draft` for drafts; bash `secret_env` did not work |
| `skills/report-writing/references/visuals.md` | Verified SVG to PNG (`rsvg-convert`) and mermaid CLI commands; plain-English labelling rule |

9. **Images that look fine as files are too small on the page.** On the test draft at
   80% width, the chart's text was hard to read and the six-box flowchart was
   too small to read. (Seen in a screenshot of the rendered draft.)

### Open

- **Image upload by REST (route A):** tested end to end on a draft on 17 November 2026
  and confirmed visually (see "Route A" in `confluence-publish.md`). The draft was
  deleted. Still to confirm: that a teammate can do it with their own token.
- **Mermaid CLI:** renders on macOS with an installed Chrome and `--scale 2`. It does not
  work out of the box without `chrome-headless-shell`. Not yet tested on a teammate's
  machine.
- **No analysis has yet run through the full flow.** The pilot on a past study is the
  first end-to-end test.

---

## First automated review of the plugin itself (November 2026)

An automated reviewer read the first draft of the plugin and found real problems in the rules we wrote.

### Observations

1. The workflow let an unresolved MISMATCH or a declined High issue through, while the PR
   gate said neither could pass.
2. "Nothing runs until the design is agreed" conflicted with the need to run exploratory
   queries to inform Design decisions.
3. The SQL fingerprint was not defined precisely, so producer and verifier could hash
   different bytes.
4. A narrow factual question could skip the evidence pack even when the number supported
   a decision.
5. The publishing command put the API token in `curl`'s arguments, where a process list
   could show it.
6. Dated re-run results files were allowed but the verifier did not look for them.

### Plugin actions taken

| File | Change |
|------|--------|
| `AGENTS.example.md` §8 | Unresolved MISMATCH blocks merge; method High issues need a fix or explicit user acceptance; report High issues need a fix |
| `skills/analysis-workflow/SKILL.md` | Exploratory queries allowed in Design; MISMATCH cannot be accepted as it stands; missing pack files are NOT REPLAYABLE; narrow questions get a minimal pack when they support a decision |
| `skills/analysis-workflow/references/evidence-pack.md` | One hashing procedure (`file-statement-v1`); dated results file naming |
| `agents/replay-verifier.md` | MATCH requires fingerprint and cutoff checks; finds dated results files |
| `agents/report-checker.md` | Below-minimum visuals is High; dates trace to methodology or SQL |
| `skills/report-writing/references/confluence-publish.md` | Token passed on stdin; replacement-by-new-filename guidance |
| `skills/report-writing/references/visuals.md` | Puppeteer config path; script location |

### Second review round on the fixes

Reviewing the first round of fixes found further gaps, which were also fixed:

- A NOT REPLAYABLE step could pass the gate even if its fallback recomputation or
  fingerprint failed. The gate now requires every check that ran to pass.
- Matching rows with a failed fingerprint or cutoff check had no status. Added
  **CHECK FAILED**, distinct from MATCH and MISMATCH.
- A changed `study_base.sql` could go unnoticed. The pack now records `base_sha256` and the
  verifier checks it.
- Two re-runs on the same day would overwrite each other. Re-run result files now carry a
  UTC timestamp.
- A MISMATCH could be relabelled NOT REPLAYABLE because a source had moved. That now needs
  evidence the source cannot be rewound, and passing fingerprint and cutoff checks.
- A Profile minimum of 0 would have let a report with no visual pass. No visual is always
  High.
- The token setup wrote the token to a temporary file, which would remain if the store step
  failed. It now uses `cortex secret store --prompt`, which reads the token without echo and
  without a file.

### Agent metadata follow-up

- Agent frontmatter was initially deferred based on the sibling plugin, without a
  registration test. A follow-up added `name` and `description` to all three agents,
  following the [official subagent format](https://docs.snowflake.com/en/user-guide/cortex-code/extensibility#extensibility-subagents).
  The conventional `agents/` directory needs no manifest override. Live registration
  still needs an install/reload test; metadata validation alone does not prove it.

---

## Pilot: replaying an existing published study (November 2026)

The first end-to-end test of the plugin's checks, run on one published study in a scratch
folder. Nothing was published or changed. The study's figures are kept in the team's
private analysis repository.

### What was checked and what happened

| Check | Result |
|-------|--------|
| SQL fingerprints | 12 of 12 saved statement bodies match their recorded SHA-256 and character counts. The study uses its own method (hash of the body between `BEGIN`/`END` marker lines), not `file-statement-v1`. The verifier must follow the method the pack states. |
| Recompute from saved aggregates | The headline totals and rates in the report reproduce from the saved results. |
| Re-run against the current warehouse | The main query's CTEs were re-run unchanged with the final output restricted to the cohort and 24-hour rate sections. All 4 cohort counts and all 16 rate rows (112 numeric fields) matched the saved results exactly. Verdict: **MATCH, partial** (1 of 12 statements, 2 of the output sections). Everything else was not re-run. |
| `report-checker` mechanics on the published page | The word count was inside the limit (about 8 minutes of reading), there were no ticket IDs, and there were **0 visuals**. Under the plugin's standard, no visuals is a High issue. |
| Visuals built from saved results | One bar chart and one flowchart, both rendered and inspected. The chart's values match the report's own day-one table. |

### Observations

1. **A partial replay must be reported as partial.** Restricting the final `SELECT` changes
   the statement text, so the fingerprint no longer applies to what was run. The verifier
   should say which statements and output sections were replayed, not just "MATCH".
2. **The study was not an atomic snapshot**, yet its recorded results still reproduced at
   the same cutoff. A later re-run is therefore worth trying before declaring a study
   NOT REPLAYABLE.
3. **There is no `snow` CLI or Python connector on this machine.** Replays ran through the
   Cortex SQL tool by pasting the saved statement, which does not scale to large packs.
   A script runner is worth adding if replays become routine.
4. **Chart labels differ in precision from the report.** The chart rounds to one decimal
   place while the report's table uses two. State the rule in the report: either match
   them or say the chart is rounded.

### Open

- Adding the two visuals to that study's published page needs the owner's permission and was not done.
- A teammate has not yet run the flow end to end.

---

## Complete audit of the first review comments (November 2026)

### Observations

Reviewing all 27 inline comments, five review bodies and two discussion comments found
30 distinct findings, including two outside the diff and one present only in a summary.
Most fixes were already present, but related instructions still contradicted them:

- Design dates were allowed in traceability but still failed the High-severity rule.
- The checker and chart generator defaulted to original results, ignoring cited reruns.
- Partial replay and uncheckable metadata had no consistent overall or gate outcome.
- Replacing a recorded hash was offered as a repair without proving the SQL produced the
  saved result. Source movement and non-atomic execution could also mask missing proof.
- The media example still used 80% width, and post-publication links could remain local.

### Plugin actions taken

| Files | Change |
|---|---|
| `agents/` | Add documented agent metadata; define verification verdicts once; check cited results versions and distinguish design dates from measured values |
| `AGENTS.example.md`, workflow and report-writing guidance | Align the gate, exploratory-query boundary, visual minimum and traceability with the checks |
| `evidence-pack.md`, `visuals.md` | Preserve exact result/SQL versions; add a UUID to rerun filenames; recognize historical names; render from cited results |
| `confluence-publish.md` | Full-width media example; persist the page link through the authorized branch/PR workflow |

### Open

Live agent registration and a teammate's end-to-end analysis remain separate checks.
This audit changes instructions; it does not rerun warehouse studies or publish pages.

### Fresh review follow-up

The fresh PR review caught remaining inconsistencies: replay could execute before
provenance passed; failed fallback evidence had no output slot; anonymous record-level
data and sensitive text were absent from the High criteria; exact quotations could repeat
private data; and original preservation still allowed overwrites. These now have explicit
rules and scenario checks. The verdict test compares whole tokens rather than substrings;
replacement semantics stay in the scenario review instead of exact-prose assertions.

---

## Plain writing, checker and first-time setup (November 2026)

### Observations

1. **Reports were hard to read for non-analysts.** A saved chart used statistical terms
   that a non-technical reader would not follow (see the first entry above). Nothing in the
   rules named jargon as a failure, and the only check for it sat inside `report-checker`
   among many other duties.
2. **Percentages hid the size of the group.** A percentage on its own does not show how
   many people stand behind it. The rules asked for a denominator but did not ask for the
   real count to lead.
3. **Implication lines could repeat the finding.** Nothing required them to explain why a
   finding matters to a reader who missed the point.
4. **The em dash appeared in plugin text.** It is a common sign of machine-written text.
5. **No one checked grammar, flow or tone.** `report-checker` checks numbers, length and
   visuals. Language quality was left to a human proofread late in the process.
6. **A session with an administrator role could change data.** On 19 November 2026, with
   secondary roles on, a `DELETE` on a source table ran successfully even though the
   analysis role held read access only. With secondary roles off, the same statement was
   refused. The read-only role alone was not enough.
7. **A new teammate had to work out setup alone.** Role, tools, token and the Profile were
   each documented, but in different places and in an order the person had to guess.

### Correct pattern

- Writing rules are blocking and apply to everything written for a reader (`AGENTS.md` §12).
- A separate agent, `writing-checker`, owns language quality. `report-checker` keeps numbers,
  length, visuals and traceability.
- Every analysis session starts with only the Profile's role active.
- One skill, `analysis-setup`, walks a new teammate through setup and asks them to act
  only when the agent cannot.

### Plugin actions taken

| File | Change |
|---|---|
| `AGENTS.example.md` §12 | New blocking rule: no jargon, explain the implication, counts before percentages, no em dash, plain sentences |
| `AGENTS.example.md` §3 | Run `USE SECONDARY ROLES NONE` before the first query |
| `AGENTS.example.md` §6, §8, §11 | Point to §12; `writing-checker` High issues are closed only by a fix; jargon, em dash and bare percentages are forbidden |
| `agents/writing-checker.md` | New read-only agent for grammar, flow, tone, ease of understanding and the writing rules |
| `agents/report-checker.md` | Language checks moved to `writing-checker` |
| `skills/report-writing/references/plain-writing.md` | Plain-words list, counts-first examples, how to write the Implication |
| `skills/report-writing/` | Standards row, Implication wording and handover checklist updated |
| `skills/analysis-setup/SKILL.md` | New instruction book for first-time setup |
| `skills/analysis-workflow/SKILL.md` | Runs setup first when needed; Review phase includes `writing-checker` |
| `tests/` | Contract tests for the new rules, the agent and the setup skill; a test that no em dash appears in any plugin file |

### Open

- `writing-checker` and `analysis-setup` have not yet been run by a teammate in a fresh
  session. Metadata and structure are tested; behaviour is not.

## Joint subscription report: decisions, charts and review rounds (November 2026)

Recorded while refining one report that joined three earlier studies, 19 to 24 November
2026. Study figures stay in the team's private analysis repository.

### Observations

1. **Reports ended in a to-do list.** The template's "What should happen next" table made
   most items "find out more", so a finished report looked unfinished.
2. **Proposed owners reached the report.** "Do not invent owners" did not stop the agent
   copying proposed owners from the pack and labelling them "proposed". That still reads
   as an assignment.
3. **The executive read failed although every check passed.** Read as a decision maker
   with five minutes, the first draft hid its most consequential number mid-paragraph,
   left it out of the summary, led with method and definitions, and gave two of four
   findings that were only warnings.
4. **Charts met the rules by adding text.** "Label population, period, unit and
   denominator; be readable without the text" was met with 5 to 10 line footnote blocks
   inside each image. The chart text added about 300 words and checkers disagreed on
   whether it counted.
5. **Two word counts for one report.** Checkers counted about 1,800 or about 2,100 words
   depending on chart text and markdown. The length limit was written in five places.
6. **Long coined labels, and one short label that overstated.** Accurate terms were heavy
   to read; the shorter "went through" claimed more than the records checked.
7. **Shortening dropped evidence that changed the answer.** Overall coverage of a field
   stayed in; much better coverage in a newer subset was cut. That changes "analyse the
   usable recent records" into "collect more first".
8. **Five review rounds.** Each rewrite drew new High issues and some fixes contradicted
   earlier ones (for example, whether an Implication may quote the finding's number, and
   whether counts-before-percentages applies to headings).
9. **Review status was not tied to a file version.** The writing check was not rerun after
   the last edits, and nothing recorded which version it had passed.

### Correct pattern

- Frame records what the analysis must settle. The report leads with the finding that
  most changes the decision and closes with "What this report supports": decisions, with
  exact roadmap status, and open questions only where they could change a decision.
- No owners, leads or teams in the report. Roadmap "covered" only when the item names the
  work.
- `report-checker` runs an executive read on the report and charts before anything else.
- A chart carries title, subtitle, axes, legend and data labels; caveats go beside it.
- One word counter, one place for the limit.
- The shortest familiar label that keeps what was measured.
- Checkers own one area each, cite a rule, do not reopen fixed issues without a change,
  and stop after two automatic rounds. Review verdicts record file hashes.

### Plugin actions taken

| File | Change |
|---|---|
| `AGENTS.example.md` | Profile: roadmap location, length counted by the script and set only here. §6 executive read. §7 labels, no owners, exact roadmap claims. §8 review hashes must match |
| `skills/report-writing/SKILL.md` | Lead rule, opening shape, caution-only section, labels, define in place with method after findings, limits state their consequence, "Shorten without changing the answer", "What this report supports" |
| `skills/report-writing/references/report-template.md` | New order; "What this report supports" replaces "What should happen next"; optional "Numbers not to over-read" |
| `skills/report-writing/references/visuals.md` | Five things on a chart; caveats in the caption; exception when leaving one out would mislead |
| `skills/report-writing/references/plain-writing.md` | New §2 labels with a "must not imply" table; churn and retention swaps name what was measured; count rule scope for tables and headings; Implication may quote the finding's number |
| `skills/report-writing/scripts/count_words.py` | New stdlib word counter used by every checker |
| `agents/report-checker.md` | Executive read first; meaning and decision-use checks; rule citations; re-review rule; file hashes in output |
| `agents/writing-checker.md` | Length moved to `report-checker`; count rule scope; rule citations; re-review rule; file hashes |
| `skills/analysis-workflow/SKILL.md` | Frame records what must be settled and roadmap items; Write and Review updated; two-round stop; recheck in proportion; pre-publish hash and link check |
| `skills/analysis-workflow/references/evidence-pack.md` | Optional `report/` folder; one named current report; review verdicts with hashes |
| `tests/` | Counter, single length source and report-closing contract tests; 13 new review cases |

### Open

- The new checker behaviour has not yet been run on a real report in a fresh session.
  Structure is tested; behaviour is not. The review cases above are the semantic check.
- The `footnotes()` helper sits in the study's own chart script, not in the plugin. Leave
  the preserved evidence as it is; new charts follow `visuals.md`.
