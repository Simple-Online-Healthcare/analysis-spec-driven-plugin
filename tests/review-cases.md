# Review-contract checks

Run `python3 -m unittest discover -s tests -v` for structural regressions. These checks
do not prove agent behavior. For a semantic check, give an independent reviewer the
rules and the scenarios below, without executing warehouse queries or publishing pages.
Ask for the verdict, overall status and gate outcome with the rule that determines it.

Assume a complete pack and matching fingerprints/cutoff unless a case says otherwise.

| Scenario | Expected result |
|---|---|
| All outputs replay unchanged; no shared base | MATCH, base NOT USED, ALL MATCH; verification passes |
| Rows match but SQL hash differs | CHECK FAILED, CHECKS FAILED; blocked |
| One shared base differs; two dependent topics match | Both dependent steps CHECK FAILED; blocked |
| Rows match but hash method is unknown | Fingerprint CANNOT BE CHECKED, NOT RUN, INCOMPLETE; blocked |
| Half the output matches a restricted diagnostic query | MATCH (partial), INCOMPLETE; blocked; diagnostic hash is separate |
| Source watermark advanced but original history is still available; rows differ | MISMATCH; blocked |
| Original run was non-atomic but a complete replay matches | MATCH, ALL MATCH; verification passes |
| Required history expired, no snapshot exists; saved aggregate fallback checks pass | NOT REPLAYABLE, PARTLY NOT REPLAYABLE; verification passes with documented limits |
| Same expired-history case but saved rate disagrees with counts | CHECK FAILED, CHECKS FAILED; blocked |
| Results file is missing; available SQL has no known failing check | NOT REPLAYABLE, INCOMPLETE; missing pack file blocks |
| SQL file is missing; fallback rate disagrees with counts | CHECK FAILED takes precedence; blocked; fingerprint unavailable also recorded |
| A changed SQL file is given a new hash without a new execution | Not a valid repair; restore original SQL or execute and save a new version |
| SQL/base hash differs or is uncheckable before replay | Do not execute; CHECK FAILED for a difference, NOT RUN for unknown metadata; missing files follow missing-file precedence |
| Current SQL differs but a retained revision and base match recorded hashes and cutoff | Replay the retained matching revision, not the current files |
| Fallback changes NOT REPLAYABLE to CHECK FAILED | Preserve both passing and failing fallback evidence in the report |
| Failed original is explicitly superseded; independently verified replacement supplies every affected claim, chart and downstream result | Current evidence can pass; preserve and report the original failure separately as resolved by the replacement |
| Original is labelled superseded but replacement is unverified or an affected chart still uses the original | Original failure remains in gate scope and blocks |
| Historical JSON lacks SQL revision; index maps it to a retained revision whose hash matches | Use the index mapping without rewriting original JSON |
| Legacy results use a hyphenated date, such as `topic_results_2026-11-17.json` | Include them in inventory and verify against their recorded SQL revision |
| Report's period is in methodology, not result rows | Design date is traced, not High |
| Report and chart cite a rerun, original results differ | Check the cited rerun and name it in output; no automatic substitution |
| Two results files conflict and the report/index do not choose one | High traceability issue |
| Profile minimum is zero and report has zero visuals | High |
| Profile minimum is two and report has one visual | High |
| Report contains anonymous record-level entries or sensitive free text | High; no PASS; give location and redacted excerpt without reproducing private content |
| User requests replacement of a failed results file | Save a new version and supersession record; keep the original unchanged |
| Two reruns start in the same second | Distinct UUID names; exclusive creation prevents overwriting |
| Published page link exists only locally | Handover incomplete until authorized branch push and PR-description update |
| Text contains an em dash | writing-checker High; report cannot pass |
| Text says "23% cancelled" with no count and total | writing-checker High; suggested rewrite shows the count and total, then the percentage in brackets |
| Text says "412 of 1,830 customers (23%)" | Passes the count rule |
| A finding's Implication only repeats the finding | writing-checker High |
| A finding has no Implication | writing-checker High |
| Jargon such as "cohort" appears with no plain wording or bracketed explanation | writing-checker High |
| A sentence of 34 words, otherwise clear | writing-checker Medium |
| Correct text with one doubled word | writing-checker Low |
| writing-checker suggests a rewrite that needs a fact the text lacks | It names the missing fact and does not invent one |
| A short label ("went through") is used where only payment records were checked | report-checker High: the label says more than was measured; fix names the records checked |
| Summary omits the finding that most changes the decision | report-checker High: executive read fails |
| Summary leads with the largest number; a smaller confirmed failure that drives the decision appears second | report-checker Medium: lead chosen by size |
| "No matching message record" is rewritten as "these patients were not messaged" | report-checker High: missing record presented as a confirmed failure |
| A shortened draft drops a newer period whose usable data changes the recommendation | report-checker High: cut evidence would change the recommendation |
| A related roadmap item does not name the work; the report says it "will be done soon" | report-checker High (`AGENTS.md` §7); fix: "related, not covered by `<item>`" |
| The decisions table names a proposed owner or lead | report-checker High (`AGENTS.md` §7) |
| An open question would not change any decision | report-checker Medium: move it to the pack |
| A chart image holds a five-line block of definitions | report-checker Medium: move them to the caption |
| A table caption gives the total; cells show counts and percentages | Passes the count rule |
| Review hashes in the evidence index differ from the current report | Gate not met (`AGENTS.md` §8); run the recheck that matches the edit |
| Re-review: an issue marked Fixed, text unchanged, checker now prefers other wording | Not reopened and not raised again |
| Clear, accurate report within length, every claim traced | PASS; no High or Medium issues and no rewrites beyond optional Low ones |
| New teammate starts a session before the plugin is registered | analysis-setup asks for a new session and does not continue |
| Session still has other roles active | analysis-setup runs `USE SECONDARY ROLES NONE` and confirms only the Profile role is active before any query |
| Person lacks the Profile's Snowflake role | analysis-setup gives a ready-to-send message for the administrator and marks the check not ready |
| Person will not publish to Confluence | analysis-setup marks publishing "not needed" and skips the token step |
| Token is not stored | analysis-setup offers the guide and tells the person to enter it in their own terminal, never in chat |
