story: none
date: 2026-11-19
elements: ListCreatableTypes, ReadCreateFields, FieldRecord, IssueTypeRecord
sources: docs/milestones/0001-issues-epics-and-board/artifacts/jira-fields-research-2026-11-18.md, docs/milestones/0001-issues-epics-and-board/artifacts/jira-work-model-research-2026-11-18.md

The create dialog reads the types a person may create from `createmeta/{key}/issuetypes` and each type's fields from `createmeta/{key}/issuetypes/{id}`, at its largest page of 200, and pages until total. A larger page is refused with `Parameter 'maxResults' must not exceed the limit '200'`. The deprecated createmeta with expand is never called, because Atlassian announced its removal.

A type's hierarchy level tells standard types (0) from epics (1). That each item of the type list carries it is UNCONFIRMED; QUESTIONS.md asks it. A create may set only the fields of its type's create screen, and the book checks the screen field by field, in the screen's order.
