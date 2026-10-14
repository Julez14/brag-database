---
name: resume-builder
description: Build or revise a job-tailored, Overleaf-ready LaTeX resume using verified context from the user's Brag Database. Import or save resumes as Markdown only when explicitly requested.
---

# Resume Builder

Use the user's [LaTeX template](assets/resume-template.tex) as the source of truth for document class, packages, commands, spacing, header, and section layout. Replace resume content to suit the opportunity while retaining that template's structure and Overleaf-compatible syntax. The template body is a formatting example and user-provided starting point, not independent confirmation that a claim remains current. Keep the name and contact links unless the user updates them.

## Output location

Always write final resume artifacts (`.tex`, the rendered `.pdf`, and separate review notes) to the user's `~/Downloads` folder, optionally in a descriptive role-specific subfolder, unless the user explicitly requests another location. Keep temporary build and preview files outside Downloads. Return clickable links to the final files. This output preference does not authorize saving or importing a resume into the Brag Database.

## Gather evidence

Read the sibling `brag-database` skill and its `references/cloud-search.md`, then run its `scripts/vault.py describe` to identify the configured Cloudflare instance. Search that cloud index for role requirements, projects, responsibilities, metrics, and public work. Inspect source context and its draft/final/hypothetical status. Use user-provided facts from the current request as such; distinguish them from retrieved evidence. Do not mine local notes for experience, invent achievements or metrics, or attribute a team result to the user without support. Resolve material conflicts before using a claim.

When a retrieved resume informs current experience, read `resume_created_at` and `resume_date_source` to judge its age. If either is absent, treat the original date as unknown; the vault note's `created` date is an import date, not evidence that the resume is current. Prefer newer confirmed experience when an older resume conflicts with it.

For a job-tailored resume, ask for the job description or a job link if neither is available. If a link is supplied, read the posting. Identify distinct, meaningful keywords and phrases in the description, including responsibilities, methods, tools, domain terms, and qualifications. Prefer requirements that are repeated or central to the role. Group obvious variants under one canonical keyword (for example, `A/B tests` and `A/B testing`), so scoring does not reward repetition.

Adjust the Education section's expected graduation date to **April 2027** or **April 2028**, choosing the user's graduation timeline that satisfies the job description's required graduation window. If both dates qualify or the posting gives no graduation requirement, use the user's current expected date, defaulting to April 2028 unless updated. If neither qualifies, flag the eligibility mismatch. These dates should reflect a timeline the user can actually pursue; ask for confirmation only if current evidence conflicts with the selected timeline.

## Draft and score

Choose the most relevant supported experiences and accomplishments. Write concise, specific bullets. Where evidence permits, express the result, its measure, and the action that caused it (XYZ); vary their order for natural reading. Do not add an unsupported number merely to complete XYZ. Include a public link to a project, launch, publication, or profile when one is available and relevant; use accessible `\href{...}{\underline{...}}` links in LaTeX. Do not link to private source notes.

For each bullet, count the **distinct canonical job-description keywords visibly present** in that bullet, ignoring case and counting each at most once. Score = that count. Revise bullets to raise the score with relevant, truthful terms while keeping them readable and accurate. Do not imply expertise merely to increase a score. Put remaining relevant, supported keywords in the template's Skills and Interests section, under the appropriate category; omit any unsupported terms. Prefer important keywords across the resume over repeating the same few in every bullet.

Return the complete `.tex` source or a linked `.tex` file as requested. Outside the LaTeX, give a compact bullet score table with each bullet's identifying excerpt, matched keywords, and score; list any material job keywords omitted for lack of evidence. Scores and source citations are review notes, never resume text. If a claim needs confirmation, flag it outside the resume rather than silently asserting it. Escape LaTeX special characters in edited text and keep the template's commands intact.

## Render and fill exactly one page

Every resume must fill **exactly one complete page**, with no second page and no substantially underfilled page. Compile the final LaTeX into a PDF, verify its page count programmatically, render the PDF to an image, and visually inspect the actual page before delivery. A successful compilation or a page count of one alone does not satisfy this requirement.

Use the template's page size and margins to define the usable page area. Distribute content naturally from the header to near the bottom of that area, targeting the final text line within roughly two normal text lines of its bottom edge. Keep normal margins, readable type, and consistent spacing; avoid large empty areas, clipped text, overlaps, and stretched gaps.

If the page is underfilled, add the next most relevant verified accomplishments or useful detail, or modestly increase cramped spacing. If it overflows, tighten wording and remove lower-priority material first. Preserve the template's class, packages, commands, header, and section structure; small spacing adjustments are permitted when needed to achieve the full-page layout. Never invent claims, repeat content, or add filler merely to fill space, and do not shrink fonts or margins to force a fit.

Recompile, recount pages, and inspect a fresh render after each layout revision until the resume fills exactly one page cleanly. Deliver the matching `.tex` and `.pdf` files in Downloads, with scores and source citations outside both resume files. If rendering cannot be completed, report the blocker and do not present the layout as verified.

## Save or import a resume only on explicit request

Drafting, revising, or rendering a resume does not authorize adding it to the Brag Database. Only an explicit instruction to save or import a particular resume permits a note in the configured `Resumes` folder. If multiple versions exist, use the one the user identifies; ask only if the target is unclear. Convert the selected resume to readable Markdown before saving, preserving its wording, ordering, headings, bullets, dates, and public links as closely as Markdown allows. For an imported user-authored resume, preserve the source text 1:1 except changes required by format conversion; do not paraphrase or improve it. For a newly generated resume, use the final selected version without silently regenerating it. Do not include LaTeX commands, keyword scores, or internal source citations in the saved resume.

For every saved or imported resume, put `resume_created_at` and `resume_date_source` in YAML frontmatter, separate from the note's `created` and `updated` dates. Use the user's stated original resume date when available; otherwise use an embedded source creation timestamp (for example, PDF `CreationDate` or document properties). For a resume newly authored in this session, use its actual creation date. Preserve the source timestamp's time and offset when available. Set `resume_date_source` to `user_stated`, `pdf_metadata`, `document_metadata`, or `session` as appropriate. A PDF creation timestamp establishes when that PDF was generated, which may be later than the first draft of its content. If there is no reliable original date, set `resume_created_at: null` and `resume_date_source: unknown`, and flag the missing date outside the resume. Do not infer the date from a filename, graduation year, filesystem copy time, or vault import time. Keep the source filename and checksum when available so later retrieval can assess provenance. Preserve these fields when revising an existing resume unless the user corrects them or stronger source evidence resolves an unknown date.

Use the sibling `brag-database/scripts/vault.py save` with a `<configured resumes folder>/<descriptive name>.md` destination (normally `Resumes/`). It refuses overwrites; for revisions, read the existing destination and supply its current `expected_sha256`. Follow an explicit filename from the user. Report the saved path and note that upload/indexing may follow later. Do not save a PDF or LaTeX file inside the vault unless the user separately requests that format.
