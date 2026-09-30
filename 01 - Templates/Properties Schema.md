
Use only properties that support search or navigation. Folders represent workflow; properties represent what a note is about.

## **`type`**

Describes the role of the note.

- `concept` - Knowledge expressed in your own words
- `resource` - External learning resources
- `moc` - Maps of Content / navigation notes

## **`domain`**

The primary subject area, written consistently in lowercase, such as `software engineering`, `data engineering`, or `networking`.

## **`created`**

The note creation date in `YYYY-MM-DD` format. Templates fill this automatically.

## **`resource_type`**

Used when `type: resource`.

- `book`
- `course`
- `article`
- `video`
- `documentation`
- `website`
- `podcast`

Avoid adding a `status` property. The Inbox and destination folders already show whether a note has been processed.

## CI validation

Developed concepts require `type`, `domain`, and `created`. Processed resources
require `type`, `domain`, and `resource_type`. MOC files in a domain's home
folder require `type` and `domain`. A supplied `created` value is always
validated, including on resources and MOCs.

Rough inbox/backlog captures and general home pages may omit frontmatter.
When present, their properties follow the same type-specific requirements.
Templates and repository-level documents are exempt. Run the validator with
`python .scripts/check_properties.py` after installing the checker dependencies
described in the README.
