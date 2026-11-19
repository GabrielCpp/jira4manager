"""The callers a journey can name. The manager is the standing account the book signs in with: on the sandbox, the site's admin whose token
saddlebag holds; on the local fake Jira, the account the fake accepts. The revoked caller sends the manager's email with a token Jira no
longer accepts, as a person does once their token expired."""

from __future__ import annotations

from dataclasses import dataclass

from ostler.book import Actor


@dataclass(frozen=True)
class Member(Actor):
    revoked: bool = False

    @property
    def identity(self) -> str:
        return self.handle


MANAGER = Member("manager")
REVOKED = Member("revoked", revoked=True)

CAST = (MANAGER, REVOKED)
