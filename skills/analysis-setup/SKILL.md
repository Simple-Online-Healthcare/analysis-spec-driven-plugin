---
name: analysis-setup
description: "First-time setup for a teammate who has just installed this plugin. Checks the tools, the repository, the Profile, the Snowflake role, and publishing access, fixes what it can, and tells the person exactly what to do for the rest. Use when: set up the plugin, getting started, first time, I just installed this, check my setup, is my setup ready, onboarding, role missing, cannot run analysis. Triggers: setup, set up, install, installed, onboarding, getting started, first time, check setup, ready to analyse."
tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "AskUserQuestion"]
---

# Analysis Setup: The Instruction Book

This skill gets a new teammate from "I installed the plugin" to "I can run an analysis"
with as little effort as possible. You, the agent, do the checking. You ask the person to
act only for the few things you cannot do yourself.

> **Authority:** `AGENTS.md` in the repository's top folder holds the rules and the **Analysis Profile**.
> Read the Profile first. Every value you check below comes from it. Follow `AGENTS.md`
> §12 in everything you write: plain words, no jargon, no em dash, counts before
> percentages.

## How to behave

- **Say what you are about to do** in one sentence before you start. Tell the person it
  takes about five minutes and that you will only ask for help when you cannot do
  something yourself.
- **One thing at a time.** Run a check. If it passes, say so in a few words and move on.
  If it fails, stop, explain the problem in plain words, give the exact fix, and wait.
- **Say who does what.** For each fix, say whether you will do it or the person must.
  If you will do it and it changes anything, ask permission first. If the person must do
  it, give the exact words or command.
- **Never ask for a password, a token or any secret in chat.** Never print one. If a step
  needs a secret, tell the person to enter it in their own terminal.
- **Change only what setup needs, and never commit, push or merge.** Setup may create
  `AGENTS.md` in the repository's top folder, only with permission.
- **Do not guess.** If a check cannot run, record it as "not checked" and say why.
- **Keep the result in chat.** Do not write a setup report to a file.

## The checks

Work through these in order. Use the Profile's values, not values from memory.

### 1. The plugin is switched on in this session

Skills and agents only appear in a **new** Cortex session after an install. If this skill
is running, the skills are working. Check the agents: the four agents are
`replay-verifier`, `method-reviewer`, `report-checker` and `writing-checker`.

- All four are available: pass.
- Any is missing: ask the person to close this chat, start a new session in the same
  folder, and ask again. Tell them that this is normal after a first install.
- Check the **`cro-squad`** plugin is installed and active, because experiment results
  come from its `$cro-experiment-analysis` skill (Profile, **Experiment method**). If it is
  missing or has not been updated recently, offer to install or update it. Without it,
  analyses that use experiments stop and ask rather than rebuilding the method.

### 2. The tools on this computer

Run each and read the result. Do not install anything without asking.

| Tool | Check | Needed for | If missing |
|---|---|---|---|
| Git | `git --version` | saving work | Ask the person to install Git, then re-run this step |
| GitHub command-line tool | `gh --version`, then `gh auth status` | opening pull requests | If not signed in, the person runs `gh auth login` in their own terminal (it asks questions, so it cannot run through chat) |
| Python 3 | `python3 --version` | building charts | Ask the person to install Python 3 |
| Chart converter | `rsvg-convert --version`, or Google Chrome installed | turning charts into images | Either works. On a Mac: offer `brew install librsvg` and ask permission, or use headless Chrome (see `report-writing/references/visuals.md`) |
| Node | `npx --version` | flowcharts (optional) | Optional. Flowcharts can also be drawn without it |

### 3. The analysis repository

- The current folder is the repository named in the Profile (**Evidence repository**).
  If not, ask the person to open the right folder.
- Check `git status`. If there are changes not yet saved to git, tell the person and ask
  what to do. Do not stash or discard anything without being told.
- The Profile's **Base branch** exists on this computer and on GitHub.
- `AGENTS.md` exists in the repository's top folder and has a completed Analysis Profile:
  no placeholder text, no empty value.
  - If `AGENTS.md` is missing: tell the person what it is (the team's rules and settings,
    in one file). Offer to copy `AGENTS.example.md` from the plugin to the repository's
    top folder.
    With permission, copy it, then ask the person to confirm the Profile values one row
    at a time, with your recommended value first. Do not commit it. Tell them it goes
    to the team through a pull request.
  - If it exists but values look wrong, list the rows and ask.

### 4. The domain context file

- The Profile names where domain context lives (for example `context/<domain>.md`). Check
  that a file exists for the subject the person plans to study.
- If none exists, ask which subject they will study. Do not invent definitions. The file
  only holds links to the team's agreed definitions. If those links are missing, tell the
  person who to ask, and record the check as "Needs you".

### 5. Snowflake: the right role and a safe session

This is the most important check. The Profile's **Warehouse and role** row says which role
to use.

1. Run `USE ROLE <role>`, using the role named in the Profile. Do not run any query
   before this. If Snowflake refuses, the person does not have the role yet. Tell them to
   ask their Snowflake administrator, and offer this message to copy:

   > Hello. I am setting up the team's analysis workflow. Please grant me the Snowflake
   > role `<role from the Profile>` so I can run read-only analyses. Thank you.

2. Run `USE SECONDARY ROLES NONE`. Explain in plain words: "Without this, other roles you
   hold could quietly give this session the power to change data. This keeps the session
   read-only." This must come before any query in every analysis session.
3. Run `select current_role(), current_secondary_roles(), current_warehouse()` and show
   the result. Pass only if the role and warehouse match the Profile and no other role is
   active.
4. Run one small read from a source named in the domain context file, for example a count
   with a date filter. It must succeed.
5. Check that a temporary table can be made in the scratch location the Profile names
   (**Scratch location**), then delete it. If the Profile gives no exact location, ask the
   person where their private working area is, and suggest adding it to the Profile. Say
   what you did.
6. Do not try to write to any shared or production object to prove it is blocked.

### 6. Publishing access (only if they will publish reports)

Ask: "Will you publish reports to Confluence?" If no, mark as "not needed" and skip.

- The Atlassian connection works: call the Atlassian tool that lists accessible sites.
- The token for image upload (route A in `skills/report-writing/references/confluence-publish.md`):
  run `cortex secret list`. It shows names only. Look for `ATLASSIAN_API_TOKEN`.
  - Found: pass.
  - Not found: tell the person that images can still be added by hand (route B), and
    offer to walk them through `skills/report-writing/references/atlassian-token-setup.md`.
    They must run the store command in their own terminal. You never see the token.

### 7. Ticketing

The Profile names the ticket system. Check that the tool for it answers (for example, look
up one ticket the person names). If it does not, mark it "Needs you" and say how to
reconnect. This is not a blocker for running an analysis.

## Finish

Show a short table in chat. Use only these four results: Ready, Needs you, Not needed,
Not checked.

| Check | Result | What happens next |
|---|---|---|
| 1 Plugin switched on | Ready / Needs you / Not checked | one line |
| 2 Tools | ... | ... |
| 3 Repository and Profile | ... | ... |
| 4 Domain context | ... | ... |
| 5 Snowflake role and safe session | ... | ... |
| 6 Publishing | Ready / Needs you / Not needed | ... |
| 7 Ticketing | ... | ... |

Then say, in plain words:

- If checks 1, 3, 4 and 5 are ready: "You are ready. Ask me for an analysis, for example:
  'Analyse how many customers reordered within 60 days.' I will ask you a few questions
  first, one at a time."
- If any of those four is not ready: name the single next step and who does it.

Close by reminding the person of two habits: start every analysis session with
`USE SECONDARY ROLES NONE`, and never share your access token for Atlassian.
