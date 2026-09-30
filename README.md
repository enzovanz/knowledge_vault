# Enzo Knowledge Base

An Obsidian vault for capturing, studying, and connecting concepts across technology, business, and the social sciences.

Open `00 - Home/Enzo Knowledge Base.md` to navigate the vault and review the current inboxes.

## Structure

- `00 - Home/` — main vault dashboard
- `01 - Templates/` — concept, resource, MOC, and workflow templates
- `97 - Assets/` — attachments and other supporting files
- `98 - Concept Backlog/` — concepts grouped by domain for later study
- `99 - Concept Inbox/` — quick concept captures to process soon
- `100 - Resource Inbox/` — books, articles, courses, and other unprocessed sources
- `Tech/`, `Business/`, and `Social Sciences/` — domain-specific MOCs, knowledge notes, and processed resources

Each domain follows the same layout:

- `00 - Home/` — domain home pages and maps of content (MOCs)
- `10 - Knowledge/` — developed concept notes
- `90 - Resources/` — processed source notes

## Workflow

1. Capture a concept in `99 - Concept Inbox` or a source in `100 - Resource Inbox`.
2. Move concepts intended for later study to the appropriate folder under `98 - Concept Backlog`.
3. Apply the matching template and explain the subject in your own words.
4. Add a concrete example and only the connections that are useful.
5. Link a completed concept from one relevant MOC.
6. Move it to the domain's `10 - Knowledge` folder, or move a processed source to `90 - Resources`.

A note is complete when it can be understood without reopening the original source.

## Conventions

- Keep domains broad; use MOCs to organize narrower themes.
- Use recognized, descriptive note titles.
- Keep unfinished concepts out of `10 - Knowledge`.
- Store personal Obsidian workspace state outside version control.

## Internal link checks

The `Check internal links` GitHub Actions workflow runs after every push to
`main`, or manually from the repository's Actions tab. It checks Markdown notes
for missing local file targets, including Obsidian wikilinks, aliases, embeds,
and Markdown links, images, and reference links. Bare note titles and shortened
vault paths are supported, as are relative paths and URL-encoded spaces.

The check ignores code examples, HTML comments, YAML frontmatter, external URLs,
and heading/block fragments. It checks that the target file exists, not that a
heading or block exists. Raw HTML links and links in Canvas files are outside
its scope. Missing targets in inbox and backlog notes also fail the check.
Git-ignored files cannot satisfy links; new, non-ignored files are included in
local checks, so remember to commit them with the notes that reference them.
Diagnostics point to the start of the Markdown block containing a broken link.

Run the same check locally with Python 3.12:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r scripts/requirements.txt
python scripts/check_links.py
```

Run the checker's tests with:

```sh
python -m unittest discover -s scripts -p 'test_*.py'
```

A failed run exits with an error and lists missing targets in the workflow log
and GitHub annotations. Because this workflow runs after a push, the commit is
already on `main`: failure does not reject or undo it. Fix the links and push
again. To prevent unchecked changes from entering `main`, use a pull request
workflow with required status checks and branch protection or rulesets.
