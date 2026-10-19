<!-- template: task; audience: engineer -->
# Release a new version

Cut a tagged release of the plugin and export it to the public repository the install line names.

## Before you begin

- You have `uv` and Python 3.12 or later, the floor `pyproject.toml` sets, and the test suite passes on `main`.
- You work from a checkout of the build repository, which carries `scripts/release.py`; the public
  repository does not ship the export script.
- You have push permission to the public repository, `ryanmat/technical-writer`, and to the build repository.
- The eval gate spends money: the full Sonnet 5.5 report over the 27 cases cost 7.56 USD at v0.2.0, and the gate stops at the ceiling `--max-cost-usd` sets.

## Steps

The version string lives in three files and the tests require it to match in all of them.

To release a version:

1. Set the version in `pyproject.toml`, `.claude-plugin/plugin.json`, and `.claude-plugin/marketplace.json`.

2. Move the `Unreleased` entries in `CHANGELOG.md` under a heading for the version and the date.

3. Run the tests and the linters. Both exit 0.

   ```bash
   uv run pytest
   uv run sh -c 'set -e; ruff check .; ruff format --check .'
   ```

4. Run the eval gate over the holdout cases. It exits 0 when every case is at its bar.

   ```bash
   uv run python evals/gate.py --tag holdout --model claude-sonnet-5-5 --max-cost-usd 10
   ```

5. Commit the version bump, the changelog, and the report the gate wrote under `evals/reports/`.

6. Tag the commit and push the branch with the tag.

   ```bash
   git tag -a v<VERSION> -m "v<VERSION>"
   git push origin main v<VERSION>
   ```

7. Export the tagged tree into a clean clone of the public repository, from the build repository checkout. The script prints the public commit it made and exits 0; exit 1 names a file that carries a private identifier, and nothing is written.

   ```bash
   uv run python scripts/release.py --tag v<VERSION> --public <PUBLIC_CLONE>
   ```

8. Push the public clone's `main` and the tag.

   ```bash
   git -C <PUBLIC_CLONE> push origin main v<VERSION>
   ```

9. Install from the public repository on each machine. The last command prints the version and the same `gitCommitSha` on every machine.

   ```bash
   claude plugin marketplace add ryanmat/technical-writer@v<VERSION>
   claude plugin install technical-writer@technical-writer
   claude plugin list
   ```

## Next steps

Add the release's rows to the results table in the README and update the tag in [Install the technical-writer plugin](install.md).
