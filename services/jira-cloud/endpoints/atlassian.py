"""The Atlassian pages the book's claims rest on, as the research notes under docs/milestones/0001-issues-epics-and-board/artifacts/ read
them. Jira itself is never in this repository, so an element points at the published contract and not at code. A pointer into a spec
names the operation as `<METHOD> <path>` or the schema by its name."""

PLATFORM = "https://dac-static.atlassian.com/cloud/jira/platform/swagger-v3.v3.json"
AGILE = "https://dac-static.atlassian.com/cloud/jira/software/swagger.v3.json"

BASIC_AUTH = "https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/"
ISSUES_GROUP = "https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/"
ISSUE_SEARCH = "https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/"
USER_SEARCH = "https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-user-search/"
LABELS = "https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-labels/"
SPRINT_GROUP = "https://developer.atlassian.com/cloud/jira/software/rest/api-group-sprint/"
ENHANCED_SEARCH = ("https://community.developer.atlassian.com/t/rfc-61-evolving-search-capabilities-addressing-scalability-with-a-new-"
                   "enhanced-search-api/83027")
SOFTWARE_LISTS = ("https://community.developer.atlassian.com/t/rfc-127-jira-software-cloud-api-changes-improving-scalability-for-"
                  "software-space-issue-results/98871")
EPIC_LINK = ("https://community.developer.atlassian.com/t/deprecation-of-the-epic-link-parent-link-and-other-related-fields-in-rest-apis-"
             "and-webhooks/54048")
CREATEMETA = "https://community.developer.atlassian.com/t/create-issue-meta-endpoint-deprecation/75413"
CREATE_FAILS = "https://support.atlassian.com/jira/kb/issue-creation-in-jira-fails-silently-after-entering-all-field-data/"
SPRINT_ON_CREATE = "https://support.atlassian.com/jira/kb/creating-an-issue-in-a-sprint-using-the-jira-rest-api/"
STATUS_CATEGORIES = "https://community.developer.atlassian.com/t/bad-documentation-for-rest-api-3-statuscategory/78565"
BACKLOG_COLUMN = "https://community.developer.atlassian.com/t/additional-backlog-column-returned-from-api/58269"
KANBAN_BACKLOG = "https://community.atlassian.com/forums/Jira-questions/Accessing-Backlog-Issues-on-Kanban-Boards-via-JIRA-REST-API/qaq-p/2697457"
