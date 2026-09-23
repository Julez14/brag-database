# Agent instructions

## Purpose and current state

Build a personal, cloud-searchable memory of application answers and interview preparation. The user writes freely in Obsidian and expects future applications to benefit from previous work. Follow the latest explicit user instructions when they change this design.

This repository starts with documentation only. Do not describe integrations, infrastructure, tests, or deployments as completed until they actually exist. Read README.md for the product breakdown and update it as implementation progresses.

## Documentation audience

README.md is a concise introduction for someone who wants to clone and use the project. Explain the purpose, value, intended user workflow, and how the products work together in plain language. Keep planning, technical constraints, and roadmaps in AGENTS.md. Add usable setup instructions to the README when installation actually works; do not invent commands or imply the documented design is already implemented. Preserve the public repository's user-facing focus.

## Accepted architecture

- Obsidian edits ordinary local Markdown, usually one file per application or position's interview preparation. Preserve flexible writing; do not require a structured form or an AI conversation to add notes.
- Remotely Save syncs the vault with private Cloudflare R2. Do not introduce Obsidian Sync as a paid dependency.
- R2 holds the canonical cloud source for retrieval. Device copies remain editable and synchronized.
- Use Cloudflare AI Search connected to R2 for managed chunking, embeddings, semantic search, and keyword search. Semantic retrieval is an explicit requirement.
- Use AI Search's MCP integration for Codex access. Add a custom server only if a verified requirement cannot be served by the existing interface.
- A future Codex skill defines retrieval and answer drafting.
- Version 1 does not require D1, a separately managed Vectorize index, or automatic AI tag enrichment. AI Search handles the retrieval index.
- Start with original Markdown and user-authored template fields. Markdown frontmatter and inline tags are not automatically filterable AI Search attributes. Add stable R2 object metadata only if retrieval evaluation proves that filtering would help.
- Codex must search the cloud through MCP. Do not silently substitute local vault search or assume a machine-specific path.

## Design boundaries

Keep infrastructure minimal. This project currently needs no separate web editor, application dashboard, Gmail integration, Notion connector, or browser extension. These are possible future features, not accepted implementation requirements.

The repository contains software and documentation, not the personal vault. Use fictional fixtures; never commit real applications, private notes, API tokens, plugin credential files, or account secrets. Keep instance names, prefixes, and resource bindings configurable. Do not publish an unauthenticated personal search endpoint.

Device sync and AI Search ingestion operate independently. The plugin requires Obsidian to be running and able to execute; sleeping devices and mobile background restrictions delay uploads. Newly uploaded notes become searchable after indexing. Configure timing rather than promise immediate availability. Two-way sync propagates deletions; retain recoverable history separately.

## Retrieval and drafting

Return relevant source passages with file/section references. Use semantic and keyword retrieval to find differently phrased questions and exact names. Distinguish drafts, final answers, hypothetical preparation, and confirmed experiences.

Codex should inspect source context, tailor the answer to the prompt and audience, respect length constraints, and preserve the user's voice. Never invent achievements, metrics, motivations, responsibilities, or outcomes. Distinguish personal contributions from team results. Cite sources outside the paste-ready draft and identify missing information. If cloud search fails, say so and retry or request the necessary input; do not fabricate retrieval results.

Use AI Search to retrieve evidence and let Codex compose the final answer. Do not add an unnecessary second answer-generation step inside the search service. Save drafts/final answers only through a user-authorized workflow; do not submit applications automatically.

## Optional derived search documents

Start with original Markdown as AI Search input. Introduce one derived document per question/answer only if retrieval evaluation demonstrates a need. Keep derived artifacts outside Remotely Save's scope, preserve source references and exact answer text, and avoid indexing both copies as independent evidence. Handle source changes, renames, and deletions so obsolete derived answers do not remain searchable.

## Development and verification

Consult current official Cloudflare documentation for APIs, MCP capabilities, billing, and sync behavior. Reuse relevant available skills. Avoid copying outdated APIs or assuming D1 is a native AI Search source.

There are no package scripts or tests yet. When code is introduced, document its actual setup, required secrets, commands, and deployment state. Verify changes in proportion to risk: prioritize sync round-trips, stale/deleted sources, authenticated retrieval, and paraphrased questions finding the correct evidence. Use temporary or isolated fixtures for destructive/conflict cases.

Do not provision paid resources or deploy merely because this design describes them; follow the scope of the active user request. Finish authorized implementation and verification before reporting completion. Keep README.md and these instructions consistent with decisions actually made.

## Implementation roadmap

- [ ] Configure a private R2 bucket and Remotely Save on a disposable test vault.
- [ ] Connect AI Search to R2 and verify semantic and keyword retrieval through authenticated MCP access.
- [ ] Write and install the Codex application-answer skill.
- [ ] Test cross-device sync, cloud-only retrieval, updates, deletions, and answer citations with fictional examples.
- [ ] Evaluate retrieval on representative application and interview questions before adding filterable R2 metadata.
- [ ] Bring in existing interview and application notes after the workflow is verified.

## Technical references

- [Remotely Save](https://github.com/remotely-save/remotely-save)
- [Cloudflare AI Search: how it works](https://developers.cloudflare.com/ai-search/concepts/how-ai-search-works/)
- [AI Search R2 source and object metadata](https://developers.cloudflare.com/ai-search/configuration/data-source/r2/)
- [AI Search overview and MCP integration](https://developers.cloudflare.com/ai-search/)
