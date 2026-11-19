# Visuals

Every report has at least `max(1, Profile minimum)` visuals. Most
readers are non-technical, so a good picture is often what carries the finding. A table
alone does not count toward the minimum.

## Choose the visual in Design, not after

The **visual brief** is part of the agreed design. Decide what picture answers the
question before the analysis queries run, so they return the data it needs. Read-only
exploration may inform this choice during Design.

| The report needs to show | Use |
|--------------------------|-----|
| How a number compares between groups or periods | Grouped bar chart |
| How a number changes over time or over days since an event | Line or bar chart by time |
| How a total breaks into parts | Stacked bar (state the denominator) |
| A journey, process or decision path the reader must follow | Flowchart |
| Which step in a process loses the most | Flowchart annotated with counts, or a funnel bar |

One or two clear visuals beat a page of competing charts. Three is a typical maximum.
Use verified counts and derived values only. Never use illustrative numbers.

## Every visual must

- Have a plain-English title that states the finding or the question, not a code name.
- Use ordinary words everywhere, including subtitles, axis titles and footnotes. Do not
  put statistical or interval notation on the chart ("N", "[d, d+1)", "clustered
  inference"). Explain it in the sentence near the chart or in the pack.
- Label the **population, period, unit and denominator**.
- State whether categories overlap.
- Use direct labels or a plain-English legend. Avoid jargon.
- Keep percentages at a useful precision, with counts where sample size matters.
- Be readable without the surrounding text, and have one sentence nearby saying what it
  shows.
- Use a colour-blind-safe palette. The team's existing charts use `#0072b2` (blue) and
  `#b45309` (orange) on white with dark text.
- Have a text description (`<title>` and `<desc>` in SVG) so it is accessible.
- Be generated from saved results, never from numbers typed by hand.

## Charts: SVG from saved results, PNG for publishing

The team's existing studies build charts with the Python standard library only. Keep
that: no extra packages to install.

1. `render_visuals.py` reads the exact results versions mapped to each visual in
   `evidence_index.md`, including dated reruns, and writes SVG into `visuals/`. Record
   those input filenames; do not automatically choose the original or latest file.
2. It has a `--check` mode that verifies the existing SVGs match the results without
   rewriting them, and checks that no active or external content is embedded.
3. Convert for publishing:

   ```bash
   rsvg-convert -w 1600 visuals/chart.svg -o visuals/chart.png
   ```

   PNG is safer than SVG in Confluence.

The team's earlier studies include a worked example: a stdlib generator with a `--check`
mode (`render_tables.py`) that builds two SVG charts from saved aggregates.

## Flowcharts

Write the flow as mermaid text in `visuals/<name>.mmd`: readable, diffable and easy for a
teammate to edit.

```
flowchart LR
    stepOne[Plain-English step] --> stepTwo[Next step]
```

Render to PNG with the mermaid CLI, using an installed Chrome and skipping Puppeteer's
browser download. Create a `puppeteer.json` first. Keep it in `visuals/`, or anywhere else
and pass its **absolute path** to `-p`. Adjust `executablePath` if Chrome is installed
elsewhere.

```json
{"executablePath": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "args": ["--no-sandbox"]}
```

```bash
PUPPETEER_SKIP_DOWNLOAD=1 npx -y -p @mermaid-js/mermaid-cli mmdc -i visuals/flow.mmd -o visuals/flow.png --scale 2 -p visuals/puppeteer.json
```

Verified on macOS with mermaid-cli 12.2.0. Notes from that test:

- The CLI has no `-w` option in this version. Use `--scale`.
- Without the puppeteer config it fails looking for `chrome-headless-shell`. Either set
  `executablePath` to an installed Chrome as above, or install that browser with
  `npx puppeteer browsers install chrome-headless-shell` and then **omit** the config
  and `PUPPETEER_SKIP_DOWNLOAD`, so Puppeteer finds it itself. Do not point
  `executablePath` at a different browser than the one you installed.
- A left-to-right flow of six boxes renders as a thin banner. Prefer `flowchart TD` or
  fewer boxes so the text stays large enough to read in a report.
- If the CLI will not run on your machine, draw the flowchart as SVG with the same stdlib
  approach as the charts.

Keep flowcharts to one idea. Use plain words in the boxes, not field names. Mermaid
rules: no spaces in node IDs, quote labels containing brackets or punctuation. Put a
label with a line break in double quotes and use `<br/>`; the mermaid CLI renders it
(tested), although some other mermaid viewers show it as literal text. A top-down flow with
four branches and plain-English labels rendered clearly in the pilot.

## Size for the page, not the file

Readers see the visual inside a page column, so text that looks fine in the PNG can be tiny
on the page. In the Confluence test, a chart at 80% width and a six-box left-to-right
flowchart were both hard to read. So:

- Build charts with large text (the smallest label should still be legible at about
  700 px wide) and publish them at full column width.
- Keep a flowchart to about four boxes across, or use `flowchart TD` so it grows downwards.
- Look at the rendered page, not only the PNG, before delivery.
- For mermaid text size, put a config file beside the diagram and pass it with `-c`:
  `{"theme":"default","themeVariables":{"fontSize":"22px"},"flowchart":{"nodeSpacing":40,
  "rankSpacing":50,"padding":16,"wrappingWidth":520,"htmlLabels":true}}`. A bigger font alone
  wraps the text into narrow, very tall boxes, so raise `wrappingWidth` with it and keep each
  label to about two short lines. Check the result is wider than tall.
- Keep terms identical across the text, chart, flowchart and tables (for example "renewal
  cycles", not "renewals" in one place). Longer labels can collide on a chart: wrap them
  over three lines and look at the render.

## Inspect before delivery

Always view the rendered PNG (read the file) before it goes into a report or a PR. Check:
text is not cut off, labels do not overlap, the numbers match the results, and the title
and denominator are visible. Do not assume a sandbox image path exists. Verify it first.

## Saving

Save the chart/flow sources (`.svg`, `.mmd`) and the PNGs in `visuals/`. The generating
script, `render_visuals.py`, sits at the analysis folder root (see `evidence-pack.md`).
Confluence is a publishing target, not the source of truth.
