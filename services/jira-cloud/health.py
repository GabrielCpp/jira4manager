from datetime import date

from ostler.book import Journey

from .endpoints import GetMyself
from .model.cast import MANAGER


class TheTokenIsAccepted(Journey):
    """What every other journey stands on, read before any of them runs: the site answers, and it accepts the standing account's email and
    token and names the account."""

    def steps(self, today: date):
        yield GetMyself(by=MANAGER)
