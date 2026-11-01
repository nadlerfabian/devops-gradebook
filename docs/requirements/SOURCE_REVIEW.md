# Course source review and original acceptance lists

Compiled on 27 October 2026 from the local course snapshot. Companion to [ACCEPTANCE_CRITERIA.md](ACCEPTANCE_CRITERIA.md).

The inventory covers every week overview, theory chapter, laboratory, and homework for weeks 1–10. The extracts below preserve original German acceptance wording for traceability; they are source material, not completed project checks. Code examples are references, not independent binding specifications. No excluded sibling folder was used.

## Week 01 — source inventory

- [Woche 01 – Einführung in DevOps und Linux](../../../cds-devops/woche-01-devops-linux/README.md) — `woche-01-devops-linux/README.md`
- [Was ist DevOps?](../../../cds-devops/woche-01-devops-linux/docs/01-was-ist-devops.md) — `woche-01-devops-linux/docs/01-was-ist-devops.md`
- [Entwicklung der Softwareentwicklung](../../../cds-devops/woche-01-devops-linux/docs/02-entwicklung-der-softwareentwicklung.md) — `woche-01-devops-linux/docs/02-entwicklung-der-softwareentwicklung.md`
- [Der DevOps-Lebenszyklus](../../../cds-devops/woche-01-devops-linux/docs/03-devops-lebenszyklus.md) — `woche-01-devops-linux/docs/03-devops-lebenszyklus.md`
- [Linux-Grundlagen](../../../cds-devops/woche-01-devops-linux/docs/04-linux-grundlagen.md) — `woche-01-devops-linux/docs/04-linux-grundlagen.md`
- [Benutzer und Berechtigungen](../../../cds-devops/woche-01-devops-linux/docs/05-benutzer-und-berechtigungen.md) — `woche-01-devops-linux/docs/05-benutzer-und-berechtigungen.md`
- [Labor Woche 1 – Linux-Grundlagen praktisch](../../../cds-devops/woche-01-devops-linux/labor/README.md) — `woche-01-devops-linux/labor/README.md`
- [Hausaufgabe Woche 1](../../../cds-devops/woche-01-devops-linux/hausaufgabe/README.md) — `woche-01-devops-linux/hausaufgabe/README.md`

### Original lab acceptance criteria

```text
## Abnahmekriterien

- [ ] Ubuntu läuft; `cat /etc/os-release` zeigt eine Linux-Distribution an.
- [ ] Der Übungsbaum `~/devops-uebung/projekt` existiert mit den Unterordnern `src`, `docs`,
      `config`, `skripte`, `logs`.
- [ ] `projekt/docs/readme.txt` hat die Rechte **644** (`-rw-r--r--`).
- [ ] `projekt/config/settings.conf` hat die Rechte **600** (`-rw-------`).
- [ ] `projekt/skripte/start.sh` hat die Rechte **755** (`-rwxr-xr-x`) und ist ausführbar.
- [ ] `projekt/geheim.txt` existiert mit den Rechten **600**.
- [ ] `backup/notizen.txt` existiert als Kopie.
- [ ] Sie haben die Meldung `Permission denied` beim Lesen einer Datei ohne Leserecht selbst
      reproduziert.
- [ ] (Optional) `pruefe-loesung.sh` meldet „Alle Kriterien erfuellt".

Machen Sie zum Abschluss einen Screenshot der Ausgabe von
`ls -l ~/devops-uebung/projekt/config ~/devops-uebung/projekt/skripte` für die Abgabe.
```

### Original homework self-check

```text
## Selbstkontrolle

| Kriterium | Beschreibung |
| --- | --- |
| Teil A – Aufgaben 1–10 | Jeder Befehl korrekt und lauffähig. |
| Teil A – Aufgaben 11–20 | Jeder Befehl korrekt und lauffähig. |
| Teil A – Form von `befehle.txt` | Vollständig, nummeriert, nachvollziehbar, korrekt benannt. |
| Teil B – Fachliche Richtigkeit | Entstehung und Zweck von DevOps korrekt dargestellt. |
| Teil B – Bezug auf mind. 2 Konzepte | Zwei Konzepte aus `docs/` benannt und richtig erklärt. |
| Teil B – Umfang und Sprache | 400–600 Wörter, verständlich, korrekte Rechtschreibung. |
| Teil B – Eigene Argumentation | Nachvollziehbare, eigenständige Schlussfolgerung. |

---
```

## Week 02 — source inventory

- [Woche 02 – Versionsverwaltung mit Git und GitHub](../../../cds-devops/woche-02-git-github/README.md) — `woche-02-git-github/README.md`
- [01 – Warum Versionsverwaltung?](../../../cds-devops/woche-02-git-github/docs/01-warum-versionsverwaltung.md) — `woche-02-git-github/docs/01-warum-versionsverwaltung.md`
- [02 – Git-Grundlagen](../../../cds-devops/woche-02-git-github/docs/02-git-grundlagen.md) — `woche-02-git-github/docs/02-git-grundlagen.md`
- [03 – Branching und Merging](../../../cds-devops/woche-02-git-github/docs/03-branching-und-merging.md) — `woche-02-git-github/docs/03-branching-und-merging.md`
- [04 – Zusammenarbeit mit GitHub](../../../cds-devops/woche-02-git-github/docs/04-zusammenarbeit-mit-github.md) — `woche-02-git-github/docs/04-zusammenarbeit-mit-github.md`
- [05 – Merge-Konflikte](../../../cds-devops/woche-02-git-github/docs/05-merge-konflikte.md) — `woche-02-git-github/docs/05-merge-konflikte.md`
- [Laborübung Woche 02 – Von Null zu Git und GitHub](../../../cds-devops/woche-02-git-github/labor/README.md) — `woche-02-git-github/labor/README.md`
- [Hausaufgabe Woche 02 – Persönliches GitHub-Portfolio](../../../cds-devops/woche-02-git-github/hausaufgabe/README.md) — `woche-02-git-github/hausaufgabe/README.md`

### Original lab acceptance criteria

```text
## Abnahmekriterien

- [ ] `git --version` zeigt eine Version ≥ 2.30.
- [ ] `git config --global --list` enthält `user.name`, `user.email`,
      `init.defaultbranch=main` und `pull.rebase=false`.
- [ ] `ssh -T git@github.com` bestätigt die Authentifizierung mit Ihrem
      Benutzernamen.
- [ ] Das Repository `git-labor` ist geklont; `git remote -v` zeigt `origin`
      mit einer SSH-URL.
- [ ] Mindestens ein eigener Commit ist auf `main` gepusht.
- [ ] Ein Feature-Branch wurde über einen **gemergten Pull Request** in `main`
      übernommen; der Merge ist im Graphen sichtbar.
- [ ] Der mit `konflikt-uebung.sh` erzeugte Merge-Konflikt wurde aufgelöst und
      committet; `git log --oneline --graph --all` zeigt den Merge-Commit.
- [ ] Sie können erklären, was `git merge --abort` tut.

---

Theorie zu dieser Übung: [docs/](../docs/) · zurück zur
[Wochenübersicht](../README.md).
```

### Original homework self-check

```text
## Selbstkontrolle

| Kriterium | Beschreibung |
| --- | --- |
| Profil-README | Spezial-Repo `<user>/<user>` vorhanden; klare, gut strukturierte Selbstvorstellung. |
| Projekt-README | Enthält Zweck, Voraussetzungen, Setup und Nutzung; verständlich und sauber formatiert. |
| Commit-Qualität | ≥ 5 atomare Commits mit imperativ-englischen, aussagekräftigen Messages. |
| Feature-Branch + gemergter PR | Eigener Feature-Branch, Pull Request mit inhaltlicher Beschreibung, erfolgreich gemergt. |
| `.gitignore` | Sprachgerecht und wirksam; keine ignorierbaren Dateien im Repo. |
| Lizenz | Passende Open-Source-Lizenz als `LICENSE`-Datei vorhanden. |
| Repo-Hygiene | Klare Struktur, keine Geheimnisse, keine Caches/Build-Artefakte, sinnvolle Dateinamen. |
```

## Week 03 — source inventory

- [Woche 03 – Softwareentwicklung und Build-Prozesse](../../../cds-devops/woche-03-build-prozesse/README.md) — `woche-03-build-prozesse/README.md`
- [01 – Aufbau moderner Softwareprojekte](../../../cds-devops/woche-03-build-prozesse/docs/01-aufbau-moderner-projekte.md) — `woche-03-build-prozesse/docs/01-aufbau-moderner-projekte.md`
- [02 – Abhängigkeiten und Paketmanager](../../../cds-devops/woche-03-build-prozesse/docs/02-abhaengigkeiten-und-paketmanager.md) — `woche-03-build-prozesse/docs/02-abhaengigkeiten-und-paketmanager.md`
- [03 – Der Build-Prozess](../../../cds-devops/woche-03-build-prozesse/docs/03-build-prozess.md) — `woche-03-build-prozesse/docs/03-build-prozess.md`
- [04 – Automatisierung](../../../cds-devops/woche-03-build-prozesse/docs/04-automatisierung.md) — `woche-03-build-prozesse/docs/04-automatisierung.md`
- [Labor Woche 03 – Die Taskboard-App bauen und ausführen](../../../cds-devops/woche-03-build-prozesse/labor/README.md) — `woche-03-build-prozesse/labor/README.md`
- [Hausaufgabe Woche 03 – Ein neuer Endpunkt: `GET /api/tasks/stats`](../../../cds-devops/woche-03-build-prozesse/hausaufgabe/README.md) — `woche-03-build-prozesse/hausaufgabe/README.md`

### Original lab acceptance criteria

```text
## Abnahmekriterien

- [ ] Virtuelle Umgebung erstellt und aktiviert (`(.venv)` im Prompt).
- [ ] `pip install -r requirements-dev.txt` fehlerfrei durchgelaufen.
- [ ] `make run` startet die App; <http://127.0.0.1:8000> zeigt die Oberfläche,
      eine Aufgabe wurde im Browser angelegt.
- [ ] Alle fünf API-Aufrufe (`/health`, POST, GET, PUT, DELETE) liefern die
      erwarteten Antworten inklusive `204` beim Löschen und `400` bei leerem Titel.
- [ ] `pytest` (oder `make test`) zeigt `21 passed`.
- [ ] `make lint` läuft durch (`All checks passed!`, `9 files already formatted`).
- [ ] `MAX_TITLE_LENGTH` gesenkt, fehlschlagende Tests beobachtet, Änderung
      zurückgenommen – danach wieder `21 passed`.
- [ ] `python -m build` erzeugt `.whl` und `.tar.gz` in `dist/`, Inhalt des wheels
      mit `unzip -l` inspiziert.
- [ ] Screenshot der laufenden App **und** der bestandenen Tests erstellt (Abgabe).
```

### Original homework self-check

```text
## Selbstkontrolle

| Kriterium | Beschreibung |
|---|---|
| Funktion des Endpunkts | `GET /api/tasks/stats` liefert `200` und korrekte Werte für `total`, `done`, `open` – auch auf leerem Board. |
| Saubere Umsetzung | Route im Blueprint, Zählung über `_repo().list()`, **keine** Änderung an der Repository-Schnittstelle, idiomatischer Code. |
| Tests | Mindestens 3 aussagekräftige Tests (leer, gemischt, alle erledigt) über die Fixture `client`; alle grün. |
| Lint | `ruff check .` meldet `All checks passed!`. |
| Coverage | Gesamtabdeckung bleibt ≥ 80 % (`make cov` bzw. `pytest --cov`). |
| Pull Request | Eigener Branch, sprechende Commits, PR mit klarer Beschreibung gegen `main`. |
```

## Week 04 — source inventory

- [Woche 04 – Containerisierung mit Docker](../../../cds-devops/woche-04-docker/README.md) — `woche-04-docker/README.md`
- [01 – Virtuelle Maschinen vs. Container](../../../cds-devops/woche-04-docker/docs/01-vm-vs-container.md) — `woche-04-docker/docs/01-vm-vs-container.md`
- [02 – Docker-Architektur](../../../cds-devops/woche-04-docker/docs/02-docker-architektur.md) — `woche-04-docker/docs/02-docker-architektur.md`
- [03 – Dockerfile-Best-Practices](../../../cds-devops/woche-04-docker/docs/03-dockerfile-best-practices.md) — `woche-04-docker/docs/03-dockerfile-best-practices.md`
- [04 – Volumes und Netzwerke](../../../cds-devops/woche-04-docker/docs/04-volumes-und-netzwerke.md) — `woche-04-docker/docs/04-volumes-und-netzwerke.md`
- [05 – Docker Compose](../../../cds-devops/woche-04-docker/docs/05-docker-compose.md) — `woche-04-docker/docs/05-docker-compose.md`
- [Labor Woche 04 – Docker in der Praxis](../../../cds-devops/woche-04-docker/labor/README.md) — `woche-04-docker/labor/README.md`
- [Hausaufgabe Woche 04 – Die eigene Anwendung containerisieren](../../../cds-devops/woche-04-docker/hausaufgabe/README.md) — `woche-04-docker/hausaufgabe/README.md`

### Original lab acceptance criteria

```text
## Abnahmekriterien

- [ ] `docker run hello-world` gibt „Hello from Docker!" aus (Schritt 1)
- [ ] Interaktiver Ubuntu-Container gestartet und wieder verlassen (Schritt 3)
- [ ] `taskboard:naiv` gebaut; Grösse notiert (Schritt 4)
- [ ] `taskboard:local` gebaut; deutlich kleiner als `taskboard:naiv` (Schritt 5)
- [ ] `curl /health` liefert `{"status":"ok","version":"0.0.0-dev"}` (Schritt 6)
- [ ] `docker exec ... whoami` gibt `appuser` aus (Schritt 8)
- [ ] `docker history` zeigt die Layer (Schritt 9)
- [ ] Compose-Stack läuft, `db` ist `healthy` (Schritt 10)
- [ ] Aufgabe über die UI angelegt und per API bestätigt (Schritt 11)
- [ ] Persistenz-Experiment durchgeführt: nach `down` bleiben Daten, nach `down -v` sind sie weg (Schritt 12)

---

[← Zur Wochenübersicht](../README.md) · [Weiter zur Hausaufgabe →](../hausaufgabe/README.md)
```

### Original homework self-check

```text
## Selbstkontrolle

| Kriterium | Beschreibung |
|---|---|
| Dockerfile: Multi-Stage & baut fehlerfrei | Zwei Stufen, `docker build` läuft ohne Fehler durch |
| Unprivilegierter Benutzer + HEALTHCHECK | `USER` gesetzt (`whoami` = nicht root), `HEALTHCHECK` auf `/health` |
| `.dockerignore` + korrekte Layer-Reihenfolge | `.git`/`.env`/`tests` ausgeschlossen; `requirements` vor Code kopiert |
| Image gebaut und als `taskboard:local` getaggt | Tag exakt `taskboard:local` |
| Compose-Stack startet (`web` + `db`) | `depends_on: condition: service_healthy`, benanntes Volume, Stack wird `healthy` |
| `/api/tasks/stats` antwortet im Container | Nachweis mit korrekter, plausibler JSON-Statistik |
| Grössenvergleich dokumentiert | Screenshot mit `taskboard:local` und `taskboard:naiv`, Zahlen genannt |
| Begründung der Optimierungen | Nachvollziehbar, bezieht sich auf die eigenen Zahlen |
```

## Week 05 — source inventory

- [Woche 05 – Continuous Integration](../../../cds-devops/woche-05-continuous-integration/README.md) — `woche-05-continuous-integration/README.md`
- [01 – Grundlagen der Continuous Integration](../../../cds-devops/woche-05-continuous-integration/docs/01-grundlagen-ci.md) — `woche-05-continuous-integration/docs/01-grundlagen-ci.md`
- [02 – Automatisierte Tests](../../../cds-devops/woche-05-continuous-integration/docs/02-automatisierte-tests.md) — `woche-05-continuous-integration/docs/02-automatisierte-tests.md`
- [03 – GitHub Actions](../../../cds-devops/woche-05-continuous-integration/docs/03-github-actions.md) — `woche-05-continuous-integration/docs/03-github-actions.md`
- [04 – Qualitätssicherung](../../../cds-devops/woche-05-continuous-integration/docs/04-qualitaetssicherung.md) — `woche-05-continuous-integration/docs/04-qualitaetssicherung.md`
- [Labor – Eine CI-Pipeline Schritt für Schritt bauen](../../../cds-devops/woche-05-continuous-integration/labor/README.md) — `woche-05-continuous-integration/labor/README.md`
- [Hausaufgabe – Pipeline um automatisches Linting erweitern](../../../cds-devops/woche-05-continuous-integration/hausaufgabe/README.md) — `woche-05-continuous-integration/hausaufgabe/README.md`

### Original lab acceptance criteria

```text
## Abnahmekriterien

- [ ] `.github/workflows/ci.yml` liegt im Wurzelverzeichnis und löst bei Push und
      Pull Request aus.
- [ ] Der `lint`-Job läuft `ruff check .` und ist grün.
- [ ] Der `test`-Job läuft `pytest --cov=app ...`, zeigt `21 passed` und hält das
      80-%-Coverage-Gate ein.
- [ ] Der `test`-Job läuft als Matrix über Python 3.11 **und** 3.12.
- [ ] Der `build`-Job hat `needs: [lint, test]` und baut das Image (ohne Push).
- [ ] `setup-python` nutzt `cache: pip` mit korrektem `cache-dependency-path`.
- [ ] Der Lauf erzeugt das Artefakt `coverage-report` mit `coverage.xml`.
- [ ] Sie haben einen roten Build absichtlich erzeugt und wieder repariert.
- [ ] Die README zeigt ein CI-Statusbadge.

Weiter zur [Hausaufgabe](../hausaufgabe/README.md): die Pipeline um ein
blockierendes Lint-Gate und Branch-Schutz erweitern.
```

### Original homework self-check

```text
## Selbstkontrolle

| Kriterium | Beschreibung |
|---|---|
| Lint-Gate erweitert | Eigener/erweiterter `lint`-Job führt `ruff check .` **und** `ruff format --check .` aus; beide Schritte sind vorhanden und blockierend |
| Verkettung mit `build` | `build` deklariert `needs: [lint, test]`; ein rotes Gate verhindert den Build nachweislich |
| Branch-Schutz | Auf `main`: PR erforderlich, Status-Checks als Merge-Voraussetzung; roter Check sperrt den Merge |
| Nachweis rot → grün | PR-Link plus beide Screenshots; der Verlauf ist nachvollziehbar (erst rot und gesperrt, dann grün und mergebar) |
| Saubere Umsetzung | `main` ist grün, sinnvolle Commit-Messages, CI-Badge in der README |
```

## Week 06 — source inventory

- [Woche 6 – Continuous Deployment und Cloud Computing](../../../cds-devops/woche-06-continuous-deployment-cloud/README.md) — `woche-06-continuous-deployment-cloud/README.md`
- [01 – Continuous Delivery vs. Continuous Deployment](../../../cds-devops/woche-06-continuous-deployment-cloud/docs/01-delivery-vs-deployment.md) — `woche-06-continuous-deployment-cloud/docs/01-delivery-vs-deployment.md`
- [02 – Cloud-Grundlagen](../../../cds-devops/woche-06-continuous-deployment-cloud/docs/02-cloud-grundlagen.md) — `woche-06-continuous-deployment-cloud/docs/02-cloud-grundlagen.md`
- [03 – Deployment auf Render](../../../cds-devops/woche-06-continuous-deployment-cloud/docs/03-deployment-auf-render.md) — `woche-06-continuous-deployment-cloud/docs/03-deployment-auf-render.md`
- [04 – Deployment-Strategien](../../../cds-devops/woche-06-continuous-deployment-cloud/docs/04-deployment-strategien.md) — `woche-06-continuous-deployment-cloud/docs/04-deployment-strategien.md`
- [05 – Konfiguration und Secrets](../../../cds-devops/woche-06-continuous-deployment-cloud/docs/05-konfiguration-und-secrets.md) — `woche-06-continuous-deployment-cloud/docs/05-konfiguration-und-secrets.md`
- [Labor Woche 6 – Continuous Deployment auf Render](../../../cds-devops/woche-06-continuous-deployment-cloud/labor/README.md) — `woche-06-continuous-deployment-cloud/labor/README.md`
- [Hausaufgabe Woche 6 – Installations- und Deployment-Dokumentation (Runbook)](../../../cds-devops/woche-06-continuous-deployment-cloud/hausaufgabe/README.md) — `woche-06-continuous-deployment-cloud/hausaufgabe/README.md`

### Original lab acceptance criteria

```text
## Abnahmekriterien

- [ ] Ein Web Service `taskboard` läuft auf Render (Free Tier) und ist unter
      `<APP_URL>` erreichbar.
- [ ] `GET <APP_URL>/health` liefert `{"status":"ok","version":"1.0.0"}` – die per
      `APP_VERSION` gesetzte Version erscheint.
- [ ] Der Health Check Path steht auf `/health`, `GUNICORN_WORKERS` ist `1`
      (Standard), `PORT=8000` ist gesetzt.
- [ ] Ein Push auf `main` hat einen automatischen Deploy ausgelöst; die Änderung
      („Taskboard – live") ist unter `<APP_URL>/` sichtbar.
- [ ] `./smoke-test.sh https://<APP_URL>` endet mit `SMOKE TEST PASSED`.
- [ ] `render.yaml` liegt im Repo-Wurzelverzeichnis und Renders Blueprint-Vorschau
      akzeptiert sie.
- [ ] `RENDER_DEPLOY_HOOK` (Secret) und `APP_URL` (Variable) sind in GitHub
      gesetzt; der Auto-Deploy in Render ist abgeschaltet.
- [ ] Der Workflow *CD* läuft grün und der Smoke-Test darin besteht.

---

Zur [Wochenübersicht](../README.md) · [Hausaufgabe](../hausaufgabe/README.md).
```

### Original homework self-check

```text
## Selbstkontrolle

| Kriterium | Beschreibung |
|---|---|
| Reproduzierbarkeit | Eine fachfremde Person kommt mit dem Dokument allein bis zur laufenden Instanz. Befehle sind vollständig, korrekt und in richtiger Reihenfolge; keine ungeklärten Platzhalter, keine Sackgassen. |
| Vollständigkeit | Alle Abschnitte A–H vorhanden und inhaltlich gefüllt. |
| Konfigurationsvariablen | Tabelle mit Name, Standard, geheim, Wirkung; `DATABASE_URL`, `APP_VERSION`, `LOG_LEVEL`, `PORT` enthalten; Geheimnisse korrekt behandelt. |
| Verifikation | Nachprüfbare Erfolgskontrolle mit konkret erwarteten Ausgaben (`/health`, Smoke-Test, Log). |
| Rollback | Korrekte, umsetzbare Rückrollanleitung samt Verifikation und Grenzen. |
| Troubleshooting | Mindestens vier realistische Fehlerbilder mit Symptom, Ursache, Lösung. |
| Klarheit und Form | Struktur, Sprache, Formatierung; kopierbare Codeblöcke; konsistente Platzhalter (`<APP_URL>` o. Ä.). |

Besonders schwer wiegen: geheime Werte im Klartext im Dokument oder Repository
und Befehle, die so nicht funktionieren.
```

## Week 07 — source inventory

- [Woche 7 – Infrastructure as Code (IaC)](../../../cds-devops/woche-07-infrastructure-as-code/README.md) — `woche-07-infrastructure-as-code/README.md`
- [01 – Infrastrukturautomatisierung](../../../cds-devops/woche-07-infrastructure-as-code/docs/01-infrastrukturautomatisierung.md) — `woche-07-infrastructure-as-code/docs/01-infrastrukturautomatisierung.md`
- [02 – Terraform-Grundlagen](../../../cds-devops/woche-07-infrastructure-as-code/docs/02-terraform-grundlagen.md) — `woche-07-infrastructure-as-code/docs/02-terraform-grundlagen.md`
- [03 – Variablen und Outputs](../../../cds-devops/woche-07-infrastructure-as-code/docs/03-variablen-und-outputs.md) — `woche-07-infrastructure-as-code/docs/03-variablen-und-outputs.md`
- [04 – State](../../../cds-devops/woche-07-infrastructure-as-code/docs/04-state.md) — `woche-07-infrastructure-as-code/docs/04-state.md`
- [Labor Woche 7 – Taskboard mit Terraform provisionieren](../../../cds-devops/woche-07-infrastructure-as-code/labor/README.md) — `woche-07-infrastructure-as-code/labor/README.md`
- [Hausaufgabe Woche 7 – Webserver mit Terraform](../../../cds-devops/woche-07-infrastructure-as-code/hausaufgabe/README.md) — `woche-07-infrastructure-as-code/hausaufgabe/README.md`

### Original lab acceptance criteria

```text
## Abnahmekriterien

- [ ] `terraform version` zeigt eine Version ≥ 1.5.
- [ ] `terraform init` lief erfolgreich; `.terraform/` und `.terraform.lock.hcl` sind vorhanden.
- [ ] `terraform validate` meldet „Success!"; `terraform fmt` ändert nichts mehr.
- [ ] `terraform apply` erzeugt den Stack; `curl http://localhost:8000/health` liefert `{"status":"ok",...}`.
- [ ] `terraform state list` zeigt alle vier Ressourcen.
- [ ] Drift wurde erzeugt (`docker rm -f`) und von `terraform plan` als „will be created" erkannt.
- [ ] Variablen mit `validation`, ein Volume, ein Netzwerk und drei Outputs sind vorhanden.
- [ ] `terraform destroy` räumt alles auf; das Image bleibt dank `keep_locally` erhalten.
- [ ] `.gitignore` verhindert, dass State- oder `.tfvars`-Dateien committet werden.

---

[← Wochenübersicht](../README.md) · [Hausaufgabe →](../hausaufgabe/README.md)
```

### Original homework self-check

```text
## Selbstkontrolle

| Kriterium | Beschreibung |
|---|---|
| `terraform`-Block & Provider | `required_version` gesetzt, Provider `kreuzwerker/docker` gepinnt (`~> 3.0`) |
| nginx-Container läuft | `docker_image` + `docker_container`; `apply` erzeugt einen erreichbaren Container |
| Eigene `index.html` ausgeliefert | Bind-Mount/Volume hängt die eigene Datei korrekt in den Web-Root; `curl` zeigt den eigenen Text |
| Port-Variable mit Validierung | `type = number`, funktionierender `validation`-Block (privilegierte Ports werden abgelehnt) |
| Output mit URL | `output` gibt die korrekte, aus dem Port zusammengesetzte URL aus |
| `fmt` & `validate` sauber | `terraform fmt` ändert nichts; `terraform validate` meldet „Success!" |
| Korrekte `.gitignore` | State-, `.terraform/`- und `.tfvars`-Dateien ausgeschlossen; kein State im Repo |
| `README.md` mit Anleitung | Kurze, korrekte `init`/`apply`/`destroy`-Anleitung inkl. Voraussetzung |
| Bonus: zwei Instanzen via `for_each` | Zwei nginx-Instanzen mit verschiedenen Ports über `for_each`; Output mit beiden URLs. |
```

## Week 08 — source inventory

- [Woche 08 – Kubernetes](../../../cds-devops/woche-08-kubernetes/README.md) — `woche-08-kubernetes/README.md`
- [01 – Warum Kubernetes?](../../../cds-devops/woche-08-kubernetes/docs/01-warum-kubernetes.md) — `woche-08-kubernetes/docs/01-warum-kubernetes.md`
- [02 – Cluster-Architektur](../../../cds-devops/woche-08-kubernetes/docs/02-cluster-architektur.md) — `woche-08-kubernetes/docs/02-cluster-architektur.md`
- [03 – Pods, Deployments und Services](../../../cds-devops/woche-08-kubernetes/docs/03-pods-deployments-services.md) — `woche-08-kubernetes/docs/03-pods-deployments-services.md`
- [04 – Skalierung und Rolling Updates](../../../cds-devops/woche-08-kubernetes/docs/04-skalierung-und-rolling-updates.md) — `woche-08-kubernetes/docs/04-skalierung-und-rolling-updates.md`
- [05 – Konfiguration und Probes](../../../cds-devops/woche-08-kubernetes/docs/05-konfiguration-und-probes.md) — `woche-08-kubernetes/docs/05-konfiguration-und-probes.md`
- [Labor – Taskboard in Kubernetes betreiben](../../../cds-devops/woche-08-kubernetes/labor/README.md) — `woche-08-kubernetes/labor/README.md`
- [Hausaufgabe – Skalieren und ausfallfrei aktualisieren](../../../cds-devops/woche-08-kubernetes/hausaufgabe/README.md) — `woche-08-kubernetes/hausaufgabe/README.md`

### Original lab acceptance criteria

```text
## Abnahmekriterien

- [ ] `kubectl get nodes` zeigt **3 Knoten** `Ready` (1 Control-Plane, 2 Worker).
- [ ] Das Image wurde mit `kind load` in den Cluster geladen; kein `ErrImagePull`.
- [ ] Deployment und Service sind angewendet; der Pod ist `1/1 Running`.
- [ ] `curl …/health` liefert `{"status":"ok","version":"1.0.0"}`.
- [ ] Nach `kubectl delete pod` entsteht **automatisch** ein neuer Pod
      (Selbstheilung).
- [ ] Auf **3 Replikate** skaliert, über beide Worker verteilt (`get pods -o wide`).
- [ ] Rolling Update auf `taskboard:v2` durchgeführt; `rollout status` meldet
      `successfully rolled out`.
- [ ] Die curl-Schleife während des Updates zeigt **ausschliesslich `[200]`** –
      kein Fehlversuch.
- [ ] `rollout undo` erfolgreich ausgeführt.
- [ ] Cluster mit `kind delete cluster --name taskboard` entfernt.

---

Zurück zur [Wochenübersicht](../README.md) · Weiter zur
[Hausaufgabe](../hausaufgabe/README.md).
```

### Original homework self-check

```text
## Selbstkontrolle

| Kriterium | Beschreibung |
|---|---|
| Skalierung auf 3 Replikate | Weg dokumentiert; Sollzustand korrekt auf 3 gesetzt. |
| Nachweis 3 laufender Pods | `get pods -o wide` zeigt 3× `Running` inkl. Spalte `NODE`. |
| curl-Protokoll ohne Fehlversuch | Lückenlos, mit Zeitstempeln und HTTP-Status; deckt den ganzen Rollout ab; **kein** Fehler. |
| `rollout status` erfolgreich | Ausgabe belegt `successfully rolled out`. |
| Analyse readinessProbe + maxUnavailable | Beide Mechanismen korrekt erklärt, inkl. Zusammenspiel und Zwei-Endpunkte-Begründung. |
| Rollback demonstriert | `rollout undo` mit `history`/`status` belegt. |
| Saubere, reproduzierbare Abgabe | Struktur wie gefordert, Manifeste konsistent, Protokolle als Text. |
| Bonus: HPA unter Last | metrics-server, HPA aktiv, Hochskalieren belegt. |
```

## Week 09 — source inventory

- [Woche 09 – Monitoring, Logging und DevSecOps](../../../cds-devops/woche-09-monitoring-devsecops/README.md) — `woche-09-monitoring-devsecops/README.md`
- [01 – Monitoring-Grundlagen](../../../cds-devops/woche-09-monitoring-devsecops/docs/01-monitoring-grundlagen.md) — `woche-09-monitoring-devsecops/docs/01-monitoring-grundlagen.md`
- [02 – Metriken mit Prometheus](../../../cds-devops/woche-09-monitoring-devsecops/docs/02-metriken-mit-prometheus.md) — `woche-09-monitoring-devsecops/docs/02-metriken-mit-prometheus.md`
- [03 – Logging](../../../cds-devops/woche-09-monitoring-devsecops/docs/03-logging.md) — `woche-09-monitoring-devsecops/docs/03-logging.md`
- [04 – Alarmierung](../../../cds-devops/woche-09-monitoring-devsecops/docs/04-alarmierung.md) — `woche-09-monitoring-devsecops/docs/04-alarmierung.md`
- [05 – DevSecOps](../../../cds-devops/woche-09-monitoring-devsecops/docs/05-devsecops.md) — `woche-09-monitoring-devsecops/docs/05-devsecops.md`
- [Labor Woche 09 – Observability-Stack und Security-Scanning](../../../cds-devops/woche-09-monitoring-devsecops/labor/README.md) — `woche-09-monitoring-devsecops/labor/README.md`
- [Hausaufgabe Woche 09 – Monitoring-Dashboard dokumentieren](../../../cds-devops/woche-09-monitoring-devsecops/hausaufgabe/README.md) — `woche-09-monitoring-devsecops/hausaufgabe/README.md`

### Original lab acceptance criteria

```text
## Abnahmekriterien

- [ ] Der Stack läuft; `docker compose ... ps` zeigt alle vier Container `Up`, `db` `healthy`.
- [ ] In <http://localhost:9090/targets> steht der Job `taskboard` auf **UP**.
- [ ] Das Lastskript lief; `sum(rate(flask_http_request_total[5m]))` liefert einen Wert > 0.
- [ ] Die fünf PromQL-Abfragen aus Schritt 4 wurden ausgeführt und verstanden (5xx-Rate bleibt 0, 4xx-Rate zeigt die 404er).
- [ ] Das Grafana-Dashboard „Taskboard Overview" zeigt in allen vier Panels Daten.
- [ ] Ein **eigenes p95-Panel** wurde hinzugefügt (Screenshot vorhanden).
- [ ] `TaskboardDown` wurde durch `docker compose stop web` auf **Firing** gebracht (Screenshot vorhanden).
- [ ] `trivy image taskboard:local` wurde ausgeführt und ein Fund samt **Fixed Version** benannt.
- [ ] Das Gate `trivy image --severity HIGH,CRITICAL --exit-code 1` wurde ausgeführt und der Exit-Code interpretiert.
- [ ] `trivy fs ../beispiel-app` wurde ausgeführt; das Image wurde per `--pull` neu gebaut und erneut gescannt (Vorher/Nachher notiert).
```

### Original homework self-check

```text
## Selbstkontrolle

| Kriterium | Beschreibung |
| --- | --- |
| Panel-Dokumentation | Alle fünf Panels mit je Metrik, korrektem PromQL, Frage, begründetem Normalbereich und Eingriffsschwelle. Echte Metriknamen. |
| SLO 1 (Verfügbarkeit/Fehler) | SLI benannt, SLO formuliert, Error Budget korrekt gerechnet, Angemessenheit begründet. |
| SLO 2 (Latenz) | Wie SLO 1, für ein Latenzziel. |
| Eigene Alarmregel | Gültige, symptombasierte YAML-Regel mit `for`, `severity`, Annotations; Schwelle nachvollziehbar begründet. |
| Runbook-Skizze | Nachvollziehbare Schritte: Bedeutung, Echtheitsprüfung, erste Massnahmen. |
| Trivy-Auswertung | Drei schwerste Funde mit CVE/Paket/Severity/Fix **und** Kontext-Bewertung der Ausnutzbarkeit in dieser App (nicht nur CVSS) plus Empfehlung. |
| Form und Nachvollziehbarkeit | `MONITORING.md` sauber strukturiert, Dashboard-JSON **importierbar**, Screenshots vorhanden und aussagekräftig. |
```

## Week 10 — source inventory

- [Woche 10 – Abschlussprojekt](../../../cds-devops/woche-10-abschlussprojekt/README.md) — `woche-10-abschlussprojekt/README.md`
- [01 – Projektanforderungen](../../../cds-devops/woche-10-abschlussprojekt/docs/01-projektanforderungen.md) — `woche-10-abschlussprojekt/docs/01-projektanforderungen.md`
- [02 – Dokumentation](../../../cds-devops/woche-10-abschlussprojekt/docs/02-dokumentation.md) — `woche-10-abschlussprojekt/docs/02-dokumentation.md`
- [03 – Bewertungsschema Abschlussprojekt](../../../cds-devops/woche-10-abschlussprojekt/docs/03-bewertungsschema.md) — `woche-10-abschlussprojekt/docs/03-bewertungsschema.md`
- [04 – Abnahme-Checkliste](../../../cds-devops/woche-10-abschlussprojekt/docs/04-abnahme-checkliste.md) — `woche-10-abschlussprojekt/docs/04-abnahme-checkliste.md`
- [Labor Woche 10 – Integrations-Session](../../../cds-devops/woche-10-abschlussprojekt/labor/README.md) — `woche-10-abschlussprojekt/labor/README.md`
- [Hausaufgabe Woche 10 – Abgabe des Abschlussprojekts](../../../cds-devops/woche-10-abschlussprojekt/hausaufgabe/README.md) — `woche-10-abschlussprojekt/hausaufgabe/README.md`

### Original lab acceptance criteria

```text
## Definition of Done

Die Integrations-Session ist erfolgreich, wenn:

- [ ] die Pipeline von einem frischen Commit bis zum Render-Deployment grün läuft;
- [ ] `kubectl get pods` ≥ 2 gesunde Replikate zeigt;
- [ ] das Grafana-Dashboard live auf Last reagiert und das Prometheus-Target UP ist;
- [ ] der Trivy-Scan in der Pipeline läuft;
- [ ] ein frischer Klon allein nach dem README startet;
- [ ] die Selbsteinschätzung nach dem Bewertungsschema ausgefüllt ist;
- [ ] Tag `v1.0.0` gesetzt ist.
```

```text
## Abnahmekriterien

- [ ] Alle Punkte der „Definition of Done" sind erfüllt.
- [ ] Die [Abnahme-Checkliste](../docs/04-abnahme-checkliste.md) ist so weit wie
      möglich geschlossen; offene Punkte sind benannt und terminiert.

---

[← Wochenübersicht](../README.md) · [Hausaufgabe: Abschlussprojekt →](../hausaufgabe/README.md)
```

### Original homework self-check

Week 10 uses the final project checklist and assessment rubric instead of a separate homework self-check. See the final checklist below.

## Original final-project acceptance checklist

Source: [week 10 final checklist](../../../cds-devops/woche-10-abschlussprojekt/docs/04-abnahme-checkliste.md). Reproduced as source text; do not tick these quoted boxes as project evidence.

```text
# 04 – Abnahme-Checkliste

Diese Checkliste prüfen Sie **vor der Abgabe** selbst. Jeder Punkt ist so
formuliert, dass er objektiv erfüllt oder nicht erfüllt ist – kein „mehr oder
weniger". Ist ein Kasten leer, fehlt Arbeit. Die Gliederung folgt den
Kriterien des [Bewertungsschemas](03-bewertungsschema.md).

Eine Kopie zum Abhaken im eigenen Repository liegt unter
[`code/projekt-vorlage/abnahme-checkliste.md`](../code/projekt-vorlage/abnahme-checkliste.md).

## Git und Zusammenarbeit

- [ ] Öffentliches GitHub-Repository existiert und ist erreichbar.
- [ ] **`normansuesstrunk`** ist als Collaborator eingeladen (Leserechte genügen).
- [ ] `main` ist durch eine Branch Protection Rule gegen direkte Pushes geschützt
      („Require a pull request before merging").
- [ ] Mindestens fünf Pull Requests sind gemergt.
- [ ] Jeder dieser PRs hat eine Beschreibung, die *was* und *warum* festhält.
- [ ] Jeder dieser PRs war zum Merge-Zeitpunkt grün in der CI.
- [ ] `CONTRIBUTING.md` beschreibt GitHub Flow, Commit- und Selbstprüfungsregeln.
- [ ] Die Commit-Historie zeigt kontinuierliche Arbeit über die Wochen, nicht
      einen einzelnen Grosscommit.
- [ ] Tag `v1.0.0` ist gesetzt und ein Release mit Anmerkungen ist veröffentlicht.

## Containerisierung

- [ ] `Dockerfile` verwendet einen Multi-Stage-Build.
- [ ] Das Runtime-Image enthält keine Build-Tools oder pip-Caches.
- [ ] `docker run --rm <image> whoami` gibt nicht `root` aus.
- [ ] `docker build .` läuft ohne Fehler durch.
- [ ] `curl localhost:8000/health` liefert im Container `{"status":"ok",...}`.
- [ ] `docker-compose.yml` definiert die Dienste `web` und `db`.
- [ ] Nach `down` und erneutem `up` sind Daten dank benanntem Volume erhalten.
- [ ] `web` startet erst, wenn `db` gesund ist (`condition: service_healthy`).

## CI-Pipeline

- [ ] `.github/workflows/ci.yml` läuft bei jedem Pull Request.
- [ ] Die Pipeline enthält einen Lint-Schritt (`ruff check` und Formatprüfung).
- [ ] Die Pipeline führt die Tests aus (`pytest`).
- [ ] Ein Coverage-Gate von mindestens 80 % ist aktiv (`fail_under = 80`).
- [ ] Die Pipeline baut das Container-Image.
- [ ] Ein absichtlich fehlerhafter Commit macht die Pipeline nachweislich rot.
- [ ] Grüner CI-Status ist Voraussetzung zum Mergen.

## CD und Deployment

- [ ] `render.yaml` beschreibt den Dienst auf Render.
- [ ] Die Anwendung ist unter einer öffentlichen Render-URL erreichbar.
- [ ] `GET /health` liefert auf Render `200`.
- [ ] Ein Merge auf `main` löst automatisch ein neues Deployment aus.
- [ ] `DEPLOYMENT.md` beschreibt Deployment, Rollback und Störungsbehandlung.

## Infrastructure as Code

- [ ] Terraform-Konfiguration nutzt den Provider `kreuzwerker/docker`.
- [ ] `terraform init` und `terraform validate` laufen fehlerfrei.
- [ ] `terraform apply` startet den Container, `terraform destroy` entfernt ihn.
- [ ] Konfiguration nutzt Variablen statt hartkodierter Werte.
- [ ] `terraform.tfstate` und `.terraform/` stehen in `.gitignore`.

## Kubernetes

- [ ] Manifeste für Namespace, Deployment und Service liegen unter `k8s/`.
- [ ] Der Service bildet Port 80 auf targetPort 8000 ab.
- [ ] Das Deployment läuft mit mindestens zwei Replikaten.
- [ ] Eine Liveness-Probe prüft `/health`.
- [ ] Eine Readiness-Probe prüft `/ready`.
- [ ] `kubectl get pods` zeigt alle Replikate als `Running` und `READY 1/1`.

## Monitoring und Sicherheit

- [ ] Prometheus scrapt den `/metrics`-Endpunkt.
- [ ] Das Target steht in Prometheus unter `Status → Targets` auf UP.
- [ ] Ein Grafana-Dashboard „<Projekt> Overview" existiert.
- [ ] Das Dashboard zeigt mindestens Request-Rate, Fehlerrate und Latenz.
- [ ] Das Dashboard-JSON ist im Repository versioniert.
- [ ] Ein Trivy-Scan läuft in der Pipeline und ist im Log sichtbar.
- [ ] Der Trivy-Schwellwert ist gesetzt und dokumentiert.
- [ ] `git log -p` enthält keine Passwörter, Tokens oder Keys.
- [ ] Secrets liegen in GitHub Secrets bzw. der Deploy-Umgebung, nicht im Code.

## Dokumentation

- [ ] `README.md` erklärt Was, Warum und einen kopierbaren Schnellstart.
- [ ] Eine Architekturübersicht mit C4-Diagramm (Kontext + Container) existiert.
- [ ] `DEPLOYMENT.md` ist als abarbeitbares Runbook geschrieben.
- [ ] `MONITORING.md` beschreibt Metriken, Dashboard und Schwellwerte.
- [ ] Mindestens zwei ADRs unter `docs/adr/` mit den vier Pflichtabschnitten.
- [ ] Eine kursfremde Person kann das Projekt allein anhand der Doku starten.

## Selbsteinschätzung und Abgabe

- [ ] Die Tabelle aus dem [Bewertungsschema](03-bewertungsschema.md#selbsteinschätzung-vor-der-abgabe)
      ist mit Punkten und Belegen ausgefüllt und liegt als `BEWERTUNG.md` im
      Projekt-Repository.
- [ ] Ein frischer Klon des Repositorys startet allein nach dem README.
- [ ] Der Einsatz von KI-Werkzeugen ist gemäss den
      [Regeln des Moduls](../../README.md#plagiate-und-ki-werkzeuge)
      deklariert.

Erst wenn **alle** relevanten Kästen gefüllt sind, ist das Projekt abgabereif.

[← 03 – Bewertungsschema](03-bewertungsschema.md)
```

## Review scope

46 theory/project chapters plus 10 week overviews, 10 lab guides, and 10 homework guides = 76 indexed weekly source files.

Additional references: course README and setup checker; example-app README and pyproject; project contribution template; week-6 CD workflow and smoke-test script; week-9 dashboard JSON. Detailed steps, exercise prompts, and example configurations remain available through the original source links.

Assessment is based on the final repository; labs/homework are not separately graded. Pure theory (e.g. historical models, kernel internals, cloud service-model definitions) informs design and examination preparation but does not automatically add an app feature or deployment component.
