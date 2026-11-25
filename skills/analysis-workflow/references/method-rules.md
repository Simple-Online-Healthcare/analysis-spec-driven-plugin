# Method rules

Generic rules for designing and checking a descriptive analysis. `method-reviewer` checks
the design and SQL against these. Domain specifics (what counts as a repeat order, a
customer, a completed purchase) belong in the domain context file, not here.

## 1. State the study, completely

Every analysis states, in `methodology.md`:

| Item | What to say |
|------|-------------|
| Population | Who or what is included, and what is excluded, with the reason |
| Unit of analysis | What one row or count represents (people, accounts, orders, events) |
| Denominator | What every rate is divided by, kept when an outcome is absent |
| Dates | Entry window, observation cutoff (inclusive or exclusive, timezone) |
| Time anchor | The event follow-up is measured from |
| Follow-up | How long each unit is followed, per reported horizon |
| Exclusions | Each rule, with a count of what it removed |
| Definitions of record used | Named, with where they live |

Explain why a choice was made when the source documents the reason. When the reason is
undocumented, say so. Label a proposed rationale as interpretation, not history.

## 2. Counts mean one thing

- Say what a count represents. Do not let one label silently replace another (people vs
  records vs events).
- Do not call something a cycle, session, episode or cohort without defining it from the
  actual query. Do not rely on a mutable current value to define a past one.
- Replace vague words ("pattern", "signal", "cohort") with the exact observation or an
  ordinary-language definition.

## 3. Compare like with like

- Use **equal follow-up** for compared groups and horizons. Do not compare one day's
  percentage with a multi-day total as if both were daily rates.
- Require **full follow-up for each horizon reported.** Do not drop a recent unit from a
  short-horizon result only because a longer outcome is not yet mature.
- Compare comparable groups. Do not assign historical groups using today's status.
- Keep first-event rules, timezone and exact time boundaries consistent when repeating an
  analysis.
- When comparing periods, preserve numbering, eligibility and follow-up, and account for
  repeated entities appearing in both. Distinguish **reproducing a fixed historical
  population** from **checking a genuinely different period**. Never claim persistence
  across periods without that check.
- Describe stability as an observed comparison. A non-significant test is not proof of
  equivalence.

## 4. Keep the denominator

- A unit with no outcome stays in the denominator.
- An "any action" outcome is a **distinct union**, not the sum of overlapping categories.
  State whether categories overlap.
- Report counts alongside rates where sample size matters.

## 5. Missing data is a result

- Treat coverage of a field as a finding: separate available, linked, missing and
  unlinked.
- Never assign the latest recorded value to every past event, and never analyse only the
  known-value units as though they represent everyone.
- Do not use a coverage check whose group is defined through the thing being measured. If a
  group can only be identified through the outcome itself (for example, patients linked only
  through their orders), its rate is fixed by construction and is not evidence. Comparing a
  field's coverage between people who did and did not have the outcome, in a group defined
  independently of it, is allowed and is a finding (section 5).
- Check whether a newer, usable period exists before calling historical missing data a
  permanent limitation.
- Separate source capture gaps, ingestion gaps and transformation gaps before
  recommending engineering work. Check for reusable models first. Never claim that a
  snapshot restores overwritten history or observes every change between runs.

## 6. Association is not causation

- Keep association separate from causation. A preceding event is not a recorded reason.
- Do not describe an effect of an intervention without a design that supports it.
- State measured impact separately from potential opportunity. Never invent recovered
  revenue, retained customers or lift.
- Distinguish: what happened, why it may have happened, what action should be tested.

## 7. Separate kinds of knowledge

Keep these apart and label each:

1. a business rule (with provenance, for example a stated operating rule and its date),
2. a model classification,
3. an observed record,
4. a hypothesis,
5. an unverified assumption.

Record the provenance of a user-supplied rule in working notes. Do not erase it because
an event lacks a redundant field. Flag a genuine conflict between sources rather than
silently choosing one.

## 8. Intervals, tests and small counts

- Say how uncertainty was computed and what it accounts for (for example repeated units).
- Unadjusted pointwise intervals are not multiplicity-adjusted. Say so when it matters.
- Decide small-count handling in Design and record it. Do not report cells that identify
  individuals.

## 9. Reproducing and extending earlier work

- Name earlier work by subject when it supplies a finding ("A previous study of X
  found..."). Do not present an earlier period as current or merge different denominators
  silently.
- Do not describe routine revisions as competing studies.
- State when an earlier result was corrected and by how much.

## 10. Before saying a measure moved: mix and seasonality

Do not say a measure rose or fell over time until both checks below are done and written in
`methodology.md`. A movement that survives them is reported as a movement; one that does not
is reported as what it is.

**Mix.** Split the change into a change in who is counted and a change in the rate within each
group. Check, as they apply:

- marketing channel (including email and text message, and paid against unpaid);
- new against repeat (or logged in against not logged in, where that is the reliable signal);
- subscription against one-time purchase;
- drug or category.

Report the mix part as a range across both ways of setting up the split (weighting by the
earlier mix and by the later mix), because the two rarely agree. Say which groups drove it.
For a count (orders, conversions) rather than a rate, also report the size of each group:
growth in the number counted is a third part, separate from mix and from the rate.
State when a group's labelling changed during the period, because a labelling change looks
like a mix change.

**Seasonality.** The business has strong weekly and monthly cycles. Before calling a movement:

- compare whole weeks with whole weeks, and the same days of the week;
- compare with the same point in the month (pay day and month end move demand);
- look at the same weeks a year earlier where the history exists;
- mark known events (releases, experiments, promotions, changes in ad spend) on the timeline.

Judge a movement against the same days and weeks in comparable periods, not by its size
alone. A shift that holds across several comparable weeks is a change even when it is no
bigger than the usual weekly swing. A single week that differs by about the usual swing is
not yet a change; say so.

## 11. Experiments

When an analysis uses an experiment's result, the experiment method lives in the `cro-squad`
plugin, not here. Call `$cro-experiment-analysis`; it runs the health check
(`$cro-monitor`) and returns a result block with its route.

- **Standard route (default):** the pre-built experiment results with the confidence level,
  tail, direction and primary metric configured in Statsig. Do not override them.
- **Custom route:** allowed when the standard route cannot answer the question. Every
  departure is named in `methodology.md` and agreed in Design, and the skill's health warnings
  appear in the report beside the number they affect.
- No result is used before its health is known: sample ratio mismatch, missing events or
  metadata, whether it ran to completion, and power. A sample ratio mismatch voids the result.
- An experiment result is a randomised comparison. A before-and-after comparison of the same
  change is not, and is labelled as such.

If the `cro-squad` plugin is not installed, say so, do not rebuild the method by hand, and ask
the user how to proceed.
