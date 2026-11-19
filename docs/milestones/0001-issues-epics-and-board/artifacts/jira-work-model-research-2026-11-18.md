# Jira work model research, 2026-11-18

This file records Jira Cloud REST facts for the issue, epic and board features of the first release, each with its Atlassian source and an UNCONFIRMED mark where no official page backed it.

Abbreviations used for sources: PLATFORM-SPEC is https://dac-static.atlassian.com/cloud/jira/platform/swagger-v3.v3.json and AGILE-SPEC is https://dac-static.atlassian.com/cloud/jira/software/swagger.v3.json.

## 1. Epic to child link

- The `parent` field is the replacement for the `Epic Link` and `Parent Link` custom fields, and it covers company-managed and team-managed projects. Source: https://community.developer.atlassian.com/t/deprecation-of-the-epic-link-parent-link-and-other-related-fields-in-rest-apis-and-webhooks/54048
- Atlassian staff announced the deprecation on 30 November 2021 for REST APIs and webhooks of company-managed projects. Source: https://community.developer.atlassian.com/t/deprecation-of-the-epic-link-parent-link-and-other-related-fields-in-rest-apis-and-webhooks/54048
- The announced deadline for the old behaviour was 30 November 2022, and the old behaviour may be switched off at any point after it. Source: https://community.developer.atlassian.com/t/deprecation-of-the-epic-link-parent-link-and-other-related-fields-in-rest-apis-and-webhooks/54048
- The announcement also deprecates the `epic` field, and it removes `Epic Link` and `Parent Link` from createmeta and editmeta. Source: https://community.developer.atlassian.com/t/deprecation-of-the-epic-link-parent-link-and-other-related-fields-in-rest-apis-and-webhooks/54048
- The announcement says JQL and the Jira UI do not change in that deprecation. Source: https://community.developer.atlassian.com/t/deprecation-of-the-epic-link-parent-link-and-other-related-fields-in-rest-apis-and-webhooks/54048
- The changelog item values `Epic Link` and `Parent` are replaced by `IssueParentAssociation`. Source: https://developer.atlassian.com/cloud/jira/platform/deprecation-notice-issue-reparenting-changelogs/
- The Atlassian support page on epics says older filters using `Epic Link` still work and that new filters should use `parent`. Source: https://support.atlassian.com/jira-software-cloud/docs/what-is-an-epic/
- A search summary of the JQL fields page says the Epic link function was retired in favour of Parent as of February 2024. The page text itself could not be fetched, so the date is UNCONFIRMED. Source: https://support.atlassian.com/jira-software-cloud/docs/jql-fields/
- On create, send `fields.parent` in `POST /rest/api/3/issue`. The spec example uses `"parent": {"key": "PROJ-123"}`. Source: PLATFORM-SPEC, operation `POST /rest/api/3/issue`.
- The 2021 announcement shows `{"fields": {"parent": {"id": "<parent issue id>"}}}` for create and for edit. Source: https://community.developer.atlassian.com/t/deprecation-of-the-epic-link-parent-link-and-other-related-fields-in-rest-apis-and-webhooks/54048
- On edit, `PUT /rest/api/3/issue/{issueIdOrKey}` accepts the parent by key or ID. Source: PLATFORM-SPEC, operation `PUT /rest/api/3/issue/{issueIdOrKey}`.
- To clear the parent of a standard issue, send `update.parent.set.none` set to true. Source: PLATFORM-SPEC, operation `PUT /rest/api/3/issue/{issueIdOrKey}`.
- The agile spec gives a second way to clear the parent of a team-managed issue, which is `{ fields: { parent: {} } }`. Source: AGILE-SPEC, operation `POST /rest/agile/1.0/epic/none/issue`.
- `POST /rest/agile/1.0/epic/{epicIdOrKey}/issue` moves up to 50 issues into an epic. It does not work for epics in next-gen projects. Source: AGILE-SPEC.
- `POST /rest/agile/1.0/epic/none/issue` removes up to 50 issues from their epics. It does not work for next-gen projects. Source: AGILE-SPEC.
- Because those two agile calls fail for team-managed projects, the client should use the `parent` field edit for both project styles. This is a design inference from the two facts above.
- To list the children of an epic, use JQL `parent = KEY`. The JQL fields page says `parent` works in team-managed and company-managed spaces. Source: https://support.atlassian.com/jira-software-cloud/docs/jql-fields/
- The JQL `parentEpic` operator, for example `parentEpic in (DEMO-1, SAMPLE-4)`, applies to company-managed spaces only. Source: https://support.atlassian.com/jira-software-cloud/docs/jql-fields/
- A support article says `parentEpic` also returns the sub-tasks of the epic's children. Source: https://support.atlassian.com/jira/kb/retrieve-all-child-and-linked-work-items-of-an-epic-in-jira-cloud/
- The agile `GET /rest/agile/1.0/epic/{epicIdOrKey}/issue` is marked deprecated, and its description tells callers to use a JQL search with `parent` for next-gen projects. Source: AGILE-SPEC.
- The classic `/rest/api/3/search` is marked deprecated and being removed. Callers should use `GET /rest/api/3/search/jql` with `nextPageToken`. Source: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/
- The enhanced search drops the `total` count and replaces `startAt` with a page token. Source: https://community.developer.atlassian.com/t/rfc-61-evolving-search-capabilities-addressing-scalability-with-a-new-enhanced-search-api/83027
- A page token expires after 7 days, per a search summary of the RFC thread. The exact wording was not fetched, so this is UNCONFIRMED. Source: https://community.developer.atlassian.com/t/rfc-61-evolving-search-capabilities-addressing-scalability-with-a-new-enhanced-search-api/83027

## 2. Issue type hierarchy

- Issue types carry an integer `hierarchyLevel`. Source: PLATFORM-SPEC, schema `IssueTypeDetails`.
- The create-issue-type schema documents `-1` for Subtask and `0` for Base. Source: PLATFORM-SPEC, schema `IssueTypeCreateBean`.
- A separate spec schema says levels run 0, 1, 2 and up, with negative values for subtasks. Source: PLATFORM-SPEC, schema `IssueTypeHierarchyPayload`.
- Epic = 1 is UNCONFIRMED on an official reference page. A search of Atlassian support and community pages returned that value, but the spec text does not state it. Source: https://support.atlassian.com/jira/kb/jira-epic-issues-have-subtasks-under-them-along-with-child-issues/
- Levels above Epic need Jira Premium or Enterprise. This is from a search summary and is UNCONFIRMED. Source: https://community.atlassian.com/forums/Jira-questions/How-to-set-up-hierarchy-with-Epic-Story-Feature-Task-Sub-task-in/qaq-p/3091938
- `GET /rest/api/3/project/{projectId}/hierarchy` was named in a search summary as the call that groups issue types by level. It was not checked in the spec, so it is UNCONFIRMED. Source: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-projects/
- The parent of an issue must sit one hierarchy level above it. This is from a search summary and is UNCONFIRMED. Source: https://community.atlassian.com/forums/Jira-questions/How-to-set-up-hierarchy-with-Epic-Story-Feature-Task-Sub-task-in/qaq-p/3091938
- `GET /rest/api/3/issue/createmeta/{projectIdOrKey}/issuetypes` returns a page of issue types with `startAt`, `maxResults`, `total` and `issueTypes`. Source: PLATFORM-SPEC, schema `PageOfCreateMetaIssueTypes`.
- `GET /rest/api/3/issue/createmeta/{projectIdOrKey}/issuetypes/{issueTypeId}` returns a page of field metadata with `startAt`, `maxResults`, `total` and `fields`. Source: PLATFORM-SPEC, schema `PageOfCreateMetaIssueTypeWithField`.
- The field metadata endpoint is paginated, so the client must page through it. Source: https://community.developer.atlassian.com/t/create-issue-meta-endpoint-deprecation/75413
- `GET /rest/api/3/issue/createmeta` with `expand` is marked deprecated and points to CHANGE-1304. Source: PLATFORM-SPEC, operation `GET /rest/api/3/issue/createmeta`.
- The Atlassian post of 12 December 2023 said the old endpoint would be deprecated on 3 June 2024 and would then return 404. Source: https://community.developer.atlassian.com/t/create-issue-meta-endpoint-deprecation/75413
- On 9 August 2024 Atlassian staff said the old endpoint still had heavy traffic, and no firm removal date was given. The thread has no answer to a timeline question of 2 April 2025. Source: https://community.developer.atlassian.com/t/create-issue-meta-endpoint-deprecation/75413
- The removal date of the old createmeta call is UNCONFIRMED. The client should use only the two narrower endpoints.
- `GET /rest/api/3/project/{key}` returns `style` with the enum values `classic` and `next-gen`, and a boolean `simplified`. Source: PLATFORM-SPEC, schema `Project`.
- The spec does not state that `classic` means company-managed or that `next-gen` means team-managed, and it does not define `simplified`. The mapping is UNCONFIRMED on an official page, though the agile spec labels "next-gen" items and Atlassian's current docs call them team-managed. Source: AGILE-SPEC.
- Atlassian replaced the issue-links hierarchy plan with parent associations, and that notice is marked cancelled. Source: https://developer.atlassian.com/cloud/jira/platform/deprecation-notice-hierarchy-levels/

## 3. Statuses

- `GET /rest/api/3/project/{projectIdOrKey}/statuses` returns an array with one object per issue type. Source: PLATFORM-SPEC, schema `IssueTypeWithStatus`.
- Each object has `id`, `name`, `self`, `subtask` and a `statuses` array. Source: PLATFORM-SPEC, schema `IssueTypeWithStatus`.
- Each status in `statuses` follows `StatusDetails`, which includes `statusCategory` with `colorName`, `id`, `key`, `name` and `self`. Source: PLATFORM-SPEC, schemas `StatusDetails` and `StatusCategory`.
- The spec example for that endpoint omits `statusCategory` from its status items. The client must not assume it is always present. Source: PLATFORM-SPEC, operation `GET /rest/api/3/project/{projectIdOrKey}/statuses`.
- The category keys `new`, `indeterminate` and `done` are observed behaviour, with ids 2, 4 and 3, and a fourth key `undefined` named "No Category" with id 1. Source: https://community.developer.atlassian.com/t/bad-documentation-for-rest-api-3-statuscategory/78565
- No official page lists the keys, so the key set is UNCONFIRMED. The spec's own transitions example shows an invented key `in-flight`, which must be treated as sample data. Source: PLATFORM-SPEC, operation `GET /rest/api/3/issue/{issueIdOrKey}/transitions`.

## 4. Transitions

- `GET /rest/api/3/issue/{issueIdOrKey}/transitions` returns `{ "expand": ..., "transitions": [...] }`. Source: PLATFORM-SPEC, schema `Transitions`.
- Each transition has `id` as a string, `name`, `to`, `hasScreen`, `isAvailable`, `isConditional`, `isGlobal`, `isInitial`, `looped` and `fields`. Source: PLATFORM-SPEC, schema `IssueTransition`.
- `to` is a `StatusDetails` object, so it holds the target status id, name and `statusCategory`. Source: PLATFORM-SPEC, schema `IssueTransition`.
- `expand=transitions.fields` fills `fields` with the transition screen fields, and fields hidden from the screen are not returned. Source: PLATFORM-SPEC, operation `GET /rest/api/3/issue/{issueIdOrKey}/transitions`.
- The query parameter `includeUnavailableTransitions` adds transitions that fail a condition, so `isAvailable` can be false only when it is set. Source: PLATFORM-SPEC.
- Each field in `transitions.fields` carries `required`, `hasDefaultValue`, `allowedValues`, `operations` and `schema`. Source: PLATFORM-SPEC, operation `GET /rest/api/3/issue/{issueIdOrKey}/transitions`.
- `POST /rest/api/3/issue/{issueIdOrKey}/transitions` takes `transition` with the id, and optional `fields` and `update` for the transition screen. It returns 204 on success. Source: PLATFORM-SPEC.
- The POST returns 400 when no transition is given, when a field outside the transition screen is sent, or when a field appears in both `fields` and `update`. Source: PLATFORM-SPEC.
- The POST also returns 409 for a conflicting update and 422 for a configuration problem. Source: PLATFORM-SPEC.
- The spec does not say what the error is when a required screen field is missing. The client should read `required` from `transitions.fields` first, and the failure response for a missing required field is UNCONFIRMED. Source: PLATFORM-SPEC.

## 5. Agile boards

- `GET /rest/agile/1.0/board?projectKeyOrId=CASE` filters boards that are relevant to a project, meaning the board filter JQL references the project. Source: AGILE-SPEC, operation `GET /rest/agile/1.0/board`.
- The list also takes `type`, `name`, `orderBy`, `expand`, `startAt` and `maxResults`. Source: AGILE-SPEC.
- Board `type` valid values in the list filter are `scrum`, `kanban` and `simple`. Source: AGILE-SPEC.
- Board creation accepts only `scrum` and `kanban`. Source: AGILE-SPEC, operation `POST /rest/agile/1.0/board`.
- That the list includes team-managed project boards is partly confirmed. A community post shows a next-gen board with a `location` of type project, and the agile spec marks several operations as covering next-gen items. No official page states it outright, so it is UNCONFIRMED. Source: https://community.developer.atlassian.com/t/rest-api-for-retrieving-board-and-project-is-not-working/13642
- A team-managed project may get several boards in future, so the client must not assume one board per project. Source: https://community.developer.atlassian.com/t/changes-to-the-tmp-board-and-project-features-endpoints/53519
- `GET /rest/agile/1.0/board/{boardId}/configuration` returns `columnConfig.columns[]` with `name`, `min`, `max` and `statuses[]` holding `id` and `self`. Source: AGILE-SPEC, schema `BoardConfigBean`.
- The configuration also returns `filter`, `location`, `ranking`, `estimation` for scrum and `subQuery` for kanban. Source: AGILE-SPEC, operation `GET /rest/agile/1.0/board/{boardId}/configuration`.
- The last column that has statuses mapped to it is treated as the Done column. Source: AGILE-SPEC.
- A kanban board can return a column named "Backlog" with no statuses, which is a placeholder for the hidden backlog. This is community evidence and UNCONFIRMED officially. Source: https://community.developer.atlassian.com/t/additional-backlog-column-returned-from-api/58269
- Moving a card between columns means a status transition through `POST /rest/api/3/issue/{key}/transitions`, choosing a transition whose `to.id` is a status of the target column. This is a design inference, since the agile spec has no move-to-column operation.
- `GET /rest/agile/1.0/board/{boardId}/issue`, `GET /rest/agile/1.0/board/{boardId}/backlog` and `GET /rest/agile/1.0/sprint/{sprintId}/issue` are marked deprecated. Source: AGILE-SPEC.
- Their token-paginated replacements are `GET /rest/software/1.0/board/{boardId}/issue`, `.../board/{boardId}/backlog` and `.../sprint/{sprintId}/issue`. They take `nextPageToken`, `maxResults`, `jql`, `fields`, `expand` and `reconcileIssues`. Source: AGILE-SPEC.
- Atlassian published the change as RFC-127 on 5 February 2026, with launch and deprecation tentatively at the end of March 2026 and removal after a target 6-month period. Source: https://community.developer.atlassian.com/t/rfc-127-jira-software-cloud-api-changes-improving-scalability-for-software-space-issue-results/98871
- The RFC drops `startAt` and `total`, adds `nextPageToken` and `isLast`, and caps comments and changelogs at 20 per issue. Source: https://community.developer.atlassian.com/t/rfc-127-jira-software-cloud-api-changes-improving-scalability-for-software-space-issue-results/98871
- The removal date of the old agile issue endpoints is UNCONFIRMED.
- The `GET /rest/software/1.0/board/{boardId}/backlog/approximate-count` and `.../board/{boardId}/issue/approximate-count` endpoints exist in the spec for counts. Source: AGILE-SPEC.
- Other agile list endpoints keep offset pagination with `startAt`, `maxResults`, `isLast`, `total` and `values`. Source: AGILE-SPEC, schema `PageBeanBoard`.
- The agile intro page names `startAt`, `maxResults`, `total` and `values`, says `total` is optional, and does not mention `isLast`. Source: https://developer.atlassian.com/cloud/jira/software/rest/intro/
- The backlog is incomplete issues that belong to no future or active sprint. Source: AGILE-SPEC, operation `GET /rest/agile/1.0/board/{boardId}/backlog`.
- Whether `GET /board/{id}/backlog` works on a kanban board is UNCONFIRMED. A community thread reports a 400 for a kanban board whose UI shows 35 backlog issues, and the suggested workaround was the board configuration plus a JQL search. Source: https://community.atlassian.com/forums/Jira-questions/Accessing-Backlog-Issues-on-Kanban-Boards-via-JIRA-REST-API/qaq-p/2697457
- The result when the kanban backlog is disabled is UNCONFIRMED. No official page describes it.
- A community thread reports that the backlog endpoint omitted a resolved issue on a next-gen board, and Atlassian called it a missing feature. Source: https://community.developer.atlassian.com/t/jira-software-cloud-get-issues-for-board-rest-api-does-not-return-the-correct-issues-for-boards-of-next-gen-projects/32951
- Board features such as Backlog and Sprints on team-managed boards are toggled with `PUT /rest/agile/1.0/board/{boardId}/features`, and `GET /rest/agile/1.0/board/{boardId}/features` reads them. Source: https://community.developer.atlassian.com/t/changes-to-the-tmp-board-and-project-features-endpoints/53519
- `GET /rest/agile/1.0/board/{boardId}/sprint?state=active` lists sprints and takes `state` with the values `future`, `active` and `closed`. Source: AGILE-SPEC, operation `GET /rest/agile/1.0/board/{boardId}/sprint`.
- `POST /rest/agile/1.0/backlog/issue` takes `{"issues": [...]}`, moves at most 50 issues, and returns 204. Source: AGILE-SPEC.
- `POST /rest/agile/1.0/sprint/{sprintId}/issue` takes `issues`, optional `rankBeforeIssue`, `rankAfterIssue` and `rankCustomFieldId`. It moves at most 50 issues, only to open or active sprints, and returns 204. Source: AGILE-SPEC.
- `PUT /rest/agile/1.0/issue/rank` takes `issues` plus `rankBeforeIssue` or `rankAfterIssue`, and optionally `rankCustomFieldId`. It ranks at most 50 issues. Source: AGILE-SPEC.
- The rank call returns 204 on success and 207 with per-issue results when some issues fail. Source: AGILE-SPEC.
- `GET /rest/agile/1.0/board/{boardId}/epic` is not marked deprecated in the spec. Source: AGILE-SPEC.
- Atlassian's RFC author confirmed that `GET /board/{boardId}/epic` is not affected by RFC-127. Source: https://community.developer.atlassian.com/t/rfc-127-jira-software-cloud-api-changes-improving-scalability-for-software-space-issue-results/98871
- The epic-scoped issue endpoints `.../board/{boardId}/epic/{epicId}/issue` and `.../board/{boardId}/epic/none/issue` are marked deprecated. Source: AGILE-SPEC.
- `GET /rest/agile/1.0/epic/{epicIdOrKey}` and `POST /rest/agile/1.0/epic/{epicIdOrKey}` do not work for epics in next-gen projects. Source: AGILE-SPEC.
- Agile endpoints accept an issue id or key in `issues`. Source: AGILE-SPEC, request examples.

## 6. Create and edit

- `POST /rest/api/3/issue` takes `fields` and `update`. A body with `project.id` or `project.key`, `issuetype.id`, `summary` and the other fields on the create screen is the shape in the spec example. Source: PLATFORM-SPEC, operation `POST /rest/api/3/issue`.
- The spec example sets `assignee` as `{"id": "<accountId>"}`, `priority` as `{"id": "..."}`, `parent` as `{"key": "..."}` and `reporter` as `{"id": "..."}`. Source: PLATFORM-SPEC.
- `description`, `environment` and multi-line custom fields take Atlassian Document Format, which is `{"type": "doc", "version": 1, "content": [...]}`. Single-line custom text fields take a plain string. Source: PLATFORM-SPEC, operation `POST /rest/api/3/issue`.
- Create returns 201, and returns 400 for missing required fields, invalid values, fields not allowed on the issue type, or missing permission. Source: PLATFORM-SPEC.
- Create also returns 422 when a configuration problem prevents it. Source: PLATFORM-SPEC.
- `GET /rest/api/3/issue/{issueIdOrKey}/editmeta` returns the edit screen fields visible to and editable by the user. Source: PLATFORM-SPEC, operation `GET /rest/api/3/issue/{issueIdOrKey}/editmeta`.
- `PUT /rest/api/3/issue/{issueIdOrKey}` ignores transitions, returns 204 on success, and 400 for fields not on the issue type. Source: PLATFORM-SPEC.
- The edit endpoint does not check screen configurations to decide whether a field is editable. Source: PLATFORM-SPEC, operation `PUT /rest/api/3/issue/{issueIdOrKey}`.
- `GET /rest/api/3/user/assignable/search` takes `project` for a new issue, or `issueKey`, `issueId` and `actionDescriptorId` for an existing issue or a transition. Source: PLATFORM-SPEC.
- That endpoint takes the first thousand users in the `startAt` and `maxResults` range and then filters, so a page can hold fewer users than `maxResults`. Source: PLATFORM-SPEC, operation `GET /rest/api/3/user/assignable/search`.
- The `query` parameter on that endpoint filters by name or email text. The exact matching rule is not in the text read. Source: PLATFORM-SPEC.
- Email addresses in the response can be hidden by profile privacy controls. Source: https://developer.atlassian.com/cloud/jira/platform/profile-visibility/

## 7. Epic progress

- No official endpoint returns epic progress. A search of the platform and software references found none, so the client must compute it. The absence is UNCONFIRMED as a statement on an official page. Source: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/
- Child links live on the child, so the client needs one JQL search with `parent in (...)` or `parent = KEY`, then a count by `statusCategory`. Source: https://community.developer.atlassian.com/t/how-to-find-an-epics-child-issues-without-a-separate-api-call/71384
- The agile `epic` object holds only a `done` boolean, an id, a name and a color, and the agile epic endpoints do not work for next-gen projects. Source: AGILE-SPEC, operation `GET /rest/agile/1.0/epic/{epicIdOrKey}`.
- The Atlassian roadmap view shows a progress bar from the status of child issues, but no API exposes it. This comes from a search summary and is UNCONFIRMED. Source: https://support.atlassian.com/jira-software-cloud/docs/what-is-an-epic/
- The custom field `Epic Name` became optional from 15 January 2023, remains available, and loses no data. Source: https://community.developer.atlassian.com/t/the-epic-name-field-will-become-optional-from-15-jan-2023/59937
- The board and backlog display switched to the epic summary, with the rollout noted for 22 March 2023. Source: https://community.developer.atlassian.com/t/the-epic-name-still-required/67137
- Until a site received the change, the REST API returned 400 when Epic Name was missing on create. Source: https://community.developer.atlassian.com/t/the-epic-name-still-required/67137
- A site that has not rolled out the change can still require Epic Name, so the client should read it from createmeta and send it only when it is listed as required. This is a design inference.
- No official page states whether `Epic Status` exists as a separate field. It is UNCONFIRMED, and an epic's state is its normal workflow status.

## 8. Rate limiting on writes

- A 429 response carries `Retry-After` in seconds, `X-RateLimit-Reset` as an ISO 8601 timestamp, and `RateLimit-Reason`. Source: https://developer.atlassian.com/cloud/jira/platform/rate-limiting/
- The reason values are `jira-quota-global-based`, `jira-quota-tenant-based`, `jira-burst-based` and `jira-per-issue-on-write`. Source: https://developer.atlassian.com/cloud/jira/platform/rate-limiting/
- Atlassian says to retry only if the API is idempotent and the response includes a `Retry-After` header. Source: https://developer.atlassian.com/cloud/jira/platform/rate-limiting/
- The page does not define idempotency and does not say whether `POST` create or `PUT` edit qualifies. That is UNCONFIRMED. Source: https://developer.atlassian.com/cloud/jira/platform/rate-limiting/
- For `jira-per-issue-on-write`, Atlassian says to add delays between writes to the same issue, and other requests can continue. Source: https://developer.atlassian.com/cloud/jira/platform/rate-limiting/
- For quota exhaustion, Atlassian says to pause all requests until the window resets. Source: https://developer.atlassian.com/cloud/jira/platform/rate-limiting/
- Atlassian advises exponential backoff with jitter, using `Retry-After` as the minimum delay, a random factor of 0.7 to 1.3, and about 4 retries. Source: https://developer.atlassian.com/cloud/jira/platform/rate-limiting/
- Some 503 responses can also carry `Retry-After`. Source: https://developer.atlassian.com/cloud/jira/platform/rate-limiting/
