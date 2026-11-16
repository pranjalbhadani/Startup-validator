# Contributions

This project was developed by our team of three people.
This document summarises my involvement in **Startup Validator** and clarifies the scope of work I personally contributed to the project.

## Project overview

Startup Validator is an AI-assisted application for evaluating startup ideas. It uses a multi-agent workflow to examine different aspects of an idea and combine the analysis into a consolidated assessment.

The project brings together a backend, a frontend, and an orchestration layer for the analysis workflow. The repository's documented technology stack includes **Python, FastAPI, React, LangGraph, Gemini API, and ChromaDB**.

## My areas of contribution

My work on this project has focused primarily on system design and the coordination of the multi-agent workflow.

### 1. System design and architecture

- Contributed to the overall system design and how the main application components fit together.
- Worked on defining the responsibilities and interactions between the frontend, backend, and analysis workflow.
- Considered how startup-idea inputs move through the system and how the resulting analysis is presented to the user.

### 2. Multi-agent workflow

- Contributed to the design and implementation of the agent workflow used to analyse a startup idea.
- Worked on how specialised analysis steps are coordinated and how their outputs contribute to the overall assessment.
- Considered the data passed between workflow stages and how the final result is assembled.

> **Scope note:** These bullets describe my high-level areas of involvement. They do not mean that I independently authored every component, agent, prompt, integration, or file in the repository. Specific code changes should be attributed using the Git commit history and the associated pull requests.

## Attribution and project history

Startup Validator is a collaborative codebase. I claim credit only for work I personally performed. Existing upstream work and contributions from other developers remain attributable to their original authors.

The repository's Git history, fork relationship, commit authorship, and pull requests are the source of truth for determining who changed particular files. This document is a readable summary; it does not replace that history.

## Contribution evidence

- [Repository commit history](https://github.com/MitullGoel-05/Startup-validator/commits)
- [Direct Pushes authored by me](https://github.com/pranjalbhadani/Startup-validator/activity?ref=main&activity_type=direct_push)
