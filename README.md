# analysis-spec-driven

A spec-driven data analysis workflow for agentic IDEs, shipped as a
[Cortex](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code) plugin. It
runs: **frame → design → run → verify → write → review → hand over**.

The problem it solves: when Cortex handles an analysis in one shot, there is no standard
way to decide what to analyse, how to approach it, how to keep the evidence so it can be
re-run, or how to write the report. This plugin gives every analysis the same shape.

- **Frame and Design** settle the question and the method with you, one decision at a
  time, each with evidence and a recommendation, before analysis queries run. Read-only
  exploratory queries may inform those decisions.
- **Run** saves every statement and aggregate result as an **evidence pack** committed to
  your analysis repository.
- **Verify** re-runs the saved SQL (or, when sources have moved, checks the saved results
  and SQL fingerprints) so a result can be trusted.
- **Write** produces a plain-English report for non-technical readers, with visuals, in
  1,500 words (hard maximum 2,000).
- **Review** uses independent read-only sub-agents. The workflow never merges a PR.
- **Setup** is built in: after installing, ask your agent to "set up the analysis
  plugin". It checks your tools, repository, Snowflake role and publishing access, fixes
  what it can, and tells you exactly what to do for the rest.

This plugin is **Cortex-only** and **domain-neutral**. Domain definitions (for example
what a "repeat order" means) live in your analysis repository's context files, not
here.

## What's in the box

| Component | Purpose |
|-----------|---------|
| `AGENTS.example.md` | The mandatory, blocking rules plus an **Analysis Profile** (the only team-specific block). Copy to your analysis repo root as `AGENTS.md` and edit the Profile. |
| `skills/analysis-workflow/` | The workflow skill. Routes by intent and runs the phases. |
| `skills/analysis-setup/` | The instruction book. Checks a new teammate's setup step by step and tells them exactly what to do. |
| `skills/report-writing/` | How reports are written: plain English, visuals, length, template, Confluence publishing. Includes `references/plain-writing.md`: the plain-words list and writing rules. |
| `agents/replay-verifier` | Re-runs saved SQL and compares to saved results. |
| `agents/method-reviewer` | Checks the design against the method rules. |
| `agents/report-checker` | Checks words, visuals, traceability and plain English. |
| `agents/writing-checker` | Checks grammar, flow, tone and ease of understanding, and enforces the writing rules (no jargon, counts before percentages, no em dash, clear implications). |
| `docs/field-feedback.md` | Every rule tied to a failure that was actually observed. Add to it. |

### Design principle

Three layers, each owning its content once:

- **Rules (always on)** → `AGENTS.md`
- **Workflow (user-triggered)** → the `analysis-workflow` and `report-writing` skills
- **Isolated checks (spawned)** → sub-agents in `agents/`

There are deliberately no hooks and no gate state. The sibling plugin
[`dbt-spec-driven`](https://github.com/Simple-Online-Healthcare/dbt-spec-driven-plugin)
removed its hook-based gates because they did not catch the mistakes that actually
happened. The same reasoning applies here: the controls are the Design questions, the
replay check and the independent reviews.

## Configuration: contribute, don't fork

Everything team-specific lives in one place: the **Analysis Profile** table at the top
of `AGENTS.md`. The skills, agents and numbered rules are generic and refer to Profile
values by name. To adopt the plugin you edit only your Profile, so improvements flow back
as contributions rather than forks.

## Requirements

- Cortex Code / Cortex Desktop.
- `git` and the GitHub CLI (`gh`, authenticated).
- A Snowflake connection with a read-only role for the data you analyse. Switch off all
  your other roles at the start of every session with `USE SECONDARY ROLES NONE`.
- An analysis repository with a place for evidence packs (set in the Profile).
- For publishing to Confluence: the Atlassian MCP tool. Image upload (route A) also needs
  a personal Atlassian API token stored as a Cortex secret named `ATLASSIAN_API_TOKEN`.
  Setup steps are in
  [`skills/report-writing/references/atlassian-token-setup.md`](skills/report-writing/references/atlassian-token-setup.md).
  Never commit the token. Without it,
  use route B (manual drag-in).
- For charts: Python 3 and `rsvg-convert`. For flowcharts: `node`/`npx` for the mermaid
  CLI, or draw them as SVG.

## Install

1. Copy `AGENTS.example.md` to the **root of your analysis repository** as `AGENTS.md`
   and edit the **Analysis Profile**.
2. Install the plugin into Cortex.
   - **From a local clone:** point the Cortex plugin manager at the clone, or place the
     directory in `~/.snowflake/cortex/plugins/`.
   - **From GitHub:** use the plugin manager's GitHub source for
     `Simple-Online-Healthcare/analysis-spec-driven-plugin`. The repository is public, so
     no sign-in is needed to download it.
3. Start a **new** session in your analysis repo (skills and agents only appear in a new
   session) and say: "set up the analysis plugin". The `analysis-setup` skill does the
   rest. When it reports you are ready, ask for an analysis or invoke
   `/analysis-spec-driven:analysis-workflow`.

## The workflow

1. **Frame**: the decision the analysis informs, the reader, the stage requested and what
   a "no change" answer would mean. A narrow question gets a short answer, not a study.
2. **Design**: one question at a time. Ends with the agreed design, each check marked
   Objective or Needs-human, and a **visual brief** saying what pictures the report needs.
3. **Run**: SQL, aggregate results and query IDs saved as the evidence pack; visuals
   generated from the results.
4. **Verify**: `replay-verifier` checks every results version and reports replay,
   provenance and cutoff outcomes. Failed, partial and unrun checks block handover;
   unrecoverable sources require documented passing fallback checks.
5. **Write**: the report, from verified results only.
6. **Review**: `method-reviewer`, `report-checker` and `writing-checker`.
7. **Hand over**: PR to the analysis repo. Publish to Confluence only with explicit
   permission.

## Contributing

This plugin is meant to be changed by the team as it is used.

1. Branch from `main`. The default branch is protected: changes need a PR with one
   approving review, and review threads must be resolved. Nobody bypasses this.
2. When a rule fails in real use, add an entry to `docs/field-feedback.md` (what
   happened, which rule or file changed, what changed) and fix it in the same PR.
3. Keep the Profile the only place with team-specific values.
4. Keep domain content (for example a particular product area or finance) out of this repo. It belongs in
   the analysis repository's `context/` files.
5. Keep real data out of this repo. Never add counts, rates, names or study results taken
   from your own data, even as an example or in the field-feedback log. They belong in your
   private analysis repository. Use placeholders such as `<N>` and `<total>` here.

## Roadmap

- **v2: AB tests.** A separate Design template (hypothesis, primary metric and
  guardrails, randomisation unit, power, sample-ratio check, stopping rule) and a readout
  path, reusing the `experimentation/` notebooks in the analysis repository.
- **Service identity** for unattended runs, only if scheduled analyses are wanted.
- **Machine-readable profile** (`profile.yml`) as an alternative to the Markdown table.

## License

MIT, see [`LICENSE`](./LICENSE).
