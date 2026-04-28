#!/usr/bin/env python3
"""
Bootstrap a new project following the Project Framework.
Creates the folder structure and populates initial documentation.

Standard library only -- no third-party dependencies.
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


class ProjectBootstrapper:
    """Handles creation of new project structure and documentation."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.projects_dir = repo_root / "_projects"
        self.templates_dir = repo_root / "_projects" / "_scripts" / "templates"

    def create_project(self, config: Dict[str, str]) -> Path:
        """Create a new project with the given configuration."""
        date_prefix = datetime.now().strftime("%Y%m%d")
        original_name = config["name"]

        self.projects_dir.mkdir(parents=True, exist_ok=True)

        sequence_num = self._get_next_sequence_number(self.projects_dir, date_prefix)
        project_name = f"{date_prefix}.{sequence_num:02d}.{original_name}"
        config["name"] = project_name

        project_path = self.projects_dir / project_name

        if project_path.exists():
            print(f"Error: Project '{project_name}' already exists at {project_path}", file=sys.stderr)
            sys.exit(1)

        self._create_folder_structure(project_path)
        self._create_readme(project_path, config)
        self._create_initial_task(project_path, config)
        self._create_next_task_prompt(project_path, config)
        self._create_plans_readme(project_path, config)

        print(f"Successfully created project: {project_path}")
        return project_path

    def _get_next_sequence_number(self, projects_dir: Path, date_prefix: str) -> int:
        """Determine the next sequence number for projects created today."""
        if not projects_dir.exists():
            return 1

        existing_projects = []
        for item in projects_dir.iterdir():
            if item.is_dir() and item.name.startswith(date_prefix):
                parts = item.name.split(".")
                if len(parts) >= 3 and parts[1].isdigit():
                    existing_projects.append(int(parts[1]))

        if existing_projects:
            return max(existing_projects) + 1
        return 1

    def _create_folder_structure(self, project_path: Path) -> None:
        """Create the standard folder structure for a project."""
        folders = [
            "tasks",
            "plans",
            "checkpoints",
            "changelogs",
            "design-decisions",
            "coding-guidelines",
            "wrong-assumptions",
            "dont-dos",
        ]

        project_path.mkdir(parents=True, exist_ok=True)

        for folder in folders:
            (project_path / folder).mkdir(exist_ok=True)
            (project_path / folder / ".gitkeep").touch()

    def _create_readme(self, project_path: Path, config: Dict[str, str]) -> None:
        """Create the project README with project information."""
        template = self._load_template("project_readme.md")

        dependencies = config.get("dependencies", "None identified")
        if dependencies.lower() in ["none", "n/a", ""]:
            dependencies = "None identified"

        risks = config.get("risks", "None identified")
        if risks.lower() in ["none", "n/a", ""]:
            risks = "None identified"

        success_criteria = config.get("success_criteria", "")
        if success_criteria:
            success_lines = [f"- {line.strip()}" for line in success_criteria.split(",")]
            success_criteria = "\n".join(success_lines)
        else:
            success_criteria = "- Project goals achieved\n- All tests passing\n- Documentation updated"

        content = template.format(
            project_name=config["name"],
            project_description=config["description"],
            created_date=datetime.now().strftime("%Y-%m-%d"),
            project_goal=config["goal"],
            project_timeline=config["timeline"],
            project_tech=config["tech"],
            project_type=config["type"].replace("-", " ").title(),
            project_components=config["components"],
            dependencies=dependencies,
            success_criteria=success_criteria,
            risks=risks,
        )

        (project_path / "README.md").write_text(content)

    def _create_initial_task(self, project_path: Path, config: Dict[str, str]) -> None:
        """Create the initial task plan based on project type."""
        template = self._load_template(f"initial_task_{config['type']}.md")

        if not template:
            template = self._load_template("initial_task_generic.md")

        content = template.format(
            project_name=config["name"],
            project_goal=config["goal"],
            project_tech=config["tech"],
            project_components=config["components"],
            created_date=datetime.now().strftime("%Y-%m-%d %H:%M"),
        )

        (project_path / "tasks" / "T01_0_plan.md").write_text(content)

    def _create_next_task_prompt(self, project_path: Path, config: Dict[str, str]) -> None:
        """Create the next-task.md with Rules of Engagement and portable project paths."""

        rel_project_path = self._get_relative_project_path(project_path)

        content = f"""# Next Task: {config["name"]}

## RULES OF ENGAGEMENT - READ FIRST

**When this file is loaded in a new conversation, follow these steps in order:**

### Step 1: Gather Context Silently

Read all project files without outputting:
- Every file in `changelogs/` -- understand the full history. Non-negotiable.
- `plans/` and `plans/README.md` -- active plans and status
- `tasks/` -- current task files
- `checkpoints/` -- milestone summaries
- `design-decisions/`, `coding-guidelines/`, `wrong-assumptions/`, `dont-dos/`

### Step 2: Present Status

Present:

- **Overall Objective**: [1-2 sentences]
- **Changelogs Reviewed**: [N changelogs read] -- [list of changelog slugs or "none yet"]
- **What's Been Completed**: [Key milestones]
- **What's Pending**: [Remaining work]
- **Agreed Focus for This Session**: [From previous session]

If you have observations, concerns, or context the human should know, share
them briefly between the status and the options.

### Step 3: Present Options

- **A (Recommended):** [description]
- **B:** [description]
- **C:** [description]

### Step 4: Wait for Direction

Do NOT proceed until the human explicitly confirms an option or gives direction.

### Execution Philosophy: Do-First

When executing project work, the default posture is to DO the work, not TELL
the human to do the work:

1. **Do it yourself.** Use every tool available: CLI, MCP servers, APIs, browser
   automation, code generation. Think creatively.
2. **Request tools.** If you need access or a tool you don't have, ask for it
   specifically. Name the tool, explain what it enables, describe how to provide it.
3. **Prepare everything, hand off the minimum.** If something is truly impossible
   for you to do, do maximum prep work -- set up prerequisite data, configure
   everything possible -- and provide step-by-step instructions so the human's
   remaining effort is minimal.
4. **Never leave bare instructions.** Do not say "go create X." Instead: "I've
   prepared A and B. The one thing I need from you is Z. Here is exactly how."

---

## Quick Resume Instructions

Drop this file into your conversation to quickly resume work on this project.

## Project: {config["name"]}

**Description**: {config["description"]}
**Goal**: {config["goal"]}
**Tech Stack**: {config["tech"]}
**Components**: {config["components"]}

## Essential Files to Review

### 1. Latest Checkpoint (if exists)
```
{rel_project_path}/checkpoints/
```

### 2. Current Task
```
{rel_project_path}/tasks/
```

### 3. Project README
```
{rel_project_path}/README.md
```

## Knowledge Folders to Check

### Design Decisions
```
{rel_project_path}/design-decisions/
```

### Coding Guidelines
```
{rel_project_path}/coding-guidelines/
```

### Wrong Assumptions
```
{rel_project_path}/wrong-assumptions/
```

### Don't Dos
```
{rel_project_path}/dont-dos/
```

### Changelogs
```
{rel_project_path}/changelogs/
```

### Plans
```
{rel_project_path}/plans/
```

## Current Status

**Created**: {datetime.now().strftime("%Y-%m-%d")}
**Current Task**: T01 (Initial Setup)
**Status**: Planning

---

*This file provides paths to all project resources for quick context loading.*
"""

        (project_path / "next-task.md").write_text(content)

    def _create_plans_readme(self, project_path: Path, config: Dict[str, str]) -> None:
        """Create the plans/README.md with an empty plan registry."""
        content = f"""# Implementation Plans

Plans created for this project. Each plan documents a specific implementation effort.

## Plan Registry

| Plan | Status | Created | Completed | Description |
|------|--------|---------|-----------|-------------|

### Status Legend

- **Pending**: Plan created, not yet started
- **In Progress**: Currently being executed
- **Completed**: All phases/tasks finished
- **Abandoned**: Plan was cancelled or superseded

---

*Last updated: {datetime.now().strftime("%Y-%m-%d")}*
"""
        (project_path / "plans" / "README.md").write_text(content)

    def _get_relative_project_path(self, project_path: Path) -> str:
        """Get the project path relative to the repo root."""
        try:
            rel_path = project_path.relative_to(self.repo_root)
            return str(rel_path)
        except ValueError:
            return str(project_path)

    def _load_template(self, template_name: str) -> Optional[str]:
        """Load a template file, returning None if it doesn't exist."""
        template_path = self.templates_dir / template_name

        if not template_path.exists():
            if template_name == "project_readme.md":
                return self._get_fallback_readme_template()
            elif template_name.startswith("initial_task"):
                return self._get_fallback_task_template()
            return None

        return template_path.read_text()

    def _get_fallback_readme_template(self) -> str:
        """Provide a fallback README template."""
        return """# Project: {project_name}

## Overview
{project_description}

**Created**: {created_date}

## Project Information

### Goal
{project_goal}

### Timeline
{project_timeline}

### Technology Stack
{project_tech}

### Project Type
{project_type}

### Affected Components
{project_components}

## Dependencies
{dependencies}

## Success Criteria
{success_criteria}

## Known Risks
{risks}

## Status

### Current Phase
Planning and Setup

### Last Updated
{created_date}

## Quick Links
- [Next Task](next-task.md) - Drop this file into chat to resume
- [Current Task](tasks/)
- [Changelogs](changelogs/)
- [Latest Checkpoint](checkpoints/)
- [Design Decisions](design-decisions/)
- [Coding Guidelines](coding-guidelines/)

## Notes
This project follows the Project Framework for structured multi-day development.

To resume work: Simply drag and drop the `next-task.md` file into your conversation.
"""

    def _get_fallback_task_template(self) -> str:
        """Provide a generic task template."""
        return """# Task T01: Initial Setup and Analysis

**Created**: {created_date}
**Status**: Planning

## Objective
Begin work on {project_goal}

## Approach

### Phase 1: Analysis
1. Examine the current state of {project_components}
2. Identify key areas that need attention
3. Map dependencies and constraints

### Phase 2: Planning
1. Break down the work into manageable subtasks
2. Identify critical path items
3. Establish success metrics

### Phase 3: Implementation Strategy
1. Determine the order of operations
2. Identify potential risks and mitigations
3. Plan for testing and validation

## Technology Considerations
- Stack: {project_tech}
- Components: {project_components}

## Next Steps
1. [ ] Complete initial analysis
2. [ ] Create detailed implementation plan
3. [ ] Set up development environment if needed
4. [ ] Begin first implementation task

## Notes
- This is the initial task plan
- Will be refined based on analysis results
- Feedback will be captured in T01_1_feedback.md
- Execution details will be logged in T01_2_execution.md
"""


def main():
    parser = argparse.ArgumentParser(description="Bootstrap a new Project Framework project")

    parser.add_argument("--name", required=True, help="Project name (kebab-case)")
    parser.add_argument("--description", required=True, help="Brief project description")
    parser.add_argument("--goal", required=True, help="Primary project goal")
    parser.add_argument("--timeline", required=True, help="Target timeline")
    parser.add_argument("--tech", required=True, help="Technology stack")
    parser.add_argument(
        "--type",
        required=True,
        choices=["feature-development", "refactoring", "migration",
                 "bug-fix", "optimization", "research", "other"],
        help="Project type",
    )
    parser.add_argument("--components", required=True, help="Affected components")
    parser.add_argument("--success-criteria", required=True, help="Success criteria (comma-separated)")
    parser.add_argument("--dependencies", default="None", help="External dependencies")
    parser.add_argument("--risks", default="None", help="Known risks")

    args = parser.parse_args()

    try:
        repo_root = Path(os.popen("git rev-parse --show-toplevel").read().strip())
    except Exception:
        repo_root = Path.cwd()

    config = {
        "name": args.name,
        "description": args.description,
        "goal": args.goal,
        "timeline": args.timeline,
        "tech": args.tech,
        "type": args.type,
        "components": args.components,
        "success_criteria": args.success_criteria,
        "dependencies": args.dependencies,
        "risks": args.risks,
    }

    bootstrapper = ProjectBootstrapper(repo_root)
    project_path = bootstrapper.create_project(config)

    print(f"\nProject structure created at: {project_path}")
    print(f"Project name: {config['name']} (automatically prefixed with date)")
    print("\nCreated files:")
    print("  - README.md (project overview and goals)")
    print("  - next-task.md (quick resume file - drag into chat)")
    print("  - tasks/T01_0_plan.md (initial task plan)")
    print("  - plans/README.md (plan registry)")
    print("\nCreated folders:")
    print("  - plans/ (for implementation plans)")
    print("  - checkpoints/ (for milestone summaries)")
    print("  - changelogs/ (for session changelogs)")
    print("  - design-decisions/ (for architectural choices)")
    print("  - coding-guidelines/ (for project standards)")
    print("  - wrong-assumptions/ (for corrected misconceptions)")
    print("  - dont-dos/ (for anti-patterns to avoid)")
    print("\nNext steps:")
    print(f"  1. Review the task plan at {project_path}/tasks/T01_0_plan.md")
    print(f"  2. To resume in a new session: Drag {project_path}/next-task.md into chat")
    print(f"  3. Or continue working in the current session")


if __name__ == "__main__":
    main()
