# Evidence pack

The evidence pack is the committed record of an analysis: enough to see exactly what was
asked, run, found and checked, and to re-run it. It follows the shape already used by the
team's earlier studies. Aggregate results only. No personal or record-level data.

## Layout

```
analyses/<dd-mm-yy>-<slug>/
  methodology.md             question, decision, reader, agreed design, definitions, limits
  study_base.sql             shared base CTEs reused by the queries below (if any)
  <topic>.sql                one file per analysis step, exactly as executed
  <topic>_results.json       saved aggregates for that step
  <topic>.md                 optional: plain notes on that step
  evidence_index.md          navigation and provenance for every artifact
  final_verification.md      what was checked, what was not, what remains limited
  executive_study.md         the report (see report-writing)
  report/                    optional: a report rewritten after verification, with its charts
  visuals/                   PNG, SVG and flow-diagram source used in the report
  render_visuals.py          stdlib script that builds the visuals from saved results
```

`<topic>` names a step in plain words (`completeness`, `reasons`, `main_comparison`). Keep
the same stem across the `.sql`, `_results.json` and `.md` of one step.

## What each file must contain

### methodology.md
The question, the decision informed, the alternatives considered, what the analysis must
settle, what is out of scope, the reader and the stage requested; the agreed
design from the Design phase (decisions, population, unit, denominator, dates, cutoff,
follow-up, exclusions, Done-when checks, visual brief, small-count handling); known
limits. Ticket IDs belong here, not in the report.

### `<topic>.sql`
The statements exactly as executed, in run order, each preceded by an intent comment
(`AGENTS.md` §9). If a statement relies on a shared base, say which part of
`study_base.sql` it uses.

### `<topic>_results.json`
- `purpose`: one line
- `cutoff`: the observation cutoff with timezone and whether it is inclusive
- `query_id`, `executed_at_utc`, `sql_sha256` and `sql_hash_method` for each statement
- `base_sha256`: SHA-256 of the bytes of `study_base.sql` as it was at run time, if the
  step uses a shared base
- `schema`: column names and types of each result
- `rows`: the aggregate rows (counts, rates and denominators together)
- `source_freshness`: latest timestamp seen in each source at run time
- `code_revision`: the dbt or definition revision used, if any
- `run_id`: a UUID generated once per execution; reuse it for that execution's results
- `sql_revision`: the retained Git revision containing the executed topic SQL and base
  when a later run changes them; the recorded hashes must match that version

For a historical results file without `sql_revision`, record a verified hash-matching
revision mapping in `evidence_index.md` rather than editing the original JSON. The verifier
uses that mapping. If no matching revision is available, record the unavailable check.

No individual-level values, identifiers or free text.

### evidence_index.md
A table of every artifact and what it establishes; versions and dates (cutoff, windows,
revisions, hashes); the **execution boundary** (what this pack ran, what it only read,
what it did not do); scratch objects created; known limits. Map every report claim and
visual to the exact results filename and its SQL/base revision. Mark superseded results
with the correction, reason and replacement file using the verifier's **Gate scope** rule;
preserve their original verdicts rather than silently substituting or hiding failures.

Name the **current report**: one path, so nobody has to choose between drafts. Under
"Review", record each checker's verdict with the SHA-256 of the report and chart files it
checked. A file whose hash no longer matches needs the matching recheck.

### final_verification.md
Written after Verify and Review: the verdict per results version using **Verdict rules**
in `agents/replay-verifier.md`, what was recomputed independently, corrections made and
their size, and the limits that remain. State plainly what was **not** checked.

### executive_study.md
The report. See the `report-writing` skill. Measured values come from their cited saved
results version; design dates come from `methodology.md` or the executed SQL.

### visuals/ and render_visuals.py
Visuals are generated from the saved results by the script. The script has a `--check`
mode that verifies the existing outputs match the results without rewriting them. See
`report-writing/references/visuals.md`.

## SQL hashing (one procedure)

New packs use `sql_hash_method: "file-statement-v1"`:

- Each statement in `<topic>.sql` sits under a header line `-- statement: <id>`.
- The hash is the SHA-256 of the statement's UTF-8 text as saved in the file, **including
  its intent comments**, excluding the header line, with leading and trailing whitespace
  trimmed and one trailing semicolon removed.
- The same procedure is used when saving and when verifying, so a comment edit changes the
  hash. Preserve executed SQL, including its comments. If it changes, keep the original
  revision and execute and save a new results version; do not replace the original hash.

An older pack may record a different `sql_hash_method`. The verifier follows the method the
pack states, and reports it. If the method is missing or unclear, the fingerprint check is
"cannot be checked", not MATCH.

## Rules for the pack

- A result without its SQL, or SQL without its saved result, is incomplete.
- Query text, hashes and joins stay in the pack. The report links to them in plain terms.
- Originals are preserved. If a result is corrected, record the correction in
  `final_verification.md` and keep the original file unchanged. Handle a request to
  replace a failed result by saving a new results version and recording its supersession,
  not by overwriting the original evidence.
- Do not commit: record-level extracts, screenshots of dashboards with real data, working
  notes, tokens, or temporary scratch exports.
- If the same step is re-run later, add
  `<topic>_results_<yyyymmddThhmmssZ>_<run_id>.json` beside the original. Use the UTC start
  time and the execution's UUID, so runs starting in the same second have different names.
  Create the file exclusively; if it already exists, stop rather than overwrite it.
- Inventory also recognizes earlier `<topic>_results_<yyyy-mm-dd>.json`,
  `<topic>_results_<yyyymmdd>.json` and
  `<topic>_results_<yyyymmddThhmmssZ>.json` files; do not rename historical evidence.
  Pair each results file with `<topic>.sql` and any base at its recorded revision. If
  SQL changes, retain the original revision and record `sql_revision` for each version;
  do not check old results against new SQL. The verifier checks every version.

## Sizing

Keep `<topic>_results.json` as small as the report needs. Large intermediate aggregates
can stay in the warehouse if the pack records how to recreate them and their hash.
