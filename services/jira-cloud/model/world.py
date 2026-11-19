"""The standing world the seed builds on a site and `FakeJira::mockup_world()` serves: the three projects of the milestone mockups, their issue
types, statuses, boards, sprints and screens. The app never writes any of it, so the model starts with it and no call makes it."""

from __future__ import annotations

from .records import SPRINT_KIND, BoardRecord, Column, FieldRecord, IssueTypeRecord, ProjectRecord, SprintRecord, StatusRecord

CFT = "com.atlassian.jira.plugin.system.customfieldtypes:"
STANDARD = ("Bug", "Story", "Task")
TYPES = ("Bug", "Story", "Task", "Epic")

PROJECTS = (
    ProjectRecord("CASE", "Case Platform", "classic", False),
    ProjectRecord("CASE1", "Case Portal", "next-gen", True),
    ProjectRecord("OPS", "Operations", "classic", False),
)

WORKFLOWS = {
    "CASE": (("To Do", "new"), ("In Progress", "indeterminate"), ("In Review", "indeterminate"), ("Done", "done")),
    "CASE1": (("Backlog", "new"), ("To Do", "new"), ("In Progress", "indeterminate"), ("Done", "done")),
    "OPS": (("To Do", "new"), ("In Progress", "indeterminate"), ("Done", "done")),
}
INITIAL = {"CASE": "To Do", "CASE1": "Backlog", "OPS": "To Do"}
NO_TRANSITION = {"CASE": (("In Review", "To Do"),), "CASE1": (), "OPS": ()}

STATUSES = tuple(StatusRecord(f"{project}:{name}", project, name, category) for project, flow in WORKFLOWS.items() for name, category in flow)
ISSUE_TYPES = tuple(IssueTypeRecord(f"{project.key}:{name}", project.key, name, 1 if name == "Epic" else 0) for project in PROJECTS for name in TYPES)

BOARDS = (
    BoardRecord("CASE board", "CASE board", "scrum", "CASE",
                (Column("To Do", ("To Do",)), Column("In Progress", ("In Progress",)), Column("In Review", ("In Review",)), Column("Done", ("Done",))),
                "Filter for CASE board", "project = CASE ORDER BY Rank ASC", True),
    BoardRecord("CASE1 board", "CASE1 board", "kanban", "CASE1",
                (Column("Backlog", ("Backlog",)), Column("To Do", ("To Do",)), Column("In Progress", ("In Progress",)), Column("Done", ("Done",))),
                "Filter for CASE1 board", "project = CASE1 ORDER BY Rank ASC", True),
    BoardRecord("OPS board", "OPS board", "kanban", "OPS",
                (Column("To Do", ("To Do",)), Column("In Progress", ("In Progress",)), Column("Done", ("Done",))),
                "Filter for OPS board", "project = OPS ORDER BY Rank ASC", False),
)

SPRINTS = (
    SprintRecord("Sprint 14", "CASE board", "Sprint 14", "active"),
    SprintRecord("Sprint 15", "CASE board", "Sprint 15", "future"),
    SprintRecord("Sprint 16", "CASE board", "Sprint 16", "future"),
)
SPRINT_GOALS = {"Sprint 14": "Intake v2 on staging", "Sprint 15": "Audit trail, first slice", "Sprint 16": ""}

SEVERITIES = ("S1 Critical", "S2 Major", "S3 Minor", "S4 Trivial")
BROWSERS = ("Chrome", "Firefox", "Safari", "Edge")
COMPONENTS = {"CASE": ("Intake", "Review queue", "Audit", "Attachments"), "CASE1": (), "OPS": ("Backups", "Databases", "Email")}
VERSIONS = {"CASE": ("2026.12", "2027.01"), "CASE1": (), "OPS": ()}

SCREENS = {
    "CASE:Bug": ("cf[Severity]!", "priority", "assignee", "cf[Reviewer]", "cf[QA engineer]", "parent", "cf[Sprint]", "labels", "components", "fixVersions", "environment", "cf[Root cause]"),
    "CASE:Story": ("priority", "assignee", "cf[Reviewer]", "cf[QA engineer]", "cf[Story Points]", "parent", "cf[Sprint]", "labels", "components", "fixVersions", "duedate", "cf[Acceptance criteria]"),
    "CASE:Task": ("priority", "assignee", "cf[Reviewer]", "parent", "cf[Sprint]", "labels", "components", "duedate"),
    "CASE:Epic": ("priority", "assignee", "labels", "components", "fixVersions", "duedate"),
    "CASE1:Bug": ("priority", "assignee", "cf[Browsers]", "parent", "labels", "duedate", "environment"),
    "CASE1:Story": ("priority", "assignee", "cf[Designer]", "cf[Story point estimate]", "parent", "labels", "duedate"),
    "CASE1:Task": ("priority", "assignee", "cf[Story point estimate]", "parent", "labels", "duedate"),
    "CASE1:Epic": ("priority", "assignee", "labels", "duedate"),
    "OPS:Bug": ("cf[Affected service]!", "priority", "assignee", "parent", "labels", "components", "environment"),
    "OPS:Story": ("priority", "assignee", "parent", "labels", "components", "duedate"),
    "OPS:Task": ("priority", "assignee", "parent", "labels", "components", "duedate"),
    "OPS:Epic": ("priority", "assignee", "labels", "duedate"),
}
LEADING = ("summary", "issuetype", "project", "description")

KINDS: dict[str, tuple[str, str | None, str | None, str | None, tuple[str, ...], bool]] = {
    "summary": ("Summary", None, "summary", None, ("set",), True),
    "issuetype": ("Issue Type", None, "issuetype", None, (), True),
    "project": ("Project", None, "project", None, ("set",), True),
    "description": ("Description", None, "description", None, ("set",), True),
    "priority": ("Priority", None, "priority", None, ("set",), True),
    "assignee": ("Assignee", None, "assignee", None, ("set",), True),
    "parent": ("Parent", None, "parent", None, ("set",), True),
    "labels": ("Labels", "string", "labels", None, ("add", "set", "remove"), True),
    "components": ("Components", "component", "components", None, ("add", "set", "remove"), True),
    "fixVersions": ("Fix versions", "version", "fixVersions", None, ("set", "add", "remove"), True),
    "duedate": ("Due date", None, "duedate", None, ("set",), True),
    "environment": ("Environment", None, "environment", None, ("set",), True),
    "cf[Sprint]": ("Sprint", None, None, SPRINT_KIND, ("set",), True),
    "cf[Story Points]": ("Story Points", None, None, CFT + "float", ("set",), True),
    "cf[Reviewer]": ("Reviewer", None, None, CFT + "userpicker", ("set",), True),
    "cf[QA engineer]": ("QA engineer", None, None, CFT + "userpicker", ("set",), True),
    "cf[Severity]": ("Severity", None, None, CFT + "select", ("set",), True),
    "cf[Acceptance criteria]": ("Acceptance criteria", None, None, CFT + "textarea", ("set",), True),
    "cf[Root cause]": ("Root cause", None, None, CFT + "cascadingselect", ("set",), False),
    "cf[Story point estimate]": ("Story point estimate", None, None, "com.pyxis.greenhopper.jira:jsw-story-points", ("set",), True),
    "cf[Designer]": ("Designer", None, None, CFT + "userpicker", ("set",), True),
    "cf[Browsers]": ("Browsers", "option", None, CFT + "multicheckboxes", ("add", "set", "remove"), True),
    "cf[Affected service]": ("Affected service", None, None, CFT + "cascadingselect", ("set",), False),
}
TYPE_OF = {
    "summary": "string", "issuetype": "issuetype", "project": "project", "description": "string", "priority": "priority", "assignee": "user",
    "parent": "issuelink", "labels": "array", "components": "array", "fixVersions": "array", "duedate": "date", "environment": "string",
    "cf[Sprint]": "array", "cf[Story Points]": "number", "cf[Reviewer]": "user", "cf[QA engineer]": "user", "cf[Severity]": "option",
    "cf[Acceptance criteria]": "string", "cf[Root cause]": "option-with-child", "cf[Story point estimate]": "number", "cf[Designer]": "user",
    "cf[Browsers]": "array", "cf[Affected service]": "option-with-child",
}
ITEMS_OF_SPRINT = "json"


def allowed(project: str, field: str) -> tuple[str, ...]:
    if field == "cf[Severity]":
        return SEVERITIES
    if field == "cf[Browsers]":
        return BROWSERS
    if field == "components":
        return COMPONENTS[project]
    if field == "fixVersions":
        return VERSIONS[project]
    if field == "priority":
        return ("Highest", "High", "Medium", "Low", "Lowest")
    return ()


def _fields() -> tuple[FieldRecord, ...]:
    made: list[FieldRecord] = []
    for project in PROJECTS:
        types = [name for name in TYPES if f"{project.key}:{name}" in SCREENS]
        order: list[str] = list(LEADING)
        required: dict[str, list[str]] = {}
        screens: dict[str, list[str]] = {}
        for name in types:
            for field in LEADING:
                screens.setdefault(field, []).append(name)
            for entry in SCREENS[f"{project.key}:{name}"]:
                field = entry.rstrip("!")
                if field not in order:
                    order.append(field)
                screens.setdefault(field, []).append(name)
                if entry.endswith("!"):
                    required.setdefault(field, []).append(name)
        for field in order:
            label, items, system, custom, operations, editable = KINDS[field]
            essential = ("summary", "issuetype", "project")
            made.append(FieldRecord(
                f"{project.key}:{field}", field, project.key, label, TYPE_OF[field], ITEMS_OF_SPRINT if field == "cf[Sprint]" else items, system, custom,
                operations, tuple(screens[field]), tuple(types) if field in essential else tuple(required.get(field, ())), allowed(project.key, field),
                editable))
    return tuple(made)


FIELDS = _fields()
