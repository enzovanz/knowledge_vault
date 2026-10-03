# Working in this vault

Keep notes focused, connected, and easy to review. Prefer a small update to an existing note over a new note that repeats it.

## Placement

| Content | Location |
| --- | --- |
| Rough concepts to process soon | `99 - Concept Inbox/` |
| Concepts to study later | `98 - Concept Backlog/<Domain>/` |
| Unprocessed books, articles, and other sources | `100 - Resource Inbox/` |
| Developed concepts | `<Domain>/10 - Knowledge/` |
| Processed source notes | `<Domain>/90 - Resources/` |
| Domain navigation and maps of content (MOCs) | `<Domain>/00 - Home/` |
| Attachments | `97 - Assets/` |

Use the existing `Tech`, `Business`, and `Social Sciences` domains. Organize narrower subjects with MOCs.

## Processing notes

1. Read the capture and search for related notes before editing. Merge useful additions into existing concepts; preserve the user's edits and distinct insights.
2. Use the matching template in `01 - Templates/` and follow [[Properties Schema]]. Preserve existing creation dates; use today's date for new notes.
3. Move finished notes to the appropriate domain folder. A developed concept should make sense without reopening its source.
4. Link each developed concept directly from at least one MOC in the same domain. Add useful related-note and source links; update source concept lists when relevant.
5. Update references after moves or renames. Remove redundant inbox captures once fully incorporated; retain any unprocessed material.

## Keep notes tight

- Give each note one clear purpose. Split only when a distinct concept deserves independent explanation or reuse; avoid fragmenting every subtopic.
- Start with a one- or two-sentence summary, explain the mechanism, and give one useful example. Add more only when they teach something different.
- Explain each idea once. Link to an existing explanation instead of repeating it across notes.
- Cut filler, repeated conclusions, rhetorical questions, long example lists, and unnecessary background. Keep qualifications that affect correctness.
- Use plain language and recognized, descriptive titles that are unique across the vault. Avoid empty sections and decorative metadata.
- Keep edits scoped to the requested material and necessary connections.

## Before finishing

Run `.venv/bin/python .scripts/validate.py` to check links, properties, MOC coverage, and unique titles. See [[README]] for setup and [[KB Update Workflow]] for the existing workflow. Briefly report what was merged, added, moved, or removed.
