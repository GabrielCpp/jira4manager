# Disagreements

Each entry: the step, what the design notes and the research say, what the app did, and the classification.

## 1. The stack names a fake Jira that does not exist yet

- Step: `ops/stack.yml` brings up `jira-cloud:fake-jira` with `cargo xtask fake-jira --port 8787`, found while writing the book.
- Notes: `docs/design/agent-test-environment.md` and the milestone's decision "The local fake Jira" describe the command, its flags and the world it serves. The walking skeleton is to build it.
- App did: nothing. The repository holds no Cargo workspace and no `xtask`, so the command fails and `ostler env up jira-cloud` cannot start the local environment.
- Classification: app missing. The book keeps the command as the notes write it and invents no stand-in. Until the walking skeleton lands, the book plays only against the sandbox environment, with `JIRA_SITE`, `JIRA_EMAIL` and `JIRA_TOKEN` set.

## 2. The fake Jira listens on loopback, which a container does not publish

- Step: `ops/services/fake-jira.yml.j2` runs the command inside a container and publishes port 8787.
- Notes: the test-environment note says the command serves on `127.0.0.1`.
- App did: not yet built, so not observed.
- Classification: open. A server bound to the container's loopback is unreachable through a published port. The stack keeps the command as written; the story that builds `cargo xtask fake-jira` decides whether it takes a bind address, or whether the stack runs the fake on the host.
