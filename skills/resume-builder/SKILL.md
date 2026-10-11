---
name: resume-builder
description: Build or revise a job-tailored, Overleaf-ready LaTeX resume using verified context from the user's Brag Database. Import or save resumes as Markdown only when explicitly requested.
---

# Resume Builder

Use the user's [LaTeX template](assets/resume-template.tex) as the source of truth for document class, packages, commands, spacing, header, and section layout. Replace resume content to suit the opportunity while retaining that template's structure and Overleaf-compatible syntax. The template body is a formatting example and user-provided starting point, not independent confirmation that a claim remains current. Keep the name and contact links unless the user updates them.

## Gather evidence

Read the sibling `brag-database` skill and its `references/cloud-search.md`, then run its `scripts/vault.py describe` to identify the configured Cloudflare instance. Search that cloud index for role requirements, projects, responsibilities, metrics, and public work. Inspect source context and its draft/final/hypothetical status. Use user-provided facts from the current request as such; distinguish them from retrieved evidence. Do not mine local notes for experience, invent achievements or metrics, or attribute a team result to the user without support. Resolve material conflicts before using a claim.

For a job-tailored resume, ask for the job description or a job link if neither is available. If a link is supplied, read the posting. Identify distinct, meaningful keywords and phrases in the description, including responsibilities, methods, tools, domain terms, and qualifications. Prefer requirements that are repeated or central to the role. Group obvious variants under one canonical keyword (for example, `A/B tests` and `A/B testing`), so scoring does not reward repetition.

## Draft and score

Choose the most relevant supported experiences and accomplishments. Write concise, specific bullets. Where evidence permits, express the result, its measure, and the action that caused it (XYZ); vary their order for natural reading. Do not add an unsupported number merely to complete XYZ. Include a public link to a project, launch, publication, or profile when one is available and relevant; use accessible `\href{...}{\underline{...}}` links in LaTeX. Do not link to private source notes.

For each bullet, count the **distinct canonical job-description keywords visibly present** in that bullet, ignoring case and counting each at most once. Score = that count. Revise bullets to raise the score with relevant, truthful terms while keeping them readable and accurate. Do not imply expertise merely to increase a score. Put remaining relevant, supported keywords in the template's Skills and Interests section, under the appropriate category; omit any unsupported terms. Prefer important keywords across the resume over repeating the same few in every bullet.

Return the complete `.tex` source or a linked `.tex` file as requested. Outside the LaTeX, give a compact bullet score table with each bullet's identifying excerpt, matched keywords, and score; list any material job keywords omitted for lack of evidence. Scores and source citations are review notes, never resume text. If a claim needs confirmation, flag it outside the resume rather than silently asserting it. Escape LaTeX special characters in edited text and keep the template's commands intact.

## Save or import a resume only on explicit request

Drafting, revising, or rendering a resume does not authorize adding it to the Brag Database. Only an explicit instruction to save or import a particular resume permits a note in the configured `Resumes` folder. If multiple versions exist, use the one the user identifies; ask only if the target is unclear. Convert the selected resume to readable Markdown before saving, preserving its wording, ordering, headings, bullets, dates, and public links as closely as Markdown allows. For an imported user-authored resume, preserve the source text 1:1 except changes required by format conversion; do not paraphrase or improve it. For a newly generated resume, use the final selected version without silently regenerating it. Do not include LaTeX commands, keyword scores, or internal source citations in the saved resume.

Use the sibling `brag-database/scripts/vault.py save` with a `<configured resumes folder>/<descriptive name>.md` destination (normally `Resumes/`). It refuses overwrites; for revisions, read the existing destination and supply its current `expected_sha256`. Follow an explicit filename from the user. Report the saved path and note that upload/indexing may follow later. Do not save a PDF or LaTeX file inside the vault unless the user separately requests that format.
