# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Working Principles

Behavioral guidelines to reduce common mistakes. They bias toward caution over speed; for trivial tasks, use judgment.

### Think before coding

Don't assume. Don't hide confusion. Surface tradeoffs.

Before implementing:

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### Simplicity first

Minimum code that solves the problem. Nothing speculative.

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### Surgical changes

Touch only what you must. Clean up only your own mess.

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it and delete it — but **prove it is dead first**.

When your changes create orphans:

- Remove imports/variables/functions that _your_ changes made unused.

The test: every changed line should trace directly to the user's request.

### Proving code is dead

"No importer" is not proof. A symbol can be reached without ever appearing in an `import`
statement, and each such consumer needs its own check before you delete anything:

- **Packaging metadata is consumed by installers, not by imports.** `[project].dependencies` in
  `pyproject.toml` exists so that `pip install ondewo-nlu-client` pulls the package into a _user's_
  environment. Grepping this repo for `import x` says nothing about whether a downstream consumer
  needs it — and dropping a genuinely required entry produces an `ImportError` that only surfaces
  after release, in someone else's venv. Read what actually imports the symbol **in the shipped
  package** (`ondewo/`), and remember that a dependency can legitimately be needed at build time
  (`[build-system].requires`) or only by `examples/` / the dev extra.
- **Strings, not identifiers.** Reflection (`getattr`, `importlib`), entry points, Makefile targets,
  `git add` paths, and Docker build steps reference files and symbols by name as text.
- **Generated code.** `ondewo/nlu/services/*.py` is emitted by `generate_services.py`, not written by
  hand. Deleting from the output without touching the generator means the next `make generate_services`
  puts it straight back.
- **Config that lints itself.** mypy's `warn_unused_configs` reports an override section as unused
  only for the scope it was run over: `faker.*`, `polling.*` and `tqdm.*` look dead under
  `mypy ondewo tests` and are live under `mypy ondewo tests examples`. Run the union scope.

If you cannot prove a thing is unreferenced, leave it and say so. Deleting live code is far worse
than leaving dead code.

### Goal-driven execution

Define success criteria. Loop until verified.

Transform tasks into verifiable goals:

- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:

```text
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

These guidelines are working if: fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and
clarifying questions come before implementation rather than after mistakes.

## Logging

```python
from loguru import logger as log
```

- **Levels:** `log.trace()`, `log.debug()`, `log.info()`, `log.warning()`, `log.error()`, `log.exception()`. Choose by
  hotness/verbosity — `trace` for per-token / hot-path detail, `debug` for routine method entry/exit, `info` for notable
  lifecycle events, `warning` / `error` / `exception` for problems.
- **Interpolate with f-strings, not loguru's `{}` positional args.** Consistent with the Code Style rule, use
  `f"…{value}"`; only add the `f` prefix when the string actually interpolates (`"START: …"` with no params stays a
  plain string).
- **`START:` / `DONE:` bracketing.** Wrap a method (or other notable operation) with a `START:` line at entry and a
  `DONE:` line at exit, both naming `ClassName: method_name` (append `: param={value}` context where useful):

  ```python
  log.debug("START: IntentBertClassifier: predict")
  ...
  log.debug(f"DONE: IntentBertClassifier: predict. Elapsed time: {perf_counter() - start_time:.5f}")
  ```

- **Timing uses `perf_counter()`, rendered `:.5f`.** Measure elapsed time with `time.perf_counter()` captured as a start
  value and subtracted at the `DONE:` line; always format the elapsed value with the `:.5f` spec:

  ```python
  from time import perf_counter

  start_time: float = perf_counter()
  ...
  log.info(f"DONE: SESSION SERVICER: DetectIntent. Elapsed time: {perf_counter() - start_time:.5f}")
  ```

  Never measure a duration with `time.time()` — reserve `time.time()` for wall-clock timestamps (epoch seconds persisted
  to a DB / proto, unique-id or filename stamps). `perf_counter()` has an undefined epoch and must not be stored or
  compared across processes.

## Docstrings

Google-style, triple double-quotes:

```python
"""
Short imperative summary line.

Args:
    param_name (type):
        Description of the parameter.

Returns:
    type:
        Description of the return value.

Raises:
    ExceptionType:
        When this exception is raised.
"""
```

## Git Commits

- **Never include Claude as author or co-author** in commit messages, PR descriptions, or any other text. Do not add
  `Co-Authored-By: Claude…` trailers, "Generated with Claude Code" footers, or any similar attribution.
- The user's own git author identity (already configured in git) is the only identity that should appear on commits.
- This rule overrides the default Claude Code commit-template guidance.
- **Never prepend the JIRA ticket ID** (e.g. `[OND211-2386]`) to the commit subject yourself. The `giticket` pre-commit
  hook reads the ticket from the branch name (`(feature|bugfix|support|hotfix)/<TICKET>-…`) and prepends `[<ticket>]`
  (with a trailing space) automatically. Writing the prefix manually produces a duplicate like
  `[OND211-2386] [OND211-2386] feat: …`. Write the subject as plain Conventional Commits (`feat: …`, `fix(scope): …`,
  `docs(types): …`) and let the hook add the prefix on commit.

## General Principles

- Follow existing patterns before introducing new abstractions.
- Keep changes minimal and consistent with surrounding code.
- Validate inputs early with descriptive, context-rich error messages.
- Use context managers for files, sockets, and thread pools.
- Prefer region comments for grouping methods in files that already use them.
- End edited Markdown and YAML files with a trailing newline.

## Regenerating stubs after an API change

Point the `ondewo-nlu-api` submodule at the api commit
(`git -C ondewo-nlu-api fetch origin <branch> && git -C ondewo-nlu-api checkout <api-sha>`), then run
**both** generators — they are different:

- `make generate_ondewo_protos` — the `*_pb2.py` / `*_pb2.pyi` / `*_pb2_grpc.py` family.
- `make generate_services` — the hand-generator that produces `ondewo/nlu/services/*.py` (+
  `create_async_services` derives `async_*.py` / `client.py`). **A new RPC needs THIS too**, or the
  service client has no method for it. A server-streaming RPC generates a method returning
  `Iterator[<ResponseMessage>]` (async: `AsyncIterator[…]`) in `services/<service>.py`. Do **not** run the
  full `make build` (it resets the submodule off your commit). Verified 2026-07-19 (OND211-2418): the
  container-logs RPCs needed both generators; running only `generate_ondewo_protos` leaves
  `services/operations.py` without the new methods. Commit the `_pb2*` + `services/*` changes together with
  the submodule pointer; push and hand the client SHA to cai's `pyproject.toml` pin.

## Release gotchas (hard-won this session)

These bit us during the 6.14.0 release. Keep them in mind when releasing.

- **Trust the registry, not the log.** `make release_all_clients` wraps each client in `|| echo "Already released …"`, so a _failed_ release is reported as "done". After any release, verify the GitHub release **and** the published package (PyPI / npm) directly.
- **`npm install failed after 5 attempts` in a release log is usually a red herring** — that text is the echo _inside_ the docker `RUN for i in 1..5; do npm install …` retry loop, not a real failure (`npm install` succeeds → `#10 DONE`). Look further down for the real error (a TTY error, an eslint failure, a `setup.py` error).
- **Codegen must run TTY-free.** The `docker run` that invokes the proto-compiler must not pass `-it` — non-interactively it fails with `cannot attach stdin to a TTY-enabled container because stdin is not a terminal`. Fix the script (drop `-it`), or run the whole release under a pseudo-TTY: `script -qc 'make …' /dev/null`.
- **Release Makefiles print secrets.** Some `docker run … -e <TOKEN>=…` recipe lines lack a leading `@`, so `make` echoes the expanded token. Rotate any token printed during a release; fix by prefixing the recipe line with `@`.
- The release auto-pulls the **latest** `ondewo-proto-compiler` tag.
- **npm package names are inconsistent** — e.g. the JS client publishes as `@ondewo/ondewo-nlu-client-js` (double `ondewo`), not `@ondewo/nlu-client-js`. Check `src/package.json`'s `name` before querying npm.
- **PyPI build needs setuptools.** The release image (`Dockerfile.utils`) is `python:3.12-slim`, which bundles no `setuptools`, so `python setup.py sdist bdist_wheel` dies with `ModuleNotFoundError: No module named 'setuptools'`. `Dockerfile.utils` must `pip install … setuptools wheel`.

## Python tooling — uv + ruff + mypy + pyproject.toml (this session's refactor)

This repo was migrated off `setup.py` / `.flake8` / `mypy.ini` to a single **pyproject.toml** with **uv**, **ruff**, and **mypy**. Going forward:

- **Build backend stays setuptools** (for PyPI compatibility). Build with `python -m build --no-isolation` or `uv build` — NOT `python setup.py sdist bdist_wheel` (setup.py is deleted). `Dockerfile.utils` installs `twine setuptools wheel build`.
- **Dependencies via uv + a committed `uv.lock`.** CI runs `uv sync --extra dev --frozen`. To add/change a dep: edit `[project.dependencies]`/`[project.optional-dependencies].dev` in pyproject.toml then `uv lock`.
- **Lint is ruff** (`[tool.ruff]`, line-length 120, generated `*_pb2*` excluded) — `uv run ruff check .`. flake8 is gone.
- **mypy config lives in `[tool.mypy]`.** Do **NOT** re-create `mypy.ini` — it silently _shadows_ the pyproject config. Generated `*_pb2*` modules get `ignore_errors` overrides.
- **Do NOT re-add `setup.py`** — with setuptools>=61 it conflicts with `[project]` on duplicated metadata.
- **PEP 625**: the sdist is now underscore-normalised (`ondewo_<name>-<v>.tar.gz`); anything that greps the tarball name by hand must use underscores.
- The version-bump release target edits the version in **pyproject.toml** (not setup.py); the release stages `pyproject.toml uv.lock`.

## uv migration — completed conversion (this session)

The repo is now fully on **uv** (not just pyproject.toml):

- `make setup_developer_environment_locally` bootstraps uv (installs it if missing), runs `uv sync --extra dev` (creates `.venv` + installs all runtime+dev deps + pre-commit), then `uv run pre-commit install`. **No conda** — the old `create_conda_env`/`setup_conda_env` scaffolding was removed.
- Every Makefile target uses uv: `uv sync --extra dev` (deps), `uv run pytest`/`ruff`/`mypy` (tools), `uv build` (wheel). No `pip install`, no `python -m build`, no `python setup.py`.
- New targets: `make ruff` / `make ruff_fix` / `make ruff_format` / `make mypy`. The `flake8` target is **removed**.
- Removed for good: `requirements.txt`, `requirements-dev.txt`, `setup.cfg` — deps + tool config live in `pyproject.toml`. Do **not** re-add them.
- `Dockerfile.utils` installs uv (`COPY --from=ghcr.io/astral-sh/uv`) and builds with uv; it no longer `COPY`s `requirements.txt`.
- **`[tool.mypy] python_version` must be `3.12`** wherever numpy 2.x is on the mypy path — its PEP-695 `type X = …` stubs fail to parse on < 3.12.
- The release `git commit` uses **`--no-verify`** so pre-commit hooks never gate an automated release.
- **Validated by a real PyPI publish** — `ondewo-t2s-client 6.5.0` was built with `uv build` and uploaded via twine end-to-end; the uv release pipeline works.

## GitHub Actions (`tests`) is a REQUIRED gate — reproduce it with `--frozen`

`.github/workflows/tests.yml` (job `unit-tests`, `runs-on: ubuntu-latest`) fires on **every** push to
**every** branch (`branches: ["**"]`) and on every pull request. It is not advisory: it is the only
automated check this repository has, so a red run is a broken branch. Its five steps are checkout,
`astral-sh/setup-uv@v6`, then these four, which are the whole gate:

```bash
uv python install 3.12
uv sync --extra dev --frozen
uv run --frozen ruff check .
uv run --frozen mypy ondewo
uv run --frozen pytest tests/unit -q --cov --cov-report=term-missing --cov-report=xml --cov-fail-under=100
```

Copy those verbatim — **including `--frozen`** — rather than reaching for the `make` targets. There is no
`gh` CLI on these machines; read the real verdict for the commit you are on straight from the API:

```bash
SHA=$(git rev-parse HEAD)
curl -s "https://api.github.com/repos/ondewo/ondewo-nlu-client-python/actions/runs?head_sha=$SHA"
```

and check `.workflow_runs[].status` / `.conclusion`. `total_count: 0` means **nobody has ever built this
commit**, which is not the same as a pass — an unpushed local commit always reads that way.

Four things measured while running the gate by hand (2026-09-02, at `f9343e4` — all four steps green,
309 tests, 100.00% coverage):

- **The coverage gate is filesystem-scanned via `[tool.coverage.run] source = ["ondewo"]`, and the bare
  `--cov` in the workflow exists only to switch coverage on and defer to it. Never "clarify" it into
  dotted `--cov=ondewo.nlu.…` arguments.** The dotted form FAILS OPEN, and worse than the pyproject
  comment claims: dropping a throwaway `ondewo/nlu/utils/_tmp_probe_uncovered.py` with two untested
  functions into the tree made the workflow's bare `--cov` report it at `0%` and fail the gate
  (`99.16%`, exit 1) — while the dotted form **naming that very module on the command line** printed
  `CoverageWarning: Module … was never imported (module-not-imported)`, omitted it from the table, and
  exited **0** with "Required test coverage of 100% reached". Naming a module explicitly is not enough;
  pytest-cov measures a dotted module only if the suite imports it. A file that genuinely should not be
  tested belongs in the `omit` list in `pyproject.toml` with a written reason, never left to vanish.
- **`--frozen` on `uv sync` does NOT validate `uv.lock` against `pyproject.toml` — it trusts the lock as
  the source of truth.** Adding a dependency to `[project].dependencies` without re-running `uv lock`
  left `uv sync --extra dev --frozen` exiting **0** while the package was simply never installed; the
  failure then surfaces far downstream as a `ModuleNotFoundError` from ruff, mypy or pytest, naming a
  module the author believes they declared. `uv lock --check` is the command that actually catches it
  (`error: The lockfile at uv.lock needs to be updated`, exit 1) — run it after any `pyproject.toml` edit.
- **`make ruff` / `make mypy` run `uv run` WITHOUT `--frozen`, which silently re-resolves and REWRITES
  `uv.lock` as a side effect.** Measured: with a dependency added to `pyproject.toml`, `uv run ruff
  check .` changed `uv.lock`'s md5 and installed the new package, then reported `All checks passed!`. So
  a green `make ruff` is not evidence the gate is green — it repaired the divergence in your working tree
  instead of reporting it, and CI's `--frozen` run will use whatever lock you actually committed. After
  touching `pyproject.toml`, `git status` before committing: the rewritten `uv.lock` must go in the same
  commit.
- **The gate type-checks `ondewo` only, which is NARROWER than `make mypy` (`ondewo/ tests/`).** Both pass
  today, and so does the union scope `uv run mypy ondewo tests examples` (146 files). The narrow scope is
  why the gate prints `note: unused section(s): module = ['faker.*', 'polling.*', 'tqdm.*']` — those three
  overrides are live only for `examples/`, as the comment in `pyproject.toml` says. It is a **note**, not
  an error; mypy still exits 0 and the step passes. Do not "fix" it by deleting those override sections —
  verify against the union scope first (see _Proving code is dead_).

## Jenkins — never trigger a multibranch scan or branch indexing

**NEVER trigger a Jenkins multibranch scan or branch indexing.** Do not call a multibranch/folder job's
`build`, `scan`, or reindex endpoints, click "Scan Repository Now" / "Build Now" on a folder, run
`p4 scan`, or use any API/CLI that reindexes branches or scans the repository. A scan/reindex runs across
**every** branch, consumes CI resources, and can kick off unintended builds and deploys.

If a branch is not building — it was not discovered, or its job is marked `buildable: false` / orphaned —
**report it and stop**. Let the user or a Jenkins admin adjust branch-discovery/config or rename the branch
to the convention. Never force a build by scanning or reindexing.

## `ClientConfig` must not print its secrets

`@dataclass` generates a `__repr__` that prints **every** field, so `log.debug(f"…{config}")` — or any
traceback carrying locals — wrote the ROPC `password` and the PEM `grpc_cert` to the log in clear text.
Downstream consumers really do log config objects: a repository-wide sweep in ondewo-vtsi found this class
among the leakers, alongside thirteen of its own dataclasses. All five ONDEWO Python clients had the same
defect and all five now carry the same fix.

`ondewo/nlu/client_config.py` names the secrets once and renders around them:

```python
SECRET_FIELD_NAMES: ClassVar[FrozenSet[str]] = frozenset({"password", "grpc_cert"})
```

Four properties are load-bearing:

- **An empty secret renders as `''`, never as `***REDACTED***`.** The marker reads as "this is set and
  sensitive", which is actively misleading when the real fault is that nobody set it — usually the very
  thing being debugged. The `__repr__` therefore redacts only a _truthy_ value.
- **A new secret field must join `SECRET_FIELD_NAMES` in the same commit.** That frozenset is the entire
  policy; nothing infers sensitivity from a field name.
- **Redaction covers `repr()` / `str()` only.** Measured on the real class: `to_json()`, `to_dict()` and
  `dataclasses.asdict()` still return the plaintext password. `to_json()` exists here even though
  `ef8c751` dropped this class's own `@dataclass_json` — `BaseClientConfig` still carries it. That is
  deliberate, because serialization has to round-trip through `from_json`; so never log a serialized
  config, and do not "fix" it by redacting there.
- **The guard is behavioural.** `tests/unit/test_client_config_redacts_secrets.py` builds a `ClientConfig`
  with distinctive planted values and reads its `repr`. It does not grep for `__repr__`, because a grep
  passes just as well for a `__repr__` that prints the secret anyway. It also asserts each secret is really
  **on the object** (`config.password == PASSWORD`) before asserting it is absent from the repr — reading
  only the repr would pass vacuously against unfixed code. The certificate is compared against
  `GRPC_CERT.encode()`, since `BaseClientConfig.__post_init__` encodes it to `bytes`; comparing to the
  `str` would fail while the redaction it guards worked perfectly.

Run it with `uv run pytest tests/unit/test_client_config_redacts_secrets.py -q` — 5 tests.

**`ondewo/qa/client_config.py` is NOT covered.** It is an empty `BaseClientConfig` subclass with no
`__repr__` of its own, so it still prints the inherited certificate verbatim — measured:
`ClientConfig(host='h', port='1', grpc_cert=b'PLANTED-CERT-abc')`. It has no password field, so the PEM is
the whole exposure — but that is a live one, not a hypothetical. Give it the same `SECRET_FIELD_NAMES` +
`__repr__`, and certainly before it ever grows a credential field.

**The fix is unreleased.** `git tag --contains HEAD` is empty here (newest tag `7.0.2`), and ondewo-vtsi
pins `ondewo-nlu-client==7.0.2` by exact version, so the redaction cannot reach it until this package cuts
a release.

## The commit-msg hook order is already correct here — keep it

`.pre-commit-config.yaml` lists `conventional-pre-commit` **before** `giticket`, fixed on this branch by
`517dd96` (2026-07-15) — a month ahead of the same fix in the sip, csi and vtsi clients, which were still
wrong until 2026-08-14 and are the reason this is worth writing down. pre-commit runs hooks in
file order, and `giticket` rewrites the subject to `[OND211-2418] <subject>`, which is not a valid
Conventional Commit. With `giticket` first the validator is handed the prefix the other hook just added and
rejects it, so **no conforming commit message exists at all** — one hook failing on the other hook's output.
The only escapes were `--no-verify` (which also skips ruff, ruff-format, mypy and uv-lock) or renaming the
branch away from its ticket.

Both hooks carry a comment saying so. If either block is ever moved, move them as a pair: validator first,
decorator second.

## Releasing: preflight and the traps that have actually bitten

Written after a release program across every ONDEWO client in one session. Each item below
cost real time or a broken artefact; every statement is derived from THIS repo's Makefile.

### Before you touch the version, check the released tag is in `master`

Releases here are cut from a `release/<version>` branch and are **not always merged back**, so
`master` can be missing work that is already published — and because a later version number
sorts above the unmerged one, a consumer upgrading silently loses it. The ondewo-nlu-client-python
7.1.0 release was exactly this: it shipped from a `master` that had never seen 7.0.5's
offline-token hand-off, so PyPI's newest release was a regression against its predecessor.

```bash
latest=$(git tag --sort=-v:refname | head -1)
git merge-base --is-ancestor "$latest" master && echo "in master" || echo "NOT in master -- merge first"
```

A fast-forward (`git merge --ff-only <tag>`) is the common case. A true merge needs care: resolve
metadata toward `master` and keep BOTH release-note sections, newest first — a reader upgrading
from the older line still needs the older entry.

### `git add` on a dirty submodule stages the WRONG commit

This repo has submodules (`ondewo-nlu-api`, `ondewo-proto-compiler`). If a submodule's working
tree is dirty, `git add <submodule>` stages **its current HEAD**, not the pointer you resolved
during a merge — silently regressing it to an older commit. `git checkout master -- <submodule>`
fixes the index but the next `git add` re-breaks it. Move the working tree instead:

```bash
want=$(git ls-tree master <submodule> | awk '{print $3}')
git -C <submodule> checkout -q "$want" && git add <submodule>
```

### The release notes are sliced by an EXACTLY-CASED heading

`CURRENT_RELEASE_NOTES` slices `RELEASE.md` with a perl range. In THIS repo the opening
pattern is, verbatim:

```text
Release ONDEWO NLU Python Client ${ONDEWO_NLU_VERSION}
```

So the heading of a new entry must read exactly `## Release ONDEWO NLU Python Client <version>`. **This wording is
not consistent across the ONDEWO repos** — some say `... <Name> Client`, some `... Client
<Name>` with the words reversed, the API repos say `... API` with no `Client` at all, and the
casing varies (`Js`, `Nodejs`, `Typescript`, `Survey`). Do not carry a heading over from a
sibling repo. Copy the PREVIOUS entry in this file and change only the version, or read the
pattern above out of the Makefile.

A heading that does not match yields an **empty slice**, and the GitHub release is then
created with empty notes or fails outright. Verify before releasing:

```bash
grep -c '^## Release ONDEWO NLU Python Client ' RELEASE.md     # must be >= 1 for your new version
```

### Publish order decides how a partial failure is recovered

`make release` in this repo runs:

1. `create_release_branch`
2. `create_release_tag`
3. `release_to_github_via_docker`
4. `push_to_pypi_via_docker`
5. `push_to_pypi`

The **PyPI publish happens LAST**. So a failure before it means nothing shipped, but the
branch, tag and GitHub release may already exist — and `spc` will then refuse a re-run. Recover
by running only the remaining step, not the whole target.

### Verify against the registry, with the REAL package name

This package publishes as **`ondewo-nlu-client`**, which is not always the repository name — the JS client
publishes as `@ondewo/ondewo-nlu-client-js` (doubled `ondewo`), so a lookup by repo name returns
a 404 that reads like a failed release. Check the name in the manifest first, then:

```bash
curl -s https://pypi.org/pypi/ondewo-nlu-client/json | python3 -c "import sys,json;print(json.load(sys.stdin)['info']['version'])"
```

### The `mypy` pre-commit hook is `language: system`

It runs whatever `mypy` is on `PATH`, so a `git commit` outside the project venv fails with
`Executable mypy not found` even though `uv run mypy` passes. Commit with the venv on `PATH`
rather than reaching for `--no-verify`:

```bash
PATH="$PWD/.venv/bin:$PATH" git commit -m "..."
```

### The release prints credentials — read the log BEFORE you scrub it

`make ondewo_release` clones `ondewo-devops-accounts` and passes the registry and GitHub tokens on
the make command line, so they are echoed into the console and into any transcript capturing it.
This is a known and accepted property of the shared release path: do **not** re-plumb the recipe.
Redirect the run to a file, read it through a filter, and shred the file afterwards — and read it
**before** shredding, or a genuine failure is lost with the secrets:

```bash
umask 077; make ondewo_release > /tmp/rel.log 2>&1; echo "RC=$?"
grep -avE 'TOKEN|PASSWORD|USERNAME|_authToken' /tmp/rel.log | tail -20   # read FIRST
shred -u /tmp/rel.log; rm -rf ondewo-devops-accounts                     # then scrub
```

### Run the release from `master`, and check with `git branch --show-current`

A release ends by checking out `release/<version>`, and **nothing checks you out back**. Start the
next release from that leftover checkout and `git commit` + `git push` land on the OLD release
branch: the new `release/<version>` is cut from it, the tag points into it, and `master` never sees
the release at all. Measured on ondewo-csi-client-typescript 5.5.1 -- npm had it, the tag had it,
and `origin/master` was still at 5.5.0. Recovery was a fast-forward (`git merge --ff-only
release/5.5.1`), which worked only because nothing else had moved; a diverged `master` needs a real
merge.

```bash
git branch --show-current            # must print master BEFORE `make ondewo_release`
```

### The release `git add` list is an ALLOW-LIST, so anything outside it ships but is never committed

`make build` writes files the release target then stages from a fixed list of paths. Anything the
build touches that is not on that list reaches the registry and is **absent from the tag of that
same version** -- two different things under one name, with nothing anywhere reporting it.

Both directions have bitten: a hand-written directory the build copies into the package, and a
tracked file the build regenerates. Whatever `make build` writes, either stage it or prove the
release does not need it.

The general check costs nothing:

```bash
git status --porcelain    # MUST be empty after a release; anything left is published-but-uncommitted
```

### `git commit` exits 1 on a clean tree and takes the whole target down with it

If the release content was already committed by hand, `git commit` finds nothing to commit, returns
1, and make abandons the target -- **before** the publish, the branch, the tag and the GitHub
release -- while printing only `nothing to commit, working tree clean`. Read as a build failure it
sends you hunting a compile error that is not there. The line is prefixed with `-` so the step is
advisory; `spc` still refuses an existing branch or tag, so the guard cannot mask a double release.

### Write the RELEASE.md section BEFORE releasing, or the release body is silently empty

`CURRENT_RELEASE_NOTES` slices RELEASE.md between the heading naming this exact version and the next
`*****` separator. No heading means an EMPTY slice, `gh release create -n ""` succeeds, and you get a
release with no notes and no error anywhere. ondewo-nlu-client-js and -typescript 7.1.1 shipped that
way and had to be repaired after the fact.

```bash
cat RELEASE.md | perl -ne 'print if /<the exact heading> <version>/../^\*{5}/' | wc -l   # must be > 0
```

### Verify the three artefacts separately -- they fail independently

GitHub's release API returned 500 twice in one session, leaving the registry and the tag correct and
**no release object at all** (nlu-client-js and -angular 7.1.1); `gh release create` after the fact
repairs it without touching the artefact.
The index is also eventually consistent: a fresh
release can read as absent for a minute, and `uv lock` reports that as `no version of <pkg>==<v>
... requirements are unsatisfiable`. That is the cache, not the index -- `uv lock --refresh-package
<pkg>` resolves it. Do not burn a version number over it.

```bash
curl -s https://pypi.org/pypi/<pkg>/json | python3 -c 'import sys,json;print(json.load(sys.stdin)["info"]["version"])'
git tag --list <version> ; gh release view <version> --json body --jq '.body|length'
```
