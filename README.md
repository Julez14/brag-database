# Brag Database

Turn past applications and interview prep into a personal library you can reuse.

Brag Database is designed to help you answer questions for jobs, clubs, scholarships, and programs using your own experiences. Write notes naturally in Obsidian, sync them to your own cloud storage, and ask Codex to draft an answer using what you've already written.

Every application adds to your library. A story you prepared for “Tell me about a difficult teammate” can resurface when you're asked “How do you handle disagreement?”—even when the wording is different.

## Using your library

1. **Write in Obsidian.** Keep one note per application or position you're preparing for. Include the questions, your answers, and any rough notes. Use prose or bullet points, whichever works for you.
2. **Let it sync and index.** Your notes sync to your own Cloudflare storage, where AI Search makes them searchable by wording and meaning.
3. **Ask Codex for help.** Give it the new question, the opportunity, and any word limit. It searches your cloud library and drafts an answer with references to the notes it used.
4. **Review your saved draft.** Codex saves the questions and answer in the appropriate Obsidian folder. Edit the response, submit it yourself, and keep the final version for next time.

For example:

> Use my brag database to draft a 200-word answer to “Describe a time you showed initiative” for a student leadership application.

You keep control of your writing. The goal is to reuse real details, preserve your voice, and flag missing information instead of inventing achievements. Cloud search makes the same library available from any machine with Codex connected to it.

## How it works

| Product | What it does for you |
| --- | --- |
| **Obsidian** | Gives you a familiar place to write and edit Markdown notes. |
| **Remotely Save** | Syncs your notes across devices through Cloudflare, without Obsidian Sync. |
| **Cloudflare R2** | Stores your notes in your own cloud bucket. |
| **Cloudflare AI Search** | Indexes your Markdown and finds relevant passages by wording and meaning. |
| **Cloudflare MCP** | Gives Codex authenticated access to your cloud library. |
| **Codex + the brag-database skill** | Uses past experiences to draft answers and saves them in the right Obsidian folder. |

Your notes need to finish uploading and indexing before Codex can find the latest changes. Obsidian handles local writing; cloud storage and search make the library available from other machines.

## Get started

[Follow the setup guide](docs/setup.md) to install the skill and connect your own Obsidian vault, Cloudflare R2 bucket, and AI Search instance. Obsidian Sync is not required. Personal notes stay outside this public repository.
