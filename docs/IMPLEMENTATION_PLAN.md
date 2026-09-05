# AI Product Factory — Implementation Plan

## 1. Purpose
This document defines the practical build order for AI Product Factory until a usable first version of the project is complete.

It is intentionally more execution-oriented than the full project specification and should guide implementation sequencing, scope control, and delivery checkpoints.

If this document conflicts with `mix/context/AI_PRODUCT_FACTORY_PROJECT_SPEC.md`, the specification file wins.

---

## 2. Delivery Objective
The implementation should end in a working project that can:
- accept a high-level topic and active context,
- research and compare candidate product opportunities,
- select one viable opportunity,
- choose a suitable `ProductType`,
- generate a reviewable digital product draft,
- create Etsy listing materials,
- build a structured output package,
- persist structured run data,
- enforce budget and QA rules,
- leave only final review to the human.

This means the goal is not just a code skeleton.
The goal is a working first version of the product pipeline.

---

## 3. Build Strategy
The project should be built in small, testable phases.

Goals of the implementation approach:
- get to a runnable MVP quickly,
- avoid overbuilding,
- keep business logic separate from orchestration,
- keep deterministic logic in Python,
- introduce AI integration behind clear interfaces,
- make it easy to swap or refine parts later,
- keep cost control visible from the beginning,
- finish each phase in a way that leaves the repository in a usable state.

---

## 4. Phase Order

### Phase 1 — Project Skeleton and Tooling
Goal:
- establish the repository structure and core project scaffolding.

Deliverables:
- Python project structure
- `pyproject.toml`
- environment/config setup
- base package layout
- README
- `.env.example`
- output and data directories
- logging setup
- CLI entrypoint or runner entrypoint

Exit criteria:
- project installs locally
- app entrypoint runs
- config loading works

Out of scope:
- real agent execution
- product generation logic
- full business workflow behavior

---

### Phase 2 — Core Domain Models and Shared Contracts
Goal:
- define the internal data structures used across the workflow.

Deliverables:
- enums for statuses and product types
- models for runs, candidates, scores, products, artifacts, listings
- settings/config models
- workflow result models
- shared typing utilities

Exit criteria:
- workflow data can move through typed models without ad-hoc dict usage
- key statuses and product types are centralized

Out of scope:
- real persistence logic
- external model calls

---

### Phase 3 — Storage and Persistence Layer
Goal:
- create the first reliable persistence layer.

Deliverables:
- SQLite initialization
- schema creation
- repository/data access layer
- run persistence
- candidate persistence
- score persistence
- artifact persistence
- listing persistence
- basic file storage utilities

Exit criteria:
- a run can be created and saved
- candidate/score/product/listing records can be written and retrieved
- output directories can be created deterministically

Out of scope:
- analytics dashboards
- advanced migrations
- external sync processes

---

### Phase 4 — Workflow Infrastructure and Execution Engine
Goal:
- define the execution flow and stage boundaries.

Deliverables:
- workflow stage definitions
- pipeline runner
- stage result contracts
- context loading logic
- budget tracking hooks
- failure handling model
- refinement loop control
- stage-level logging

Exit criteria:
- the pipeline can execute all stages in order, even if some are still stubbed
- failures are recorded in a structured way
- budget and stop rules can be checked during execution

Out of scope:
- high-quality content generation
- parallel execution

---

### Phase 5 — AI Provider Abstraction and Agent Interfaces
Goal:
- isolate model access and role behavior behind interfaces.

Deliverables:
- LLM provider abstraction
- OpenAI adapter
- prompt/context assembly helpers
- agent role interfaces
- CrewAI orchestration adapter layer
- model routing hooks for cheaper vs stronger model usage

Exit criteria:
- workflow stages can call AI through stable interfaces
- provider-specific logic is isolated
- prompts can be improved without changing core workflow code

Out of scope:
- full multi-provider implementation
- advanced provider failover

---

### Phase 6 — Research and Opportunity Evaluation
Goal:
- implement the first half of the product pipeline.

Deliverables:
- research stage
- structured evidence output
- candidate generation flow
- evaluation flow
- scoring implementation
- weighted scoring logic
- viability gate enforcement
- candidate selection logic
- research/evaluation persistence wiring

Exit criteria:
- the system can accept a topic and produce ranked candidates
- one selected candidate or a structured failure state is produced

Out of scope:
- exhaustive market intelligence
- broad internet automation beyond initial practical needs

---

### Phase 7 — Product Architecture and Product Creation
Goal:
- turn the selected candidate into a structured product draft.

Deliverables:
- product architecture stage
- ProductType selection logic
- ProductType-driven output planning
- product creation stage
- structured product summary generation
- buyer-facing instruction generation
- included files generation
- key benefits generation
- artifact registry integration

Exit criteria:
- the system can turn a selected candidate into a coherent product draft package
- required artifact types are planned and tracked

Out of scope:
- advanced design polish
- large library of templates beyond MVP needs

---

### Phase 8 — QA, Packaging, Listing, and Preview Planning
Goal:
- make outputs reviewable and delivery-ready.

Deliverables:
- AI QA flow
- Technical QA flow
- QA pass/fail recording
- packaging/output folder builder
- manifest generation
- ZIP packaging
- Etsy listing generation
- preview plan generation
- delivery notes generation

Exit criteria:
- the system can produce a structured output bundle for a successful run
- QA can block incomplete outputs
- listing materials are generated for successful products

Out of scope:
- automatic Etsy publishing
- full visual asset generation pipeline

---

### Phase 9 — Cost Efficiency, Reuse, and Regeneration Controls
Goal:
- make the working MVP cheaper, more stable, and more repeatable.

Deliverables:
- caching/reuse support
- regeneration controls
- context minimization improvements
- template-first helpers
- stage-level cost reporting
- preview gating enforcement
- reuse of unchanged intermediate stages

Exit criteria:
- unchanged earlier stages do not rerun unnecessarily
- stage-level costs are visible
- the pipeline becomes cheaper to operate across repeated runs

Out of scope:
- premature optimization before the pipeline is already functional

---

### Phase 10 — Hardening and Project-Ready Completion
Goal:
- move from “working MVP” to “usable project baseline”.

Deliverables:
- smoke tests for main workflow
- validation tests for schema/config/output rules
- example run inputs
- example output package
- improved README usage instructions
- error handling cleanup
- developer notes for extending ProductTypes and stages

Exit criteria:
- a collaborator can clone the repo, configure it, and run the pipeline
- the project has a clear path for continued development
- the repository is no longer just a scaffold, but a usable implementation base

Out of scope:
- enterprise productionization
- autoscaling infrastructure
- marketplace integrations beyond MVP needs

---

## 5. Recommended Repository Structure

```text
src/
  ai_product_factory/
    agents/
    core/
    domain/
    workflows/
    storage/
    outputs/
    providers/
    utils/
    templates/

config/

data/
  sqlite/
  runs/

mix/context/

tests/
```

---

## 6. Milestones

### Milestone A — Installable Skeleton
Complete when:
- the project structure exists,
- config loading works,
- entrypoint runs,
- the repository is ready for real module implementation.

### Milestone B — Runnable End-to-End Skeleton
Complete when:
- topic + context can be loaded,
- run records are created,
- research/evaluation/product/QA/listing stages execute in sequence,
- placeholder or early outputs are generated,
- output package structure is created.

### Milestone C — First Publishable Workflow Prototype
Complete when:
- the system can generate one coherent product draft,
- produce listing materials,
- enforce viability gates,
- pass basic QA,
- create a final package for human review.

### Milestone D — Usable Project Baseline
Complete when:
- the project can be run by another developer,
- documentation is sufficient,
- the MVP flow is stable enough for continued iteration.

---

## 7. Recommended Build Priorities Inside the Code
When implementation begins, this should be the preferred order inside the repository:

1. config + entrypoint
2. domain models + enums
3. SQLite schema + storage layer
4. workflow runner + stage contracts
5. provider abstraction + OpenAI adapter
6. research/evaluation flow
7. product architecture + creation flow
8. QA + packaging
9. listing + preview planning
10. reuse/cost optimization
11. tests and hardening

---

## 8. First Runnable MVP Target
The first runnable version does not need to generate a perfect final product.

It should be able to:
1. load topic + context
2. create a run record
3. generate or simulate candidate research output
4. score candidates
5. select one candidate
6. select a ProductType
7. generate placeholder or early product artifacts
8. run QA checks
9. build final output folder
10. persist metadata to SQLite

This gives a true end-to-end skeleton before deeper quality improvements.

---

## 9. Definition of “Ready Enough to Start Real Use”
The project should be considered ready for real early use when it can:
- complete one full run without manual intervention between stages,
- return a structured failure if no viable opportunity is found,
- generate all required buyer-facing deliverables for at least one supported `ProductType`,
- save outputs and metadata reliably,
- apply budget and refinement limits,
- leave only final human review outside the system.

---

## 10. Recommended Implementation Principles During Build
- Build thin vertical slices instead of giant unfinished subsystems.
- Prefer working stubs over premature complexity.
- Keep AI prompts and orchestration replaceable.
- Keep file-based outputs easy to inspect manually.
- Prefer structured intermediate outputs.
- Avoid building parallel execution early.
- Keep costs visible from the beginning.
- Do not expand scope until the current phase has a working exit state.
- Prefer one supported flow done well over many half-built branches.

---

## 11. Immediate Next Step
The immediate next step after this plan is:

> Build Phase 1: repository skeleton, Python package structure, config, logging, entrypoint, SQLite bootstrap, and first workflow scaffolding.
