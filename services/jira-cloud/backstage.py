"""The backstage of a Jira site: the standing account's credential and the address of the site. Nothing here is a model of Jira.

The sandbox takes its site, email and token from `JIRA_SITE`, `JIRA_EMAIL` and `JIRA_TOKEN`, which `saddlebag exec` puts in the run's
environment, as the live tests take them. The local fake Jira takes the same variables when they are set, else the test account the
fake is expected to accept. Neither place lets the book put a screen on a transition while it runs, so that arrangement is refused."""

from __future__ import annotations

import os

from ostler.book import CannotArrange, Environment

FAKE_EMAIL = "ana.ruiz@acme-labs.test"
FAKE_TOKEN = "fake-jira-token"


class Backstage:
    def __init__(self, environment: Environment):
        self.environment = environment

    def address(self, name: str) -> str:
        return self.environment.address(name)

    def credential(self) -> str:
        email = os.environ.get("JIRA_EMAIL")
        token = os.environ.get("JIRA_TOKEN")
        if email and token:
            return f"{email}:{token}"
        if self.environment.name == "local":
            return f"{FAKE_EMAIL}:{FAKE_TOKEN}"
        raise CannotArrange(f"JIRA_EMAIL and JIRA_TOKEN are not set, so the book cannot sign in to {self.environment.name}")

    def revoked(self) -> str:
        email = self.credential().split(":", 1)[0]
        return f"{email}:a-token-jira-no-longer-accepts"

    def put_screen_on_done(self) -> None:
        raise CannotArrange(f"{self.environment.name} offers no call that puts a screen on a transition while the book runs: the fake takes "
                            "--transition-screen when it starts, and the sandbox needs an admin in the browser")

    def take_screen_off_done(self) -> None:
        raise CannotArrange(f"{self.environment.name} offers no call that takes a screen off a transition while the book runs")
