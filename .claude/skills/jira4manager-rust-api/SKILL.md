---
name: jira4manager-rust-api
description: "HTTP API rules for Rust with axum 0.8 on tokio: a router function that takes the state, handlers that extract, call one service and map the result, request and response types kept apart from the domain, one ApiError that renders RFC 9457 problem+json for domain errors and for extractor rejections, strict JSON bodies, and a main with graceful shutdown. The concrete mechanics behind http-design for this stack. Load when adding or changing a route, a handler, a request or response type, an error mapping or middleware, or when an axum handler fails to compile."
metadata:
  name: rust-api
  generated_by: farrier
  source: library/skills/stacks/rust/rust-api/SKILL.md
  resolve: "farrier source .claude/skills/jira4manager-rust-api/SKILL.md"
  do_not_edit: "generated — run the `resolve` command below for this machine's editable source path, edit that, then `make agent-install` to regenerate"
  tags: [rust, backend, standards]
---

# HTTP API

The resource, status code and error contract is [http-design](~/.claude/skills/http-design/SKILL.md). This skill states how axum 0.8 delivers it.

## Layout

```text
crates/api/
  src/
    lib.rs        AppState and router()
    main.rs       config, listener, serve, shutdown
    compose.rs    the composition root
    config.rs     Config from the environment
    error.rs      ApiError and the problem+json body
    extract.rs    ApiJson and ApiQuery
    routes/
      mod.rs
      tasks.rs    one file per resource
  tests/
    tasks.rs      one file per resource
```

## Router and state

```rust
#[derive(Clone)]
pub struct AppState {
    pub tasks: TaskService,
}

pub fn router(state: AppState) -> Router {
    Router::new()
        .route("/healthz", get(|| async { "ok" }))
        .merge(routes::tasks::routes())
        .layer(TraceLayer::new_for_http())
        .with_state(state)
}
```

- Build the whole app in `router(state)`. `main` passes the composed state and a test passes a state built over fakes.
- Give `AppState` one public field per service. Each resource file exports `routes() -> Router<AppState>`, and `router` merges them.
- Write a path parameter as `/tasks/{id}`. The older `/:id` form panics at startup in axum 0.8.
- Add cross-cutting behaviour as a `tower` layer on the router, before `with_state`.

## Handlers

```rust
async fn create(
    State(state): State<AppState>,
    ApiJson(body): ApiJson<CreateTask>,
) -> Result<impl IntoResponse, ApiError> {
    let task = state.tasks.add(&body.title).await?;
    let location = format!("/tasks/{}", task.id);
    Ok((
        StatusCode::CREATED,
        [(header::LOCATION, location)],
        Json(TaskResponse::from(task)),
    ))
}

async fn show(
    State(state): State<AppState>,
    Path(id): Path<String>,
) -> Result<Json<TaskResponse>, ApiError> {
    let id: TaskId = id.parse()?;
    let task = state.tasks.get(id).await?;
    Ok(Json(task.into()))
}
```

- A handler extracts, calls one service method and maps the result. A rule about the data belongs in the service.
- Return `Result<T, ApiError>` from every handler. `?` then converts a domain error or a parse error through `From`.
- Put the body extractor last in the argument list. axum allows one extractor to consume the body, and it must be the final one.
- Take a path id as `Path<String>` and parse it into the domain type in the handler. A malformed id then gets the same 404 problem body as an unknown one.
- Return `StatusCode::NO_CONTENT` alone for a delete, and 201 with a `Location` header for a create.
- When a handler fails to compile with a trait bound error on `Handler`, add `#[axum::debug_handler]` above it. The compiler then names the argument or return type at fault.

## Request and response types

```rust
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct CreateTask {
    title: String,
}

#[derive(Serialize)]
struct TaskResponse {
    id: String,
    title: String,
    done: bool,
    created_at: DateTime<Utc>,
}
```

- Declare the wire types in the route file, private to it, and convert with `From<Task>`. The JSON contract then changes only when this file changes.
- Put `#[serde(deny_unknown_fields)]` on every request body. A misspelled field becomes a 422 and not a silent default.
- Keep request fields as plain strings and numbers. The service parses them into domain values and owns the validation message.

## Errors

```rust
#[derive(FromRequest)]
#[from_request(via(axum::Json), rejection(ApiError))]
pub struct ApiJson<T>(pub T);

#[derive(FromRequestParts)]
#[from_request(via(axum::extract::Query), rejection(ApiError))]
pub struct ApiQuery<T>(pub T);
```

- Use `ApiJson` and `ApiQuery` in handlers in place of axum's `Json` and `Query` extractors. The bare extractors answer a bad request with a plain text body.
- Write one `impl From<TaskError> for ApiError` per feature error, with one `match` arm per variant.
- Send the domain message as `detail` for a 4xx. Log the source of a 5xx with `tracing::error!` and send no detail.
- axum's own rejections set the status: 400 for malformed JSON or a bad query value, 422 for a body of the wrong shape, 415 for a missing JSON content type.

The full `error.rs`, with the `Problem` body and the `application/problem+json` header, is in [references/error.md](references/error.md). Copy it when starting an API crate or adding a rejection type.

## Main

- Read `Config`, bind a `tokio::net::TcpListener`, and call `axum::serve(listener, router(compose(&config)))`.
- Chain `.with_graceful_shutdown(shutdown())`, where `shutdown` waits for Ctrl-C or SIGTERM. In-flight requests then finish before the process exits.
- Start `tracing_subscriber` first, with an `EnvFilter` that falls back to `info`.

The full `main.rs` is in [references/main.md](references/main.md). Copy it when starting an API crate.

## Closing check

```bash
cargo test -p tally-api
```

Every new route has a test in `tests/` for its success status and for each problem status it can return. [jira4manager-rust-testing](../jira4manager-rust-testing/SKILL.md) shows the harness. Then run the closing commands in [jira4manager-rust](../jira4manager-rust/SKILL.md).
