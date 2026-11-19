"""What a Jira site keeps that the app reads or writes. Projects, issue types, statuses, boards, sprints and fields are the standing world the
seed builds, and the app never writes them. Issues and labels are what a journey makes.

A standing record is named in the model by what a person can read on the site: a project by its key, a status by its project and name, a
custom field by its name. The ids Jira gives them differ from one site to the next, so the surface learns them by name."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar

CATEGORY_ORDER = {"indeterminate": 0, "new": 1, "undefined": 1, "done": 2}
PRIORITIES = ("Highest", "High", "Medium", "Low", "Lowest")
PRIORITY_IDS = {name: str(at + 1) for at, name in enumerate(PRIORITIES)}
SPRINT_FIELD = "cf[Sprint]"
SPRINT_KIND = "com.pyxis.greenhopper.jira:gh-sprint"
MOVE_LIMIT = 50


@dataclass(frozen=True)
class ProjectRecord:
    """One project of the site. `style` is `classic` for a company-managed project and `next-gen` for a team-managed one."""

    source: ClassVar[tuple[str, ...]] = ("https://dac-static.atlassian.com/cloud/jira/platform/swagger-v3.v3.json::Project",)

    key: str
    name: str
    style: str
    simplified: bool

    def __str__(self) -> str:
        return self.key


@dataclass(frozen=True)
class IssueTypeRecord:
    """One issue type a project offers. Level 0 is a standard type, 1 an epic and -1 a sub-task."""

    source: ClassVar[tuple[str, ...]] = ("https://dac-static.atlassian.com/cloud/jira/platform/swagger-v3.v3.json::IssueTypeDetails",)

    key: str
    project: str
    name: str
    hierarchyLevel: int

    @property
    def subtask(self) -> bool:
        return self.hierarchyLevel < 0

    def __str__(self) -> str:
        return self.key


@dataclass(frozen=True)
class StatusRecord:
    """One status of a project's workflow, with its category key: `new`, `indeterminate` or `done`."""

    source: ClassVar[tuple[str, ...]] = ("https://dac-static.atlassian.com/cloud/jira/platform/swagger-v3.v3.json::StatusDetails", "https://community.developer.atlassian.com/t/bad-documentation-for-rest-api-3-statuscategory/78565")

    key: str
    project: str
    name: str
    category: str

    def __str__(self) -> str:
        return self.key


@dataclass(frozen=True)
class Column:
    name: str
    statuses: tuple[str, ...]


@dataclass(frozen=True)
class BoardRecord:
    """One board of a project. A kanban board with its backlog on keeps the statuses of its first column out of the board."""

    source: ClassVar[tuple[str, ...]] = ("https://dac-static.atlassian.com/cloud/jira/software/swagger.v3.json::BoardConfigBean",)

    id: str
    name: str
    type: str
    project: str
    columns: tuple[Column, ...]
    filter: str
    filter_jql: str
    backlog: bool

    @property
    def backlog_statuses(self) -> tuple[str, ...]:
        if self.type == "kanban" and self.backlog and self.columns and self.columns[0].name == "Backlog":
            return self.columns[0].statuses
        return ()

    @property
    def board_statuses(self) -> tuple[str, ...]:
        return tuple(status for column in self.columns for status in column.statuses if status not in self.backlog_statuses)

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class SprintRecord:
    """One sprint of a scrum board: `active`, `future` or `closed`."""

    source: ClassVar[tuple[str, ...]] = ("https://dac-static.atlassian.com/cloud/jira/software/swagger.v3.json::GET /rest/agile/1.0/board/{boardId}/sprint",)

    id: str
    board: str
    name: str
    state: str

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class FieldRecord:
    """One field a create or edit screen of a project holds. `id` is the system field id, or `cf[<name>]` for a custom field, which the
    surface turns into the site's `customfield_<n>`. `screens` lists the issue types whose create screen holds the field, and `required`
    those where it is required."""

    source: ClassVar[tuple[str, ...]] = ("https://dac-static.atlassian.com/cloud/jira/platform/swagger-v3.v3.json::FieldCreateMetadata",)

    key: str
    id: str
    project: str
    name: str
    type: str
    items: str | None
    system: str | None
    custom: str | None
    operations: tuple[str, ...]
    screens: tuple[str, ...]
    required: tuple[str, ...] = ()
    allowed: tuple[str, ...] = ()
    editable: bool = True

    def __str__(self) -> str:
        return self.key


@dataclass(frozen=True)
class LabelRecord:
    """A label of the site. A label exists once an issue carries it, and Jira lists it from then on."""

    source: ClassVar[tuple[str, ...]] = ("https://dac-static.atlassian.com/cloud/jira/platform/swagger-v3.v3.json::GET /rest/api/3/label",)

    name: str

    def __str__(self) -> str:
        return self.name


class AccountRecord:
    """An Atlassian account, which the book only needs to recognise: the standing account the book signs in with."""


class FilterRecord:
    """The saved filter behind a board, which the book only needs to recognise."""


class IssueNumber:
    """The numeric id Jira gives an issue beside its key, which the book only needs to recognise: the book names an issue by its key."""


class PriorityRecord:
    """One of the site's priorities, which the book only needs to recognise: every Cloud site gives its defaults the ids 1 to 5."""


class OptionRecord:
    """An option of a select field, a component or a version, which the book only needs to recognise: it picks an option by its value."""


class TransitionRecord:
    """A transition of a workflow, which the book only needs to recognise: it picks a transition by the status it leads to."""


@dataclass(frozen=True)
class IssueRecord:
    """One issue of a project. `key` is the model's id, which the runtime pairs with the key Jira gave the issue. `rank` is the issue's
    place in its board's order, and `stamp` the order of its last change, which `updated` shows."""

    source: ClassVar[tuple[str, ...]] = ("https://dac-static.atlassian.com/cloud/jira/platform/swagger-v3.v3.json::IssueBean",)

    key: str
    project: str
    type: str
    summary: str
    status: str
    priority: str
    assignee: str | None
    parent: str | None
    labels: tuple[str, ...]
    sprint: str | None
    rank: int
    stamp: int
    description: Any = None
    values: tuple[tuple[str, Any], ...] = ()

    def value(self, field: str) -> Any:
        return dict(self.values).get(field)

    def with_value(self, field: str, value: Any) -> tuple[tuple[str, Any], ...]:
        held = dict(self.values)
        if value is None:
            held.pop(field, None)
        else:
            held[field] = value
        return tuple(sorted(held.items()))

    def __str__(self) -> str:
        return f"{self.summary!r} ({self.type.split(':')[-1]})"
