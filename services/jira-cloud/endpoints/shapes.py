"""The bodies Jira sends and accepts on the calls the app makes, each declared once. A member the site numbers or stamps (a numeric id,
`self`, an avatar, a time) is opaque: the book checks its type and leaves its value to the site."""

from __future__ import annotations

from ostler.book import Bool, Bytes, Field, Id, Int, List, Map, Num, Object, Str

from ..model.records import (AccountRecord, BoardRecord, FieldRecord, FilterRecord, IssueNumber, IssueRecord, IssueTypeRecord, LabelRecord, OptionRecord,
                             PriorityRecord, ProjectRecord, SprintRecord, StatusRecord, TransitionRecord)

SITE = "the site numbers it, and two sites number the same record apart"
LINK = "a URL on the site the book plays against"
CLOCK = "the site's clock stamps it"
NAMED = "the environment names its accounts, and the book knows the standing account only by its account id"
PAGING = "it counts or pages everything the site holds, which other people's records swell"

ISSUE = Id(IssueRecord, of=Str())
PROJECT = Id(ProjectRecord, of=Str())
ACCOUNT = Id(AccountRecord, of=Str())
BOARD = Id(BoardRecord, of=Int())
SPRINT = Id(SprintRecord, of=Int())
FILTER = Id(FilterRecord, of=Str())
FIELD = Id(FieldRecord, of=Str())
STATUS_ID = Id(StatusRecord, of=Str(), strangers="company-managed projects share status ids, so the book knows a status by its project and name")
TYPE_ID = Id(IssueTypeRecord, of=Str(), strangers="company-managed projects share issue type ids, so the book knows a type by its project and name")
NUMBER = Id(IssueNumber, of=Str(), strangers="the site numbers its issues, and the book names an issue by its key")
PRIORITY_ID = Id(PriorityRecord, of=Str(), strangers="every Cloud site gives its default priorities the ids 1 to 5")
OPTION_ID = Id(OptionRecord, of=Str(), strangers="the site numbers the options an admin adds, and the book picks one by its value")
TRANSITION_ID = Id(TransitionRecord, of=Str(), strangers="a workflow numbers its transitions, and two workflows of one site reuse the same numbers")
PROJECT_NUMBER = Id(ProjectRecord, of=Str(), strangers="the site numbers its projects, and the book names a project by its key")
LABEL = Id(LabelRecord, of=Str(), minted="a label is one record of the whole site and every run adds its own, so a search by label finds only "
                                         "what this run made")

ERRORS = Object(
    "ErrorCollection",
    errorMessages=Field(List(Str()), does="what went wrong with the request as a whole"),
    errors=Field(Map(Str()), does="what went wrong with each field, keyed by the field's id: `summary`, `parent` or `customfield_<n>`"),
)
NOT_SIGNED_IN = Bytes(b"")

CATEGORY = Object(
    "StatusCategory",
    key=Field(Str(), does="new, indeterminate or done; the app groups and counts by it"),
    id=Field(Int(), required=False, opaque="Jira numbers the categories, and only the key is what the app reads"),
    name=Field(Str(), required=False, opaque="the category's display name follows the site's language"),
    colorName=Field(Str(), required=False, opaque="a colour the app does not draw"),
    self=Field(Str(), required=False, opaque=LINK),
)
STATUS = Object(
    "StatusDetails",
    id=Field(STATUS_ID, opaque="company-managed projects share status ids, so the book knows a status by its project and name"),
    name=Field(Str()),
    statusCategory=Field(CATEGORY, does="the official example leaves it out, so the app tolerates its absence; the book expects it"),
    self=Field(Str(), required=False, opaque=LINK),
    description=Field(Str(), required=False, opaque="text an admin writes"),
    iconUrl=Field(Str(), required=False, opaque=LINK),
)
ISSUE_TYPE = Object(
    "IssueTypeDetails",
    id=Field(TYPE_ID, opaque="company-managed projects share issue type ids, so the book knows a type by its project and name"),
    name=Field(Str()),
    hierarchyLevel=Field(Int(), does="0 for a standard type, 1 for an epic, -1 for a sub-task"),
    subtask=Field(Bool()),
    self=Field(Str(), required=False, opaque=LINK),
    iconUrl=Field(Str(), required=False, opaque=LINK),
    description=Field(Str(), required=False, opaque="text an admin writes"),
)
PRIORITY = Object(
    "Priority",
    id=Field(PRIORITY_ID, does="1 Highest to 5 Lowest, the ids every Cloud site gives its default priorities"),
    name=Field(Str()),
    self=Field(Str(), required=False, opaque=LINK),
    iconUrl=Field(Str(), required=False, opaque=LINK),
)
USER = Object(
    "User",
    accountId=Field(ACCOUNT, does="the account's one stable id, which the app sends back in every user field"),
    displayName=Field(Str(), opaque=NAMED),
    active=Field(Bool()),
    accountType=Field(Str(), required=False, opaque="atlassian for a person, app for a bot"),
    emailAddress=Field(Str(), required=False, opaque="privacy settings may hide it"),
    timeZone=Field(Str(), required=False, opaque=NAMED),
    avatarUrls=Field(Map(Str()), required=False, opaque=LINK),
    self=Field(Str(), required=False, opaque=LINK),
)
SPRINT_ROW = Object(
    "Sprint",
    id=Field(SPRINT),
    name=Field(Str()),
    state=Field(Str(), does="active, future or closed"),
    originBoardId=Field(BOARD, required=False, does="the board the sprint was made on"),
    boardId=Field(BOARD, required=False, does="the board, in the Sprint field of an issue"),
    goal=Field(Str(), required=False, nullable=True, does="absent or empty when the sprint has no goal"),
    startDate=Field(Str(), required=False, opaque="the seed sets a sprint's dates on the day it runs"),
    endDate=Field(Str(), required=False, opaque="the seed sets a sprint's dates on the day it runs"),
    createdDate=Field(Str(), required=False, opaque=CLOCK),
    self=Field(Str(), required=False, opaque=LINK),
)
PARAGRAPH_TEXT = Object("Text", type=Field(Str()), text=Field(Str(), required=False))
PARAGRAPH = Object("Paragraph", type=Field(Str()), content=Field(List(PARAGRAPH_TEXT), required=False))
DOCUMENT = Object(
    "Document",
    type=Field(Str(), does="doc"),
    version=Field(Int(), does="1"),
    content=Field(List(PARAGRAPH), does="the blocks of the document; the book writes paragraphs of plain text, which every editable subset holds"),
)
OPTION = Object(
    "CustomFieldOption",
    value=Field(Str()),
    id=Field(OPTION_ID, required=False, opaque=SITE),
    self=Field(Str(), required=False, opaque=LINK),
)
PARENT_FIELDS = Object("ParentFields", summary=Field(Str()), status=Field(STATUS), issuetype=Field(ISSUE_TYPE),
                       priority=Field(PRIORITY, required=False, opaque="the row shows the child's priority, not the parent's"))
PARENT = Object(
    "Parent",
    key=Field(ISSUE),
    fields=Field(PARENT_FIELDS),
    id=Field(NUMBER, required=False, opaque=SITE),
    self=Field(Str(), required=False, opaque=LINK),
)
PROJECT_REF = Object("ProjectRef", key=Field(PROJECT), name=Field(Str()), id=Field(PROJECT_NUMBER, required=False, opaque=SITE),
                     self=Field(Str(), required=False, opaque=LINK), avatarUrls=Field(Map(Str()), required=False, opaque=LINK))
VERSION_OR_COMPONENT = Object("Named", name=Field(Str()), id=Field(OPTION_ID, required=False, opaque=SITE),
                              self=Field(Str(), required=False, opaque=LINK))

ISSUE_FIELDS = Object(
    "IssueFields",
    summary=Field(Str(), required=False),
    status=Field(STATUS, required=False),
    issuetype=Field(ISSUE_TYPE, required=False),
    priority=Field(PRIORITY, required=False, nullable=True),
    assignee=Field(USER, required=False, nullable=True, does="null when nobody is assigned"),
    parent=Field(PARENT, required=False, does="absent when the issue has no parent; replaces the Epic Link field in both project styles"),
    labels=Field(List(LABEL, unordered="Jira keeps an issue's labels as a set"), required=False),
    updated=Field(Str(), required=False, opaque=CLOCK),
    created=Field(Str(), required=False, opaque=CLOCK),
    reporter=Field(USER, required=False, nullable=True, opaque="the account that made the issue, which on a seeded issue is the seed's"),
    creator=Field(USER, required=False, nullable=True, opaque="the account that made the issue, which on a seeded issue is the seed's"),
    project=Field(PROJECT_REF, required=False),
    description=Field(DOCUMENT, required=False, nullable=True),
    environment=Field(DOCUMENT, required=False, nullable=True),
    duedate=Field(Str(format="date"), required=False, nullable=True),
    components=Field(List(VERSION_OR_COMPONENT), required=False),
    fixVersions=Field(List(VERSION_OR_COMPONENT), required=False),
    **{
        "cf[Sprint]": Field(List(SPRINT_ROW), required=False, nullable=True, does="the active or future sprint the issue is in, else null"),
        "cf[Story Points]": Field(Num(), required=False, nullable=True),
        "cf[Reviewer]": Field(USER, required=False, nullable=True),
        "cf[QA engineer]": Field(USER, required=False, nullable=True),
        "cf[Severity]": Field(OPTION, required=False, nullable=True),
        "cf[Acceptance criteria]": Field(DOCUMENT, required=False, nullable=True),
        "cf[Root cause]": Field(Map(Str()), required=False, nullable=True, opaque="a cascading select, which the app shows locked and never writes"),
        "cf[Story point estimate]": Field(Num(), required=False, nullable=True),
        "cf[Designer]": Field(USER, required=False, nullable=True),
        "cf[Browsers]": Field(List(OPTION, unordered="Jira keeps the ticked options as a set"), required=False, nullable=True),
        "cf[Affected service]": Field(Map(Str()), required=False, nullable=True, opaque="a cascading select, which the app shows locked and never writes"),
    },
)
ISSUE_ROW = Object(
    "Issue",
    key=Field(ISSUE, does="the issue key, such as CASE-131"),
    fields=Field(ISSUE_FIELDS, does="only the fields the request asked for"),
    id=Field(NUMBER, opaque=SITE),
    self=Field(Str(), required=False, opaque=LINK),
    expand=Field(Str(), required=False, opaque="the expansions Jira could add"),
)
ISSUE_DETAIL = Object(
    "IssueDetail",
    key=Field(ISSUE),
    fields=Field(ISSUE_FIELDS),
    id=Field(NUMBER, opaque=SITE),
    self=Field(Str(), required=False, opaque=LINK),
    expand=Field(Str(), required=False, opaque="the expansions Jira could add"),
    names=Field(Map(Str()), required=False, opaque="every field of the site, which holds fields the mockup world does not; the create screen's names are compared there"),
    schema=Field(Map(Map(Str())), required=False, opaque="every field of the site, which holds fields the mockup world does not; the create screen's schemas are compared there"),
    editmeta=Field(Map(Map(Str())), required=False, opaque="the edit screen of the site, which may hold system fields the mockup world leaves out; the create screen is compared field by field instead"),
)
SEARCH_PAGE = Object(
    "IssuePage",
    issues=Field(List(ISSUE_ROW), does="the page's issues in the order the JQL or the board's rank asks for"),
    isLast=Field(Bool(), required=False, does="true on the last page; the app also stops on a page with no token"),
    nextPageToken=Field(Str(), required=False, opaque="a token for the next page, which expires after 7 days"),
)
CREATED = Object(
    "CreatedIssue",
    key=Field(ISSUE, does="the new issue's key"),
    id=Field(NUMBER, opaque=SITE),
    self=Field(Str(), opaque=LINK),
)

PROJECT_ROW = Object(
    "Project",
    key=Field(PROJECT),
    name=Field(Str()),
    style=Field(Str(), does="classic for a company-managed project, next-gen for a team-managed one"),
    simplified=Field(Bool()),
    projectTypeKey=Field(Str(), does="software for a project with a board"),
    id=Field(PROJECT_NUMBER, opaque=SITE),
    self=Field(Str(), required=False, opaque=LINK),
    avatarUrls=Field(Map(Str()), required=False, opaque=LINK),
)
PROJECTS_PAGE = Object(
    "PageOfProjects",
    values=Field(List(PROJECT_ROW), does="the projects the caller may browse, by name"),
    startAt=Field(Int()),
    maxResults=Field(Int(), does="at most 100"),
    total=Field(Int(), required=False, opaque=PAGING),
    isLast=Field(Bool(), opaque=PAGING),
    self=Field(Str(), required=False, opaque=LINK),
    nextPage=Field(Str(), required=False, opaque=LINK),
)
LABELS_PAGE = Object(
    "PageOfLabels",
    values=Field(List(LABEL, unordered="Jira documents no order for its labels"), does="the labels of the site, or those starting with the query"),
    maxResults=Field(Int()),
    startAt=Field(Int(), required=False, opaque=PAGING),
    total=Field(Int(), required=False, opaque=PAGING),
    isLast=Field(Bool(), required=False, opaque=PAGING),
)
TYPE_STATUSES = Object(
    "IssueTypeWithStatus",
    name=Field(Str(), does="the issue type"),
    subtask=Field(Bool()),
    statuses=Field(List(STATUS, unordered="Jira documents no order for a workflow's statuses"), does="the statuses an issue of the type can hold"),
    id=Field(TYPE_ID, opaque="company-managed projects share issue type ids"),
    self=Field(Str(), required=False, opaque=LINK),
)
PROJECT_STATUSES = List(TYPE_STATUSES, unordered="Jira documents no order for a project's issue types")
CREATE_TYPE = Object(
    "IssueTypeIssueCreateMetadata",
    name=Field(Str()),
    hierarchyLevel=Field(Int(), does="UNCONFIRMED on an official page; the app reads it to tell standard types from epics"),
    subtask=Field(Bool()),
    id=Field(TYPE_ID, opaque="company-managed projects share issue type ids"),
    description=Field(Str(), required=False, opaque="text an admin writes"),
    iconUrl=Field(Str(), required=False, opaque=LINK),
    self=Field(Str(), required=False, opaque=LINK),
)
CREATE_TYPES = Object(
    "PageOfCreateMetaIssueTypes",
    issueTypes=Field(List(CREATE_TYPE, unordered="the issue type scheme orders the types, and the app sorts them itself")),
    startAt=Field(Int()),
    maxResults=Field(Int()),
    total=Field(Int(), required=False, opaque="a site may offer a sub-task type the mockup world leaves out"),
)
SCHEMA = Object(
    "JsonTypeBean",
    type=Field(Str(), does="the value's kind: string, number, user, option, array, priority and so on"),
    items=Field(Str(), required=False, nullable=True, does="the item kind of an array"),
    system=Field(Str(), required=False, nullable=True, does="the system field's name"),
    custom=Field(Str(), required=False, nullable=True, does="the custom field's type key; the app finds Sprint by its key and never by name"),
    customId=Field(Int(), required=False, opaque=SITE),
    configuration=Field(Map(Str()), required=False, opaque="the type's settings, which the app does not read"),
)
FIELD_META = Object(
    "FieldCreateMetadata",
    fieldId=Field(FIELD, does="summary, priority and the other system ids, or customfield_<n> for a custom field"),
    name=Field(Str()),
    required=Field(Bool()),
    schema=Field(SCHEMA),
    operations=Field(List(Str(), unordered="Jira lists a field's operations in no documented order")),
    key=Field(Str(), required=False, opaque="the field's key, which repeats its id"),
    allowedValues=Field(List(Map(Str())), required=False, opaque="option objects whose ids the site numbers; the edit tests pick by value"),
    hasDefaultValue=Field(Bool(), required=False, opaque="an admin sets defaults per context"),
    defaultValue=Field(Map(Str()), required=False, opaque="an admin sets defaults per context"),
    autoCompleteUrl=Field(Str(), required=False, opaque=LINK),
    configuration=Field(Map(Str()), required=False, opaque="the field's settings, which the app does not read"),
)
CREATE_FIELDS = Object(
    "PageOfCreateMetaIssueTypeWithField",
    fields=Field(List(FIELD_META), does="the create screen's fields in the screen's order"),
    startAt=Field(Int()),
    maxResults=Field(Int(), does="at most 200"),
    total=Field(Int(), required=False, opaque="a site's create screen may hold system fields, such as Reporter or Attachment, the mockup world leaves out"),
    results=Field(List(FIELD_META), required=False, opaque="the schema lists it beside fields; the app reads fields"),
)
TRANSITION = Object(
    "IssueTransition",
    name=Field(Str(), does="the transition's name, which in the seeded workflows is the target status's"),
    to=Field(STATUS, does="the status the transition leads to; the app picks a transition by it"),
    hasScreen=Field(Bool(), does="true when the transition shows a screen"),
    isAvailable=Field(Bool(), does="false only when includeUnavailableTransitions asks for transitions that fail a condition"),
    id=Field(TRANSITION_ID, opaque="a workflow numbers its transitions, and two workflows of one site reuse the same numbers"),
    isGlobal=Field(Bool(), required=False, opaque="how an admin drew the workflow"),
    isInitial=Field(Bool(), required=False, opaque="how an admin drew the workflow"),
    isConditional=Field(Bool(), required=False, opaque="how an admin drew the workflow"),
    isLooped=Field(Bool(), required=False, opaque="how an admin drew the workflow"),
    fields=Field(Map(Map(Str())), required=False, opaque="the screen's fields; the book reads hasScreen, and the transition call is where a required field refuses"),
)
TRANSITIONS = Object(
    "Transitions",
    transitions=Field(List(TRANSITION, unordered="Jira documents no order for a workflow's transitions"), does="the transitions the workflow allows from the issue's status"),
    expand=Field(Str(), required=False, opaque="the expansions Jira could add"),
)
PEOPLE = List(USER, unordered="Jira returns people in no documented order")

BOARD_ROW = Object(
    "Board",
    id=Field(BOARD),
    name=Field(Str()),
    type=Field(Str(), does="scrum, kanban or simple"),
    self=Field(Str(), required=False, opaque=LINK),
    location=Field(Map(Str()), required=False, opaque="the project the board sits in, with its avatar"),
    isPrivate=Field(Bool(), required=False, opaque="how an admin shares the board"),
)
BOARDS_PAGE = Object(
    "PageOfBoards",
    values=Field(List(BOARD_ROW), does="the boards whose filter names the project"),
    startAt=Field(Int()),
    maxResults=Field(Int()),
    total=Field(Int(), required=False, opaque=PAGING),
    isLast=Field(Bool(), required=False, opaque=PAGING),
)
COLUMN_STATUS = Object("ColumnStatus", id=Field(STATUS_ID, opaque="company-managed projects share status ids"), self=Field(Str(), required=False, opaque=LINK))
COLUMN = Object(
    "BoardColumn",
    name=Field(Str()),
    statuses=Field(List(COLUMN_STATUS), does="one entry per status the column holds"),
    min=Field(Int(), required=False, opaque="WIP limits are out of the app's scope"),
    max=Field(Int(), required=False, opaque="WIP limits are out of the app's scope"),
)
BOARD_CONFIG = Object(
    "BoardConfiguration",
    id=Field(BOARD),
    name=Field(Str()),
    type=Field(Str()),
    filter=Field(Object("BoardFilter", id=Field(FILTER), self=Field(Str(), required=False, opaque=LINK))),
    columnConfig=Field(Object("ColumnConfig", columns=Field(List(COLUMN), does="the board's columns in the board's order; a kanban board with "
                                                                                 "its backlog on starts with a Backlog column"),
                              constraintType=Field(Str(), required=False, opaque="WIP limits are out of the app's scope"))),
    self=Field(Str(), required=False, opaque=LINK),
    location=Field(Map(Str()), required=False, opaque="the project the board sits in"),
    estimation=Field(Map(Map(Str())), required=False, opaque="the estimation field the board names, which the seed leaves as the template sets it"),
    ranking=Field(Map(Int()), required=False, opaque="Rank is internal to Jira Software"),
    subQuery=Field(Map(Str()), required=False, opaque="a kanban board's sub-filter, which the template sets"),
)
SPRINTS_PAGE = Object(
    "PageOfSprints",
    values=Field(List(SPRINT_ROW), does="the board's sprints in the states the query asks for, in the board's order"),
    startAt=Field(Int()),
    maxResults=Field(Int()),
    isLast=Field(Bool(), required=False, opaque=PAGING),
)
FILTER_DETAIL = Object(
    "Filter",
    id=Field(FILTER),
    jql=Field(Str(), does="the board's query, which the kanban backlog fallback narrows to the backlog column's statuses"),
    name=Field(Str(), opaque="the board template names the filter"),
    self=Field(Str(), required=False, opaque=LINK),
    owner=Field(Map(Str()), required=False, opaque=NAMED),
    viewUrl=Field(Str(), required=False, opaque=LINK),
    searchUrl=Field(Str(), required=False, opaque=LINK),
    favourite=Field(Bool(), required=False, opaque="a person's choice"),
)

SEARCH_BODY = Object(
    "SearchRequest",
    jql=Field(Str(classes={"a bounded query": "project = CASE ORDER BY updated DESC"}), does="a bounded query; the book's carry the run's label"),
    fields=Field(List(Str()), required=False, does="only the fields a row or card shows; the id alone when left out"),
    maxResults=Field(Int(), required=False, does="100 for an issue list; 50 when left out"),
    nextPageToken=Field(Str(classes={"a token no page gave": "not-a-page-token"}), required=False, does="the previous page's token"),
)
ISSUE_FIELDS_IN = Object(
    "IssueFieldsSent",
    project=Field(Object("ProjectKey", key=Field(PROJECT)), required=False),
    issuetype=Field(Object("TypeId", id=Field(TYPE_ID, does="the site's id of the type, read from createmeta")), required=False),
    summary=Field(Str(), required=False),
    description=Field(DOCUMENT, required=False),
    priority=Field(Object("PriorityId", id=Field(PRIORITY_ID)), required=False),
    assignee=Field(Object("AccountRef", accountId=Field(ACCOUNT)), required=False, nullable=True),
    parent=Field(Object("ParentKey", key=Field(ISSUE)), required=False),
    labels=Field(List(LABEL), required=False),
    **{
        "cf[Severity]": Field(Object("OptionValue", value=Field(Str())), required=False),
        "cf[Reviewer]": Field(Object("AccountRef", accountId=Field(ACCOUNT)), required=False, nullable=True),
        "cf[QA engineer]": Field(Object("AccountRef", accountId=Field(ACCOUNT)), required=False, nullable=True),
        "cf[Designer]": Field(Object("AccountRef", accountId=Field(ACCOUNT)), required=False, nullable=True),
        "cf[Story Points]": Field(Num(), required=False, nullable=True),
        "cf[Story point estimate]": Field(Num(), required=False, nullable=True),
        "cf[Acceptance criteria]": Field(DOCUMENT, required=False, nullable=True),
        "cf[Browsers]": Field(List(Object("OptionValue", value=Field(Str()))), required=False),
    },
)
CREATE_BODY = Object("IssueCreate", fields=Field(ISSUE_FIELDS_IN, does="each field the create screen holds that the person filled"))
EDIT_BODY = Object(
    "IssueUpdate",
    fields=Field(ISSUE_FIELDS_IN, required=False, does="values to set, in the shape the field research lists"),
    update=Field(Map(List(Map(Str()))), required=False, does="operations: one add or remove per label, or a parent set to none"),
)
TRANSITION_BODY = Object("TransitionRequest", transition=Field(Object("TransitionId", id=Field(TRANSITION_ID, does="the id of a transition the issue offers"))))
MOVE_BODY = Object("MoveIssues", issues=Field(List(ISSUE), does="at most 50 issue keys"))
