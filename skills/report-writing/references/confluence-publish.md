# Publishing a report to Confluence

Only with explicit permission from the user. Confluence is a publishing target: the report
and its visuals live in the analysis folder first.

## Page rules

1. **Search before creating.** Find the existing page for the study series. Reuse it.
   Never create numbered duplicates.
2. Preserve the approved page identity and hierarchy. Place new pages where the Profile's
   **Naming conventions** say: the named space (check the space key, not only its display
   name; a similarly named space is the commonest mistake), the named folder, and a
   plain-English title. A page in the wrong space cannot be moved across spaces by the API
   (403). For a **draft** nobody else has seen, recreate it in the right place and delete
   the wrong one. For a **published** page, ask the user to move it in the Confluence UI,
   which keeps the page and redirects its old link; check the old link still resolves.
   Recreate a published page only if the user chooses that, after being told which links
   would break.
3. Write the page link into the pack's `README.md` and `evidence_index.md` as soon as the
   draft exists, and name the repository and folder in the page's sources section, so a later
   move updates both ends.
4. Draft the page as a **draft** first (`status: draft`) when it is new. Publish the
   draft only after the user has seen it.
5. Add source links in plain words. Do not put ticket IDs in the body.
6. Use the Atlassian HTML format. Call `getContentFormatGuide` for the tool you are using
   before authoring the body.

## What the Atlassian MCP can and cannot do

| Capability | Status |
|------------|--------|
| Create and update pages and comments | Supported |
| Upload an attachment | **Not supported.** There is no upload tool. |
| Show an image on a page | Only if the file is already attached. The media node needs the file's media ID and collection, which must come from the upload response. Never invent them. |
| External image by URL | Supported, but the URL must open for every reader. A private repository URL will not. Do not use public URLs for company data. |
| Mermaid | Not rendered natively. Do not paste mermaid code expecting a diagram. |

## Route A: upload by REST, then embed with the MCP

> **Tested on 17 November 2026** on a throwaway draft in the DT space: both PNGs
> uploaded (HTTP 200), returned a file ID and a `contentId-<pageId>` collection, the MCP
> accepted the media embed, and a screenshot of the rendered page confirmed both images
> display. The test draft was then deleted. Always open the page and look at the images
> before telling the user it is done.

Needs a **personal** Atlassian API token held as a Cortex secret named
`ATLASSIAN_API_TOKEN`. It is never written to a file, a log or the repo. Each person uses
their own. **Full setup, checks and rotation are in `atlassian-token-setup.md`.** In short,
store it from your own terminal, so it never appears in a chat and never touches a file:

```bash
cortex secret store ATLASSIAN_API_TOKEN --prompt
```

1. Create or find the page and note its page ID. For a new page, create it as a **draft**
   first.
2. Upload each PNG as an attachment. Inject the token with `cortex secret run`, which
   keeps the value out of the conversation:

   ```bash
   cortex secret run --map ATLASSIAN_API_TOKEN=ATLASSIAN_API_TOKEN -- sh -c '
     printf "user = \"%s:%s\"\n" "<your-email>" "$ATLASSIAN_API_TOKEN" | curl -s -K - \
       -X POST -H "X-Atlassian-Token: no-check" \
       -F "file=@visuals/chart.png" \
       "<confluence-base-url>/rest/api/content/<pageId>/child/attachment?status=draft"'
   ```

   The credentials are passed to `curl` on standard input (`-K -`), so the token never
   appears in the command's arguments or in a process list. (`printf` is a shell
   builtin.) Tested: returns HTTP 200 against the DT space.

   Drop `?status=draft` when the page is already published.

   **Replacing an image on a reused page:** upload the new PNG under a **new filename**
   (for example `<slug>-chart-1-v2.png`) and update the page to point at it. This is the
   tested path. Confluence also offers `PUT .../child/attachment` to replace in place;
   that has not been tested here.
3. From the response, read `extensions.fileId` and `extensions.collectionName` (it is
   `contentId-<pageId>`).
4. Update the page with the MCP, using the media pattern from the HTML guide:

   ```html
   <figure data-type="media-single" data-layout="center" data-width="100" data-width-type="percentage">
     <div data-type="media" data-media-type="file" data-id="FILE_ID" data-collection="COLLECTION" data-alt="plain description"></div>
     <figcaption>One sentence saying what the image shows.</figcaption>
   </figure>
   ```
5. Fetch the page and confirm the images are in the returned body, then open the page and
   look at them.

### What the test found

- **The bash tool's `secret_env` parameter did not resolve the secret** in this
  environment (it returned an empty value for every secret). `cortex secret run --map`
  works. Use that.
- **Uploading to a draft needs `?status=draft`.** Without it the endpoint returns 404
  ("there is a content object with status: draft").
- **Confluence rewrites the embed to a filename reference** (`<ri:attachment
  ri:filename=...>`). The attachment is what matters, so keep filenames unique and
  meaningful, and do not re-upload under the same name by accident.
- **Size on the page matters.** At `data-width="80"` a wide chart's text was hard to read
  and a six-box left-to-right flowchart was too small to read. Use `data-width="100"` for
  charts, make chart text large when you build the SVG, and keep flowcharts to about four
  boxes across, or top-down.
- **Delete a test draft with the REST API**, because the MCP has no delete tool:
  `DELETE <confluence-base-url>/rest/api/content/<pageId>?status=draft` (returns 204).
- The token needs no extra scopes for this: a normal personal Atlassian API token worked.

## Route B: manual drag-in (fallback, always available)

1. Create the page (or update it) with the MCP, leaving a clearly labelled gap per image:
   a heading-free paragraph reading `[Image: <file name>: <what it shows>]`.
2. Give the user the PNG paths.
3. The user drops each PNG into place in Confluence and deletes the placeholder.
4. Ask the user to confirm, then fetch the page to check the placeholders are gone.

## After publishing

- Add the page link to `evidence_index.md`. Commit that update with the ticket ID, if
  any, and push the analysis branch; add the same link to the PR description. Use existing
  source-control authorization or ask if absent. If not authorized, leave the change
  local and report the pending handover; never push directly to the base branch or merge.
- Do not edit published pages again without permission.
- Report anything unexpected (image missing, layout broken) to the user plainly.
