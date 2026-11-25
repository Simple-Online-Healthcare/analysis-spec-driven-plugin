# Plain writing

The writing rule is `AGENTS.md` §12. This page shows how to meet it. Use it when you write,
and when you check someone else's writing.

The test: could a colleague from another team read this once, without help, and explain it
back? If not, rewrite it.

## 1. Swap jargon for plain words (the plain-words list)

Jargon is any word or short phrase that only a specialist knows. It is prohibited. Use the
plain version. If a technical term cannot be avoided, say what it means in brackets the
first time.

| Instead of | Write |
|---|---|
| cohort | the group of people who ... (say who, and from when to when) |
| denominator | the total number of people counted |
| numerator | the number of people who did the thing |
| cutoff | the date after which nothing was counted |
| baseline | the starting level, before the change |
| attrition, churn | people who left or stopped |
| retention | people who stayed |
| conversion | people who went on to do the next step |
| segment | a group of customers who share something (say what) |
| population | everyone who could have been counted (say who) |
| follow-up period | how long each person was watched |
| time anchor | the date each person's clock starts from |
| unit of analysis | what one row of the count stands for, such as one person or one order |
| null, missing | blank, not recorded |
| outlier | a value far from all the others |
| significant | clearly bigger than chance alone would explain (or avoid, and give the numbers) |
| correlation | the two moved together (this does not mean one caused the other) |
| causal, causes | made this happen (only use when the design proves it) |
| aggregate | a total or count for a group, with no individual records |
| deduplicate | remove repeated records of the same thing |
| join, merge | match records from two lists |
| pipeline, ingest | the steps that bring data in |
| query, SQL | the saved search of the data |
| schema, table, field | avoid in reports; say "the data" or name what it holds |
| sensitivity check | a second run with one choice changed, to see if the answer moves |
| edge case | a rare situation |
| n | the number of people (write the number) |
| YoY, MoM | compared with the same period last year, compared with last month |
| KPI | the measure the team tracks (name it) |

Words that sound clear but say nothing also count: "pattern", "signal", "trend", "driver",
"insight". Replace each with what you actually saw, when, and for whom.

## 2. Counts first, percentages second

Always give the real number and the total. A percentage on its own hides how many people
stand behind it.

| Weak | Strong |
|---|---|
| 23% cancelled | `<N>` of `<total>` customers cancelled (23%) |
| Rate rose by 4 points | `<N1>` of `<total1>` last quarter, `<N2>` of `<total2>` this quarter |
| Most customers stayed | `<N>` of `<total>` customers stayed |

- Put the percentage in brackets after the count. Never alone.
- When two groups have different sizes, show both counts so the reader can see the sizes.
- Charts and tables: label the axis or column with the count, and add the total in the
  title or caption.
- Small counts: say so. "Only `<N>` people" tells the reader how much weight to give it.
- Do not round a count. Round a percentage to a whole number unless the difference matters.

## 3. Write the implication as if the reader missed the point

The **Implication** line answers three questions in plain words:

1. What does this finding mean for the business?
2. Why does it matter, and to whom?
3. What happens if nobody acts, or what should be checked next?

Do not repeat the finding in new words. Do not assume the reader saw why it matters.

| Weak | Strong |
|---|---|
| Implication: Cancellations are high on day one. | Implication: `<N>` of `<total>` customers are gone before a second order. Any plan that counts on repeat orders starts from a smaller group than it looks. Nothing here shows why they left, so the next step is to find out. |

Keep the claim inside what the evidence shows (`AGENTS.md` §7). Say "this suggests" or
"nothing here shows why". Do not say "this means" when the design cannot prove it.

## 4. Punctuation and sentences

- **No em dash.** Do not use the long dash, and do not use two hyphens in its place. Use a
  full stop, a comma, a colon or brackets.
- One idea per sentence. Aim for 20 words or fewer. The `writing-checker` flags anything
  over 30. Split anything longer.
- Active voice: "The team counted 1,800 customers", not "1,800 customers were counted".
- Put the main point first, then the detail.
- Say what a number counts: people, accounts, orders or events.
- Spell out an abbreviation the first time. Avoid ones the reader may not know.
- Use "to" for a range in running text: "10 to 14 days".

## 5. Tone

- Calm, direct and neutral. No hype ("huge", "alarming"), no hedging pile-ups ("may
  possibly suggest").
- Reports use the third person ("The study found ..."), not "I", "we" or "you". Chat and
  instructions may speak to the reader directly.
- Say plainly what is not known. Do not hide a limit in a footnote.
- Respectful of the reader: explain, do not lecture.

## 6. Say exactly what was measured

- **Use the business word of record for the outcome.** If the measure is conversion, write
  "convert" and "conversion rate" throughout. Do not drift into "pay", "buy" or "sign up",
  which each mean something narrower.
- **Define the counting unit once, then keep one word for it.** For example: "a user is one
  web browser on one device, which is how the experiment assigns groups". After that, write
  "users", not "browsers", "visitors" and "people" in turn.
- **Do not claim a state the data cannot see.** "Every user was signed in" is wrong if
  accounts are created part-way through the journey. Say what is recorded ("every user has a
  patient record, created during the assessment").
- **Results tables show one number per cell.** Rates in the cells, counts in the caption or
  a total row. A cell like "2,555 / 5,592 (45.7%)" is too busy to read in a table.
- **Experiment results use one fixed table shape:** the rate per group, the relative
  difference, then a row for the p-value to three decimal places marked "(statistically
  significant)" or "(not statistically significant)" at the stated level, and a row for the
  likely range at the stated confidence. Say whether the test was one-sided. Write "below
  0.001" for smaller p-values, and give a fourth decimal place when three would round onto
  the bar (0.0996 against a 0.10 bar, not 0.100); the label always follows the unrounded
  value.
- **State the consequence as the condition to break even.** "Lifetime value per new customer
  must rise by at least 16% to stand still" is checkable. Multiples that cancel out of the
  calculation (2x, 3x return on spend) add nothing.

## 7. Before you hand text over

- No jargon left, or each remaining term explained in brackets.
- Every finding has an Implication that stands on its own.
- Every percentage has its count and total beside it.
- No em dash anywhere.
- Each paragraph reads on its own, and each sentence leads to the next.
- Hand the text to `writing-checker` for a second reading.
