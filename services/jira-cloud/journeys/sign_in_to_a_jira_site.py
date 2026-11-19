from datetime import date

from ostler.book import Journey, Same

from ..endpoints import GetMyself, SearchProjects
from ..fixtures import ProjectsPage
from ..model.cast import MANAGER, REVOKED


class SignInToAJiraSite(Journey):
    """A manager enters their site, email and API token. The app checks them against myself, which names the account, and fills the
    sidebar with the projects they may browse, by name. On the next launch the app checks the stored token the same way and meets the same
    account. When the token stops working, every call answers 401, so the app returns to sign-in, and a sign-in with no token at all is
    refused the same way."""

    def steps(self, today: date):
        signed_in = GetMyself(by=MANAGER)
        yield signed_in
        yield SearchProjects(query=ProjectsPage(), by=MANAGER)
        relaunched = GetMyself(by=MANAGER)
        yield relaunched
        yield Same(signed_in, relaunched)
        yield GetMyself(by=REVOKED)
        yield SearchProjects(query=ProjectsPage(), by=REVOKED)
        yield GetMyself(by=None)
