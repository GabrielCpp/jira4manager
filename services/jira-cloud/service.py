"""Jira Cloud as jira4manager calls it, as ostler loads it.

Two environments play the same book. `local` is the fake Jira that `ostler env` runs from `ops/stack.yml`, serving the mockup world on
loopback. `sandbox` is the live Jira Cloud site the seed built, reached at `JIRA_SITE` with the token saddlebag holds. A difference
between the two is a defect in the fake or in the book. Jira itself is never in this repository, so no element points at its source."""

from __future__ import annotations

import os

from ostler.book import Because, Environment, Service, Stack, Unseen

from .backstage import Backstage
from .endpoints import ALL as ENDPOINTS
from .endpoints.common import SERVICE_REFUSALS
from .endpoints import ListBoardBacklog, ListBoardIssues, ListSprintIssues, ScreenComesOffDone, ScreenGoesOnDone, SearchIssues
from .health import TheTokenIsAccepted
from .journeys import ALL as JOURNEYS
from .model.cast import CAST
from .model.lifecycle import MATRICES
from .model.records import BoardRecord, FieldRecord, IssueRecord, IssueTypeRecord, LabelRecord, ProjectRecord, SprintRecord, StatusRecord
from .model.state import Serving, new_model
from .surface import JiraSurface


def site() -> str:
    named = os.environ.get("JIRA_SITE", "").strip().rstrip("/")
    if not named:
        return "https://jira-sandbox.invalid"
    return named if "://" in named else f"https://{named}"


ENVIRONMENTS = {
    "local": Environment("local", hosts={"jira": "ostler:"}, backstage=Backstage),
    "sandbox": Environment("sandbox", hosts={"jira": site()}, backstage=Backstage),
}


def stack(log_dir: str) -> Stack:
    return Stack((), log_dir)


UNSEEN = (
    Unseen(SearchIssues, "200: nextPageToken", Because.NEVER_FILLED, "a search narrowed to one run's label holds fewer than 100 issues"),
    Unseen(ListSprintIssues, "200: nextPageToken", Because.NEVER_FILLED, "a list narrowed to one run's label holds fewer than 100 issues"),
    Unseen(ListBoardIssues, "200: nextPageToken", Because.NEVER_FILLED, "a list narrowed to one run's label holds fewer than 100 issues"),
    Unseen(ListBoardBacklog, "200: nextPageToken", Because.NEVER_FILLED, "a list narrowed to one run's label holds fewer than 100 issues"),
)

service = Service[Serving](
    name="jira-cloud",
    environments=ENVIRONMENTS,
    default_environment="local",
    new_model=new_model,
    surface=JiraSurface,
    journeys=JOURNEYS,
    stack=stack,
    endpoints=ENDPOINTS,
    matrices=MATRICES,
    cast=CAST,
    outside=(ScreenGoesOnDone, ScreenComesOffDone),
    records=(ProjectRecord, IssueTypeRecord, StatusRecord, BoardRecord, SprintRecord, IssueRecord, FieldRecord, LabelRecord),
    watch=(),
    refusals=SERVICE_REFUSALS,
    health=(TheTokenIsAccepted,),
    unseen=UNSEEN,
)
