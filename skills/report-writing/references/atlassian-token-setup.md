# Setting up your Atlassian API token

Needed only for **route A** (automatic image upload to Confluence). Without it, use route B
(drag the images in by hand). See `confluence-publish.md`.

Each person uses **their own** token. Never share one, never commit one, never paste one
into a chat. The token acts as you: anything it can do, you can do, and anything it does is
recorded as you.

## What you need first

- Access to the Confluence site and the space you will publish to (the Profile names them).
- Cortex Code with the `cortex` command on your path (`cortex secret --help` should work).
- The Atlassian email address you sign in with. The upload uses it as the username.

## 1. Create the token

1. Open your Atlassian account's API tokens page:
   `https://id.atlassian.com/manage-profile/security/api-tokens`
   (Profile picture, **Manage account**, **Security**, **Create and manage API tokens**.)
2. Choose **Create API token**.
3. Give it a name that says what it is for, for example `cortex-confluence-upload`.
4. Choose an expiry. Atlassian requires one and limits how long it can be, so pick the
   shortest that suits you and put a reminder in your calendar to renew it.
5. Choose **Create**, then **Copy** the token. It is shown **once**. If you lose it, delete
   it and create another.

Leave the page open until step 2 is done, so you can copy again if the clipboard changes.

## 2. Store it as a Cortex secret

Run this in **your own terminal**, not in a chat. It asks for the token and does not show
what you paste, so the token is never typed into a chat and never written to a file:

```bash
cortex secret store ATLASSIAN_API_TOKEN --prompt
```

Paste the token when asked and press Enter. Nothing appears on screen as you paste. This
works the same on macOS, Linux and Windows.

- **It needs an interactive terminal.** If you run it through a chat tool's `!` shortcut,
  or in a script, it cannot read your input and nothing is stored. Open a real terminal.
- **Do not use a file.** An earlier version of this guide wrote the token to a temporary
  file and deleted it afterwards. If the store step failed, the file stayed on disk, so
  that method was removed. If you have a leftover `~/.atlassian-token`, delete it.

Then **copy any other text** so the token is no longer on your clipboard.

The secret name must be exactly `ATLASSIAN_API_TOKEN`. The skills refer to it by that name.

## 3. Check it worked

Confirm the key exists. This lists names only, never values:

```bash
cortex secret list
```

Then make one **read-only** call that proves the token authenticates. Replace the email and
the base URL with yours (the Profile holds the base URL):

```bash
cortex secret run --map ATLASSIAN_API_TOKEN=ATLASSIAN_API_TOKEN -- sh -c '
  printf "user = \"%s:%s\"\n" "you@yourcompany.com" "$ATLASSIAN_API_TOKEN" \
    | curl -s -K - -o /dev/null -w "HTTP %{http_code}\n" \
      "https://yourcompany.atlassian.net/wiki/rest/api/space"'
```

| Result | Meaning |
|--------|---------|
| `HTTP 200` | Working |
| `HTTP 401` | Wrong email, an expired or deleted token, or an empty secret. Redo step 2 and check the email is the one you sign in with. |
| `HTTP 403` | The token works, but your account cannot see that resource |
| `HTTP 404` | Wrong base URL. It ends in `/wiki` for Confluence Cloud |

How the token is passed matters. The command above hands the credentials to `curl` on
standard input (`-K -`), so the token never appears in the command's arguments, where a
process list could show it.

## 4. Use it

Follow route A in `confluence-publish.md`. Always inject the token with
`cortex secret run --map`. In testing, the bash tool's `secret_env` option returned an empty
value, so do not rely on it.

## Keeping it safe

- **Expiry:** renew before it lapses. A lapsed token shows up as `HTTP 401`.
- **Rotation:** to replace it, repeat steps 1 and 2. Storing the same name again overwrites
  the old value. Then delete the old token on the Atlassian page.
- **Suspected leak:** delete the token on the Atlassian page at once, then create a new one.
  Tell your team lead if it appeared in a log, a chat, a commit or a screenshot.
- **Leaving the team or changing laptop:** delete the token on the Atlassian page, and run
  `cortex secret delete ATLASSIAN_API_TOKEN` on the old machine.
- **Scope of access:** a normal personal token carries your own permissions. It was enough
  to upload and embed images and to delete a draft page it had created. Use an account that
  has only the Confluence access you need.
