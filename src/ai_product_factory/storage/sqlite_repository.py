import json
from pathlib import Path

from ..db import get_connection
from ..domain import ArtifactRecord, CandidateScore, ListingDraft, RunContext, SelectedProduct, ResearchCandidate


def _candidate_db_id(run_id: str, candidate_id: str) -> str:
    return f"{run_id}:{candidate_id}"


class SQLiteRepository:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    def save_run(self, run_context: RunContext) -> None:
        run = run_context.run
        with get_connection(self.db_path) as connection:
            connection.execute(
                """
                INSERT INTO runs (id, topic, status, created_at, output_path, total_cost, selected_product_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run.id,
                    run.topic,
                    run.status.value,
                    run.created_at.isoformat(),
                    str(run.output_path),
                    run.total_cost,
                    run.selected_product_type.value if run.selected_product_type else None,
                ),
            )
            connection.commit()

    def save_candidates(self, run_id: str, candidates: list[ResearchCandidate]) -> None:
        if not candidates:
            return

        with get_connection(self.db_path) as connection:
            connection.executemany(
                """
                INSERT INTO research_candidates (
                    id, run_id, title, problem_statement, target_audience, product_angle,
                    evidence_summary, estimated_price_range, estimated_build_speed, series_potential_note
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        _candidate_db_id(run_id, candidate.id),
                        run_id,
                        candidate.title,
                        candidate.problem_statement,
                        candidate.target_audience,
                        candidate.product_angle,
                        candidate.evidence_summary,
                        candidate.estimated_price_range,
                        candidate.estimated_build_speed,
                        candidate.series_potential_note,
                    )
                    for candidate in candidates
                ],
            )
            connection.commit()

    def save_scores(self, run_id: str, scores: list[CandidateScore]) -> None:
        if not scores:
            return

        with get_connection(self.db_path) as connection:
            connection.executemany(
                """
                INSERT INTO candidate_scores (
                    run_id, candidate_id, demand_score, competition_score, production_speed_score,
                    price_potential_score, series_potential_score, automation_fit_score,
                    weighted_final_score, recommendation_status, risk_notes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        run_id,
                        _candidate_db_id(run_id, score.candidate_id),
                        score.demand_score,
                        score.competition_score,
                        score.production_speed_score,
                        score.price_potential_score,
                        score.series_potential_score,
                        score.automation_fit_score,
                        score.weighted_final_score,
                        score.recommendation_status.value,
                        score.risk_notes,
                    )
                    for score in scores
                ],
            )
            connection.commit()

    def save_selected_product(self, run_id: str, product: SelectedProduct) -> None:
        with get_connection(self.db_path) as connection:
            connection.execute(
                """
                INSERT INTO selected_products (
                    run_id, candidate_id, product_type, product_title, product_summary,
                    buyer_problem, solution_promise, packaging_strategy
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run_id,
                    _candidate_db_id(run_id, product.candidate_id),
                    product.product_type.value,
                    product.product_title,
                    product.product_summary,
                    product.buyer_problem,
                    product.solution_promise,
                    product.packaging_strategy,
                ),
            )
            connection.commit()

    def save_artifacts(self, run_id: str, artifacts: list[ArtifactRecord]) -> None:
        if not artifacts:
            return

        with get_connection(self.db_path) as connection:
            connection.executemany(
                """
                INSERT INTO artifacts (
                    run_id, artifact_type, file_path, file_format, is_required, generation_status
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        run_id,
                        artifact.artifact_type,
                        str(artifact.file_path),
                        artifact.file_format,
                        1 if artifact.is_required else 0,
                        artifact.generation_status.value,
                    )
                    for artifact in artifacts
                ],
            )
            connection.commit()

    def save_listing(self, run_id: str, listing: ListingDraft) -> None:
        with get_connection(self.db_path) as connection:
            connection.execute(
                """
                INSERT INTO listings (run_id, title, description, tags_json, listing_version)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    run_id,
                    listing.title,
                    listing.description,
                    json.dumps(listing.tags),
                    listing.listing_version,
                ),
            )
            connection.commit()

    def list_runs(self, limit: int = 10, status: str | None = None, topic_contains: str | None = None) -> list[dict]:
        query = "SELECT id, topic, status, created_at, output_path, total_cost, selected_product_type FROM runs"
        conditions: list[str] = []
        params: list[object] = []

        if status:
            conditions.append("status = ?")
            params.append(status)
        if topic_contains:
            conditions.append("topic LIKE ?")
            params.append(f"%{topic_contains}%")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        with get_connection(self.db_path) as connection:
            rows = connection.execute(query, params).fetchall()
        return [dict(row) for row in rows]

    def get_run_details(self, run_id: str) -> dict | None:
        with get_connection(self.db_path) as connection:
            run_row = connection.execute(
                "SELECT id, topic, status, created_at, output_path, total_cost, selected_product_type FROM runs WHERE id = ?",
                (run_id,),
            ).fetchone()
            if run_row is None:
                return None

            selected_product = connection.execute(
                "SELECT candidate_id, product_type, product_title, product_summary, buyer_problem, solution_promise, packaging_strategy FROM selected_products WHERE run_id = ?",
                (run_id,),
            ).fetchone()
            listing = connection.execute(
                "SELECT title, description, tags_json, listing_version FROM listings WHERE run_id = ? ORDER BY id DESC LIMIT 1",
                (run_id,),
            ).fetchone()
            artifacts = connection.execute(
                "SELECT artifact_type, file_path, file_format, is_required, generation_status FROM artifacts WHERE run_id = ? ORDER BY id ASC",
                (run_id,),
            ).fetchall()

        details = dict(run_row)
        details["selected_product"] = dict(selected_product) if selected_product else None
        details["listing"] = dict(listing) if listing else None
        details["artifacts"] = [dict(row) for row in artifacts]
        return details

    def compare_runs(self, run_ids: list[str]) -> list[dict]:
        if not run_ids:
            return []
        placeholders = ", ".join("?" for _ in run_ids)
        query = f"""
            SELECT
                r.id,
                r.topic,
                r.status,
                r.created_at,
                r.total_cost,
                sp.product_title,
                sp.product_type,
                cs.weighted_final_score AS selected_score,
                COUNT(a.id) AS artifact_count
            FROM runs r
            LEFT JOIN selected_products sp ON sp.run_id = r.id
            LEFT JOIN candidate_scores cs ON cs.run_id = r.id AND cs.candidate_id = sp.candidate_id
            LEFT JOIN artifacts a ON a.run_id = r.id
            WHERE r.id IN ({placeholders})
            GROUP BY r.id, r.topic, r.status, r.created_at, r.total_cost, sp.product_title, sp.product_type, cs.weighted_final_score
            ORDER BY r.created_at DESC
        """
        with get_connection(self.db_path) as connection:
            rows = connection.execute(query, run_ids).fetchall()
        return [dict(row) for row in rows]

    def list_best_runs(self, limit: int = 10, sort_by: str = "newest") -> list[dict]:
        order_clause = {
            "score": "selected_score DESC, r.total_cost ASC, r.created_at DESC",
            "cost": "r.total_cost ASC, selected_score DESC, r.created_at DESC",
            "newest": "r.created_at DESC",
        }[sort_by]
        query = f"""
            SELECT
                r.id,
                r.topic,
                r.status,
                r.created_at,
                r.total_cost,
                sp.product_title,
                sp.product_type,
                cs.weighted_final_score AS selected_score
            FROM runs r
            LEFT JOIN selected_products sp ON sp.run_id = r.id
            LEFT JOIN candidate_scores cs ON cs.run_id = r.id AND cs.candidate_id = sp.candidate_id
            WHERE r.status = 'completed'
            ORDER BY {order_clause}
            LIMIT ?
        """
        with get_connection(self.db_path) as connection:
            rows = connection.execute(query, (limit,)).fetchall()
        return [dict(row) for row in rows]