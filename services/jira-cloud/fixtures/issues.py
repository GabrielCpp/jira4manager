"""What a caller sends about issues: the issue a create sends, the edits and transitions it makes, the issues it moves between a sprint and
the backlog, and the issue it opens. A later step names an issue through the fixture of the step that made it, never through its key."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from ostler.book import Actor, Fixture, On, Reference

from ..model.records import PRIORITY_IDS
from ..model.world import INITIAL

BOOK_LABEL = "j4m-book"
WALK_LABEL = "j4m-walk"
WALK_EPIC_LABEL = "j4m-walk-epic"
ROW_FIELDS = ("summary", "status", "issuetype", "priority", "assignee", "parent", "labels", "updated")


def adf(text: str) -> dict[str, Any]:
    """A description in Atlassian Document Format: one paragraph of plain text, which every editable subset holds."""
    return {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": text}]}]}


def type_reference(project: str, name: str) -> Reference:
    """The id the site gave an issue type of a project, which the surface reads from the project's create metadata."""
    return Reference(f"issuetype:{project}:{name}")


@dataclass(eq=False)
class Issue(Fixture):
    """An issue a person creates: the project, the type and the summary, and each field the create screen holds that they filled. `key` is
    unknown until Jira answers. `values` holds custom fields by `cf[<name>]`. Every issue the book makes carries the journey's label."""

    project: str = "CASE"
    type: str = "Task"
    summary: str | None = "Write the rollout checklist"
    description: Any = None
    priority: str | None = None
    assignee: str | None = None
    parent: Issue | None = None
    labels: tuple[str, ...] = (BOOK_LABEL,)
    values: dict[str, Any] = field(default_factory=dict)
    key: str | None = None

    def __str__(self) -> str:
        return f"{self.type} {self.summary!r} in {self.project}"

    @property
    def fields(self) -> dict[str, Any]:
        sent: dict[str, Any] = {"project": {"key": self.project}, "issuetype": {"id": type_reference(self.project, self.type)}}
        if self.summary is not None:
            sent["summary"] = self.summary
        if self.description is not None:
            sent["description"] = adf(self.description) if isinstance(self.description, str) else self.description
        if self.priority is not None:
            sent["priority"] = {"id": PRIORITY_IDS[self.priority]}
        if self.assignee is not None:
            sent["assignee"] = {"accountId": self.assignee}
        if self.parent is not None:
            sent["parent"] = {"key": self.parent.key}
        if self.labels:
            sent["labels"] = list(self.labels)
        sent.update(self.values)
        return sent

    @property
    def missing(self) -> str:
        """The first required field the create leaves empty, as Jira words it: `<field id>: <name> is required.`"""
        from ..model.rules import first_missing

        return first_missing(self)

    @property
    def off_create(self) -> str:
        """The first field the create sends that the type's create screen does not hold."""
        from ..model.rules import first_off_create

        return first_off_create(self)

    @property
    def status(self) -> str:
        return INITIAL[self.project]

    @classmethod
    def examples(cls, state: Any, by: Actor | None) -> Iterable[Issue]:
        yield task("Retire the fax intake", labels=(WALK_LABEL,))
        yield epic("Intake form v3", labels=(WALK_EPIC_LABEL,))
        yield task("Copy legacy attachments", labels=(WALK_EPIC_LABEL,))
        for record in state.issues:
            if record.type == "CASE:Epic":
                yield child_of(Issue(project=record.project, type="Epic", labels=record.labels, key=record.key))


def task(summary: str = "Write the rollout checklist", project: str = "CASE", **more: Any) -> Issue:
    return Issue(project=project, type="Task", summary=summary, **more)


def story(summary: str = "Reassign a case from the review queue", project: str = "CASE", **more: Any) -> Issue:
    return Issue(project=project, type="Story", summary=summary, **more)


def epic(summary: str = "Intake form v3", project: str = "CASE", **more: Any) -> Issue:
    return Issue(project=project, type="Epic", summary=summary, **more)


def bug(project: str = "CASE", summary: str = "Double-clicking Submit creates two cases", severity: str | None = "S2 Major", **more: Any) -> Issue:
    """A Bug. CASE requires Severity on its Bug create screen, so a CASE bug fills it unless `severity` is None."""
    values = dict(more.pop("values", {}))
    if project == "CASE" and severity is not None:
        values["cf[Severity]"] = {"value": severity}
    return Issue(project=project, type="Bug", summary=summary, values=values, **more)


def child_of(parent: Issue, summary: str = "Postcode lookup on the address step", type: str = "Story", **more: Any) -> Issue:
    return Issue(project=parent.project, type=type, summary=summary, parent=parent, labels=parent.labels, **more)


def labelled(issue: Issue, label: str) -> Issue:
    return issue.set(labels=(label,))


@dataclass(eq=False)
class Opening(Fixture):
    """The issue a person opens, and the fields and expansions the read asks for. The detail pane asks for every field with its name, schema
    and edit metadata; the read after a write asks for the changed field and `updated`."""

    issue: Issue = field(default_factory=Issue)
    fields: str = "*all"
    expand: str | None = "names,schema,editmeta"

    @property
    def key(self) -> str | None:
        return self.issue.key

    def __str__(self) -> str:
        return f"open {self.issue} ({self.fields})"

    @classmethod
    def examples(cls, state: Any, by: Actor | None) -> Iterable[Opening]:
        for record in state.issues:
            yield cls(Issue(project=record.project, type=record.type.split(":")[1], key=record.key))


def opening(issue: Issue) -> Opening:
    return Opening(issue)


def confirming(issue: Issue, *changed: str) -> Opening:
    """The read after a write: the field that changed and `updated`."""
    return Opening(issue, ",".join((*changed, "updated")), None)


def row_of(issue: Issue) -> Opening:
    """The read after a create: the row fields of the new issue."""
    return Opening(issue, ",".join(ROW_FIELDS), None)


@dataclass(eq=False)
class Edit(Fixture):
    """What an edit sends: `fields` sets values, `update` runs operations such as adding a label. `parent` names the epic the edit sets as
    the parent, by the fixture of the step that made it."""

    set_to: dict[str, Any] = field(default_factory=dict)
    operations: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    parent: Issue | None = None

    @property
    def fields(self) -> dict[str, Any] | None:
        sent = dict(self.set_to)
        if self.parent is not None:
            sent["parent"] = {"key": self.parent.key}
        return sent or None

    @property
    def update(self) -> dict[str, Any] | None:
        return self.operations or None


@dataclass(frozen=True)
class Editing(On):
    """An edit of one issue: the issue, and what the edit sends."""

    @property
    def issue(self) -> Issue:
        return self.target  # type: ignore[return-value]

    @property
    def edit(self) -> Edit:
        return self.body  # type: ignore[return-value]

    @property
    def key(self) -> str | None:
        return self.issue.key

    @property
    def off_screen(self) -> str:
        from ..model.rules import first_off_screen

        return first_off_screen(self)

    @classmethod
    def examples(cls, state: Any, by: Actor | None) -> Iterable[Editing]:
        for record in state.issues:
            yield cls(Issue(project=record.project, type=record.type.split(":")[1], key=record.key), Edit({"summary": "Renamed by the walk"}))


def editing(issue: Issue, **fields: Any) -> Editing:
    return Editing(issue, Edit(dict(fields)))


def retitle(issue: Issue, summary: str) -> Editing:
    return editing(issue, summary=summary)


def describe(issue: Issue, text: str) -> Editing:
    return editing(issue, description=adf(text))


def reprioritise(issue: Issue, priority: str) -> Editing:
    return editing(issue, priority={"id": PRIORITY_IDS[priority]})


def assign(issue: Issue, account: str | None) -> Editing:
    return editing(issue, assignee=None if account is None else {"accountId": account})


def set_value(issue: Issue, field_id: str, value: Any) -> Editing:
    return editing(issue, **{field_id: value})


def add_label(issue: Issue, label: str) -> Editing:
    return Editing(issue, Edit(operations={"labels": [{"add": label}]}))


def remove_label(issue: Issue, label: str) -> Editing:
    return Editing(issue, Edit(operations={"labels": [{"remove": label}]}))


def adopt(child: Issue, parent: Issue) -> Editing:
    """Sets the issue's parent to an epic, as Add existing and the epic picker do."""
    return Editing(child, Edit(parent=parent))


def orphan(child: Issue) -> Editing:
    """Clears the issue's parent, as the remove action of a child row does."""
    return Editing(child, Edit(operations={"parent": [{"set": {"none": True}}]}))


@dataclass(eq=False)
class Transition(Fixture):
    """The transition a status change runs: the one whose target is the chosen status. The surface finds its id among the issue's
    transitions."""

    to: str = "In Progress"
    issue: Issue | None = None

    @property
    def id(self) -> Reference:
        key = self.issue.key if self.issue is not None else ""
        return Reference(f"transition:{key}:{self.to}")

    def __str__(self) -> str:
        return f"the transition to {self.to}"


@dataclass(eq=False)
class Move(Fixture):
    transition: Transition = field(default_factory=Transition)


@dataclass(frozen=True)
class Transitioning(On):
    """A status change of one issue: the issue, and the transition to the chosen status."""

    @property
    def issue(self) -> Issue:
        return self.target  # type: ignore[return-value]

    @property
    def to(self) -> str:
        return self.body.transition.to  # type: ignore[attr-defined]

    @property
    def key(self) -> str | None:
        return self.issue.key

    @property
    def transition(self) -> str:
        return f"to {self.to}"

    @classmethod
    def examples(cls, state: Any, by: Actor | None) -> Iterable[Transitioning]:
        for record in state.issues:
            issue = Issue(project=record.project, type=record.type.split(":")[1], key=record.key)
            for to in ("In Progress", "In Review", "Done", "To Do"):
                yield transition(issue, to)


def transition(issue: Issue, to: str) -> Transitioning:
    return Transitioning(issue, Move(Transition(to, issue)))


@dataclass(eq=False)
class TransitionsOf(Fixture):
    """The transitions a person may run on an issue now, with the fields each one's screen holds."""

    issue: Issue = field(default_factory=Issue)
    expand: str = "transitions.fields"

    @property
    def key(self) -> str | None:
        return self.issue.key

    def __str__(self) -> str:
        return f"the transitions of {self.issue}"

    @classmethod
    def examples(cls, state: Any, by: Actor | None) -> Iterable[TransitionsOf]:
        for record in state.issues:
            yield cls(Issue(project=record.project, type=record.type.split(":")[1], key=record.key))


def transitions_of(issue: Issue) -> TransitionsOf:
    return TransitionsOf(issue)


@dataclass(eq=False)
class Moving(Fixture):
    """Issues moved into a sprint, or to the backlog when `sprint` is None. The app sends at most 50 a call."""

    moved: tuple[Issue, ...] = ()
    sprint: str | None = None

    @property
    def sprintId(self) -> str | None:
        return self.sprint

    @property
    def issues(self) -> list[str | None]:
        return [issue.key for issue in self.moved]

    @property
    def count(self) -> int:
        return len(self.moved)

    def __str__(self) -> str:
        where = self.sprint or "the backlog"
        return f"{len(self.moved)} issue(s) to {where}"

    @classmethod
    def examples(cls, state: Any, by: Actor | None) -> Iterable[Moving]:
        mine = [Issue(project=r.project, type=r.type.split(":")[1], key=r.key) for r in state.issues if r.project == "CASE"]
        if mine:
            yield cls(tuple(mine[:1]), "Sprint 15")
            yield cls(tuple(mine[:1]), None)


def into_sprint(sprint: str, *issues: Issue) -> Moving:
    return Moving(tuple(issues), sprint)


def to_backlog(*issues: Issue) -> Moving:
    return Moving(tuple(issues), None)


def too_many(sprint: str | None, issue: Issue) -> Moving:
    """One more issue than a call may move: the same issue named 51 times, so the limit refuses the call before Jira looks any issue up."""
    return Moving(tuple(issue for _ in range(51)), sprint)
