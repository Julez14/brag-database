# Set up your library

You need Obsidian, Codex, Python 3.10 or newer, and your own Cloudflare account. Keep your private vault separate from this public repository.

## Install the skill

```sh
git clone https://github.com/Julez14/brag-database.git
cd brag-database
python3 scripts/install.py --vault "$HOME/path/to/your-vault"
```

The installer links the `brag-database` skill into Codex and stores machine-specific settings in `~/.config/brag-database/config.json`. It does not upload notes or create cloud resources. The default destination folders are Career, Clubs, Scholarships and Grants, Hackathons, School, and Interview Prep.

## Connect Cloudflare MCP

```sh
codex mcp add cloudflare-api --url https://mcp.cloudflare.com/mcp
codex mcp login cloudflare-api
```

Select the intended personal Cloudflare account. The authenticated connection is used to search AI Search privately; do not enable a public AI Search endpoint or make the R2 bucket public.

## Configure Obsidian sync

Create a private R2 bucket. Create R2 S3 credentials scoped to that bucket with Object Read & Write permission. In Obsidian, install and enable Remotely Save, then use:

| Setting | Value |
| --- | --- |
| Service | S3 |
| Endpoint | `https://<ACCOUNT_ID>.r2.cloudflarestorage.com` |
| Region | `auto` |
| Bucket | Your R2 bucket |
| Remote prefix | `vault/` |
| Encryption | Off; AI Search needs readable Markdown |
| Sync direction | Bidirectional |

Put the access key and secret into the plugin settings only. Start with a disposable test vault and prefix, verify upload/download/edit/rename/delete behavior, then use `vault/` for your real notes. After the first successful sync, enable sync on save, five-minute automatic sync, and a startup sync delay. Obsidian must be open and awake for local changes to upload.

Two-way sync propagates deletions, so keep a separate backup. Avoid editing the same note on two devices at once.

## Configure AI Search

Create an AI Search instance connected to the R2 bucket. Enable both vector and keyword indexes. Use `vault/` as the source prefix, include Markdown files, and exclude `.obsidian`, templates, trash, and underscore-prefixed files. A one-hour sync interval is a reasonable starting point. Keep public endpoints off.

The equivalent API settings are in [config/ai-search.example.json](../config/ai-search.example.json). A separate Workers AI generation step is not required: AI Search retrieves passages and Codex writes the answer.

Record the actual resources locally:

```sh
python3 scripts/install.py --vault "$HOME/path/to/your-vault" \
  --account-id YOUR_ACCOUNT_ID --bucket YOUR_BUCKET \
  --namespace default --instance brag-database --prefix vault/
```

R2 upload and AI Search indexing are separate. A newly saved note becomes searchable after the next indexing job; trigger a sync manually when needed.

## Use it

Open a new Codex conversation and ask:

> Use my brag database to answer “Tell us about a time you handled disagreement” for the Example Club committee application. Maximum 200 words. Save it in my vault.

Codex searches the configured cloud index, drafts from supported evidence, and saves the questions and answer in the appropriate Obsidian folder. It marks new work as a draft and never submits an application.

On another device, install the skill, configure Remotely Save with the same bucket/prefix, and authenticate Cloudflare MCP. Cloud retrieval is shared; local paths only determine where new drafts are saved.

## Troubleshooting

- No cloud results: check R2 objects, AI Search job status, and the configured account and instance.
- Recent note missing: check Remotely Save first, then the latest AI Search job.
- Existing note changed: the save helper refuses stale revisions; reread and merge before retrying.
- Skill missing: confirm the repository remains at the install location and open a new Codex conversation.
