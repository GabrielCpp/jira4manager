story: none
date: 2026-11-19
elements: CreateIssue, EditIssue, FieldRecord, ReadCreateFields
sources: docs/milestones/0001-issues-epics-and-board/artifacts/jira-fields-research-2026-11-18.md

Jira answers a refused create or edit with `{"errorMessages": [...], "errors": {"<field id>": "<message>"}}`. A required custom field left empty comes back under its `customfield_<n>` id, as `Severity is required.` under Severity's id, and a field the screen lacks comes back as `Field '<id>' cannot be set. It is not on the appropriate screen, or unknown.`. The app shows each message under its field and the rest in the dialog.

A refusal the book compares is the first of `errorMessages`, else `<field id>: <message>` for the first field error, so the field a message belongs to is part of what the run checks. Custom field ids differ from site to site, so the book writes a custom field as `cf[<name>]` and the surface swaps the site's id in and out; see standing-records-are-named-by-name.md.

The book's create screens are the mockup world's: CASE requires Severity on a Bug and OPS requires Affected service, a cascading select the app cannot fill.
