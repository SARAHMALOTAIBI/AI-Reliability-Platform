from dataclasses import dataclass


@dataclass(frozen=True)
class Recommendation:
    priority: int
    action: str
    expected_impact: str
    difficulty: str
    affected_component: str
    supporting_evidence: str


_RECOMMENDATION_CATALOG = {
    "RETRIEVAL_FAILURE": [
        {
            "priority": 1,
            "action": (
                "Review retrieval configuration and "
                "improve retrieved chunk relevance."
            ),
            "expected_impact": "HIGH",
            "difficulty": "MEDIUM",
            "affected_component": "RETRIEVER",
        },
        {
            "priority": 2,
            "action": (
                "Add or improve a reranking stage "
                "before sending context to the model."
            ),
            "expected_impact": "HIGH",
            "difficulty": "MEDIUM",
            "affected_component": "RETRIEVER",
        },
        {
            "priority": 3,
            "action": (
                "Tune Top-K, chunk size, and chunk "
                "overlap using evaluation results."
            ),
            "expected_impact": "MEDIUM",
            "difficulty": "LOW",
            "affected_component": "RETRIEVER",
        },
    ],

    "GENERATION_FAILURE": [
        {
            "priority": 1,
            "action": (
                "Strengthen grounding instructions "
                "so the model answers only from "
                "retrieved evidence."
            ),
            "expected_impact": "HIGH",
            "difficulty": "LOW",
            "affected_component": "GENERATION",
        },
        {
            "priority": 2,
            "action": (
                "Require citations or explicit "
                "supporting evidence in generated "
                "answers."
            ),
            "expected_impact": "HIGH",
            "difficulty": "MEDIUM",
            "affected_component": "GENERATION",
        },
        {
            "priority": 3,
            "action": (
                "Add an abstention policy when "
                "available context does not support "
                "the answer."
            ),
            "expected_impact": "MEDIUM",
            "difficulty": "MEDIUM",
            "affected_component": "GENERATION",
        },
    ],

    "KNOWLEDGE_BASE_FAILURE": [
        {
            "priority": 1,
            "action": (
                "Add the missing information or "
                "documents to the knowledge base."
            ),
            "expected_impact": "HIGH",
            "difficulty": "MEDIUM",
            "affected_component": "KNOWLEDGE_BASE",
        },
        {
            "priority": 2,
            "action": (
                "Review document freshness and "
                "replace outdated knowledge."
            ),
            "expected_impact": "HIGH",
            "difficulty": "MEDIUM",
            "affected_component": "KNOWLEDGE_BASE",
        },
        {
            "priority": 3,
            "action": (
                "Re-index the knowledge base and "
                "verify document metadata."
            ),
            "expected_impact": "MEDIUM",
            "difficulty": "LOW",
            "affected_component": "KNOWLEDGE_BASE",
        },
    ],

    "PROMPT_FAILURE": [
        {
            "priority": 1,
            "action": (
                "Clarify the task and strengthen "
                "the prompt instructions."
            ),
            "expected_impact": "HIGH",
            "difficulty": "LOW",
            "affected_component": "PROMPT",
        },
        {
            "priority": 2,
            "action": (
                "Remove conflicting instructions "
                "and explicitly define the expected "
                "response format."
            ),
            "expected_impact": "HIGH",
            "difficulty": "LOW",
            "affected_component": "PROMPT",
        },
        {
            "priority": 3,
            "action": (
                "Add representative examples to "
                "improve response alignment."
            ),
            "expected_impact": "MEDIUM",
            "difficulty": "LOW",
            "affected_component": "PROMPT",
        },
    ],
}


def generate_recommendations(
    diagnosis: dict | None,
) -> list[Recommendation]:
    if not diagnosis:
        return []

    category = diagnosis.get("category")

    templates = _RECOMMENDATION_CATALOG.get(
        category,
        [],
    )

    evidence = diagnosis.get(
        "explanation",
        "Recommendation generated from root-cause diagnosis.",
    )

    recommendations = [
        Recommendation(
            priority=item["priority"],
            action=item["action"],
            expected_impact=item[
                "expected_impact"
            ],
            difficulty=item["difficulty"],
            affected_component=item[
                "affected_component"
            ],
            supporting_evidence=evidence,
        )
        for item in templates
    ]

    return sorted(
        recommendations,
        key=lambda item: item.priority,
    )
