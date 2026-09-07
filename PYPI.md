# Publish CiteGuard to PyPI (HUMAN)

**Status (2026-09-07):** No `~/.pypirc`, no `TWINE_*` / `PYPI_*` env tokens, and `twine` is not installed in this environment. Agent will **not** invent credentials. Publish is blocked until a human adds a token.

## One-time setup (human, ~5–10 min)

1. Create a PyPI account at https://pypi.org/account/register/ (or log in).
2. Enable 2FA if prompted.
3. Create an **API token**: Account settings → API tokens → “Add API token”
   - Scope: entire account **or** project `citeguard` after first upload.
   - Copy the token once (`pypi-...`).
4. On the machine that will publish:

```bash
python3 -m pip install -U build twine
# Option A: env (preferred for CI / one-shot)
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-PASTE_TOKEN_HERE

# Option B: ~/.pypirc
cat > ~/.pypirc <<'INI'
[pypi]
username = __token__
password = pypi-PASTE_TOKEN_HERE
INI
chmod 600 ~/.pypirc
```

## Build + upload (from repo root)

```bash
cd /path/to/citeguard
rm -rf dist build *.egg-info
python3 -m build
twine check dist/*
# TestPyPI first (recommended):
twine upload --repository testpypi dist/*
# Then real PyPI:
twine upload dist/*
```

Package metadata already matches `pyproject.toml` (`name = "citeguard"`, `version = "0.1.0"`).

## After publish

```bash
pip install citeguard
citeguard check --help
```

Update README install section from editable `pip install -e .` to `pip install citeguard` when the package is live.

## Agent policy

- Do **not** paste tokens into the repo, STATUS, or chat logs.
- Do **not** commit `.pypirc` or `dist/` wheels with secrets.
