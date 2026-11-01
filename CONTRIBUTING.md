# Working on Gradebook

This is an individual FHGR CDS212 project. The owner reviews and understands
submitted changes and records their reasoning in pull requests.

## Branching: GitHub Flow

1. Start each focused change on a short-lived branch from the current `main`.
2. Commit related changes in small, meaningful steps.
3. Push the branch and open a pull request targeting `main`.
4. Review the complete diff and record what changed, why, and how it was checked.
5. Wait for required CI checks to pass before merging.
6. Merge, update the local `main`, and delete the finished branch.

`main` should remain deployable once the application is introduced. Do not push
changes directly to `main` or force-push it. Configure branch protection to
require PRs and passing CI; these GitHub settings are not established merely by
writing this document.

Documentation CI and protection of `main` were established with the first PR,
as reported by the project owner. Screenshots from PR #2 show Documentation,
Lint (ruff), and Test (Python 3.12) as required checks. A deliberate lint failure
disabled merging; its repair restored passing checks and enabled merging.
Keep these checks required. Do not describe unverified or missing checks as
passing. See the [demonstration evidence](docs/evidence/README.md).

## Names and commits

Use English branch names with a type and a short hyphenated description:

- `docs/project-foundation`
- `feature/weighted-average`
- `fix/grade-validation`
- `chore/development-tools`

Use Conventional Commits with a concise imperative message, for example:

```text
docs: define gradebook scope and workflow
feat(grades): calculate weighted averages
test(grades): cover incomplete results
```

Each commit should address one coherent topic. Explain non-obvious reasons in
the commit body or PR description. Do not manufacture history or backdate work.

## Self-review before merging

Every PR describes:

- What changed and why.
- How it was verified, including actual results.
- Whether tests were added, or why they are unnecessary.
- Whether documentation and requirements need updating.
- Remaining limitations or follow-up work.

For documentation changes, read the rendered content, check links, and verify
that claims match the repository's actual state. For code changes, run the
project's documented lint, formatting, test, and coverage checks once introduced.
Do not invent test results or mark unchecked acceptance criteria complete.

The final pipeline must enforce lint/format checks, pytest coverage of at least
80%, and Docker build checks. Trivy image scanning is added with the security
work. The exact verified commands will be documented alongside those tools.

## Secrets and attribution

Do not commit passwords, tokens, real student records, `.env`, virtual
environments, caches, or Terraform state. Check staged changes before committing.
Use placeholder configuration examples and synthetic demonstration data.

Attribute reused course code/text and update the README's AI-use declaration.
The owner must be able to explain the submitted code and configuration.
