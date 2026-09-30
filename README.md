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

## CI checks

The `Knowledge base validation` GitHub Actions workflow runs after every push to
`main`, or manually from the repository's Actions tab.

### Internal links

It checks Markdown notes
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

### Note properties

The property checker follows `01 - Templates/Properties Schema.md` and the note
templates. It validates YAML safely and rejects malformed frontmatter,
duplicate properties, and invalid field values.

| Note | Required properties |
| --- | --- |
| Concepts in a domain's `10 - Knowledge` folder | `type: concept`, lowercase nonempty `domain`, valid `created` date |
| Resources in a domain's `90 - Resources` folder | `type: resource`, lowercase nonempty `domain`, recognized `resource_type` |
| Files named `* MOC.md` in a domain's `00 - Home` folder | `type: moc`, lowercase nonempty `domain` |

`created` must be a real calendar date in `YYYY-MM-DD` format. It is optional
for resources and MOCs, but validated when present. Resource types are `book`,
`course`, `article`, `video`, `documentation`, `website`, and `podcast`.
Other properties, such as authors and URLs, remain optional.

Inbox/backlog captures and other home pages may omit frontmatter entirely.
Once they include it, the same type-specific requirements apply; concept and
resource capture folders must use their corresponding type. Templates and
repository-level documents such as this README are exempt.

Invalid properties fail CI and identify the affected file in the logs and
GitHub annotations.

### MOC coverage

Every Markdown note under `<Domain>/10 - Knowledge/`, including subfolders,
must have a direct reference from at least one MOC under that same domain's
`00 - Home/` folder. MOCs are identified by `type: moc` in frontmatter, regardless
of filename. The domain is the top-level folder, such as `Tech`, not the
`domain` property.

Wikilinks, aliases, heading references, embeds, and ordinary Markdown links
count. A link must identify one file.
Links through another note or another domain's MOC do not satisfy the rule.
Code examples, HTML comments, frontmatter links, and dynamic queries do not count.
Inboxes, backlogs, resources, templates, and non-Markdown files are excluded.

Uncovered notes fail CI with an error naming the note and the domain home
folder where a MOC reference is needed.

### Unique note titles

Every Markdown file in the visible vault must have a unique filename title
(the filename without `.md`), including notes in inboxes, backlogs, resources,
templates, and the vault root. The comparison ignores capitalization and
normalizes equivalent Unicode spellings. `Example.md` and `example.md` therefore
conflict even in different domains.

Duplicates fail CI whether or not any links reference them. Using full paths
in links does not exempt duplicate titles. Rename or consolidate the notes
and update their references; the checker lists every conflicting file.
Headings, YAML title properties, and display aliases are not compared.
Hidden files/directories and non-Markdown attachments are excluded.

All validation checks run even if another validation check fails, provided
the checker tests pass.

### Run locally

Set up the dependencies and run the checks with Python 3.12:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r .scripts/requirements.txt
python .scripts/check_links.py
python .scripts/check_properties.py
python .scripts/check_moc_coverage.py
python .scripts/check_duplicate_titles.py
```

Run the checkers' tests with:

```sh
python -m unittest discover -s .scripts -p 'test_*.py'
```

A failed run exits with an error and lists missing targets in the workflow log
and GitHub annotations. Because this workflow runs after a push, the commit is
already on `main`: failure does not reject or undo it. Fix the links and push
again. To prevent unchecked changes from entering `main`, use a pull request
workflow with required status checks and branch protection or rulesets.
