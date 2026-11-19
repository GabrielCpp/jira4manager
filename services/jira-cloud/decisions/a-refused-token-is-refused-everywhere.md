story: none
date: 2026-11-19
elements: GetMyself, SearchProjects
sources: docs/milestones/0001-issues-epics-and-board/artifacts/platform-research-2026-11-17.md

The app signs every request with HTTP Basic, the email and an unscoped API token, against the site URL. Jira checks the credential before it reads the request, so a token it no longer accepts gets a 401 on every call, and so does a request with no credential. The app reads any 401 after sign-in as the token having stopped working, returns to sign-in and removes the token from the keychain. Sign-in and every launch call myself first, so the health journey reads it too.

The body of that 401 is UNCONFIRMED; QUESTIONS.md asks it.
