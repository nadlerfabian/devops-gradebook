# Gradebook — consolidated requirements and acceptance criteria

Compiled on 27 October 2026 from the local `cds-devops` course material, weeks 1–10.
This is a planning checklist, not a claim that anything has been implemented or verified.
Every checkbox starts unchecked. When completing an item, record its evidence: file, test output, workflow run, PR, screenshot, or terminal transcript.

## How to read this checklist

| Label | Meaning |
|---|---|
| **F** | Explicit final-project requirement, acceptance-checklist item, or submission rule. |
| **W** | Additional weekly laboratory/homework criterion. Exercises are not separately collected, checked, or graded according to the course README; they provide project milestones and evidence. |
| **R** | Recommended practice, reference design, or additional expectation for the highest assessment level. Not a newly invented mandatory final requirement. |
| **O** | Explicit optional/bonus extension or concept taught without an implementation requirement. |
| **D** | Gradebook decision still to specify. The course does not define its exact acceptance contract. |

An item may carry multiple labels. **F takes precedence where a requirement also appears under “Soll”, a lower rubric level, or an exercise.** Weekly Taskboard names, endpoints, fixed test counts, and file paths are preserved in [SOURCE_REVIEW.md](SOURCE_REVIEW.md), rather than silently imposed on Gradebook.

Primary authority: [project requirements][P], [final acceptance checklist][A], [assessment rubric][B], [documentation requirements][DOC], and [submission instructions][H10]. The [course README][COURSE] establishes that exercises are ungraded and requires declaration of AI assistance. The companion [source review](SOURCE_REVIEW.md) inventories every weekly chapter and preserves the original lab acceptance lists and homework self-check tables.

## Application scope and unresolved gradebook decisions

Source: [project topic and scope][P]. These are the gradebook topic's stated capabilities; detailed business rules remain to be agreed.

- [ ] **APP-01 [F]** Deliver an original, small web application with a REST API and persistence, using Taskboard as a technical reference with attribution for reused material.
- [ ] **APP-02 [F]** Select and record the topic and freeze its initial scope by the week-2 milestone; from week 8 onward, concentrate on operation, stability, and documentation.
- [ ] **APP-03 [R]** Keep the domain scope small; roughly 3–5 business endpoints are sufficient. This is scope guidance, not a hard endpoint maximum.
- [ ] **APP-04 [D]** Specify the gradebook data model for courses, students, and grades; define which create/read/update/delete operations the MVP includes.
- [ ] **APP-05 [D]** Specify averages and simple reports: grade scale, allowed precision, weighting, rounding, missing grades, empty datasets, and grouping by student/course. The course names averages/reports but supplies no numerical rules.
- [ ] **APP-06 [D]** Specify lecturer/student permissions and how identity is established; document allowed and denied actions. The topic mentions differing rights but does not prescribe a login implementation.
- [ ] **APP-07 [D]** Define how the app handles personal data and which synthetic demonstration data it uses. Define what student data each role can see.
- [ ] **APP-08 [D]** Turn APP-04–07 into concrete request/response examples and tests before implementation. Weighted grades, a Swiss 1–6 scale, registration, password recovery, exports, uploads, and multiple services are not specified course requirements.

## Week 1 — environment, Linux, and project preparation

Sources: [week overview][W1], [laboratory][L1], [homework][H1], [setup guide][SETUP], [setup checker][CHECK], [project milestones][P].

- [ ] **W01-01 [F]** A GitHub account exists and the toolchain is set up; `bash pruefe-setup.sh` succeeds. Preserve the output as environment evidence.
- [ ] **W01-02 [W]** Linux/Ubuntu is usable, including WSL2 on Windows; `cat /etc/os-release` identifies the distribution. Shell commands and executable permissions work in that environment.
- [ ] **W01-03 [R]** Verify versions and runtime readiness independently of the checker: Git ≥2.30, Python ≥3.12 for the reference stack, Terraform ≥1.5, Docker daemon running, and Compose available. The checker checks presence and prints versions; it does not enforce all minimum versions or prove Docker daemon readiness.
- [ ] **W01-04 [W]** The setup checker finds Git, `python3`, VS Code CLI, Docker, Docker Compose, Terraform, kubectl, kind, Trivy, curl, and GitHub CLI. Postman is a separate GUI setup consideration, not checked by the script.
- [ ] **W01-05 [F]** A project idea is recorded by the week-1 milestone.
- [ ] **W01-06 [R]** Apply least privilege to project scripts and local secret files; sensitive files are owner-only (e.g. `600`), scripts have appropriate execute permissions, and routine app execution does not require root.

The Linux exercise tree, 20-command worksheet, and reflection are learning deliverables, not gradebook application features. Their criteria are retained in the source review and exercise notes below.

## Week 2 — repository and working practices

Sources: [week overview][W2], [homework][H2], [Git chapters][T2], [project requirements][P], [contribution template][CONTRIB], [rubric][B].

- [ ] **W02-01 [F]** A separate public GitHub repository exists for the project, starting from the course project-template structure.
- [ ] **W02-02 [F]** Invite `normansuesstrunk` as collaborator when establishing the repository; read access suffices. The invitation is accepted or visibly pending at submission.
- [ ] **W02-03 [F]** Use GitHub Flow: deployable `main`, short-lived branches, and a PR for each change; the strategy is documented in `CONTRIBUTING.md` and summarized or linked from README.
- [ ] **W02-04 [F]** Protect `main` with “Require a pull request before merging”; direct pushes cannot bypass the intended workflow.
- [ ] **W02-05 [F]** Merge at least one PR by the week-2 milestone and at least five PRs by final submission.
- [ ] **W02-06 [F]** Every counted PR describes what changed and why, records written self-review, and had green CI at merge time. Retain PR/check links as evidence.
- [ ] **W02-07 [F]** `CONTRIBUTING.md` describes branching, commits, and self-review, including tests and documentation review.
- [ ] **W02-08 [F]** The history shows genuine continuous, thematically focused work, rather than one final bulk commit. Do not manufacture or backdate history.
- [ ] **W02-09 [W]** At least five meaningful, atomic commits exist; messages are in imperative English.
- [ ] **W02-10 [R]** Use Conventional Commits, focused PRs, English lowercase branch names with hyphens, and delete merged branches. The template specifies `feature/`, `fix/`, `chore/`, and `docs/` branch types.
- [ ] **W02-11 [R]** Follow the chapter's commit-message guidance: concise subject (≤50 characters), no final full stop, blank line before an explanatory body, body lines around 72 characters.
- [ ] **W02-12 [W]** Commit a suitable open-source `LICENSE` and a language-appropriate `.gitignore`; no virtual environments, caches, generated build output, or secrets are tracked.
- [ ] **W02-13 [W/F]** README explains purpose, prerequisites, setup, and usage, with working example commands.
- [ ] **W02-14 [R]** Track work with GitHub Issues/Projects; this is recommended, not required.

## Week 3 — local app, API, tests, and builds

Sources: [week overview][W3], [laboratory][L3], [homework][H3], [project structure][T31], [dependencies][T32], [build][T33], [automation][T34], [reference app][REF], [final contract][P].

- [ ] **W03-01 [F]** A documented start command (`make run` or equivalent) starts the app locally; business endpoints and initial tests work.
- [ ] **W03-02 [F]** App listens on port **8000** and exposes `/health`, `/ready`, and `/metrics`.
- [ ] **W03-03 [F]** `GET /health` returns HTTP 200 and JSON containing `status: ok`; liveness does not access the database.
- [ ] **W03-04 [F/R]** `GET /ready` checks storage/database availability: HTTP 200 when ready, HTTP 503 when unavailable. Demonstrate the failure path with a fake/unhealthy repository. In-memory mode can report ready without Postgres.
- [ ] **W03-05 [F]** `GET /metrics` exposes valid Prometheus-format metrics usable by the monitoring stack.
- [ ] **W03-06 [F]** With `DATABASE_URL`, the app uses Postgres; without it, the app runs using in-memory storage, without changing application code.
- [ ] **W03-07 [R]** Use the reference design or document an alternative: application factory, injectable configuration/repository/metric registry, routes separated from storage, and tests separated from app code.
- [ ] **W03-08 [R]** Provide a usable web page at `/`, and exercise a domain operation through the browser. A particular UI design/framework is not prescribed or graded.
- [ ] **W03-09 [R]** Specify API status codes and validation consistently: reference examples use GET/PUT 200, POST 201, DELETE 204, invalid input 400, unknown ID 404, and JSON error bodies. Adapt the exact contract to the gradebook MVP.
- [ ] **W03-10 [R]** Tests cover success, invalid/missing/out-of-range data, wrong types, unknown IDs, empty datasets, summary calculations, and health/readiness/metrics. Use meaningful assertions and independent fixtures.
- [ ] **W03-11 [R]** Multiple app instances/tests can run in one process without shared data or duplicate Prometheus registration; inject a fresh `CollectorRegistry` per test when following the reference design.
- [ ] **W03-12 [W/F]** `pytest`, `ruff check .`, `ruff format --check .`, and coverage checks pass. Coverage below 80% fails via `fail_under = 80` (or higher) in `pyproject.toml`.
- [ ] **W03-13 [R]** Project metadata and test/lint/coverage configuration are versioned in `pyproject.toml`; declared Python versions agree with tooling and deployment.
- [ ] **W03-14 [R]** Version runtime/development dependency declarations separately; keep `.venv/` out of Git. Use exact resolution/lock data for reproducible installs rather than assuming compatible-version ranges are reproducible.
- [ ] **W03-15 [R]** Automate install/run/test/cov/lint/fmt/build/up/down/clean/help through Make or an equivalent. Make command targets use `.PHONY`; help and image/tag overrides are documented.
- [ ] **W03-16 [W]** Demonstrate a meaningful test failure, repair/revert it, and show all tests passing again; retain screenshots of the running app and passing tests.
- [ ] **W03-17 [W]** Demonstrate `python -m build` producing wheel and sdist, and inspect wheel contents. These are build-learning evidence; the final project requires a Docker image, not necessarily a published Python package.
- [ ] **W03-18 [R]** Expose `APP_VERSION` in `/health` and an application-info metric; use identifiable versions for deployed artifacts.
- [ ] **W03-19 [W/D]** If transferring the statistics exercise to Gradebook, specify an appropriate grade summary and at least three meaningful scenarios. This adaptation is a proposal; the literal Taskboard exercise remains separately documented below.

## Week 4 — Docker and Compose

Sources: [week overview][W4], [laboratory][L4], [homework][H4], [Dockerfile practices][T43], [volumes/networking][T44], [Compose][T45], [final checklist][A].

- [ ] **W04-01 [F]** `docker build -t gradebook:local .` succeeds with a multi-stage `Dockerfile`; dependencies are installed in the builder and copied into runtime.
- [ ] **W04-02 [F]** Runtime contains no build tools/compilers or pip caches.
- [ ] **W04-03 [W/R]** Use a slim, versioned base image; the Python exercise specifies `python:3.12-slim`. Copy dependency files before application code for layer caching.
- [ ] **W04-04 [F]** Container runs as non-root; `docker run --rm gradebook:local whoami` proves it.
- [ ] **W04-05 [W]** Docker `HEALTHCHECK` calls `/health`, using tools actually present in runtime; the running container becomes healthy.
- [ ] **W04-06 [W/R]** Production entry point uses Gunicorn bound to `0.0.0.0:8000`; exec-form startup or `sh -c` with `exec` delivers termination signals to Gunicorn for graceful shutdown.
- [ ] **W04-07 [W]** `.dockerignore` excludes at least `.git`, `.env`, `tests`, and `__pycache__`; additionally exclude local venvs and generated caches/reports.
- [ ] **W04-08 [F]** Containerized `/health` returns expected JSON on localhost:8000.
- [ ] **W04-09 [F]** Root `docker-compose.yml` defines services **`web`** and **`db`**, using **PostgreSQL 16**.
- [ ] **W04-10 [F]** `docker compose up --build` starts the app and database; web gets its connection string via `DATABASE_URL`.
- [ ] **W04-11 [F]** Database health check proves readiness; `web.depends_on.db.condition: service_healthy` delays app startup until the database is healthy.
- [ ] **W04-12 [F]** Database uses a named volume; create records, run `down`, then `up`, and prove those records persist.
- [ ] **W04-13 [R]** Connect using Compose service DNS (`db:5432`), keep the DB port internal unless justified, and configure sensible restart behavior (reference: `unless-stopped`).
- [ ] **W04-14 [R]** Use one Gunicorn worker in in-memory mode. Multiple workers/replicas serving shared mutable data require shared storage; demonstrate consistent records when using Postgres.
- [ ] **W04-15 [W]** Exercise domain behavior against the Compose/Postgres stack, not only the development server; retain a response proving the statistics operation works in the built image.
- [ ] **W04-16 [W]** Build naive and optimized images, record both actual sizes in a screenshot, and write 150–250 words explaining size/security improvements with the measured numbers.
- [ ] **W04-17 [W]** Inspect image layers with `docker history`; understand/preserve evidence that `down` keeps data and `down -v` deletes it. Perform destructive volume experiments only on disposable exercise data.

## Week 5 — CI and enforced quality gates

Sources: [week overview][W5], [laboratory][L5], [homework][H5], [Actions][T53], [quality assurance][T54], [final requirements][P].

- [ ] **W05-01 [F/W]** `.github/workflows/ci.yml` runs on every PR and on pushes; a run on `main` is green.
- [ ] **W05-02 [F]** CI runs blocking `ruff check .` and `ruff format --check .` checks.
- [ ] **W05-03 [F]** CI executes pytest and enforces coverage ≥80%; the coverage threshold is versioned, not merely shown in a report.
- [ ] **W05-04 [F/W]** CI builds the Docker image only after lint and tests pass; use `needs: [lint, test]` when following the course's separate-job structure.
- [ ] **W05-05 [F]** Branch protection requires passing CI before merge; at minimum the weekly task names lint and Python 3.12 test checks.
- [ ] **W05-06 [F/W]** A demonstration PR first fails because of intentional lint/format/test/coverage failure, is visibly unmergeable, then passes after repair and is merged. Preserve run history and red/green screenshots, linked from the PR.
- [ ] **W05-07 [W]** Add a functioning CI badge to README.
- [ ] **W05-08 [W/R]** Enable pip caching with the correct dependency-file path; compare two runs to show the cache is reused.
- [ ] **W05-09 [W]** Upload `coverage.xml` as `coverage-report`; avoid duplicate artifact names from matrix jobs.
- [ ] **W05-10 [W/D]** Record the lab's Python 3.11 + 3.12 matrix requirement and resolve it against the reference project's `requires-python >=3.12` before implementation; do not quietly advertise unsupported versions. See reconciliation notes.
- [ ] **W05-11 [R]** Keep independent lint/test checks parallel, make failures block downstream jobs, and promptly repair red `main` builds.
- [ ] **W05-12 [R]** Use least-privilege workflow permissions (`contents: read` for read-only CI), versioned actions, correct working-directory paths, and `pull_request` for untrusted PR tests. Do not execute untrusted PR code with secrets via `pull_request_target`.
- [ ] **W05-13 [R]** Optionally install local lint/format pre-commit hooks for fast feedback; they do not replace server-side CI gates.

## Week 6 — deployment and runbook

Sources: [week overview][W6], [laboratory][L6], [homework][H6], [Render chapter][T63], [configuration/secrets][T65], [CD example][CD], [smoke test][SMOKE], [final requirements][P].

- [ ] **W06-01 [F]** A Docker-based service is reachable at a public Render URL; root `render.yaml` describes it and Render accepts the Blueprint.
- [ ] **W06-02 [F]** Public `GET /health` returns HTTP 200 and expected status JSON; show the configured app version and retain a screenshot with visible URL.
- [ ] **W06-03 [F]** Merging to `main` automatically deploys without a manual release step.
- [ ] **W06-04 [W/R]** Deploy only after successful CI on `main`; the lab's completed setup uses `.github/workflows/cd.yml`, a secret `RENDER_DEPLOY_HOOK`, a non-secret `APP_URL`, and Render's independent push auto-deploy switched off.
- [ ] **W06-05 [W]** Configure Render health path `/health`, `PORT=8000`, and one worker when using in-memory storage. Document the selected root directory, Dockerfile path, region, plan, and environment.
- [ ] **W06-06 [W]** A merge causes a recognizable UI/version change at the public URL, and the CD workflow finishes green.
- [ ] **W06-07 [W/R]** A smoke test checks `/health` with bounded cold-start retries, `/ready`, and a domain create/read/delete round trip; asserts statuses and content, cleans up its test record, exits nonzero on failure, and prints success only after all checks pass.
- [ ] **W06-08 [R]** Verify the intended version reached the live service; a healthy old instance alone is insufficient evidence of a completed new deployment. The example's fixed wait is a teaching simplification.
- [ ] **W06-09 [F]** Root `DEPLOYMENT.md` is an actionable runbook for deployment, rollback, and incident diagnosis.
- [ ] **W06-10 [W]** Runbook A: required accounts, tools with version/check commands, and access rights.
- [ ] **W06-11 [W]** Runbook B: copyable clone/venv/install/start commands and expected local `/health` result.
- [ ] **W06-12 [W]** Runbook C: table of every environment variable with name, default, secret yes/no, and effect; include `DATABASE_URL`, `APP_VERSION`, `LOG_LEVEL`, `PORT`, and relevant worker/deployment settings.
- [ ] **W06-13 [W]** Runbook D: one coherent primary Render setup path (Dashboard or Blueprint), first deployment, service settings, and routine redeployment.
- [ ] **W06-14 [W]** Runbook E: expected `/health`, smoke-test, and log output after deployment.
- [ ] **W06-15 [W/R]** Runbook F: executable rollback procedure, verification, and database/state limitations; perform and record a real rollback for the highest rubric level.
- [ ] **W06-16 [W]** Runbook G: at least four realistic failures, each with symptom, cause, and solution.
- [ ] **W06-17 [W]** Runbook H: service-owner/contact role, communication route, and escalation threshold. Role placeholders are permitted here by the homework.
- [ ] **W06-18 [F/W]** A person unfamiliar with the project can deploy using only the runbook; validate this with a fresh terminal or another person and record the result.
- [ ] **W06-19 [R]** Document actual hosting limits affecting cold starts, ephemeral storage, database lifetime, persistence, and rollback. Course tariff numbers are historical teaching material and must be rechecked when deploying.
- [ ] **W06-20 [F/R]** Configure through environment variables, version `.env.example` with placeholders, ignore real `.env`, and keep secrets out of source, images, logs, documentation, and Git history.

## Week 7 — Terraform

Sources: [week overview][W7], [laboratory][L7], [homework][H7], [Terraform foundations][T72], [variables/outputs][T73], [state][T74], [project requirements][P], [rubric][B].

- [ ] **W07-01 [F]** Version a Terraform configuration under `terraform/`, using `kreuzwerker/docker` and a `docker_container` resource to declaratively run a local container.
- [ ] **W07-02 [R]** Manage a real part of the gradebook infrastructure, rather than relying solely on an unrelated example container.
- [ ] **W07-03 [W/R]** Set Terraform `required_version` (lab ≥1.5) and a bounded provider version (homework `~> 3.0`); commit `.terraform.lock.hcl`.
- [ ] **W07-04 [F]** `terraform init` and `terraform validate` succeed; preserve command output.
- [ ] **W07-05 [W]** `terraform fmt -check` succeeds without changes.
- [ ] **W07-06 [F]** `terraform apply` starts the declared container, its expected HTTP response is verified, and `terraform destroy` removes the managed resource(s).
- [ ] **W07-07 [F]** Configurable values use variables instead of hardcoded deployment-specific constants.
- [ ] **W07-08 [W/R]** Document variable descriptions/types/defaults; numeric host-port validation accepts only `1024 < port <= 65535`, and an invalid port such as 80 is rejected before apply.
- [ ] **W07-09 [R]** Outputs expose useful values such as the complete app URL; demonstrate idempotence with a second apply producing no changes (highest rubric level).
- [ ] **W07-10 [F/W]** Ignore `.terraform/`, `*.tfstate*`, and real `*.tfvars`; only safe `*.tfvars.example` templates are tracked. No secrets or state files appear in the history.
- [ ] **W07-11 [W]** Add `terraform/README.md` covering Docker prerequisites and init/plan/apply/destroy; preserve a plan screenshot showing proposed resources and the “Plan: … to add …” summary.
- [ ] **W07-12 [W]** Lab evidence demonstrates volume/network resources, variables with validation, three outputs, all four expected resource addresses in `state list`, drift detection after a manual container deletion, and cleanup with the image retained via `keep_locally`.
- [ ] **W07-13 [W]** Preserve the separate nginx exercise: `docker_image` + `docker_container` for `nginx:alpine`, a custom `index.html` mounted into `/usr/share/nginx/html/index.html`, validated port, reachable URL output, README, and plan screenshot. This does not replace the gradebook infrastructure criterion.
- [ ] **W07-14 [O]** Bonus: create two named nginx instances with different ports using `for_each`, with both URLs in outputs.
- [ ] **W07-15 [R]** Keep state outside Git and protect it as sensitive data; `sensitive = true` only redacts display. Use Terraform state commands rather than editing the JSON by hand. Remote state is not required for this solo local project.

## Week 8 — Kubernetes, scaling, and updates

Sources: [week overview][W8], [laboratory][L8], [homework][H8], [objects/services][T83], [scaling/updates][T84], [configuration/probes][T85], [final checklist][A], [rubric][B].

- [ ] **W08-01 [F]** Version Namespace, Deployment, and Service manifests under `k8s/`; applying the manifests in kind succeeds.
- [ ] **W08-02 [F]** Service maps `port: 80` to `targetPort: 8000`; selectors match deployment/pod labels and traffic reaches the app.
- [ ] **W08-03 [F]** At least **two** replicas run, each `Running` and `READY 1/1`, with application access verified.
- [ ] **W08-04 [F]** Liveness probes use `/health` without a DB check, and readiness probes use `/ready` with dependency checks; timings including `initialDelaySeconds` and `periodSeconds` are suitable and documented.
- [ ] **W08-05 [W]** Lab kind cluster has three Ready nodes: one control-plane and two workers. Images are loaded into kind; no image-pull errors occur.
- [ ] **W08-06 [W]** Demonstrate self-healing: delete an app Pod and show its replacement becomes healthy.
- [ ] **W08-07 [W]** Scale to **three** replicas, document declarative/imperative method, and save `kubectl get pods -o wide` including `NODE`; lab evidence shows distribution across both workers.
- [ ] **W08-08 [W/R]** Use RollingUpdate with `maxUnavailable: 0`, working readiness, and suitable surge capacity (reference `maxSurge: 1`).
- [ ] **W08-09 [W/R]** Roll out a new image version and retain successful `kubectl rollout status` output.
- [ ] **W08-10 [W/R]** During the entire rollout, record a continuous timestamped curl transcript with every HTTP status; all requests succeed with 200, with no 000, 5xx, or connection failures. Use NodePort (`localhost:30080` in the lab), not pod-bound port-forwarding.
- [ ] **W08-11 [W/R]** Demonstrate `kubectl rollout undo`; save history and status proving the previous revision is restored.
- [ ] **W08-12 [W]** Write 150–250 words explaining readiness plus `maxUnavailable: 0`, why “started” differs from “ready”, and why liveness must not depend on the DB.
- [ ] **W08-13 [W]** Preserve used manifests and text transcripts as `woche08/manifeste/`, `protokoll-scale.txt`, `protokoll-rollout.txt`, `protokoll-rollback.txt`, and `analyse.md` (or explicitly document a project evidence-path mapping).
- [ ] **W08-14 [R]** Set sensible CPU/memory requests and limits; the highest rubric level expects resource limits and appropriate probe timing. Reference values are examples, not prescribed gradebook capacities.
- [ ] **W08-15 [R]** Put non-secret environment settings in ConfigMaps and real credentials in Secrets supplied outside Git; commit only safe examples. Base64 encoding is not encryption.
- [ ] **W08-16 [R]** Follow the hardened reference security context: non-root UID matching the image (reference 10001), no privilege escalation, drop all capabilities, RuntimeDefault seccomp, and read-only root filesystem with writable `/tmp` via `emptyDir` and suitable ownership.
- [ ] **W08-17 [R]** Persist durable desired-state changes in YAML/Git. If demonstrating shared gradebook records across replicas, configure a shared database; the in-memory lab only proves deployment mechanics, not shared data consistency.
- [ ] **W08-18 [W]** After disposable lab verification, demonstrate cluster cleanup. Cleanup is an exercise step, not the desired state of the final running demonstration.
- [ ] **W08-19 [O]** Bonus HPA: metrics-server works (`kubectl top pods` has values), CPU requests are configured, HPA scales up under documented load and down afterward; save `protokoll-hpa.txt`. Reference HPA uses a 70% CPU target and max 5 replicas.

## Week 9 — monitoring, logs, alerts, and security

Sources: [week overview][W9], [laboratory][L9], [homework][H9], [metrics][T92], [logging][T93], [alerts][T94], [DevSecOps][T95], [reference dashboard][DASH], [final requirements][P].

- [ ] **W09-01 [F]** Prometheus scrapes app `/metrics`; the app target is **UP** in Targets.
- [ ] **W09-02 [F]** Grafana has a project Overview dashboard with live request rate, error rate, and latency; load visibly changes the curves.
- [ ] **W09-03 [F]** The dashboard JSON is versioned, and a Trivy report is retained as milestone evidence.
- [ ] **W09-04 [W]** Compose observability stack runs web, healthy db, Prometheus, and Grafana; all four services are Up.
- [ ] **W09-05 [W]** Run load generation and the five lab PromQL queries; request rate is >0, normal test traffic has no server errors, and deliberate 404 requests are visible separately as client errors.
- [ ] **W09-06 [W]** Keep the four reference panels (request rate, 5xx ratio, p95 latency, version) and add one independently configured p95 panel; all five display data. Save an importable export and full dashboard screenshot.
- [ ] **W09-07 [W]** For every panel, document exactly: actual metric name(s), exact PromQL, operational question, observed normal range with justification, and intervention threshold with justification.
- [ ] **W09-08 [W]** Define two SLOs: one availability/error objective and one latency objective. For each name the SLI and metric, state target/window, calculate the error budget with working, and justify the target; do not choose 100%.
- [ ] **W09-09 [W/R]** Trigger the service-down alert through Pending to Firing and save a screenshot; restore service after the exercise.
- [ ] **W09-10 [W/R]** Add one original symptom-based alert beyond the three lab rules, as valid YAML with `expr`, `for`, `labels.severity`, and annotations. Explain threshold/duration and provide a 3–6-step runbook.
- [ ] **W09-11 [R]** Alerts describe user-visible symptoms and link to an actionable runbook; tune sustained-duration checks to avoid noise. Final-project alerting is listed as optional but supports the highest rubric level.
- [ ] **W09-12 [F]** CI scans the **built container image** using Trivy; the step is visible in workflow logs.
- [ ] **W09-13 [F]** Set and document the scan severity/failure policy. A meaningful security gate returns nonzero on disallowed findings; the final specification permits a documented policy such as CRITICAL.
- [ ] **W09-14 [W]** Exercise the explicit `HIGH,CRITICAL --exit-code 1` gate and interpret its exit code. Run an image scan and `trivy fs`, rebuild with updated base (`--pull`), and rescan; retain before/after findings and remediation observations.
- [ ] **W09-15 [W]** Analyze the three most severe actual findings: CVE, package, severity, fixed version if available, exploitability in this app's context, and a reasoned update/accept/monitor recommendation. If fewer than three exist, record that fact rather than invent findings.
- [ ] **W09-16 [R]** If using `.trivyignore`, record per-CVE justification and review/expiry date. Explain treatment of unfixed findings; do not disable the gate merely to get green CI.
- [ ] **W09-17 [F]** No passwords, tokens, or keys occur in source or Git history; secrets are configured in GitHub Secrets/deployment settings, not committed.
- [ ] **W09-18 [R]** Logs are usable through `docker compose logs`/`kubectl logs`; severity is controlled by `LOG_LEVEL`. Omit/mask credentials and unnecessary personal data, including student names/grades where they are not needed for diagnosis.
- [ ] **W09-19 [R]** Metrics use bounded label values and normalized route patterns, not student IDs, emails, tokens, timestamps, or concrete per-record URLs.
- [ ] **W09-20 [F/W]** Root `MONITORING.md` explains metrics, dashboard, and thresholds; include panel documentation, SLO/error-budget calculations, custom alert/runbook, and vulnerability analysis from the homework.
- [ ] **W09-21 [W]** Retain dashboard JSON, `dashboard.png`, `alert-firing.png`, scan results, and normal-range observations, with links from `MONITORING.md` (e.g. under `docs/woche-09/`).
- [ ] **W09-22 [R]** Document how to revoke/rotate leaked credentials; deleting a committed file does not remove a compromised secret from history.
- [ ] **W09-23 [O]** Additional hardening: gitleaks/pre-commit secret scanning, dependency scan in CI, SAST, SBOM (CycloneDX/SPDX), JSON logging/request IDs, or central log aggregation. None is a blanket final-project requirement.

## Week 10 — integration, documentation, and submission

Sources: [week overview][W10], [integration lab][L10], [project requirements][P], [documentation][DOC], [rubric][B], [final checklist][A], [submission][H10], [course rules][COURSE].

- [ ] **W10-01 [F]** Demonstrate the complete chain from a fresh commit through green CI and automatic Render deployment, with a healthy public service.
- [ ] **W10-02 [F]** Recheck healthy Kubernetes replicas, live dashboard/load response, UP scrape target, and Trivy in the pipeline; keep evidence in the repository or linked workflow runs.
- [ ] **W10-03 [F]** README explains what/why, prerequisites, copyable quick start, endpoint table, configuration, and links to deeper docs.
- [ ] **W10-04 [F]** Version an architecture overview (template `docs/architektur.md`) containing **C4 context and container diagrams**, technologies, interactions, and references to decisions.
- [ ] **W10-05 [F]** Root `DEPLOYMENT.md` and `MONITORING.md` are complete and consistent with the actual running system.
- [ ] **W10-06 [F]** At least **two** numbered ADRs under `docs/adr/` contain context, decision, status, and consequences; include dates, trade-offs, and alternatives. Replace example/template decisions with real project decisions.
- [ ] **W10-07 [F]** A fresh clone starts using README alone; document the verification. A project-unfamiliar person can start, deploy, and interpret monitoring without relying on course notes or undocumented knowledge.
- [ ] **W10-08 [F]** Complete `BEWERTUNG.md` with all eight rubric categories, self-assessed points, evidence links/files/commits, and total out of 100.
- [ ] **W10-09 [F]** Complete every applicable final acceptance item; distinguish real evidence from files that merely describe intended behavior. Name and schedule any remaining integration gaps during preparation.
- [ ] **W10-10 [F]** Final `main` is green; annotated tag **`v1.0.0`** identifies its final commit and is pushed to GitHub.
- [ ] **W10-11 [F]** Publish a GitHub release for `v1.0.0` with capabilities, public Render URL, and known limitations.
- [ ] **W10-12 [F]** Repository remains public, collaborator invitation is visible, and the Render `/health` endpoint is reachable at submission.
- [ ] **W10-13 [F]** Meet the documented deadline: **18 January 2027, 12:00**, using the course's stated tag-based submission rule. The repository itself is the submission; no separate upload or presentation is required.
- [ ] **W10-14 [F]** Declare which AI tools were used and for what; attribute reused code/text and demonstrate ability to explain all submitted work. This requirements compilation was prepared with Codex from the cited local course material.

## Differences and ambiguities in the source material

These are explicit reconciliation notes, not changes to the course rules.

| Topic | Source difference | Planning treatment |
|---|---|---|
| Final versus weekly scope | Course README says labs/homework are ungraded; final week defines binding project requirements. Some weekly assignments say their artifacts are used in the final assessment. | Treat F as the final baseline; retain W evidence to meet weekly instructions and support assessment. Do not turn every teaching example into a mandatory app feature. |
| Must versus Soll/rubric | Branch protection, auto-deploy, coverage, and secret hygiene appear both as explicit required items and elsewhere as flexible/advanced. | Keep the stronger explicit final requirement; a lower scoring description does not waive it. |
| Stack | Final project allows a free stack; the course examples use Python 3.12/Flask and prescribe ruff/pytest checks. | Use the reference stack unless an alternative and its equivalent checks are explicitly justified. Flask file layout is a reference design, not a universal requirement. |
| Python matrix | Week-5 lab requires Python 3.11 and 3.12, while reference `pyproject.toml` requires ≥3.12 and ruff targets py312. | Record the inconsistency. Choose/document a supported matrix; if literal lab compliance is needed, resolve with the course lead rather than lower metadata without validating compatibility. |
| Kubernetes replicas | Final minimum ≥2; week-8 exercise explicitly demonstrates 3. | Demonstrate 3 to cover the exercise; final minimum remains 2. |
| Shared storage in Kubernetes | Reference Kubernetes lab explicitly uses in-memory mode; wider chapters explain scaling shared state with Postgres. | In-memory is acceptable for the lab mechanics. Shared, persistent gradebook records across replicas require shared storage; document the environment's actual limitation. |
| Dashboard panel count | Final minimum 3 core panels; week-9 homework requires 4 provided panels plus an original p95 panel. The provided JSON already contains a p95 panel. | Keep the four originals and add a distinct p95 view (e.g. successful business requests by route), explaining what it adds. Do not count the existing p95 panel as a new contribution. |
| Alerting | Final project lists alerts under Kann; weekly lab/homework require triggered and custom alerts. | W for weekly completion and R for highest rubric level; not a new universal F requirement. |
| Terraform subject | Final project asks for a local declared container and expects a real infrastructure part; homework specifies nginx/custom HTML. | Keep gradebook infrastructure and the separate nginx exercise logically separate; do not substitute a static nginx page for the gradebook's IaC evidence. |
| Taskboard-specific work | Week 3 specifies `/api/tasks/stats`, week 4 tags `taskboard:local`, and examples quote 21/24 tests. | Literal exercise criteria are preserved in the source review. Gradebook endpoints/image names/test counts need a documented adaptation; 21 tests is not a gradebook acceptance threshold. |
| Render automatic deployment | Early lab enables push auto-deploy; completed lab switches it off and uses a hook after successful CI. | Preserve automatic deployment via the gated CD workflow, avoiding two independent deployment triggers. |
| Build once | Theory says promote an identical image; the example Render path rebuilds from Dockerfile/source and does not itself prove an identical CI image digest. | Do not claim artifact identity without verifying it. Document the chosen build/deploy path and this reference simplification; immutable image promotion is a stronger design. |
| Personal data/roles | Gradebook topic names roles and careful data handling, but no authentication, grade scale, rounding, or retention contract is supplied. | Define these as D items before development. Course privacy guidance is not a complete legal compliance specification. |
| Hosting limits | Course states free-tier costs/lifetimes and cold-start timings. | Treat as course context, not verified current provider terms; check official provider details at implementation time. |

## Additional course exercises that are not gradebook features

The [source review](SOURCE_REVIEW.md) retains exact laboratory lists and homework self-check tables; these notes prevent useful learning deliverables disappearing from the plan.

- **Week 1:** Linux exercise tree with `src/docs/config/skripte/logs`, permission checks (README 644, settings 600, script 755, secret 600), backup copy, demonstrated permission denial, and permissions screenshot. Homework: `befehle.txt` with all 20 numbered commands; `reflexion.md` with 400–600 words and at least two named DevOps concepts with an original argument. Optional exercise-checker success.
- **Week 2:** separate public profile repository with introduction, learning topics, technologies, and contact; lab Git identity/default-branch/merge-pull configuration, SSH authentication, cloned `git-labor`, first push, PR merge, resolved conflict/merge graph, and explanation of `merge --abort`. These are not additional gradebook web features. The lab's direct initial main push precedes the project's protected-branch workflow.
- **Week 3:** literal Taskboard `GET /api/tasks/stats` returns `{total, done, open}` including all zeros when empty, counts via existing `_repo().list()` in the existing blueprint without changing the repository interface, and has ≥3 tests (empty/mixed/all done) using the client fixture. Branch `feature/task-stats`, English code/comments/commits, and a merged PR with tests/lint/coverage evidence. Reference test totals are descriptive, not a general test-count rule.
- **Week 4:** literal Taskboard tags `taskboard:local` and `taskboard:naiv`, stats response from Compose/Postgres, `abgabe/docker-images.png`, `abgabe/stats-nachweis.txt`, `abgabe/BEGRUENDUNG.md`; compare the naive/optimized builds and solve the three-error Compose exercise.
- **Week 5:** demonstration PR and `abgabe/nachname-ci-rot.png` / `abgabe/nachname-ci-gruen.png`, linked from the PR; lint/test/build jobs, cache observation, coverage artifact, and badge. The homework's `git commit add .` line is a typo; do not reproduce it as a valid command.
- **Week 6:** public URL and `/health` screenshot; complete A–H runbook and successful smoke-test evidence.
- **Week 7:** nginx/custom HTML exercise and `terraform/plan-screenshot.png`; reflect on three resources from the cloud environment that could be represented as Terraform. Optional two-instance `for_each` bonus.
- **Week 8:** `woche08/` manifests, scale/rollout/rollback text logs and analysis; optional HPA log. Use text, not screenshots, for these transcripts.
- **Week 9:** five-panel JSON export, dashboard and Firing screenshots, two SLOs, custom alert/runbook, and three-finding analysis in `MONITORING.md`.
- **Week 10:** integration and final release; no new app functionality or presentation requirement.

## Optional extensions after the baseline

Source: [Soll/Kann][P], weekly bonus tasks, and theory chapters.

- [ ] **OPT-01 [O]** Staging/production environments; immutable image promotion with verified digests if adding environments.
- [ ] **OPT-02 [O]** Database migrations; if introduced, keep rollout/rollback compatibility across coexisting versions (expand/contract).
- [ ] **OPT-03 [O]** Load testing and HPA; do not confuse optional load benchmarking with the load used to prove dashboard activity/rollout continuity.
- [ ] **OPT-04 [O]** Additional security scans, SBOM, or voluntary peer review.

Feature flags, Blue-Green/Canary deployment, Ingress, PDBs, remote Terraform state, startup probes, distributed tracing, Alertmanager notification delivery, and Loki/ELK are taught concepts or possible extensions, not mandatory final implementation items. Keep app scope small.

## Assessment and evidence map

| Assessment category | Points | Main checklist sections/evidence |
|---|---:|---|
| Git and working practices | 12 | W02; repository settings, ≥5 green merged PRs, contribution rules, history |
| Containerization | 12 | W04; Dockerfile, Compose, build/non-root/health/persistence evidence |
| CI pipeline | 14 | W05; lint/test/coverage/build, enforced checks, red→green proof, caching/parallel jobs |
| CD and deployment | 12 | W06; public URL, Blueprint, gated automation, smoke test, rollback/runbook |
| Infrastructure as Code | 10 | W07; variables, init/validate/apply/destroy, output, idempotence, state hygiene |
| Kubernetes | 14 | W08; manifests, replicas/probes/service, rollout evidence, resource limits |
| Monitoring and security | 14 | W09; UP target, dashboard JSON, alerts, scans, documented thresholds, secret hygiene |
| Documentation | 12 | W06/W09/W10; README, C4, runbooks, ≥2 real ADRs, reproducibility |
| **Total** | **100** | Final self-assessment belongs in `BEWERTUNG.md` |

Course formula: `grade = 5 × (points / 100) + 1`, rounded to one decimal, passing at 60 points. Project contributes 60% of the module grade. The source states a deduction of 10 points per started late calendar day; more than three days late is not accepted without a pre-approved hardship exception. These are course submission rules, not application behavior.

## Sources

Relative course links work in this local sibling-folder layout. When publishing the project, replace them with stable course repository URLs if appropriate, or preserve sufficient source attribution; the course folder is not part of this project repository.

[COURSE]: ../../../cds-devops/README.md
[SETUP]: ../../../cds-devops/SETUP.md
[CHECK]: ../../../cds-devops/pruefe-setup.sh
[P]: ../../../cds-devops/woche-10-abschlussprojekt/docs/01-projektanforderungen.md
[A]: ../../../cds-devops/woche-10-abschlussprojekt/docs/04-abnahme-checkliste.md
[B]: ../../../cds-devops/woche-10-abschlussprojekt/docs/03-bewertungsschema.md
[DOC]: ../../../cds-devops/woche-10-abschlussprojekt/docs/02-dokumentation.md
[CONTRIB]: ../../../cds-devops/woche-10-abschlussprojekt/code/projekt-vorlage/CONTRIBUTING.md
[REF]: ../../../cds-devops/beispiel-app/README.md
[W1]: ../../../cds-devops/woche-01-devops-linux/README.md
[L1]: ../../../cds-devops/woche-01-devops-linux/labor/README.md
[H1]: ../../../cds-devops/woche-01-devops-linux/hausaufgabe/README.md
[W2]: ../../../cds-devops/woche-02-git-github/README.md
[L2]: ../../../cds-devops/woche-02-git-github/labor/README.md
[H2]: ../../../cds-devops/woche-02-git-github/hausaufgabe/README.md
[T2]: ../../../cds-devops/woche-02-git-github/docs/
[W3]: ../../../cds-devops/woche-03-build-prozesse/README.md
[L3]: ../../../cds-devops/woche-03-build-prozesse/labor/README.md
[H3]: ../../../cds-devops/woche-03-build-prozesse/hausaufgabe/README.md
[T31]: ../../../cds-devops/woche-03-build-prozesse/docs/01-aufbau-moderner-projekte.md
[T32]: ../../../cds-devops/woche-03-build-prozesse/docs/02-abhaengigkeiten-und-paketmanager.md
[T33]: ../../../cds-devops/woche-03-build-prozesse/docs/03-build-prozess.md
[T34]: ../../../cds-devops/woche-03-build-prozesse/docs/04-automatisierung.md
[W4]: ../../../cds-devops/woche-04-docker/README.md
[L4]: ../../../cds-devops/woche-04-docker/labor/README.md
[H4]: ../../../cds-devops/woche-04-docker/hausaufgabe/README.md
[T43]: ../../../cds-devops/woche-04-docker/docs/03-dockerfile-best-practices.md
[T44]: ../../../cds-devops/woche-04-docker/docs/04-volumes-und-netzwerke.md
[T45]: ../../../cds-devops/woche-04-docker/docs/05-docker-compose.md
[W5]: ../../../cds-devops/woche-05-continuous-integration/README.md
[L5]: ../../../cds-devops/woche-05-continuous-integration/labor/README.md
[H5]: ../../../cds-devops/woche-05-continuous-integration/hausaufgabe/README.md
[T53]: ../../../cds-devops/woche-05-continuous-integration/docs/03-github-actions.md
[T54]: ../../../cds-devops/woche-05-continuous-integration/docs/04-qualitaetssicherung.md
[W6]: ../../../cds-devops/woche-06-continuous-deployment-cloud/README.md
[L6]: ../../../cds-devops/woche-06-continuous-deployment-cloud/labor/README.md
[H6]: ../../../cds-devops/woche-06-continuous-deployment-cloud/hausaufgabe/README.md
[T63]: ../../../cds-devops/woche-06-continuous-deployment-cloud/docs/03-deployment-auf-render.md
[T65]: ../../../cds-devops/woche-06-continuous-deployment-cloud/docs/05-konfiguration-und-secrets.md
[CD]: ../../../cds-devops/woche-06-continuous-deployment-cloud/code/cd.yml
[SMOKE]: ../../../cds-devops/woche-06-continuous-deployment-cloud/code/smoke-test.sh
[W7]: ../../../cds-devops/woche-07-infrastructure-as-code/README.md
[L7]: ../../../cds-devops/woche-07-infrastructure-as-code/labor/README.md
[H7]: ../../../cds-devops/woche-07-infrastructure-as-code/hausaufgabe/README.md
[T72]: ../../../cds-devops/woche-07-infrastructure-as-code/docs/02-terraform-grundlagen.md
[T73]: ../../../cds-devops/woche-07-infrastructure-as-code/docs/03-variablen-und-outputs.md
[T74]: ../../../cds-devops/woche-07-infrastructure-as-code/docs/04-state.md
[W8]: ../../../cds-devops/woche-08-kubernetes/README.md
[L8]: ../../../cds-devops/woche-08-kubernetes/labor/README.md
[H8]: ../../../cds-devops/woche-08-kubernetes/hausaufgabe/README.md
[T83]: ../../../cds-devops/woche-08-kubernetes/docs/03-pods-deployments-services.md
[T84]: ../../../cds-devops/woche-08-kubernetes/docs/04-skalierung-und-rolling-updates.md
[T85]: ../../../cds-devops/woche-08-kubernetes/docs/05-konfiguration-und-probes.md
[W9]: ../../../cds-devops/woche-09-monitoring-devsecops/README.md
[L9]: ../../../cds-devops/woche-09-monitoring-devsecops/labor/README.md
[H9]: ../../../cds-devops/woche-09-monitoring-devsecops/hausaufgabe/README.md
[T92]: ../../../cds-devops/woche-09-monitoring-devsecops/docs/02-metriken-mit-prometheus.md
[T93]: ../../../cds-devops/woche-09-monitoring-devsecops/docs/03-logging.md
[T94]: ../../../cds-devops/woche-09-monitoring-devsecops/docs/04-alarmierung.md
[T95]: ../../../cds-devops/woche-09-monitoring-devsecops/docs/05-devsecops.md
[DASH]: ../../../cds-devops/woche-09-monitoring-devsecops/code/grafana/dashboards/taskboard-overview.json
[W10]: ../../../cds-devops/woche-10-abschlussprojekt/README.md
[L10]: ../../../cds-devops/woche-10-abschlussprojekt/labor/README.md
[H10]: ../../../cds-devops/woche-10-abschlussprojekt/hausaufgabe/README.md
