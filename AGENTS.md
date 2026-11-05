## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- When graphify-out/graph.json exists, run `graphify query "<question>"` before your first grep, search or source-file read for a codebase question, and put this rule in every subagent prompt that explores code. Read raw files only for lines the graph or an earlier read already located. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
- A committed graphify-out/graph.json is rewritten whole on every build, so a large diff to it in a pull request is expected. Do not flag it as churn or suggest skipping the graph rebuild or its hooks.

## Git commits

- Write commit messages in English.
- Keep each commit atomic: one logical change per commit. Do not mix unrelated changes, refactors, formatting, or dependency bumps in the same commit.
- Use Conventional Commits: `<type>: <subject>`.
  - `feat:` a new feature
  - `fix:` a bug fix
  - `docs:` documentation only
  - `refactor:` code change that neither fixes a bug nor adds a feature
  - `perf:` performance improvement
  - `test:` adding or fixing tests
  - `chore:` tooling, dependencies, config
  - `style:` formatting/whitespace with no code change
- Keep the subject lowercase, imperative, and short (roughly 50-72 characters), with no trailing period.
- Examples: `feat: add csv export to dashboard`, `fix: handle empty dataset in analysis`, `docs: document Windows venv setup`.
- If a change needs more than one sentence to explain, split it into separate commits instead of writing a long message.
