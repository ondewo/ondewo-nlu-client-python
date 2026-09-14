# Release History

*****************

## Release ONDEWO NLU Python Client 7.2.0

### Improvements

* Tracking API Version [7.2.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/7.2.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 7.1.2

### Bug fixes

* [[OND211-2418]](https://ondewo.atlassian.net/browse/OND211-2418) **The retry cadence introduced in 7.1.1 polled the token endpoint once a second for the whole of an outage.** Re-arming the loop fixed the dead-thread half of the defect and exposed a second one: a failed refresh leaves `_access_token_expires_at` unchanged and therefore in the past, so the loop's ordinary delay computation clamped to `_MIN_REFRESH_DELAY_S` (1 s) on every subsequent tick. One client at 1 Hz is harmless; ondewo runs **one client per call container**, so the clients whose refreshes fail together then retry together — the same thundering-herd shape as the login burst the offline-token hand-off exists to remove.
* **The failure path now backs off, and it jitters.** The ceiling grows `5 s * 2 ** (failures - 1)` up to a `300 s` cap, and the actual wait is drawn uniformly from `[base, ceiling]`. The jitter is the load-bearing half — a shared ladder without it keeps N clients in lockstep no matter how long the delays get. A successful refresh resets the counter, and the `stop()` and `token_expiration_in_s` guards still bound every re-arm.
* The healthy schedule is untouched: the counter is zero unless a refresh has actually failed, so a client that never fails computes exactly the delays 7.1.1 did. `KeycloakTokenProvider` takes a new optional `random_fn` for the jitter, defaulting to `random.random`, so a test can make a retry delay exact.

*****************

## Release ONDEWO NLU Python Client 7.1.1

### Bug fixes

* Tracking API Version [7.1.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/7.1.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )
* [[OND211-2418]](https://ondewo.atlassian.net/browse/OND211-2418) **A single failed token refresh disabled background refresh for the rest of the process's life.** `_refresh_loop` is the background thread's target and its body was unguarded, so any exception out of the refresh escaped the target and killed the daemon thread — permanently, because `_start_background_refresh` runs once from `__init__` and nothing re-arms it. One transient answer from the token endpoint (a 502 from a proxy, a DNS blip, a restarting Keycloak) was therefore enough to end proactive refresh for good, and the only symptom was a traceback on stderr from the dying thread. Observed in production as the dead-offline-session case, where Keycloak answers `400 invalid_grant: Offline user session not found`: neither `_refresh`, `_refresh_if_within_window` nor the loop caught it. The loop now logs the failure and retries on the next tick, so a transient failure self-heals the moment the endpoint recovers.
* **This does not, and deliberately must not, repair a genuinely dead offline session.** A refused refresh keeps being refused, the provider keeps the access token it last held, and the lazy read path in `authorization_metadata()` keeps raising — so a caller still learns the session is gone and can build a new provider. There is **no fallback to a password grant**, for the reason given in the 7.0.5 note below: a silent re-login would reintroduce the login burst the handed-off token exists to avoid, at the least predictable moment, since a realm restart invalidates every offline session at once and every provider would re-login together.

*****************

## Release ONDEWO NLU Python Client 7.1.0

### Improvements

* Tracking API Version [7.1.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/7.1.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 7.0.5

### New Features

* Tracking API Version [7.0.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/7.0.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )
* [[OND211-2418]](https://ondewo.atlassian.net/browse/OND211-2418) **A client can now authenticate from a handed-off Keycloak offline token instead of a password.** `ClientConfig` gains an optional `refresh_token` field and `KeycloakTokenProvider` an optional `refresh_token` keyword argument. When either is set the client **never sends a `grant_type=password` request at all**: it bootstraps by exchanging the supplied offline token (`grant_type=refresh_token`) for an access token and then auto-refreshes exactly as before, with the same background thread, the same `_EXPIRY_LEEWAY_S` proactive wake-up, the same lazy read-time fallback and the same `token_expiration_in_s` bound. This exists because Keycloak's brute-force detection counts failed *logins*: N processes booting at once as the same technical user are a burst the realm penalises — measured 3 of 10 password grants accepted at 0 ms spacing — while N concurrent refresh grants are not. A parent process that logs in once can now hand its offline token to the workers it starts, and they authenticate without touching the login endpoint.
* **This is additive, and a caller that does not set `refresh_token` is unaffected.** The field defaults to `""`, so an existing password config takes exactly the same code path it took in 7.0.4 — the same ROPC login with `scope=offline_access`, the same tokens, the same metadata on every gRPC call. Both new parameters are appended **last** in their respective signatures, so a caller constructing either object positionally keeps its argument binding. The constructor precondition was **widened, not removed**: `user_name` is still mandatory, and at least one of `password` and `refresh_token` must still be supplied, so a credential-less config still fails at construction rather than at the token endpoint. The one visible difference for an existing caller is the text of that `ValueError` — it now reads ``Either the field `password` or the field `refresh_token` is mandatory`` instead of ``The field `password` is mandatory``; the exception type and the accept/reject decision are unchanged. Supplying both credentials is allowed and is the normal shape mid-migration: the refresh token is the one that gets used, and there is deliberately no silent fallback to the password if it is rejected, since that would reintroduce the login burst the field exists to avoid at the least predictable moment.
* The shared-provider registry key now includes `refresh_token`. This is load-bearing rather than tidy: a config authenticating with a handed-off token carries an **empty** password, so the field that otherwise discriminates two credentials degenerates to `""` for every such config, and without the token in the key two tenants would collapse onto one provider — one project's processes silently authenticating as another's, the same class of defect fixed in 7.0.2.
* `refresh_token` is registered as a secret, so `repr()` and `str()` of a `ClientConfig` render it as `***REDACTED***`. An offline token is a long-lived bearer credential: anyone holding it mints access tokens for the life of the offline session, with no password policy and no realm login in the way. As with `password` and `grpc_cert`, an **empty** token still renders as `''` rather than as the marker, which would otherwise read as "a token is set".

### Bug fixes

* [[OND211-2418]](https://ondewo.atlassian.net/browse/OND211-2418) **A malformed token response wrote its credentials into the raised exception.** When Keycloak returned a 2xx body with no `access_token`, `KeycloakTokenProvider._store_tokens` rendered the whole payload into the `KeycloakAuthenticationError` message — and a token response is made almost entirely of credentials, so any `refresh_token` in that body was reproduced verbatim wherever the exception landed: a log line, a traceback, an archived CI report. The message now reports the response's **field names** only (`... the response carried the fields ['expires_in', 'refresh_token'] (values withheld: ...)`), which is what made the failure diagnosable in the first place; the values added nothing to that and could not be unsent. Both the login and the refresh path share `_store_tokens`, so both are covered — Keycloak issues the offline token in response to the ROPC login, so the very first response a password-authenticating client receives already carries one.

*****************

## Release ONDEWO NLU Python Client 7.0.4

### Bug Fixes

* [[OND221-2830]](https://ondewo.atlassian.net/browse/OND221-2830) Regenerated with [ondewo-proto-compiler 5.13.0](https://github.com/ondewo/ondewo-proto-compiler/releases/tag/5.13.0).
* [[OND221-2830]](https://ondewo.atlassian.net/browse/OND221-2830) Tooling: `conventional-pre-commit` now runs before `giticket` at the commit-msg stage - with giticket first, its `[OND221-2830] fix: ...` rewrite was no longer valid Conventional Commits and every commit on a ticket branch failed. `README.md` is prettier-ignored where `.prettierrc` sets `useTabs` and markdownlint's MD010 de-tabs the same blocks, and the codegen `docker run` invocations no longer pass `-it`, which fails outside a TTY.

*****************

## Release ONDEWO NLU Python Client 7.0.3

### Bug fixes

* Tracking API Version [7.0.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/7.0.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )
* [[OND211-2418]](https://ondewo.atlassian.net/browse/OND211-2418) **`ClientConfig` printed its credentials in clear text.** `@dataclass` generates a `__repr__` that renders every field, so `log.debug(f"...{config}")` — or any traceback carrying locals — wrote the Keycloak `password` and the gRPC certificate to the logs. That is not hypothetical: a repository-wide sweep in ondewo-vtsi found this class among its leaking dataclasses, and the real staging password was observed on a developer console this way. `repr()` and `str()` now render `password` and `grpc_cert` as `***REDACTED***`. An unset or empty secret still renders as `None` / `''` rather than as the marker: `***REDACTED***` reads as "this is set and sensitive", which is actively misleading when the real fault is that nobody set it — usually the very thing being debugged.
* **Behaviour change** for anyone who parsed the repr: read the attribute (`config.password`, `config.grpc_cert`) instead. Only the rendered text changed — the fields themselves, equality and `dataclasses.asdict()` are untouched.

*****************

## Release ONDEWO NLU Python Client 7.0.2

### Bug fixes

* Tracking API Version [7.0.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/7.0.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )
* [[OND211-2418]](https://ondewo.atlassian.net/browse/OND211-2418) **A client could silently authenticate as a different user.** `get_keycloak_token_provider` keyed its shared-provider registry on `id(config)` — the memory address of the `ClientConfig`. `BaseServicesInterface` keeps only the grpc channel, so the config passed to the usual `Client(config=ClientConfig(...))` becomes unreachable the moment the client is built; CPython then reuses that address for the next `ClientConfig`, and the `WeakValueDictionary` handed the new client the previous user's still-alive token provider. The second client authenticated as the first user — including when its own credentials were wrong or belonged to nobody at all. Any process that builds more than one client with different identities was affected, which is the normal shape for an integration holding one credential per project (for example a service driving several projects' technical users), and the failure is silent: calls succeed, they are simply made as the wrong principal. The registry is now keyed by a SHA-256 of the credential set (`keycloak_url`, `realm`, `client_id`, `user_name`, `password`, `token_expiration_in_s`, `keycloak_verify_ssl`), so two configs share a provider exactly when a shared provider would behave identically for both, and never otherwise. The digest is hashed rather than stored as a plain tuple so the password does not end up in a module-level dict or in this frame's locals, where a traceback renderer that prints locals would expose it. Sharing across separately-constructed clients with identical credentials is intentional and safe — the provider is torn down only when its last strong reference goes away — and it removes a redundant ROPC login.

*****************

## Release ONDEWO NLU Python Client 7.0.1

### Bug fixes

* Tracking API Version [7.0.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/7.0.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )
* [[OND211-2418]](https://ondewo.atlassian.net/browse/OND211-2418) A keycloak-authenticated client printed an `Exception ignored while calling deallocator ... PythonFinalizationError: can't join thread at interpreter shutdown` traceback on stderr whenever it was garbage-collected at interpreter exit on Python 3.13+. `KeycloakTokenProvider.__del__` calls `stop()`, which joined the background token-refresh thread unconditionally, and CPython >= 3.13 refuses that join once finalization has begun. Every short-lived process using keycloak auth ended with the traceback, and in a `pytest` run it appeared per test, where it can mask real errors. `stop()` now skips the join once `sys.is_finalizing()` is true and swallows a `RuntimeError` from the join to cover the race between the guard and the call (`PythonFinalizationError` subclasses `RuntimeError`, so the handling also works on older interpreters). The refresh thread is a daemon and is reaped by the interpreter anyway, so nothing is leaked. Behaviour on the explicit `stop()` / `close()` / `__exit__` path is unchanged: it still joins the refresh thread deterministically with the same bounded timeout, the self-join guard is untouched, and `stop()` stays idempotent.

*****************

## Release ONDEWO NLU Python Client 7.0.0

### Breaking Changes

* Tracking API Version [7.0.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/7.0.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )
* [[OND211-2418]](https://ondewo.atlassian.net/browse/OND211-2418) The `Login` RPC is removed from the API, and with it `Users.login()`, the async `Users.login()`, and the `LoginRequest` / `LoginResponse` messages. Authentication is Keycloak-only. The client already mints and refreshes a Keycloak access token by itself — construct it with `keycloak_url`, `realm`, `client_id`, `user_name` and `password` in the `ClientConfig` and every call carries `Authorization: Bearer <token>`. The identity must be exempt from 2FA (create one with `CreateProjectTechnicalUser` and pass its `username`), because the token comes from a non-interactive password grant.
* [[OND211-2418]](https://ondewo.atlassian.net/browse/OND211-2418) `SharedRequestData` no longer maps `LoginRequest`; `fill_missing_fields` raises `NotImplementedError` for it, as it does for any unmapped request type.
* `Users.check_login()` is **not** affected and remains the way to probe whether a token is still valid.

*****************

## Release ONDEWO NLU Python Client 6.14.1

### Improvements

* Tracking API Version [6.14.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/6.14.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )
* Examples: every example now reads its settings from a single `examples/environment.env` (loaded by `examples/example_env.py`) instead of a config file that was never present in the repo. Real environment variables override it, so CI and containers need no edit.
* Examples: new `examples/agents/create_agent_with_ssl.py` showing a TLS gRPC channel whose CA certificate is taken from `ONDEWO_NLU_CAI_GRPC_CERT_BASE64` rather than read from a file — the shape a container, CI secret or Kubernetes Secret actually injects.
* Examples: `ONDEWO_NLU_CAI_SECURE` selects a secure or insecure channel. TLS requires both the flag and a CA certificate; without the certificate the examples fall back to an insecure channel and say so, because a secure channel with no `grpc_cert` cannot be constructed.

### Bug fixes

* `ondewo.qa.services.async_qa` raised `ModuleNotFoundError` on import — `ondewo.qa.core.async_services_interface` never existed. The module has been unimportable since it was added and shipped that way. Added the missing interface; also removed the mypy override that was silencing the error.
* `SharedRequestData.session_review_id` returned `projects/<p>/agent/sessions/<s>/reviews/None` instead of `None`: it guarded on `session_uuid` but interpolated `session_review_uuid`. The truthy result passed `fill_missing_fields`' emptiness check and would reach the server as a real resource name.
* `SharedRequestData` sent Context requests to a `parent` field that `context.proto` renamed to `session_id`, so `CreateContextRequest`, `ListContextsRequest` and `DeleteAllContextsRequest` raised `AttributeError`. `DeleteAllContextsRequest` additionally mapped to the project name where the proto has always documented a session name.
* `ClientPool.release_client` waited forever instead of closing a surplus client when the pool was full (blocking `put`), and `ClientPool.__init__` deadlocked outright for a `max_size_ratio` below 1. The client-creation counter was also mutated without a lock, so concurrent overflow acquires could exceed `n_clients_created_limit`.

### Breaking Changes

* `ondewo.nlu.utils.login` and `ondewo.nlu.utils.async_login` are removed, along with the `nlu_token` argument of `ServicesInterface` / `AsyncServicesInterface`. Both were inert: `login()` returned an empty string and the token it produced was never sent. Authentication is Keycloak bearer only — pass `keycloak_url`, `realm`, `client_id`, `user_name` and `password` to `ClientConfig` and the SDK mints and refreshes the token itself.

*****************

## Release ONDEWO NLU Python Client 6.14.0

### Improvements

* Tracking API Version [6.14.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/6.14.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 6.13.0

### Improvements

* Tracking API Version [6.13.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/6.13.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 6.12.0

### Improvements

* Tracking API Version [6.12.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/6.12.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 6.11.0

### Improvements

* Tracking API Version [6.11.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/6.11.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 6.10.0

### Improvements

* Tracking API Version [6.10.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/6.10.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 6.9.0

### Improvements

* Tracking API Version [6.9.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/6.9.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 6.8.0

### Improvements

* Tracking API Version [6.8.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/6.8.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 6.7.0

### Improvements

* Tracking API Version [6.7.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/6.7.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 6.6.0

### Improvements

* Tracking API Version [6.6.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/6.6.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 6.5.0

### Improvements

* Tracking API Version [6.5.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/6.5.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 6.4.0

### Improvements

* Tracking API Version [6.4.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/6.4.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 6.3.0

### Improvements

* Tracking API Version [6.3.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/6.3.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 6.2.0

### Improvements

* Tracking API Version [6.2.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/6.2.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 6.1.0

### Improvements

* Tracking API Version [6.1.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/6.1.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 6.0.0

### Improvements

* Tracking API Version [6.0.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/6.0.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 5.0.1

### Improvements

* Added functionality to pass grpc options to grpc clients based on [ONDEWO CLIENT UTILS PYTHON 2.0.0](https://github.com/ondewo/ondewo-client-utils-python/releases/tag/2.0.0)

*****************

## Release ONDEWO NLU Python Client 5.0.0

### Improvements

* Tracking API Version [5.0.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/5.0.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 4.9.0

### Improvements

* Tracking API Version [4.9.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/4.9.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 4.8.0

### Improvements

* Tracking API Version [4.8.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/4.8.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 4.7.0

### Improvements

* Tracking API Version [4.7.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/4.7.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 4.6.0

### Improvements

* Tracking API Version [4.6.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/4.6.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 4.5.0

### Improvements

* Tracking API Version [4.5.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/4.5.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 4.4.0

### Improvements

* Tracking API Version [4.4.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/4.4.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 4.3.0

### Improvements

* Tracking API Version [4.3.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/4.3.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 4.2.0

### Improvements

* Tracking API Version [4.2.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/4.2.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 4.1.0

### Improvements

* Tracking API Version [4.1.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/4.1.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 4.0.0

### Improvements

* Tracking API Version [4.0.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/4.0.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 3.5.0

### Improvements

* Tracking API Version [3.5.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/3.5.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 3.4.0

### Improvements

* Tracking API Version [3.4.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/3.4.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 3.3.0

### Improvements

* Tracking API Version [3.3.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/3.3.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 3.2.0

### Improvements

* Tracking API Version [3.2.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/3.2.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 3.1.0

### Improvements

* Tracking API Version [3.1.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/3.1.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 3.0.1

### Improvements

* [[OND211-2044]](https://ondewo.atlassian.net/browse/OND211-2044) - Added Reindex Agent Endpoint

*****************

## Release ONDEWO NLU Python Client 3.0.0

### Improvements

* Tracking API Version [3.0.0](https://github.com/ondewo/ondewo-nlu-api/releases/tag/3.0.0) ( [Documentation](https://ondewo.github.io/ondewo-nlu-api/) )

*****************

## Release ONDEWO NLU Python Client 2.15.0

### Improvements

* Upgraded to NLU API Version 2.15.0 and Proto-Compiler Version 4.1.1

*****************

## Release ONDEWO NLU Python Client 2.14.0

### Improvements

* Upgraded to NLU API Version 2.14.0 and Proto-Compiler Version 4.0.0

*****************

## Release ONDEWO NLU Python Client 2.10.0

### Improvements

* [[OND211-2039]](https://ondewo.atlassian.net/browse/OND211-2039) - Added pre-commit hooks and adjusted files to them
* Upgraded to NLU API Version 2.10.0

*****************

## Release ONDEWO NLU Python Client 2.9.0

### Improvements

* [[OND211-2039]](https://ondewo.atlassian.net/browse/OND211-2039) - Improved automated release process
* Upgraded to NLU API Version 2.9.0

*****************

## Release ONDEWO NLU Python Client 2.8.6

### Improvements

* Implemented make target release for automated release process

*****************

## Release ONDEWO NLU Python Client 2.8.5

### Bugfix

* Change grpc_pb2 to pb2_grpc

*****************

## Release ONDEWO NLU Python Client 2.8.4

### Bugfix

* Use ondewo.nlu operations module instead of `google.longrunning`

*****************

## Release ONDEWO NLU Python Client 2.8.3

### Bugfix

* Use ondewo.nlu operations module instead of `google.longrunning`

*****************

## Release ONDEWO NLU Python Client 2.8.2

### Improvements

* Downgraded to `dataclasses-json==0.5.4` due to backend compatibility

*****************

## Release ONDEWO NLU Python Client 2.8.1

### Improvements

* Aligned and fixed library versions to be aligned with backend
* Increased version number to 2.8.1

*****************

## Release ONDEWO NLU Python Client 2.8.0

### Improvements

* Easier release process to pypi through docker image (no python installation required)
* [[OND211-2011]](https://ondewo.atlassian.net/browse/OND211-2011) - Intent. List all user says from cache incl. enrichment based on agent parent instead of project_id

*****************

## Release ONDEWO NLU Python Client 2.7.0

### New features

* [[OND211-1938]](https://ondewo.atlassian.net/browse/OND211-1938) - Generated code with ondewo-proto-compiler v2.0.0 with new libraries
* [[OND211-1987]](https://ondewo.atlassian.net/browse/OND211-1987) - Operations. Added filters to ListOperations.
* [[OND211-2011]](https://ondewo.atlassian.net/browse/OND211-2011) - Intent. List all user says from cache incl. enrichment

### Improvements

* [[OND211-1987]](https://ondewo.atlassian.net/browse/OND211-1987) - Operations. Fixed timestamp field of operation

*****************

## Release ONDEWO NLU Python Client 2.6.0

### New features

* [[OND211-1959]](https://ondewo.atlassian.net/browse/OND211-1959) - Intents. GetAllTags and GetAllIntentTags endpoints.

### Improvements

* [[OND211-1927]](https://ondewo.atlassian.net/browse/OND211-1927) - Intents. Remove old Intent classification algorithms
* [[OND211-1928]](https://ondewo.atlassian.net/browse/OND211-1928) - Entities. Remove old Entity Recognition algorithms

*****************

## Release ONDEWO NLU Python Client 2.5.1

### Bugfix

* [[OND211-1953]](https://ondewo.atlassian.net/browse/OND211-1953) Intents. Fix import bug regarding IntentTagRequest

*****************

## Release ONDEWO NLU Python Client 2.5.0

### New features

* [[OND211-1793]](https://ondewo.atlassian.net/browse/OND211-1793) AI Services. Added endpoint to classify an intent given an agent

### Improvements

* [[OND211-1940]](https://ondewo.atlassian.net/browse/OND211-1940) Session Review. Allow the filtering of sessions by intent tags
* [[OND211-1942]](https://ondewo.atlassian.net/browse/OND211-1942) Intents. Allow the addition/deletion of multiple tags at a time
* [[OND211-1942]](https://ondewo.atlassian.net/browse/OND211-1942) Intents. Rename of the IntentTagMessage to IntentTagRequest

*****************

## Release ONDEWO NLU Python Client 2.4.2

### Bug fixes

* [[OND211-1911]](https://ondewo.atlassian.net/browse/OND211-1911) Correct setup.py version

*****************

## Release ONDEWO NLU Python Client 2.4.1

### Improvements

* [[OND211-1911]](https://ondewo.atlassian.net/browse/OND211-1911) Updated requirements compatibility for ondewo-logging

*****************

## Release ONDEWO NLU Python Client 2.4.0

### New features

* [[OND211-1836]](https://ondewo.atlassian.net/browse/OND211-1836) Support intent tags with filtering
* [[OND211-1850]](https://ondewo.atlassian.net/browse/OND211-1850) API Update. Allow sorting and searching of entity values on listing
* [[OND211-1850]](https://ondewo.atlassian.net/browse/OND211-1850) API Update. Enable Entity Type View on all Entity Type CRUD operations

### Improvements

* [[OND211-1911]](https://ondewo.atlassian.net/browse/OND211-1911) Updated requirements compatibility

### Bug fixes

* [[OND211-1911]](https://ondewo.atlassian.net/browse/OND211-1911) Update Ondewo Logging dependency to fix the Log4J vulnerability on ElasticSearch

*****************

## Release ONDEWO NLU Python Client 2.3.3

*****************

## Release ONDEWO NLU Python Client 2.3.2

### Improvements

* [[OND212-36]](https://ondewo.atlassian.net/browse/OND211-36) Addition of the Client Pool for easier retrieval of client for multi-thread/process purposes

*****************

## Release ONDEWO NLU Python Client 2.3.1

### Bug fixes

* [[OND211-1877]](https://ondewo.atlassian.net/browse/OND211-1877) Resolve submodule cloning issue

*****************

## Release ONDEWO NLU Python Client 2.3.0

### Improvements

* [[OND211-1877]](https://ondewo.atlassian.net/browse/OND211-1877) Extend the Intent Messages to include information about it being a prompt or not
* [[OND211-1877]](https://ondewo.atlassian.net/browse/OND211-1877) Use the proto-compiler for generating code from protos
* [[OND211-1843]](https://ondewo.atlassian.net/browse/OND211-1843) Output contexts added to SessionReviewStep

*****************

## Release ONDEWO NLU Python Client 2.2.1

### Improvements

* [[OND211-1844]](https://ondewo.atlassian.net/browse/OND211-1844) Enable the typing information to be installable through PyPi.
* [[OND211-1804]](https://ondewo.atlassian.net/browse/OND211-1804) Add more examples of usages related to the Intent operations.

*****************

## Release ONDEWO NLU Python Client 2.2.0

### New Features

* [[OND211-1841]](https://ondewo.atlassian.net/browse/OND211-1841) Re-generate code to be compliant with the new NLU API version 2.2.0
* [[OND211-1841]](https://ondewo.atlassian.net/browse/OND211-1841) Handle custom platform messages

*****************

## Release ONDEWO NLU Python Client 2.1.0

### New Features

* [[OND212-34]](https://ondewo.atlassian.net/browse/OND211-34) Re-generate code to be compliant with the new NLU API version 2.1.0
* [[OND212-34]](https://ondewo.atlassian.net/browse/OND211-34) Enable the services: Utilities and Server Statistics
* [[XXX002-38]](https://ondewo.atlassian.net/browse/OND211-38) Add endpoints to list project ids, get project config and get server state to qa.proto.
* [[OND211-1799]](https://ondewo.atlassian.net/browse/OND211-1799) Add ExtractEntitiesFuzzy endpoint to the AIServices Servicer
* [[OND211-1774]](https://ondewo.atlassian.net/browse/OND211-1774) Add endpoints to directly create/update/get/delete and list parameters.
* [[OND211-1773]](https://ondewo.atlassian.net/browse/OND211-1773) Add endpoints to directly create/update/get/delete and list responses (=intent messages).
* [[OND211-1785]](https://ondewo.atlassian.net/browse/OND211-1785) Add CreateSession endpoint to the Session Servicer
* [[OND211-1734]](https://ondewo.atlassian.net/browse/OND211-1734) Add ExportBenchmarkAgent endpoint to the Agent Servicer

*****************

## Release ONDEWO NLU Python Client 2.0.0

### New Features

* [[OND211-354]](https://ondewo.atlassian.net/browse/OND211-354) Establish a clear hierarchy for the merging of entities within the generalized waterfall strategy.
   Include intent parameters to entity selection criteria.
* [[OND211-1767]](https://ondewo.atlassian.net/browse/OND211-1767) Change the training phrase message to include a language_code field
* [[OND211-1760]](https://ondewo.atlassian.net/browse/OND211-1760) Implement endpoint to directly list training phrases.
* [[OND211-1744]](https://ondewo.atlassian.net/browse/OND211-1744) Add initiation protocol into train agent endpoint
* [[OND211-1732]](https://ondewo.atlassian.net/browse/OND211-1732) Implement endpoints directly create/update/get/delete training phrases.
* [[OND211-1731]](https://ondewo.atlassian.net/browse/OND211-1731) Implement endpoints to directly create/update/get/delete and list entity values.
* [[OND211-1724]](https://ondewo.atlassian.net/browse/OND211-1724) Add compression_level field to ExportAgentRequest message.

### Improvements

* [[OND212-29]](https://ondewo.atlassian.net/browse/OND211-29) Inject context example script added
* [[OND212-29]](https://ondewo.atlassian.net/browse/OND211-29) Full conversation demo example script added

### Migration Guide

* `pip install ondewo-nlu-client==2.0.* --upgrade`

*****************

## Release ONDEWO NLU Python Client 1.1.2

### New Features

* added to the [pypi](https://pypi.org/project/ondewo-nlu-client/)

### Migration Guide

* `pip install ondewo-nlu-client==1.1.2`

*****************

## Release ONDEWO NLU Python Client 1.1.1

### New Features

* py2 compatibility

*****************

## Release ONDEWO NLU Python Client 1.1.0

### New Features

 Implemented new endpoints:

* [[OND211-1693]](https://ondewo.atlassian.net/browse/OND211-1693) Implement regex validation endpoints.
* [[OND211-1714]](https://ondewo.atlassian.net/browse/OND211-1714) Implement intent cleaning endpoints.
* [[OND211-1714]](https://ondewo.atlassian.net/browse/OND211-1714) Implement entity_type cleaning endpoints.
* [[OND211-1714]](https://ondewo.atlassian.net/browse/OND211-1714) Implement endpoints to add new training phrases to intents.

*****************

## Release ONDEWO NLU Python Client 1.0.1

### Improvements

* Add convenient Make targets for easier development

### Bug fixes

* Fix the setup.py configuration

### Known issues not covered in this release

* CI/CD Integration is missing
* Code Quality checks
* Extend the README.md with an examples usage

*****************

## Release ONDEWO NLU Python Client 1.0.0

### New Features

* First public version

### Improvements

* Open source

### Breaking Changes

* Type definition for Parameters improved (`context.proto`)

### Known issues not covered in this release

* CI/CD Integration is missing
* Code Quality checks
* Extend the README.md with an examples usage

### Migration Guide

* Usages of the Context Parameters must be adapted to the new typed structure
