story: none
date: 2026-11-19
elements: ListTransitions, RunTransition, StatusRecord, ScreenGoesOnDone, ScreenComesOffDone
sources: docs/milestones/0001-issues-epics-and-board/artifacts/jira-work-model-research-2026-11-18.md

A status changes only through a transition the workflow offers from the issue's status, and the app reads the offer before it runs one. The seeded workflows let every status reach every other, except that CASE has no transition from In Review back to To Do. No workflow offers the status the issue already holds. A transition the issue does not offer is refused as `Transition id '<id>' is not valid for this issue.`; the surface names the id by the status it leads to, since two workflows of one site reuse the same ids.

The app never sends a transition screen's fields. When the chosen transition shows a screen with a required field and no default, the app does not run it and offers the browser. The book models that state as an admin putting a screen with a required Resolution on the transitions into Done, which refuses the call with `resolution: Resolution is required.`. Neither environment lets the book arrange that while it runs, so the cells that need it are skipped; QUESTIONS.md asks for the knob. A transition is never retried, because a repeat could move the issue twice.
