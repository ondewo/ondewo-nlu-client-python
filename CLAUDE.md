# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Role in the ONDEWO repo family

This is a **generated SDK repo**: Python gRPC stubs (`ondewo/**/*_pb2.py`, `*.pyi`, `*_pb2_grpc.py`)
plus high-level sync/async service wrappers (`ondewo/nlu/services/*.py`, `async_*.py`) compiled from
the protos in the sibling repo **ondewo-nlu-api**, which is vendored here as the git submodule
`ondewo-nlu-api/`. The generated package is consumed by **ondewo-cai** (the backend gRPC server)
via a pin in its `pyproject.toml`.

```
ondewo-nlu-api (.proto, submodule here) → THIS REPO (generated) → ondewo-cai (pyproject pin)
```

**Never hand-edit generated files** — change the protos in ondewo-nlu-api and regenerate.
The only hand-maintained files are the `Makefile`, scripts, and packaging metadata.

## Regenerating after a proto change

Versions/pins live in the `Makefile`: `ONDEWO_NLU_VERSION` (must match the API's major.minor),
`ONDEWO_NLU_API_GIT_BRANCH` (submodule ref), `ONDEWO_PROTO_COMPILER_GIT_BRANCH` (Docker compiler, e.g.
`tags/5.9.0`). Docker is required (the compiler runs as a container).

1. Point the submodule at the right API commit:
   - pushed branch/tag: `git -C ondewo-nlu-api fetch --all && git -C ondewo-nlu-api checkout <ref>`
   - **unpushed local API work**:
     `git -C ondewo-nlu-api fetch /home/arath/ondewo/ondewo-nlu-api <branch> && git -C ondewo-nlu-api checkout FETCH_HEAD`
2. Update the two Makefile vars for consistency (version + branch).
3. **Do NOT run plain `make build`** unless the API ref exists on GitHub — its
   `checkout_defined_submodule_versions` step does `git fetch --all` against origin and would reset
   the submodule. Run the steps individually instead:
   `make clear_package_data build_compiler generate_ondewo_protos generate_services update_setup`
4. Expected churn: a change to `llm_evaluation.proto` also regenerates `session_pb2.py`
   (descriptor cascade — `session.proto` imports it); `generate_services` rewrites the sync + async
   wrappers; `update_setup` bumps `setup.py`. The first pre-commit pass after `create_async_services`
   may "fail" because hooks reformat fresh files — the built-in rerun self-heals.
5. Sanity: `make check_build`; grep a new symbol in `ondewo/nlu/llm_evaluation_pb2.py` and in
   `ondewo/nlu/services/llm_evaluations.py` + `async_llm_evaluations.py`.

## Git

- This repo **has a giticket hook**: write a plain Conventional-Commits subject and let the hook
  prepend `[<TICKET>]` from the branch name (typing it yourself yields `[<TICKET>] [<TICKET>]`).
- Commit the submodule bump together with all regenerated files. `dist/` is gitignored.
- Use the same `feature/<TICKET>-…` branch name as ondewo-nlu-api / ondewo-cai.

## Wiring into ondewo-cai

- Dev: push this repo, then in `ondewo-cai/pyproject.toml` set
  `"ondewo-nlu-client @ git+https://github.com/ondewo/ondewo-nlu-client-python.git@<sha>"`,
  run `uv lock`, and reinstall the venv package
  (`uv pip install --python .venv/bin/python --force-reinstall --no-deps "ondewo-nlu-client @ git+…@<sha>"`).
  Note: `uv sync` in cai always restores whatever the lock pins — editable installs of this repo get
  reverted by the next sync.
- Quick local iteration (before pushing): `uv pip install --python <cai>/.venv/bin/python -e .` —
  but switch to the git pin before committing cai.
- Release: after `ondewo-nlu-api`'s `make release_all_clients`, cai switches to
  `ondewo-nlu_client==X.Y.Z` from PyPI.

## Client usage notes (for probes/tests against a running cai)

`ondewo.nlu.client.Client` / `async_client.AsyncClient` with
`ClientConfig(host, port, user_name, password, http_token)` performs the `Users.Login` dance
automatically and sends the `cai-token` metadata. `http_token` is mandatory non-empty but only
consumed by HTTP proxies — any value works on a direct gRPC connection. Local cai listens plaintext
on `localhost:50055` (`use_secure_channel=False`); working precedent: `ondewo-cai/scripts/intents/detent_intent.py`.
