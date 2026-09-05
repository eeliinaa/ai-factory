import json

from ..core import LLMResponse, ProviderRequest


class OpenAIProvider:
    def complete(self, request: ProviderRequest) -> LLMResponse:
        if request.stage_name == "research":
            content = json.dumps(
                {
                    "evidence_summary": "Buyers want compact, editable planning systems that reduce wedding-planning overwhelm.",
                    "candidates": [
                        {
                            "id": "candidate-1",
                            "title": "Editable Wedding Planner Bundle",
                            "product_type": "TEMPLATE_BUNDLE",
                            "target_customer": "Engaged couples planning their own wedding",
                            "problem_statement": "Couples need a clear timeline, checklist, and vendor tracker in one place.",
                            "solution_summary": "Provide an editable wedding-planning bundle with printable and spreadsheet-based assets.",
                            "why_now": "Digital wedding planning tools remain in demand due to convenience and instant download expectations.",
                            "price_anchor": "$9-$19",
                            "differentiation": "Simple but structured planner with editable spreadsheet support.",
                            "research_notes": ["Checklist bundles perform well", "Editable planners increase perceived value"],
                        },
                        {
                            "id": "candidate-2",
                            "title": "Wedding Emergency Kit Checklist",
                            "product_type": "TEMPLATE_BUNDLE",
                            "target_customer": "Couples and planners needing day-of readiness",
                            "problem_statement": "Buyers want to avoid last-minute wedding-day problems.",
                            "solution_summary": "Provide a printable emergency checklist and vendor contact pack.",
                            "why_now": "Day-of organization tools stay relevant year-round.",
                            "price_anchor": "$6-$12",
                            "differentiation": "Focused urgency-driven checklist bundle.",
                            "research_notes": ["Low complexity", "Good add-on bundle potential"],
                        },
                    ],
                }
            )
        elif request.stage_name == "evaluation":
            content = json.dumps(
                {
                    "selected_candidate_id": "candidate-1",
                    "backup_candidate_ids": ["candidate-2"],
                    "rejected_candidate_ids": [],
                    "scores": [
                        {
                            "candidate_id": "candidate-1",
                            "demand_score": 8.0,
                            "competition_score": 6.5,
                            "production_speed_score": 8.0,
                            "price_potential_score": 7.0,
                            "series_potential_score": 8.0,
                            "automation_fit_score": 8.0,
                            "weighted_final_score": 7.6,
                            "recommendation_status": "selected",
                            "risk_notes": "Balanced complexity and value for a first bundle.",
                        },
                        {
                            "candidate_id": "candidate-2",
                            "demand_score": 7.0,
                            "competition_score": 6.0,
                            "production_speed_score": 8.0,
                            "price_potential_score": 6.5,
                            "series_potential_score": 7.0,
                            "automation_fit_score": 7.0,
                            "weighted_final_score": 6.9,
                            "recommendation_status": "backup",
                            "risk_notes": "Simpler product but slightly lower perceived value.",
                        },
                    ],
                    "failure_reason": None,
                }
            )
        elif request.stage_name == "product_architecture":
            content = json.dumps(
                {
                    "product_type": "TEMPLATE_BUNDLE",
                    "product_title": "Editable Wedding Planner Bundle",
                    "product_summary": "A printable and editable wedding planning kit with timeline, checklist, and vendor tracker.",
                    "buyer_problem": "Couples need one planning system that is easy to customize and print.",
                    "solution_promise": "Deliver a compact bundle with clear planning pages plus spreadsheet support.",
                    "packaging_strategy": "Bundle printable PDFs, an editable spreadsheet, and buyer instructions in a ZIP.",
                    "artifact_plan": [
                        {
                            "artifact_type": "planner_pdf",
                            "file_name": "wedding-planner.pdf",
                            "file_format": "pdf",
                            "purpose": "Main printable planner.",
                            "is_required": True,
                            "generation_instructions": "Create a printable wedding planning PDF with timeline and checklist sections.",
                        },
                        {
                            "artifact_type": "vendor_sheet",
                            "file_name": "vendor-tracker.xlsx",
                            "file_format": "xlsx",
                            "purpose": "Editable vendor tracking spreadsheet.",
                            "is_required": True,
                            "generation_instructions": "Create a workbook with vendor, contact, budget, and due-date tracking.",
                        },
                        {
                            "artifact_type": "buyer_guide",
                            "file_name": "how_to_use.md",
                            "file_format": "md",
                            "purpose": "Buyer instructions.",
                            "is_required": True,
                            "generation_instructions": "Write a short buyer guide explaining the files and usage.",
                        },
                        {
                            "artifact_type": "final_bundle_zip",
                            "file_name": "editable-wedding-planner-bundle.zip",
                            "file_format": "zip",
                            "purpose": "Final delivery bundle.",
                            "is_required": True,
                            "generation_instructions": "Package all deliverables into a ZIP.",
                        },
                    ],
                }
            )
        elif request.stage_name == "product_creation":
            content = json.dumps(
                {
                    "created_artifacts": [
                        {
                            "artifact_type": "planner_pdf",
                            "file_name": "wedding-planner.pdf",
                            "render_spec": {
                                "kind": "pdf",
                                "title": "Editable Wedding Planner",
                                "page_size": "letter",
                                "sections": [
                                    {
                                        "heading": "Timeline Overview",
                                        "body": "Use this section to map major planning milestones across the engagement period.",
                                        "bullet_points": [
                                            "Set wedding date and venue shortlist",
                                            "Confirm budget priorities",
                                            "Book core vendors"
                                        ]
                                    },
                                    {
                                        "heading": "Weekly Checklist",
                                        "body": "Review progress weekly and check off completed planning tasks.",
                                        "bullet_points": [
                                            "Guest list updates",
                                            "Vendor confirmations",
                                            "Payment due dates"
                                        ]
                                    }
                                ]
                            }
                        },
                        {
                            "artifact_type": "vendor_sheet",
                            "file_name": "vendor-tracker.xlsx",
                            "render_spec": {
                                "kind": "spreadsheet",
                                "workbook_title": "Vendor Tracker",
                                "sheets": [
                                    {
                                        "name": "Vendors",
                                        "columns": [
                                            {"header": "Vendor", "width": 24},
                                            {"header": "Category", "width": 18},
                                            {"header": "Contact", "width": 28},
                                            {"header": "Budget", "width": 14},
                                            {"header": "Due Date", "width": 16}
                                        ],
                                        "rows": [
                                            ["Photographer", "Photo", "hello@example.com", "$1800", "2026-11-01"],
                                            ["Florist", "Flowers", "florals@example.com", "$900", "2026-10-15"]
                                        ]
                                    }
                                ]
                            }
                        },
                        {
                            "artifact_type": "buyer_guide",
                            "file_name": "how_to_use.md",
                            "render_spec": {
                                "kind": "text",
                                "content": "# How to Use\n\n1. Print the planner PDF or fill it in digitally.\n2. Update the vendor spreadsheet with real contacts and payment dates.\n3. Keep the ZIP together so all planning files stay in one place.\n"
                            }
                        },
                        {
                            "artifact_type": "final_bundle_zip",
                            "file_name": "editable-wedding-planner-bundle.zip",
                            "render_spec": {
                                "kind": "bundle",
                                "notes": "Packaging step will assemble the final ZIP from rendered artifacts."
                            }
                        }
                    ]
                }
            )
        else:
            content = (
                f"[Placeholder AI response] Stage={request.stage_name}; "
                f"Model={request.model}; no OPENAI_API_KEY configured."
            )

        return LLMResponse(
            model=request.model,
            content=content,
            metadata={
                "provider": "openai",
                "mode": "placeholder",
                "stage_name": request.stage_name,
                "prompt_version": request.prompt_version,
                "cost_estimation": "none",
                "require_json": request.require_json,
            },
        )