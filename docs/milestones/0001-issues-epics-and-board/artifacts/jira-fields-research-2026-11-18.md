# Jira Cloud fields and custom fields: REST API research (2026-11-18)

Scope: facts a desktop client needs to build its create form and its issue detail pane from Jira's field metadata.
Each fact cites a source tag from the list at the end.
The v3 platform and Jira Software references were read from Atlassian's published OpenAPI specs, which back the reference pages [S1–S7].
UNCONFIRMED marks a claim no source settled.

## 1. Create metadata: `GET /rest/api/3/issue/createmeta/{projectIdOrKey}/issuetypes/{issueTypeId}`

- The endpoint returns a page of field metadata for one project and one issue type [S1].
- It needs the *Create issues* project permission [S1].
- Query parameters: `startAt` (default 0) and `maxResults` (default 50, maximum 200) [S1].
- A `maxResults` above 200 returns 400 with `"Parameter 'maxResults' must not exceed the limit '200'"` [S1].
- The page object holds `fields` (array), `startAt`, `maxResults` and `total` [S1]. The schema also lists a `results` array with the same item type [S1].
- One field entry (`FieldCreateMetadata`) has these properties [S1]:
  - `fieldId` (string, required). Example: `"assignee"`, `"customfield_10020"`.
  - `key` (string, required).
  - `name` (string, required). The display name.
  - `required` (boolean, required).
  - `schema` (required): `type` (required), `items`, `system`, `custom`, `customId` (int64), `configuration`.
  - `operations` (string array, required). Example: `["set"]`, or `["set","add"]` for a multi select.
  - `allowedValues` (array, optional).
  - `hasDefaultValue` (boolean, optional) and `defaultValue` (any, optional).
  - `autoCompleteUrl` (string, optional).
  - `configuration` (object, optional).
- `schema.system` names a system field. `schema.custom` is the custom field type key. `schema.items` names the item type when `type` is `array` [S1].
- Doc example entry: `{"fieldId":"assignee","hasDefaultValue":false,"key":"assignee","name":"Assignee","operations":["set"],"required":true}` [S1].
- The companion `GET /rest/api/3/issue/createmeta/{projectIdOrKey}/issuetypes` lists issue types, with the same `startAt`/`maxResults` defaults (0, 50, max 200) [S1].
- The older `GET /rest/api/3/issue/createmeta` with `expand=projects.issuetypes.fields` is deprecated [S1][S25].

## 2. Edit metadata and field display names

- `GET /rest/api/3/issue/{issueIdOrKey}/editmeta` returns "the edit screen fields for an issue that are visible to and editable by the user" [S1].
- Response: `{"fields": {"<fieldId>": FieldMetadata}}`, an object keyed by field id [S1].
- `FieldMetadata` has the same properties as the createmeta entry except `fieldId`. The map key carries the id [S1].
- A field appears only when all of these hold [S1]:
  - it is on a screen of the issue's screen scheme;
  - the field configuration shows it;
  - field-specific conditions pass (for example Assignee needs assign permission);
  - a custom field has a valid context for the project and issue type;
  - the workflow step is editable (`jira.issue.editable`);
  - the user has *Edit issues*;
  - workflow `jira.permission.*` properties allow it.
- Fields hidden on the issue layout settings page stay editable and are still returned [S1].
- `overrideScreenSecurity` and `overrideEditableFlag` exist, but only Connect and Forge apps with *Administer Jira* can use them. Other callers get 403 [S1].
- So editmeta lists only edit-screen fields that this user can edit. Read-only fields of the issue are absent [S1].
- `PUT /rest/api/3/issue/{id}` itself "doesn't check screen configurations to determine if a field is editable" [S1].
- Display names for an issue's fields: `GET /rest/api/3/issue/{id}?expand=names,schema` [S1].
  - `names` "Returns the display name of each field".
  - `schema` "Returns the schema describing a field type".
  - `editmeta` is also an expand option, so one call can return values, names, schemas and edit metadata [S1].
- `GET /rest/api/3/field` returns all system and custom fields the user can see [S2]. Each item has `id`, `key`, `name`, `custom`, `orderable`, `navigable`, `searchable`, `clauseNames`, `schema`, and `scope` [S2].
- `scope` is set for fields of team-managed projects: `{"type":"PROJECT","project":{...}}` [S2].
- `GET /rest/api/3/field/search` is the paged variant, with `type`, `id`, `query`, `orderBy`, `projectIds` and `expand` [S2].

## 3. `schema.custom` type keys

Prefix `cft` = `com.atlassian.jira.plugin.system.customfieldtypes`.

| Field type | `schema.custom` | Source |
|---|---|---|
| User picker (single) | `cft:userpicker` | [S1] |
| User picker (multiple) | `cft:multiuserpicker` | [S1] |
| Select list (single) | `cft:select` | [S1] |
| Select list (multiple) | `cft:multiselect` (`type: array`, `items: option`) | [S1] |
| Radio buttons | `cft:radiobuttons` | [S1] |
| Checkboxes | `cft:multicheckboxes` | [S1] |
| Number | `cft:float` | [S1] |
| Date picker | `cft:datepicker` | [S1] |
| Date time picker | `cft:datetime` | [S1] |
| Text field (single line) | `cft:textfield` | [S1] |
| Paragraph (multi-line) | `cft:textarea` | [S1] |
| URL | `cft:url` | [S1] |
| Labels (custom) | `cft:labels` | [S1][S9] |
| Cascading select | `cft:cascadingselect` | [S1] |
| Sprint | `com.pyxis.greenhopper.jira:gh-sprint` | [S6][S12] |
| Team | `com.atlassian.teams:rm-teams-custom-field-team` (`type: any`) | [S8] |
| Story point estimate (team-managed) | `com.pyxis.greenhopper.jira:jsw-story-points`. Community post only. | [S12] |
| Story Points (company-managed) | `cft:float`. Atlassian calls it "just a regular numeric field". | [S6] |
| Rank | `com.pyxis.greenhopper.jira:gh-lexo-rank`. UNCONFIRMED. | none |
| People (team-managed) | UNCONFIRMED. | none |

- The v3 spec lists every `cft:` key above. It does not tie each key to a UI name [S1]. The mapping from UI name to key is UNCONFIRMED for checkboxes, radio buttons and date time, but the key names are unambiguous.
- The Team schema also carries `configuration: {"com.atlassian.jira.plugin.system.customfieldtypes:atlassian-team": true}` [S8].
- The Sprint key "will be the same on every instance". Match fields by `schema.custom`, not by name [S6][S12].
- Jira Software calls Rank an internal field that "shouldn't be read or updated using the REST API" [S6].
- Team-managed "People" is the equivalent of a company-managed user picker [S16]. Its `schema.custom` key is UNCONFIRMED.

## 4. Values to send on create and edit

- Create: `POST /rest/api/3/issue` with `fields` (set values) and optional `update` (operations) [S1].
- Edit: `PUT /rest/api/3/issue/{id}` with `fields` and/or `update` [S1].
- One field cannot appear in both `fields` and `update` in one request. UNCONFIRMED from Atlassian docs. Community reports show the error "Field labels cannot appear in both 'fields' and 'update'".
- `update` operations are `set`, `add`, `remove`, `edit` and `copy` [S1]. Each field's `operations` array in the metadata says which apply [S1].

| Field | JSON value | Source |
|---|---|---|
| Single user picker | `{"accountId": "5b10..."}`. `{"id": "5b10..."}` also works. | [S1][S10][S11] |
| Multi user picker | `[{"accountId": "..."}, ...]`. An empty array clears it. | [S11][S23] |
| Single select / radio | `{"value": "red"}` | [S1][S9] |
| Single select by id | `{"id": "10001"}`. UNCONFIRMED from Atlassian Cloud docs. | none |
| Multi select / checkboxes | `[{"value": "red"}, {"value": "blue"}]` | [S9] |
| Cascading select | `{"value": "green", "child": {"value": "blue"}}` | [S9] |
| Number | `42.07` (JSON number) | [S9] |
| Date picker | `"2011-10-03"` (`YYYY-MM-DD`). The system `duedate` uses the same form. | [S1][S9] |
| Date time | `"2011-10-19T10:29:29.908+1100"` | [S9] |
| Text field (single line) | plain string | [S1] |
| Paragraph, `description`, `environment` | Atlassian Document Format object | [S1] |
| URL | plain string | [S9] |
| Labels | `["bugfix", "blitz_test"]` | [S1] |
| Labels add/remove | `"update": {"labels": [{"add": "triaged"}, {"remove": "blocker"}]}` | [S1] |
| Components | `[{"id": "10000"}]` | [S1] |
| Fix versions / affects versions | `[{"id": "10001"}]` | [S1] |
| Priority | `{"id": "20000"}` | [S1] |
| Parent | `{"key": "PROJ-123"}`. ID also accepted. | [S1] |
| Remove parent | `"update": {"parent": [{"set": {"none": true}}]}`. Exact shape UNCONFIRMED. | [S1] |
| Sprint | the sprint id as a bare number: `"customfield_10021": 2` | [S6][S15] |
| Team | the team UUID as a plain string | [S8] |
| Assignee / reporter | `{"accountId": "..."}`. The create example uses `{"id": "..."}`. | [S1][S10] |

- The doc text on user fields says to use "`id` (for account ID) ... instead of `name`" [S10]. The `User` schema says `accountId` is "Required in requests" [S1]. An Atlassian developer advocate states both keys "work interchangeably" [S11].
- JRACLOUD-72000 reported that `accountId` failed for a multi-user picker. Atlassian closed it as Invalid [S23].
- Sprint can be set on create when the Sprint field is on the create screen [S15]. Otherwise Jira returns "Field 'sprint' cannot be set. It is not on the appropriate screen, or unknown." [S15].
- "an issue can only be in one active or future sprint at a time, and only the active/future sprint can edited" [S6].
- The Agile move-to-sprint endpoint accepts only "open or active sprints", up to 50 issues per call [S7].
- The exact error for setting a closed sprint through the field is UNCONFIRMED.
- Team: subtasks inherit the parent's Team and cannot change it [S8].
- On read, Team returns an object `{id, name, avatarUrl, isVisible, title, isShared}`, not the bare UUID [S8].

## 5. User search for user pickers

| Endpoint | What it filters | Paging | Permission |
|---|---|---|---|
| `GET /rest/api/3/user/picker?query=` | prefix match on `displayName` / `emailAddress` | `maxResults` default 50. It scans only the first 1000 users, so results can be short. | *Browse users and groups*. Otherwise exact name match only. |
| `GET /rest/api/3/user/search?query=` | active users matching query or property | `startAt` 0, `maxResults` 50, up to the 1000th user | *Browse users and groups*. Otherwise empty results. |
| `GET /rest/api/3/user/assignable/search?project=&query=` | users who can be assigned in a project, issue or transition | `startAt` 0, `maxResults` 50. It filters after fetching, so results can be short. | *Browse users and groups* or *Assign issues* |
| `GET /rest/api/3/user/viewissue/search?projectKey=&query=` | users who can browse the issue or project | `startAt` 0, `maxResults` 50 | *Browse users and groups* |

All rows come from [S3].

- The picker response is `{"total", "header", "users": [{accountId, accountType, displayName, avatarUrl, html}]}`. `html` highlights the match with `<strong>` [S3].
- It accepts `excludeAccountIds` and `showAvatar` [S3].
- Privacy settings may hide `emailAddress` in every endpoint [S3].
- Assignee: use `assignable/search`. It returns only users who hold *Assign issues* rights [S3].
- Custom user fields ("Reviewer", "QA engineer") have no permission gate in Jira's docs. `user/search` or `user/picker` fits them. This advice is an inference from the endpoint descriptions. No Atlassian page names an endpoint for custom user fields (UNCONFIRMED as official guidance).
- A single-user picker custom field can carry "User Filtering" to groups or project roles [S22]. The KB says filtering "is not available for User picker (multiple users) fields" [S22]. Neither public endpoint applies that filter, so a client may offer users Jira later rejects (UNCONFIRMED).
- An invalid user returns 400 `{"errors":{"customfield_15240":"User '...' is not valid for this user picker."}}` [S14].
- createmeta's `autoCompleteUrl` for user fields points at `/rest/api/1.0/users/picker?fieldName=...&fieldConfigId=...&projectId=...`. That URL works with basic auth and fails under OAuth 2.0 [S19]. The field-aware filter it may apply is UNCONFIRMED.

## 6. Labels

- `GET /rest/api/3/label` returns a paginated list: `{"startAt","maxResults","total","isLast","values":["performance","security"]}` [S4].
- Its parameters are `startAt` (0), `maxResults` (default 1000), `query` (case-insensitive prefix, applied before paging) and `scope` (`RECENT_PROJECTS` or `ALL_BROWSEABLE_PROJECTS`) [S4].
- createmeta gives labels fields an `autoCompleteUrl` of `/rest/api/1.0/labels/suggest?query=` [S17].
- That route is undocumented. Connect apps get 403 on it and Forge apps get 401 [S17][S18].
- `GET /rest/api/3/jql/autocompletedata/suggestions?fieldName=&fieldValue=` is a documented alternative [S5]. It also covers custom label fields [S17]. Its `maxResults` caps at 50 (default 15) and is experimental [S5].
- A new label needs no create call. Sending a new string in `labels` (or `update.labels.add`) creates it [S1]. No Atlassian page states this outright (UNCONFIRMED as a documented rule). The request example sends free-form labels [S1], and no label-create endpoint exists in the v3 spec [S1].
- Labels cannot contain spaces. This is UNCONFIRMED from API docs. A Cloud bug shows the UI rejecting spaces while still creating a label with one [S21].

## 7. Fields the caller cannot set, and missing required fields

- Create metadata is computed "for the user". The old endpoint says it returns "the create screen fields for each issue type for the user" [S1].
- `POST /issue` says the settable fields "are the same fields that appear on the issue's create screen" [S1].
- Permission-gated system fields drop out of the screen for users who lack the permission. Reporter is absent without *Modify Reporter* [S20][S24]. Whether createmeta omits every field the user cannot set is UNCONFIRMED.
- Create returns 400 when the request [S1]:
  - is missing required fields;
  - contains invalid field values;
  - contains fields that cannot be set for the issue type;
  - comes from a user without permission.
- The error body is `{"errorMessages": [...], "errors": {"<fieldId>": "<message>"}}` [S1][S13].
- Missing required custom field example: `{"errorMessages":[],"errors":{"customfield_10139":"Custom Field 1 is required."}}` [S13].
- The reference example puts a missing system field under `errorMessages`: `{"errorMessages":["Field 'priority' is required"],"errors":{}}` [S1]. A client must read both keys.
- A field not on the create screen returns `"Field '<id>' cannot be set. It is not on the appropriate screen, or unknown."` [S15].
- A required field missing from the create screen still blocks creation, and Jira reports it as required [S13]. createmeta then cannot show it, because it lists screen fields only (UNCONFIRMED).
- Create also returns 422 for "a configuration problem" [S1]. Edit returns 409 for a conflicting update [S1].

## 8. Team-managed vs company-managed field ids

- Custom field ids differ per site. "Custom fields may indeed have different IDs on every instance, this is expected." [S12]
- Team-managed custom fields belong to one project. A field "created in one team-managed space" cannot be shared with another [S16]. `GET /rest/api/3/field` marks them with `scope.type = PROJECT` and the owning project [S2].
- Two team-managed projects with a "Severity" dropdown therefore have two distinct `customfield_*` ids. This follows from [S2][S16]. No source states it as a rule (UNCONFIRMED).
- Story points use different fields. Company-managed boards use "Story Points" (`cft:float`). Team-managed projects use "Story point estimate" (`jsw-story-points`, community post only) [S6][S12].
- A board's configured estimation field comes from the Agile board configuration resource [S6]. That is the reliable way to pick the right one per board.
- The Sprint field is one site-wide Jira Software field with key `gh-sprint`, and both project types use it. This is UNCONFIRMED. [S6] identifies Sprint by schema and describes it as a single Jira Software field. Community reports show team-managed projects adding look-alike fields named "Sprint" [S26]. Match Sprint by `schema.custom`, never by name.
- The Team field is a single site field, enabled per site and per project [S8].

## UNCONFIRMED summary

1. Rank `schema.custom` = `com.pyxis.greenhopper.jira:gh-lexo-rank`. Seen only in non-Cloud KB and third-party sources.
2. Team-managed People field `schema.custom` key.
3. Story point estimate `com.pyxis.greenhopper.jira:jsw-story-points`. One community post, no Atlassian doc.
4. UI-name-to-key mapping for checkboxes (`multicheckboxes`), radio (`radiobuttons`) and date time (`datetime`). The keys exist in the spec, but no Cloud page maps them to UI names.
5. Single select set by `{"id": ...}` in Cloud.
6. Exact `update.parent` shape for removing a parent.
7. Exact error when setting the Sprint field to a closed sprint.
8. Official guidance on which user-search endpoint suits custom user fields. Whether any public endpoint honours a field's user filtering.
9. New labels are created implicitly by sending the string. Supported by examples, not stated.
10. The no-spaces rule for labels through the API.
11. createmeta omits every field the user cannot set (shown only for reporter).
12. Same field in both `fields` and `update` is rejected. Community error text only.
13. Sprint field is a single site-wide field shared by both project types.
14. Team-managed same-named fields get distinct ids per project. Inferred, not stated.

## Sources

- [S1] Jira Cloud REST v3, Issues group (createmeta, editmeta, create, edit, get issue) and schemas. https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/ . Read from the spec at https://developer.atlassian.com/cloud/jira/platform/swagger-v3.v3.json
- [S2] Jira Cloud REST v3, Issue fields group. https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-fields/
- [S3] Jira Cloud REST v3, User search group. https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-user-search/
- [S4] Jira Cloud REST v3, Labels group. https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-labels/
- [S5] Jira Cloud REST v3, JQL group (field autocomplete suggestions). https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-jql/
- [S6] Jira Software Cloud REST intro, "Jira Software field input formats". https://developer.atlassian.com/cloud/jira/software/rest/intro/ . Read from the spec at https://developer.atlassian.com/cloud/jira/software/swagger.v3.json
- [S7] Jira Software Cloud REST, Sprint group (move issues to sprint). https://developer.atlassian.com/cloud/jira/software/rest/api-group-sprint/
- [S8] Team field in Jira REST API. https://developer.atlassian.com/platform/teams/components/team-field-in-jira-rest-api
- [S9] Jira REST API examples (Server docs, custom field input formats). https://developer.atlassian.com/server/jira/platform/jira-rest-api-examples/
- [S10] User privacy API migration guide. https://developer.atlassian.com/cloud/jira/platform/deprecation-notice-user-privacy-api-migration-guide/
- [S11] Developer community: custom field format for single and multiple user. https://community.developer.atlassian.com/t/rest-api-custom-field-format-for-single-user-and-multiple-user-is-out-of-date/82139
- [S12] Developer community: variancy of Jira Cloud custom field keys. https://community.developer.atlassian.com/t/confirm-variancy-of-jira-cloud-issue-field-keys-for-custom-fields/21134
- [S13] KB: Issue creation fails silently after entering all field data. https://support.atlassian.com/jira/kb/issue-creation-in-jira-fails-silently-after-entering-all-field-data/
- [S14] KB: User is not valid for this user picker. https://support.atlassian.com/jira/kb/user-user-is-not-valid-for-this-user-picker-while-creating-jira-issue/
- [S15] KB: Creating an issue in a sprint using the Jira REST API. https://support.atlassian.com/jira/kb/creating-an-issue-in-a-sprint-using-the-jira-rest-api/
- [S16] Available custom fields for team-managed projects. https://support.atlassian.com/jira-software-cloud/docs/available-custom-fields-for-team-managed-projects/
- [S17] Developer community: options for a custom label field. https://community.developer.atlassian.com/t/how-to-get-possible-options-for-a-custom-label-field-via-the-rest-api-v2-or-v3/88269
- [S18] Developer community: scope for the labels/suggest route. https://community.developer.atlassian.com/t/what-is-the-scope-needed-for-the-labels-suggest-route/64863
- [S19] Developer community: OAuth 2.0 is not enabled for method (1.0 users/picker). https://community.developer.atlassian.com/t/oauth-2-0-is-not-enabled-for-method/60843
- [S20] JSDCLOUD-11454: reporter not on screen without Modify Reporter. https://jira.atlassian.com/browse/JSDCLOUD-11454
- [S21] JRACLOUD-82154: Jira Cloud allows a label with a space. https://jira.atlassian.com/browse/JRACLOUD-82154
- [S22] KB: Can't search for some users in single user picker field. https://support.atlassian.com/jira/kb/cant-search-for-some-users-in-single-user-picker-field-in-jira-cloud/
- [S23] JRACLOUD-72000: multi-user picker and accountId (closed, Invalid). https://jira.atlassian.com/browse/JRACLOUD-72000
- [S24] KB: You don't have permission to modify the reporter. https://support.atlassian.com/jira/kb/you-dont-have-permission-to-modify-the-reporter-in-this-project-in-jira/
- [S25] Changelog CHANGE-1304: create issue meta endpoint deprecation. https://developer.atlassian.com/cloud/jira/platform/changelog/#CHANGE-1304
- [S26] Community: the source of the new field "Sprint[Checkboxes]". https://community.atlassian.com/forums/Jira-questions/The-source-of-the-new-field-quot-Sprint-Checkboxes-quot/qaq-p/2622196
