story: none
date: 2026-11-19
elements: SearchIssues, ListSprintIssues, ListBoardIssues, ListBoardBacklog
sources: docs/milestones/0001-issues-epics-and-board/artifacts/platform-research-2026-11-17.md, docs/milestones/0001-issues-epics-and-board/artifacts/jira-work-model-research-2026-11-18.md

The issue lists page by token: an answer holds `isLast` and, while more remain, a `nextPageToken` the next request sends back. They carry no `total` and no `startAt`. Every other list of the release pages by offset with `startAt`, `maxResults` and `isLast`.

Atlassian removed `/rest/api/3/search` for the token-paged `/rest/api/3/search/jql`, and RFC-127 moved the board, backlog and sprint lists the same way. A token comes only from the page before it, so the book refuses any token it sends: it never holds a real one, because a search narrowed to one run's label fits on one page. The app counts from the issues it loaded, since no answer gives a total.
