# AI Product Factory — Project Specification

## 1. Project Overview

AI Product Factory is a lean AI-assisted system designed to turn a high-level topic into a publication-ready digital product for Etsy with minimal human involvement.

The system should not stop at idea generation. Its goal is to move from topic selection and opportunity evaluation to real product creation, packaging, and Etsy listing preparation.

This project is intended as a side-income product engine, optimized for speed, practicality, low operating complexity, and repeatable output generation.

---

## 2. Core Goal

The primary goal of the system is:

> To automatically transform a high-level topic and its thematic context into one Etsy-ready digital product package.

The system must be able to:
- identify promising sub-problems within a broader topic,
- evaluate product opportunities,
- select a strong product direction,
- generate actual product assets,
- prepare Etsy listing copy,
- prepare preview content guidance,
- package final outputs for review and publishing.

---

## 3. Primary Business Objective

The initial business objective is to reach first revenue as quickly as possible through digital products.

The system should be optimized for:
- low development risk,
- fast product generation,
- practical outputs,
- multiple testable products over time,
- learning from market feedback.

The initial monetization and validation channel is Etsy.

---

## 4. Input Model

The system input consists of:

1. **A high-level topic**
2. **An active thematic context file**

### Example inputs
- Topic: `professional workflow products`
- Topic: `AI-assisted decision support products`
- Topic: `document analysis tools for professionals`

The thematic context file provides the topic-specific strategic framing and should be treated as the active working context for the current run.

In addition to the thematic context file, the system may also use a global project context file that defines stable architectural and business rules.

---

## 5. Output Model

The minimum required output is an Etsy-ready product draft package.

### Output minimum must include:
- finished product files,
- Etsy title,
- Etsy description,
- product summary,
- buyer-facing “How to use” instructions,
- clear “What’s included” list,
- key benefits,
- preview content plan,
- a structured final output folder.

The system must produce outputs that are ready for final human review, not merely raw brainstorming material.

---

## 6. Human Involvement Model

Human involvement should be minimized.

### Required human involvement
- Final review of the finished output only.

### Not required in the normal MVP flow
- Manual subtopic selection
- Manual product direction approval between phases
- Manual format selection
- Manual intervention during intermediate agent steps

The system should continue automatically from topic analysis to product creation unless it reaches an explicit failure condition or configured stop rule.

---

## 7. MVP Scope

The first MVP should support one reliable end-to-end flow:

```text
Topic + Thematic Context
→ Research / Evidence Collection
→ Opportunity Evaluation
→ Best Candidate Selection
→ Product Architecture
→ Product Creation
→ AI QA
→ Technical Build / Packaging
→ Technical QA
→ Listing Generation
→ Preview Plan
→ Final Package
→ Human Final Review
```

The MVP should prioritize stability and clarity over breadth.

---

## 8. Non-Goals for the First MVP

The first MVP should NOT attempt to include:
- automatic Etsy publishing,
- full SaaS product generation,
- browser extensions,
- local installable mini-tools,
- fully autonomous large-scale portfolio publishing,
- complex visual design automation,
- parallel execution across many agents,
- custom model training.

Mini-tools may become a future direction, but they are not a priority for the first MVP.

---

## 9. System Philosophy

The project should follow this principle:

> Use AI only where reasoning, evaluation, or content generation is needed.  
> Use Python for deterministic execution.

This means:
- AI handles research interpretation, evaluation, product design, content generation, and listing copy.
- Python handles file generation, packaging, validation, storage, data processing, and workflow control where logic is deterministic.

The system should not be designed as “everything is an agent”.

---

## 10. Technology Direction

Initial stack:
- Python
- CrewAI
- OpenAI
- SQLite

### Architecture constraints
- The architecture must remain portable.
- The business logic must not be tightly coupled to one LLM provider.
- LLM access should be isolated behind an abstraction layer.
- The agent orchestration layer should not own all business rules.
- The project should be able to evolve later toward different model providers or local backends.

OpenAI is the initial engine, not a permanent architectural dependency.

---

## 11. Agent Strategy

The MVP should use a small number of specialized AI roles instead of many granular agents.

### Recommended core AI roles
1. **Research Agent**
2. **Evaluator Agent**
3. **Product Architect**
4. **Product Creator**
5. **QA Agent**
6. **Listing Agent**

These roles may be implemented as CrewAI agents initially, but the system should remain conceptually independent from the orchestration framework.

### Important principle
Do not create separate LLM agents for tasks that can be performed more reliably and cheaply in code.

---

## 12. Code-Driven System Modules

The following should be implemented in Python rather than as LLM agents:

- Context Manager
- Budget Controller
- Technical QA
- PDF Builder / export layer
- File/folder structure builder
- ZIP/package builder
- Database write layer
- Artifact registry
- Performance metrics ingestion layer

These are execution modules, not reasoning modules.

---

## 13. Research Model

Research must be evidence-first.

The research phase should not only generate ideas. It should first collect structured market evidence and then derive opportunities from it.

### Research should gather signals such as:
- keyword or search direction,
- competition proxies,
- price range,
- dominant product formats,
- visible gaps or weaknesses,
- estimated production speed,
- potential for repeatable product series.

Only after gathering evidence should the system generate and compare product opportunities.

### 13.1 Cost-efficient research rules
- Research should prioritize the minimum evidence needed to support a decision, not maximum breadth.
- Candidate generation should be limited to a small set of viable options per run.
- If a niche or subtopic has already been researched recently, the system should reuse prior evidence where possible.
- Re-research should happen only when the topic meaningfully changes or cached evidence is stale.

---

## 14. Opportunity Evaluation Model

Opportunity selection must use a structured scoring model, not only freeform LLM preference.

### Initial scoring dimensions should include:
- demand,
- competition / saturation,
- production speed,
- price potential,
- series potential,
- automation fit.

Exact weights may be refined later, but the scoring model must exist from the beginning.

The evaluation stage must produce explicit reasoning for why one opportunity is chosen over another.

### 14.1 Initial scoring weights
The MVP should start with the following default scoring weights:
- demand: **25%**
- competition / saturation: **20%**
- production speed: **20%**
- price potential: **10%**
- series potential: **15%**
- automation fit: **10%**

The total weighted score should be normalized to a 0–100 scale.

### 14.2 Scoring rules
- Each scoring dimension should be rated on a 0–100 scale.
- Higher demand is better.
- Lower competition should produce a better normalized competition score.
- Faster production speed is better.
- Higher price potential is better.
- Higher series potential is better.
- Higher automation fit is better.

### 14.3 Minimum viability gates
A candidate should not be selected as the final winner if any of the following is true:
- demand score is below **50**
- production speed score is below **50**
- automation fit score is below **40**
- final weighted score is below **65**

If no candidate passes the minimum viability gates, the system should return a structured failure state instead of forcing a weak selection.

### 14.4 Tie-breaking priority
If two or more candidates have very similar final scores, the tie should be resolved in this order:
1. higher production speed
2. lower competition / saturation
3. higher series potential
4. higher automation fit

### 14.5 Evaluation output requirement
The evaluation stage should output, for each candidate:
- raw scores by dimension
- weighted final score
- short explanation for each major score
- main risks
- final recommendation status: `selected`, `backup`, or `rejected`

---

## 15. ProductType Architecture

The system must not treat all digital products as one universal type.

A `ProductType` layer is required.

### Initial priority ProductTypes
- `WORKSHEET_BUNDLE`
- `TEMPLATE_BUNDLE`
- `PDF_TOOLKIT`
- `PROMPT_TEMPLATE_HYBRID`

### Lower-priority or later ProductTypes
- `CHECKLIST_PACK`
- `MIXED_PROFESSIONAL_BUNDLE`
- `NOTION_WORKSPACE`

### Not a first-MVP priority
- local mini-tools,
- installable utilities,
- browser extensions.

Each `ProductType` should later define:
- required outputs,
- optional outputs,
- QA rules,
- listing rules,
- preview rules,
- packaging rules.

Prompt-only products should not be the default first product type. Prompts are better used as a bonus component or as part of a hybrid offer.

### 15.1 Required outputs by initial ProductType

#### `WORKSHEET_BUNDLE`
Required outputs:
- main worksheet PDF
- editable worksheet source file
- instruction file
- product summary
- buyer-facing "How to use"
- included files list
- Etsy listing draft
- preview content plan

Optional outputs:
- prompt companion file
- sample completed worksheet
- quick-start page

#### `TEMPLATE_BUNDLE`
Required outputs:
- main template file or template set
- example-filled version
- instruction file
- product summary
- buyer-facing "How to use"
- included files list
- Etsy listing draft
- preview content plan

Optional outputs:
- prompt companion file
- quick tips sheet
- alternate template variation

#### `PDF_TOOLKIT`
Required outputs:
- main PDF guide/toolkit
- supporting worksheet or checklist
- instruction / quick-start file
- product summary
- buyer-facing "How to use"
- included files list
- Etsy listing draft
- preview content plan

Optional outputs:
- bonus template
- prompt companion file
- summary cheat sheet

#### `PROMPT_TEMPLATE_HYBRID`
Required outputs:
- prompt library
- main template or worksheet file
- instruction file
- usage examples
- product summary
- buyer-facing "How to use"
- included files list
- Etsy listing draft
- preview content plan

Optional outputs:
- quick-start guide
- bonus checklist
- example outputs

### 15.2 ProductType selection principle
The selected `ProductType` should match:
- the selected problem,
- the expected buyer workflow,
- the easiest-to-understand packaging model,
- and the fastest viable route to an Etsy-ready output.

The system should prefer simpler, clearer ProductTypes when two options are similarly strong.

### 15.3 Template-first generation principle
The system should prefer reusable structural templates over generating every product component from scratch.

Examples include:
- worksheet page templates,
- instruction file templates,
- listing structure templates,
- preview plan templates,
- bundle manifest templates.

LLM usage should focus on topic-specific content, not rebuilding stable structure repeatedly.

---

## 16. Product Output Requirements

A finished product is not just “content”.

### 16.1 Completion rule
For MVP purposes, a product is considered complete only when the final package includes all required buyer-facing materials.

### 16.2 Standard output folder structure for MVP
Each product run should produce one structured output directory.

Recommended structure:

```text
/run_{run_id}/
  /input/
    topic.txt
    thematic_context.md
    resolved_context.json

  /research/
    evidence.json
    candidate_ideas.json
    market_notes.md

  /evaluation/
    candidate_scores.json
    winner_selection.json
    evaluation_summary.md

  /product/
    /assets/
    /source/
    product_summary.md
    how_to_use.md
    included_files.md
    key_benefits.md

  /listing/
    etsy_title.txt
    etsy_description.md
    etsy_tags.txt
    listing_summary.md

  /preview/
    preview_plan.md
    preview_copy.md
    preview_assets_manifest.json

  /package/
    final_manifest.json
    delivery_notes.md
    final_bundle.zip
```

### 16.3 Folder purpose
- `input/` stores the original run inputs and resolved working context.
- `research/` stores collected evidence and candidate opportunity generation outputs.
- `evaluation/` stores scores, ranking outputs, and final opportunity selection reasoning.
- `product/` stores the actual buyer-facing product assets and supporting files.
- `listing/` stores Etsy listing content.
- `preview/` stores preview planning materials and preview-related text assets.
- `package/` stores final delivery packaging outputs and manifests.

### 16.4 Output folder rules
- Every run must have its own isolated output folder.
- File names should be deterministic and human-readable.
- The final package should be reconstructable from the run folder contents.
- Technical QA should validate required folders and files before a run is considered complete.
- Additional ProductType-specific files may be added, but the top-level folder structure should remain stable.

### 16.5 Required deliverables
- core product assets,
- instructions,
- product summary,
- buyer-facing usage guidance,
- included files list,
- key benefits,
- Etsy listing draft,
- preview plan,
- structured final package.

The exact files may differ by `ProductType`, but the delivery standard must remain consistent.

### 16.6 Structured-output-first principle
Intermediate workflow outputs should be structured and machine-readable by default.

Preferred formats include:
- JSON for scoring, manifests, routing, and structured decisions
- plain text for short fields like titles or tags
- Markdown only where human-readable review is useful

Freeform long-form generation should be reserved mainly for buyer-facing content and final review artifacts.

---

## 17. QA Model

QA must be split into two layers.

### 17.1 AI QA
AI QA evaluates:
- clarity,
- logic,
- usefulness,
- consistency,
- audience fit,
- language quality,
- copyright / obvious risk issues.

### 17.2 Technical QA
Technical QA is code-driven and should verify:
- required files exist,
- output structure is correct,
- exported files are valid,
- package completeness,
- file naming validity,
- size or format constraints,
- preview/export success where applicable.

Do not spend LLM cost on checks that are purely technical and deterministic.

### 17.3 Minimal QA pass criteria
A run should be considered QA-passing only if all of the following are true:
- the selected product clearly addresses one defined buyer problem,
- the product contents are internally consistent,
- the buyer-facing instructions are understandable,
- the included files list matches the actual packaged files,
- the Etsy listing draft accurately represents the product,
- no required deliverable is missing,
- final package generation succeeds.

### 17.4 AI QA checklist
AI QA should explicitly check:
- clarity of the product promise,
- usefulness of the product for the stated audience,
- consistency between title, summary, instructions, and listing copy,
- absence of major contradictions or confusing structure,
- whether the product feels complete enough to be reviewed for publishing.

### 17.5 Technical QA checklist
Technical QA should explicitly check:
- all required files exist,
- all required folders exist,
- referenced files are present in the package,
- manifest and included files list are aligned,
- expected export files are non-empty,
- final bundle creation succeeds,
- output paths are valid and deterministic.

### 17.6 Preview gating rule
Preview generation should happen only after the product has passed its minimum QA threshold.

The system should avoid spending additional generation cost on preview assets for products that are likely to be discarded or heavily reworked.

---

## 18. Refinement Rules

Refinement must be limited and controlled.

### Rules
- Maximum refinement cycles in MVP: **2**
- Refinement is triggered only for meaningful problems
- Minor improvements should not cause another iteration
- “Good enough to publish” is acceptable
- The system must avoid perfection loops

This is essential for cost control and execution speed.

---

## 19. Context Model

The project should use two context layers:

### 19.1 Global project context
A stable project-level context file containing:
- architecture principles,
- business direction,
- system rules,
- major decisions.

### 19.2 Active thematic context
A topic-specific context file used for the current run.

The thematic context file should be structured in a way that helps the system stay aligned within one topic area.

### Context delivery principle
Do not pass the full project context to every AI role by default.

Use a **Context Manager** to provide only relevant context slices to each role.

Examples:
- Research Agent receives business goals, topic, market constraints
- Product Creator receives selected problem, product specification, output rules
- Listing Agent receives buyer-facing positioning, included items, benefits, and tone guidance

This reduces noise, token waste, and drift.

### 19.3 Context minimization rule
Each workflow stage should receive only the smallest context package needed to complete its task reliably.

The system should avoid passing:
- full research history when only the selected candidate is needed,
- full project specification when a compact rules summary is enough,
- large prior outputs that do not affect the current stage.

Smaller context payloads should be preferred for both cost and reliability reasons.

---

## 20. Storage Model

The system should use:
- **files/folders** for real generated artifacts,
- **SQLite** for structured decisions, metadata, and performance data.

### Files should store:
- product artifacts,
- instructions,
- listing drafts,
- preview plans,
- packaging outputs.

### SQLite should store:
- runs,
- research candidates,
- scores,
- selected opportunities,
- selected product types,
- artifact metadata,
- listing metadata,
- performance data.

Do not store all long-form artifact content in SQLite by default.

### 20.1 Initial SQLite schema for MVP
The MVP should start with a simple relational schema that supports run tracking, candidate evaluation, artifact registration, listing storage, and performance feedback.

#### `runs`
Purpose:
- one row per end-to-end generation run

Suggested fields:
- `id`
- `created_at`
- `topic`
- `thematic_context_path`
- `status`
- `selected_candidate_id`
- `selected_product_type`
- `output_path`
- `total_cost`
- `notes`

#### `research_candidates`
Purpose:
- stores generated candidate opportunities discovered during research

Suggested fields:
- `id`
- `run_id`
- `title`
- `problem_statement`
- `target_audience`
- `product_angle`
- `evidence_summary`
- `estimated_price_range`
- `estimated_build_speed`
- `series_potential_note`
- `created_at`

#### `candidate_scores`
Purpose:
- stores structured scoring results per candidate

Suggested fields:
- `id`
- `run_id`
- `candidate_id`
- `demand_score`
- `competition_score`
- `production_speed_score`
- `price_potential_score`
- `series_potential_score`
- `automation_fit_score`
- `weighted_final_score`
- `recommendation_status`
- `risk_notes`
- `created_at`

#### `selected_products`
Purpose:
- stores the selected candidate translated into an actual product decision

Suggested fields:
- `id`
- `run_id`
- `candidate_id`
- `product_type`
- `product_title`
- `product_summary`
- `buyer_problem`
- `solution_promise`
- `packaging_strategy`
- `created_at`

#### `artifacts`
Purpose:
- registry of generated files and output artifacts

Suggested fields:
- `id`
- `run_id`
- `product_id`
- `artifact_type`
- `file_path`
- `file_format`
- `is_required`
- `generation_status`
- `created_at`

#### `listings`
Purpose:
- stores Etsy-facing listing drafts for generated products

Suggested fields:
- `id`
- `run_id`
- `product_id`
- `title`
- `description`
- `tags`
- `listing_version`
- `created_at`

#### `performance_metrics`
Purpose:
- stores market performance feedback for published or tracked products

Suggested fields:
- `id`
- `product_id`
- `listing_version`
- `captured_at`
- `views`
- `clicks`
- `favorites`
- `purchases`
- `conversion_rate`
- `price`
- `revenue`
- `profit`
- `days_live`

### 20.2 Schema rules
- All child tables should reference `run_id` where applicable.
- Product-level records should be traceable back to the original selected candidate.
- File artifacts should be traceable both by run and by selected product.
- The schema should favor clarity and easy querying over premature normalization.
- Long-form generated files should remain on disk, while SQLite stores metadata, decisions, scores, and references.

### 20.3 Recommended enums
#### `runs.status`
- `pending`
- `researching`
- `evaluating`
- `designing`
- `creating`
- `qa`
- `packaging`
- `completed`
- `failed`

#### `candidate_scores.recommendation_status`
- `selected`
- `backup`
- `rejected`

#### `artifacts.generation_status`
- `pending`
- `generated`
- `failed`

### 20.4 Caching and reuse rules
The system should cache and reuse intermediate results whenever safe to do so.

Examples include:
- prior research evidence for the same niche,
- previously generated structured candidate lists,
- stable template assets,
- listing scaffolds,
- product-independent instruction components.

The system should not rerun an earlier stage if its inputs and required outputs have not meaningfully changed.

### 20.5 Regeneration control rule
Changes in later stages should not force full regeneration of earlier stages unless dependencies are actually invalidated.

Examples:
- changing listing copy should not trigger fresh research,
- changing preview copy should not trigger full product regeneration,
- fixing one artifact should not require rebuilding all unrelated artifacts.

---

## 21. Performance Feedback Model

The system should accumulate performance data so future decisions can improve.

### Minimum performance data to track
- views,
- clicks,
- favorites,
- purchases,
- conversion rate,
- publish date,
- theme,
- format,
- selected problem,
- listing version.

### Strongly recommended additional performance data
- price,
- production cost,
- production time,
- revenue,
- profit,
- CTR,
- favorite rate,
- days live.

This data should support comparisons such as:
- which themes perform best,
- which product types convert best,
- which selected problems lead to stronger results,
- which listing variants perform best,
- which products generate the best return relative to production cost.

### 21.1 Optimization target
The system should optimize for **cost per publishable product**, not merely low cost per individual run.

A slightly more expensive run may be acceptable if it produces a substantially higher rate of publishable outputs.

---

## 22. Budget Control

The system must be budget-aware.

It should track AI/API cost by generation stage and enforce limits.

### Budget control examples
- max cost per product,
- max research cost,
- max refinement cycles,
- max preview/image generations.

If configured limits are exceeded, the system should stop or degrade gracefully rather than continue uncontrolled generation.

This is especially important for portfolio-style automated production.

### 22.1 Initial budget defaults for MVP
Recommended starting limits:
- max total cost per run: **$10**
- max research cost per run: **$4**
- max product creation cost per run: **$4**
- max listing + preview cost per run: **$2**
- max refinement cycles: **2**
- max preview generation attempts: **3**

These defaults can be adjusted later, but the MVP should launch with explicit budget constraints.

### 22.2 Budget behavior rules
- If the research budget is exhausted before a viable candidate is found, the run should fail gracefully.
- If the creation budget is exhausted, the system should stop instead of continuing partial low-quality generation.
- Refinement should never exceed the configured cycle limit.
- Budget usage should be written to the run record for later analysis.

### 22.3 Cost efficiency principles
The system should treat cost efficiency as a core architectural rule, not just a reporting metric.

Required principles:
- prefer cheaper models for broad exploration, formatting, and low-risk transformations,
- reserve stronger or more expensive models for final selection, architecture, and difficult quality judgments,
- prefer templates over repeated from-scratch generation,
- prefer code-driven transformations over LLM calls where deterministic logic is sufficient,
- prefer reuse of cached intermediate outputs over regeneration,
- stop early when viability thresholds are not met,
- avoid generating preview assets before the product is likely to survive QA,
- minimize context size passed into each generation step.

### 22.4 Research breadth limits
The MVP should keep research intentionally narrow.

Recommended constraints:
- a small candidate set per run,
- limited research rounds,
- limited comparative depth,
- no open-ended exploration unless explicitly configured.

The goal is decision usefulness, not exhaustive market coverage.

---

## 23. Product Prioritization Logic

The system should prefer products that are:
- faster to build,
- easier to package,
- easier to explain,
- suitable for Etsy,
- likely to produce meaningful market signals,
- reusable as a pattern for future products.

The initial priority is not technical novelty.  
The initial priority is practical speed-to-market and repeatability.

---

## 24. Definition of Success for MVP

The MVP is successful if it can reliably do the following:

1. Accept a high-level topic and active thematic context
2. Find and evaluate multiple concrete problem opportunities
3. Choose one strong product direction
4. Select a suitable initial ProductType
5. Generate one publication-ready product draft
6. Produce Etsy title and description
7. Produce buyer-facing usage and packaging materials
8. Produce a structured final folder
9. Store structured metadata and decisions
10. Leave only the final review step to the human

---

## 25. Failure Conditions

The system should explicitly detect or stop when:
- no candidate opportunity reaches minimum viability,
- budget limits are exceeded,
- required output artifacts cannot be generated,
- QA fails after the maximum number of refinement cycles,
- packaging requirements cannot be satisfied.

Failure states should be recorded clearly rather than hidden.

### 25.1 Cost-related kill rules
The system should stop early rather than continue spending on weak runs.

Examples:
- no candidate passes minimum viability gates,
- research budget is exhausted before a viable direction is found,
- required product assets cannot be generated within remaining budget,
- QA failure implies major rework beyond allowed refinement limits,
- preview or listing generation is the only remaining step but the core product is still not publishable.

---

## 26. Future Expansion Directions

Possible later expansions include:
- more ProductTypes,
- richer Etsy analytics ingestion,
- automated listing optimization,
- portfolio comparison dashboards,
- support for mini-tools,
- support for additional marketplaces,
- more advanced preview generation,
- broader provider/model switching.

These are future opportunities, not MVP requirements.

---

## 27. High-Level Implementation Principle

The project should be built as:

> A lean AI Product Factory where AI handles reasoning-heavy work and Python handles deterministic workflow execution.

This is the central implementation principle and should override any tendency to over-agentize the system.

---

## 28. Final Summary

AI Product Factory is not an idea generator.

It is a lean system that should move from:
- topic,
- thematic context,
- structured research,
- opportunity scoring,
- product design,
- product creation,
- QA,
- packaging,
- listing preparation,

to:

> one clear, useful, reviewable, Etsy-ready digital product package.

The first version should focus on reliability, simplicity, cost control, and repeatable end-to-end execution.

If the system can reliably create one strong publishable product from one topic, the foundation is successful.
