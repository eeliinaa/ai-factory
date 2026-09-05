from dataclasses import dataclass


@dataclass
class RefinementDecision:
    should_continue: bool
    stop_reason: str


@dataclass
class RefinementTarget:
    artifact_name: str
    reason: str


def extract_refinement_targets(findings: list[str]) -> list[RefinementTarget]:
    targets: list[RefinementTarget] = []
    for finding in findings:
        if "Missing artifact" in finding:
            artifact_name = finding.split(":", 1)[-1].strip()
            targets.append(RefinementTarget(artifact_name=artifact_name, reason="missing_artifact"))
        elif "Empty artifact" in finding:
            artifact_name = finding.split(":", 1)[-1].strip()
            targets.append(RefinementTarget(artifact_name=artifact_name, reason="empty_artifact"))
    return targets


def should_continue_refinement(previous_findings: list[str], current_findings: list[str], cycle: int, max_cycles: int) -> RefinementDecision:
    if not current_findings:
        return RefinementDecision(should_continue=False, stop_reason="qa_passed")
    if cycle >= max_cycles:
        return RefinementDecision(should_continue=False, stop_reason="max_refinement_cycles_reached")
    if previous_findings and previous_findings == current_findings:
        return RefinementDecision(should_continue=False, stop_reason="no_progress")
    return RefinementDecision(should_continue=True, stop_reason="continue")
