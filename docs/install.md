<!-- template: task; audience: engineer -->
# Install the technical-writer plugin

Install the plugin into Claude Code from its tagged release, or set up the repository for development.

## Before you begin

- You run Claude Code with plugin support. The v0.2.2 release was tested with Claude Code 2.1.302.
- You can reach github.com from the machine, since the marketplace command clones the repository at the tag.
- For development only: you have `uv` installed and Python 3.12 or later, the floor `pyproject.toml` sets.

## Steps

Each release is a Git tag, and the marketplace command pins what you install to that tag, so the same two lines install the same code on every machine.

To install the plugin:

1. Register the marketplace at the release tag.

   ```bash
   claude plugin marketplace add ryanmat/technical-writer@v0.2.2
   ```

2. Install the plugin from it.

   ```bash
   claude plugin install technical-writer@technical-writer
   ```

3. Confirm the install. The command prints the plugin with its version and the commit it was installed from.

   ```bash
   claude plugin list
   ```

4. Ask Claude Code for a document, naming its type and its audience. The reply opens by naming the type and the audience it chose.

To set up a development checkout, which runs the tests and the structural checker:

1. Clone the repository.

   ```bash
   git clone https://github.com/ryanmat/technical-writer.git
   ```

2. Install the dependencies from the lock file.

   ```bash
   cd technical-writer
   uv sync
   ```

3. Run the test suite. The run ends with a count of passed tests and no failures.

   ```bash
   uv run pytest
   ```

4. Run the linters. The command exits 0 on a clean tree.

   ```bash
   uv run sh -c 'set -e; ruff check .; ruff format --check .'
   ```

## Next steps

- Read [The technical-writer workflow](how-it-works.md) for what the type, the audience, and the template change.
- Look up a type's domain, default audience, and caps in [Document types and audiences](document-types.md).
