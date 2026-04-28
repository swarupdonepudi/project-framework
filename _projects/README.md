# Projects Directory

This directory contains all projects organized under the Project Framework.

## Directory Structure

```
_projects/
├── YYYYMMDD.NN.project-name/          # Active projects
├── YYYYMMDD.NN.sp.sub-project-name/   # Active sub-projects (flat, linked to parent)
├── .completed/                         # Finished projects (archived)
├── .on-hold/                           # Paused projects
├── .shelved/                           # Indefinitely deferred projects
├── _scripts/                           # Bootstrap and utility scripts
└── _rules/                             # Cursor rules (if not in .cursor/rules/)
```

## Creating a New Project

### Using Cursor (recommended)

Pull `@start-project` into your Cursor chat. The AI will interview you and create the project.

### Using the shell script

```bash
./_projects/_scripts/start-project.sh
```

### Using the Python script directly

```bash
python3 _projects/_scripts/bootstrap_project.py \
  --name "api-migration" \
  --description "Migrate to new API" \
  --goal "Complete API v2 migration" \
  --timeline "2 weeks" \
  --tech "Python/FastAPI" \
  --type "migration" \
  --components "backend APIs" \
  --success-criteria "All endpoints migrated,Tests passing,Docs updated"
```

## Resuming Any Project

Drag the `next-task.md` file from any project into your Cursor chat to instantly load all context and resume work.

```
Drag: _projects/20260428.01.api-migration/next-task.md -> Instant resume!
```

## Creating Sub-Projects

When a work item within a project is large enough for independent tracking:

```
@start-sub-project
```

Sub-projects use the `sp.` marker in their name and are linked to their parent through file contents.

## Completing a Project

When a project is finished:

```
@complete-project
```

This marks the project as completed, moves it to `.completed/`, and fixes all path references.

## Philosophy

> **Maintain just enough context to keep momentum across sessions.**

The framework is designed to get out of your way and let you build. Each project folder carries exactly the context needed to continue. Session wrap-ups ensure nothing is lost. Completion moves projects out of your active view.
