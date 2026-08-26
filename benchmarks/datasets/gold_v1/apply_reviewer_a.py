"""
Apply Reviewer A (Sara) annotations to samples_all.json:
1. Map candidate_id -> real sample_id via internal_id_mapping.json.
2. Add a ReviewerAnnotation (reviewer_id='sara_reviewer') to each sample.
3. Compute agreement between Reviewer A's judgment and the original
   gold_label.
4. List every sample where they disagree (needs Adjudication).

Does NOT run the 70/30 split (per Mohammed's instruction).
"""
from __future__ import annotations

import json
from pathlib import Path

from reviewer_a_annotations import REVIEWER_A_JUDGMENTS

BASE_DIR = Path(__file__).parent
MAPPING_PATH = BASE_DIR / "internal_id_mapping.json"
SAMPLES_PATH = BASE_DIR / "samples_all.json"
REPORT_PATH = BASE_DIR / "reviewer_a_agreement_report.json"

REVIEWER_ID = "sara_reviewer"


def main() -> None:
    with open(MAPPING_PATH, encoding="utf-8") as f:
        mapping = json.load(f)
    with open(SAMPLES_PATH, encoding="utf-8") as f:
        samples = json.load(f)

    candidate_to_sample_id = {
        m["neutral_id"]: m["real_sample_id"] for m in mapping
    }

    sample_by_id = {s["sample_id"]: s for s in samples}

    agreements = []
    disagreements = []

    for candidate_id, reviewer_label in REVIEWER_A_JUDGMENTS.items():
        sample_id = candidate_to_sample_id[candidate_id]
        sample = sample_by_id[sample_id]

        gold_label = sample["gold_label"]

        # Add the ReviewerAnnotation.
        annotation = {
            "reviewer_id": REVIEWER_ID,
            "label": reviewer_label,
            "notes": None,
        }
        sample["reviewers"] = [annotation]

        if reviewer_label == gold_label:
            agreements.append(sample_id)
        else:
            disagreements.append(
                {
                    "sample_id": sample_id,
                    "gold_label": gold_label,
                    "reviewer_a_label": reviewer_label,
                }
            )

    with open(SAMPLES_PATH, "w", encoding="utf-8") as f:
        json.dump(samples, f, ensure_ascii=False, indent=2)

    total = len(REVIEWER_A_JUDGMENTS)
    agree_count = len(agreements)
    disagree_count = len(disagreements)
    agreement_rate = agree_count / total

    report = {
        "reviewer_id": REVIEWER_ID,
        "total_samples": total,
        "agreements": agree_count,
        "disagreements": disagree_count,
        "agreement_rate": round(agreement_rate, 4),
        "disagreement_details": disagreements,
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"Reviewer A ({REVIEWER_ID}) annotations applied to {total} samples.")
    print(f"Agreement: {agree_count}/{total} ({agreement_rate:.1%})")
    print(f"Disagreements requiring Adjudication: {disagree_count}")
    if disagreements:
        print("\nDisagreement details:")
        for d in disagreements:
            print(
                f"  {d['sample_id']}: gold={d['gold_label']} "
                f"vs reviewer_a={d['reviewer_a_label']}"
            )
    print(f"\nSaved updated samples to {SAMPLES_PATH}")
    print(f"Saved agreement report to {REPORT_PATH}")


if __name__ == "__main__":
    main()
