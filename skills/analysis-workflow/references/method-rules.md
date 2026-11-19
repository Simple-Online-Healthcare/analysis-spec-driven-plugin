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
