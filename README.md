# Project Framework

A structured system for managing AI-assisted development work across multiple sessions using Cursor (or any AI coding assistant).

## The Problem

When working on projects that span multiple AI conversations:

- **Context loss**: Critical decisions and progress get buried in long conversation histories
- **Decision amnesia**: Previously made design choices get forgotten or contradicted
- **Onboarding overhead**: Each new session requires extensive context-setting
- **Pattern repetition**: The AI suggests approaches already proven ineffective
- **Progress blindness**: It is hard to see what has been accomplished and what remains

## The Solution

Each project is a **folder that carries context between sessions**. The folder contains everything the AI needs to resume exactly where you left off: objectives, progress history, decisions made, lessons learned, and what to do next.

You drag one file -- `next-task.md` -- into your AI chat, and the AI instantly knows the full state of the project. No explaining, no searching, no rebuilding context.

## Philosophy

**Open projects = work to do.** Your list of active project folders is your to-do list. Every piece of work that will span multiple sessions gets a project. The goal is always to drive projects to completion and keep the active list as short as possible.

Creating a project captures everything you need to complete the work. Once the project exists, you stop carrying the context in your head. From there, it is mechanical: load the project, pick the next task, create a plan, execute, wrap up, repeat.

## How It Works

```
                    ┌──────────────────────┐
                    │   Identify work that │
                    │   spans 2+ sessions  │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │   Create a project   │
                    │   @start-project     │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │  Review initial plan │
                    │  Approve or revise   │
                    └──────────┬───────────┘
                               │
               ┌───────────────▼───────────────┐
               │         Session Loop          │
               │                               │
               │  1. Load next-task.md         │
               │  2. AI presents status        │
               │  3. Pick an option            │
               │  4. Create plan, execute      │
               │  5. Wrap up (@wrap-up-session)│
               │     - Update next-task.md     │
               │     - Write session changelog │
               │     - Git commit              │
               │                               │
               └───────────────┬───────────────┘
                               │
                    ┌──────────▼───────────┐
                    │  Project complete    │
                    │  @complete-project   │
                    │  Moves to .completed │
                    └──────────────────────┘
```

## Project Structure

Every project lives under `_projects/` with a standardized folder layout:

```
_projects/YYYYMMDD.NN.project-name/
├── README.md                    # Project overview and goals
├── next-task.md                 # The magic file -- drag into chat to resume
├── tasks/                       # Detailed task planning and execution
│   ├── T01_0_plan.md           # Task 1 initial plan (pending review)
│   ├── T01_1_review.md         # Developer feedback
│   ├── T01_2_revised_plan.md   # Revised plan after feedback
│   └── T01_3_execution.md     # Execution notes (after approval)
├── plans/                       # Implementation plans and registry
│   └── README.md               # Plan registry with status tracking
├── checkpoints/                 # Milestone summaries
├── changelogs/                  # Session-by-session progress records
├── design-decisions/            # Key architectural choices
├── coding-guidelines/           # Project-specific code standards
├── wrong-assumptions/           # Documented misconceptions
└── dont-dos/                    # Anti-patterns discovered
```

## Naming Convention

Projects use date-prefixed, sequence-numbered names:

```
YYYYMMDD.NN.project-name
```

- `YYYYMMDD` -- creation date (enables chronological sorting)
- `NN` -- auto-incrementing sequence number for projects created on the same day
- `project-name` -- kebab-case descriptive name

Examples:

- `20260428.01.api-migration`
- `20260428.02.auth-refactor`

## The next-task.md File

This is the core innovation. Each project's `next-task.md` contains:

- Paths to all project folders and files
- Current project status and objectives
- The **Rules of Engagement** -- the section that makes the entire framework work

To resume any project: **drag `next-task.md` into your chat**. That is it.

## Rules of Engagement

The Rules of Engagement are a set of instructions embedded at the top of every `next-task.md` file. They tell the AI exactly how to behave when the file is loaded into a new session. Without these rules, the AI would either start asking you to re-explain context or, worse, begin executing work without understanding the project state.

The Rules of Engagement enforce a four-step sequence every time a project is resumed:

### Step 1: Gather Context Silently

The AI reads all project files without producing any output:
- Every file in `changelogs/` -- the full session history, non-negotiable
- `plans/` and `plans/README.md` -- active plans and their status
- `tasks/` -- current task files and execution logs
- `checkpoints/` -- milestone summaries
- `design-decisions/`, `coding-guidelines/`, `wrong-assumptions/`, `dont-dos/` -- the project's accumulated knowledge

This is what prevents the AI from asking "so what were we doing?" at the start of every session. It already knows.

### Step 2: Present Status

After reading everything, the AI presents a structured summary:
- **Overall Objective** -- what the project is trying to achieve
- **Changelogs Reviewed** -- how many session records were read
- **What Has Been Completed** -- key milestones reached
- **What Is Pending** -- remaining work
- **Agreed Focus for This Session** -- what was agreed to in the last session

This gives you a quick health check on the project without needing to read anything yourself.

### Step 3: Present Options

The AI offers 2-3 concrete options for what to work on:
- **Option A (recommended)** -- the most logical next step
- **Option B** -- an alternative approach or different priority
- **Option C** -- another direction if applicable

This prevents the AI from silently deciding what to do. You see the choices and you pick.

### Step 4: Wait for Direction

**The AI does not begin any work until you explicitly choose an option or give direction.** This is the most important rule. Even in agent mode, the AI never auto-executes on project resume. You are always in control of what happens next.

### Execution Philosophy: Do-First

Once you give direction, the Rules of Engagement also define how the AI should execute. The posture is **do the work, do not tell the human to do the work**:

1. **Do it yourself** -- write the code, create the files, run the commands
2. **Request tools** -- if you need access you do not have, ask for it specifically
3. **Prepare everything, hand off the minimum** -- if something truly requires manual steps, do all the prep and hand off only the irreducible manual part
4. **Never leave bare instructions** -- instead of "create a file at X", create the file

### Why Rules of Engagement Matter

Without the Rules of Engagement, every session would start with the AI either:
- Asking you to re-explain what the project is about (wasting 5-10 minutes)
- Guessing what to do and starting work without your approval (risky)
- Suggesting approaches you already tried and rejected (frustrating)

The Rules of Engagement turn every session resumption into: load context silently, present status, offer options, wait. Consistently. Every time. The wrap-up rule (`@wrap-up-session`) also ensures the Rules of Engagement are preserved in `next-task.md` at every session boundary.

## Session Workflow

### Starting a Session

1. Open Cursor
2. Drag `_projects/YYYYMMDD.NN.project-name/next-task.md` into the chat
3. The AI follows the Rules of Engagement:
   - Reads all project context silently
   - Presents a structured status summary
   - Offers options for this session
   - Waits for your direction
4. You pick an option or give direction
5. The AI creates a plan, you review and approve, then it executes

### Ending a Session

Invoke `@wrap-up-session` and the AI will:

1. Update `next-task.md` with session progress
2. Create a changelog entry in `changelogs/`
3. Save any plans to `plans/`
4. Set objectives for the next session
5. Commit everything to git

## Sub-Projects

When a piece of work within a project is large enough to warrant its own independent resumption, knowledge folders, and potentially parallel execution, create a sub-project.

Sub-projects use the same naming convention with an `sp.` marker:

```
YYYYMMDD.NN.sp.sub-project-name
```

Sub-projects live **flat** alongside regular projects (not nested inside the parent). They are linked to their parent through file contents:

- The parent's `README.md` and `next-task.md` get sub-project entries
- The sub-project's files link back to the parent and inherit the parent's knowledge folders

Example: A parent project "cloud-provider-expansion" plans to add 10 cloud providers. Each provider is a sub-project because it is independently executable and has its own task plan.

```
_projects/
  20260212.01.cloud-provider-expansion/     # Parent
  20260213.01.sp.oracle-provider/           # Sub-project
  20260213.02.sp.azure-provider/            # Sub-project
  20260213.03.some-unrelated-project/       # Regular project (shares sequence)
```

## Project Lifecycle Folders

Projects move through lifecycle stages using hidden dot-folders:

| Folder                  | Purpose                                                 |
| ----------------------- | ------------------------------------------------------- |
| `_projects/`            | Active projects -- work in progress                     |
| `_projects/.completed/` | Finished projects -- archived but still resumable       |
| `_projects/.on-hold/`   | Paused projects -- blocked or temporarily deprioritized |
| `_projects/.shelved/`   | Indefinitely deferred -- may never resume               |

Completed projects remain fully functional. You can drag a completed project's `next-task.md` into a chat to resume it if follow-up work is needed.

## Knowledge Folders

Each project has six knowledge folders. These are the project's long-term memory:

| Folder               | Purpose                                      | When to create entries                                         |
| -------------------- | -------------------------------------------- | -------------------------------------------------------------- |
| `design-decisions/`  | Key architectural and strategic choices      | When facing a significant fork in the road                     |
| `coding-guidelines/` | Project-specific code standards and patterns | When discovering a pattern that should be consistently applied |
| `wrong-assumptions/` | Documented incorrect premises                | When an assumption proves false and causes rework              |
| `dont-dos/`          | Anti-patterns and failed approaches          | When discovering what does not work                            |
| `checkpoints/`       | Milestone summaries                          | After completing meaningful work that changes project state    |
| `changelogs/`        | Session-by-session progress records          | Automatically at the end of every session                      |

**Documentation discipline**: The AI must ask before creating entries in knowledge folders (except changelogs, which are mandatory). Content must be high-impact, permanent, non-obvious, and reusable. Keep these folders clean and sparse.

## Monorepo vs Multi-Repo Setup

### Monorepo (simplest)

Your `_projects/` folder lives inside your repository. Everything is in one place.

```
my-repo/
  _projects/
    _scripts/
    _rules/        (or use .cursor/rules/)
    20260428.01.my-project/
  src/
  ...
```

### Multi-Repo with Personal Orchestration Repo

Your `_projects/` folder lives in a separate personal repository. Code changes happen in any number of other repositories. All repositories are added to the same Cursor workspace.

```
Cursor Workspace:
  project-framework/          # Your personal repo (has _projects/)
    _projects/
      20260428.01.my-project/
  work-repo-1/                # Code lives here
  work-repo-2/                # Code lives here too
  work-repo-3/                # And here
```

This way, your personal execution is orchestrated in one GitHub repository, while the actual code changes can be in any number of repositories.

## Cursor Rules

The framework includes Cursor rules (`.mdc` files) that automate the workflow:

| Rule                         | Type     | Purpose                                              |
| ---------------------------- | -------- | ---------------------------------------------------- |
| `@what-is-project-framework` | Ask-only | Explains the entire framework                        |
| `@setup-project-framework`   | Action   | Bootstraps the framework for your workspace          |
| `@start-project`             | Action   | Creates a new project with interview and scaffolding |
| `@start-sub-project`         | Action   | Creates a sub-project linked to a parent             |
| `@wrap-up-session`           | Action   | End-of-session workflow (changelog, status, commit)  |
| `@complete-project`          | Action   | Archives a finished project to `.completed/`         |
| `@create-project-changelog`  | Action   | Creates a session changelog entry                    |
| `@commit-changes`            | Action   | Commits with conventional commit format              |
| `@improve-project-workflow`  | Ask-only | Gather feedback and improve the framework            |

## Getting Started

### 1. Understand the framework

Pull `@what-is-project-framework` into a Cursor chat to get a guided explanation.

### 2. Set up for your workspace

Pull `@setup-project-framework` into a Cursor chat. It will ask whether you are using a monorepo or multi-repo setup and bootstrap everything for you.

### 3. Create your first project

Pull `@start-project` into a Cursor chat. Answer the interview questions, review the initial plan, and start working.

### 4. Resume a project

Drag `_projects/YYYYMMDD.NN.project-name/next-task.md` into any Cursor chat.

### 5. End a session

Say "wrap up" or pull `@wrap-up-session` to save progress and commit.

## The Bigger Picture

The project framework transforms how you work with AI coding assistants. Instead of treating each conversation as a fresh start, you build persistent project memory that compounds across sessions.

The list of open projects becomes your honest to-do list. Each project folder carries exactly the context needed to continue. Session wrap-ups ensure nothing is lost. Completion moves projects out of your active view.

The result: you spend time building, not explaining. Every session starts productively within seconds. The AI never suggests previously rejected approaches. Complex projects maintain consistency across weeks of development.
