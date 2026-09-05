from pathlib import Path
import sqlite3


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS runs (
    id TEXT PRIMARY KEY,
    topic TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    output_path TEXT NOT NULL,
    total_cost REAL DEFAULT 0,
    selected_product_type TEXT
);

CREATE TABLE IF NOT EXISTS research_candidates (
    id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    title TEXT NOT NULL,
    problem_statement TEXT NOT NULL,
    target_audience TEXT NOT NULL,
    product_angle TEXT NOT NULL,
    evidence_summary TEXT,
    estimated_price_range TEXT,
    estimated_build_speed TEXT,
    series_potential_note TEXT,
    FOREIGN KEY (run_id) REFERENCES runs(id)
);

CREATE TABLE IF NOT EXISTS candidate_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    candidate_id TEXT NOT NULL,
    demand_score REAL NOT NULL,
    competition_score REAL NOT NULL,
    production_speed_score REAL NOT NULL,
    price_potential_score REAL NOT NULL,
    series_potential_score REAL NOT NULL,
    automation_fit_score REAL NOT NULL,
    weighted_final_score REAL NOT NULL,
    recommendation_status TEXT NOT NULL,
    risk_notes TEXT,
    FOREIGN KEY (run_id) REFERENCES runs(id),
    FOREIGN KEY (candidate_id) REFERENCES research_candidates(id)
);

CREATE TABLE IF NOT EXISTS selected_products (
    run_id TEXT PRIMARY KEY,
    candidate_id TEXT NOT NULL,
    product_type TEXT NOT NULL,
    product_title TEXT NOT NULL,
    product_summary TEXT NOT NULL,
    buyer_problem TEXT NOT NULL,
    solution_promise TEXT NOT NULL,
    packaging_strategy TEXT NOT NULL,
    FOREIGN KEY (run_id) REFERENCES runs(id),
    FOREIGN KEY (candidate_id) REFERENCES research_candidates(id)
);

CREATE TABLE IF NOT EXISTS artifacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    artifact_type TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_format TEXT NOT NULL,
    is_required INTEGER NOT NULL,
    generation_status TEXT NOT NULL,
    FOREIGN KEY (run_id) REFERENCES runs(id)
);

CREATE TABLE IF NOT EXISTS listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    tags_json TEXT NOT NULL,
    listing_version INTEGER NOT NULL,
    FOREIGN KEY (run_id) REFERENCES runs(id)
);
"""


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def get_connection(db_path: Path) -> sqlite3.Connection:
    ensure_parent_dir(db_path)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(db_path: Path) -> None:
    with get_connection(db_path) as connection:
        connection.executescript(SCHEMA_SQL)
        connection.commit()
