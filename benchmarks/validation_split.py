from __future__ import annotations

import hashlib
from collections import defaultdict
from dataclasses import replace

from benchmarks.validation_schema import (
    FailureLabel,
    ValidationSample,
    ValidationSplit,
)


DEFAULT_DEVELOPMENT_FRACTION = 0.70
DEFAULT_SPLIT_SEED = 20260824


def _stable_sample_key(
    sample_id: str,
    seed: int,
) -> str:
    payload = (
        f"{seed}:{sample_id}"
    ).encode("utf-8")

    return hashlib.sha256(
        payload
    ).hexdigest()


def _validate_unique_sample_ids(
    samples: list[ValidationSample],
) -> None:
    sample_ids = [
        sample.sample_id
        for sample in samples
    ]

    if len(sample_ids) != len(
        set(sample_ids)
    ):
        raise ValueError(
            "sample_id values must be unique."
        )


def _group_key(sample: ValidationSample) -> str:
    """Group samples that must stay together on the same side of the
    split. Samples sharing a source_fact_id represent the same
    underlying fact/case and must never be separated across
    development and held-out — REGARDLESS of which gold_label they
    have (a fact can appear as HEALTHY in one sample and
    GENERATION_FAILURE in another; both must land on the same side).
    Samples without a source_fact_id fall back to their own sample_id,
    i.e. they form a single-sample group."""
    if sample.source_fact_id:
        return f"fact::{sample.source_fact_id}"
    return f"sample::{sample.sample_id}"


def split_development_and_held_out(
    samples: list[ValidationSample],
    development_fraction: float = (
        DEFAULT_DEVELOPMENT_FRACTION
    ),
    seed: int = DEFAULT_SPLIT_SEED,
) -> tuple[
    list[ValidationSample],
    list[ValidationSample],
]:
    if not samples:
        raise ValueError(
            "At least one sample is required."
        )

    if not 0.0 < development_fraction < 1.0:
        raise ValueError(
            "development_fraction must be "
            "between 0 and 1."
        )

    _validate_unique_sample_ids(samples)

    by_label: dict[
        FailureLabel,
        list[ValidationSample],
    ] = {
        label: []
        for label in FailureLabel
    }

    for sample in samples:
        by_label[
            sample.gold_label
        ].append(sample)

    missing_labels = [
        label.value
        for label, label_samples
        in by_label.items()
        if not label_samples
    ]

    if missing_labels:
        raise ValueError(
            "Every failure label must be "
            "represented before splitting. "
            "Missing: "
            + ", ".join(missing_labels)
        )

    too_small = [
        label.value
        for label, label_samples
        in by_label.items()
        if len(label_samples) < 2
    ]

    if too_small:
        raise ValueError(
            "Each failure label needs at least "
            "two samples so both splits contain "
            "that label. Too small: "
            + ", ".join(too_small)
        )

    # --- Cross-label, group-aware assignment -------------------------
    # Build groups ACROSS THE WHOLE DATASET (not per label), so that
    # samples sharing a source_fact_id are assigned to the same side
    # no matter which gold_label they carry.
    groups: dict[str, list[ValidationSample]] = defaultdict(list)
    for sample in samples:
        groups[_group_key(sample)].append(sample)

    sorted_group_keys = sorted(
        groups.keys(),
        key=lambda key: _stable_sample_key(key, seed),
    )

    total_count = len(samples)
    raw_dev_count = round(total_count * development_fraction)
    global_target_dev_count = min(
        max(raw_dev_count, 1),
        total_count - 1,
    )

    development: list[ValidationSample] = []
    held_out: list[ValidationSample] = []
    dev_count = 0

    for group_key in sorted_group_keys:
        group_samples = groups[group_key]

        if dev_count < global_target_dev_count:
            for sample in group_samples:
                development.append(
                    replace(
                        sample,
                        split=ValidationSplit.DEVELOPMENT,
                    )
                )
            dev_count += len(group_samples)
        else:
            for sample in group_samples:
                held_out.append(
                    replace(
                        sample,
                        split=ValidationSplit.HELD_OUT,
                    )
                )

    # Verify every label ended up represented on BOTH sides.
    dev_labels = {s.gold_label for s in development}
    held_labels = {s.gold_label for s in held_out}

    labels_missing_dev = [
        label.value
        for label in FailureLabel
        if label not in dev_labels
    ]
    labels_missing_held = [
        label.value
        for label in FailureLabel
        if label not in held_labels
    ]

    if labels_missing_dev or labels_missing_held:
        raise ValueError(
            "Cross-label group-aware split could not represent every "
            "label on both sides. Missing from development: "
            + ", ".join(labels_missing_dev or ["(none)"])
            + " | Missing from held-out: "
            + ", ".join(labels_missing_held or ["(none)"])
            + ". This usually means source_fact_id groups are too "
            "coarse (e.g. too many samples sharing one group id) — "
            "consider more granular grouping."
        )

    development.sort(
        key=lambda sample: sample.sample_id
    )

    held_out.sort(
        key=lambda sample: sample.sample_id
    )

    validate_no_split_leakage(
        development,
        held_out,
    )

    return development, held_out


def validate_no_split_leakage(
    development: list[ValidationSample],
    held_out: list[ValidationSample],
) -> None:
    development_ids = {
        sample.sample_id
        for sample in development
    }

    held_out_ids = {
        sample.sample_id
        for sample in held_out
    }

    overlap = (
        development_ids
        & held_out_ids
    )

    if overlap:
        raise ValueError(
            "Development and held-out sets "
            "must not overlap. Duplicate IDs: "
            + ", ".join(sorted(overlap))
        )

    if any(
        sample.split
        != ValidationSplit.DEVELOPMENT
        for sample in development
    ):
        raise ValueError(
            "Development samples must use "
            "the development split."
        )

    if any(
        sample.split
        != ValidationSplit.HELD_OUT
        for sample in held_out
    ):
        raise ValueError(
            "Held-out samples must use "
            "the held_out split."
        )

    # Group-leakage check: no source_fact_id may appear on both sides.
    development_facts = {
        sample.source_fact_id
        for sample in development
        if sample.source_fact_id
    }

    held_out_facts = {
        sample.source_fact_id
        for sample in held_out
        if sample.source_fact_id
    }

    fact_overlap = development_facts & held_out_facts

    if fact_overlap:
        raise ValueError(
            "Development and held-out sets must not share the same "
            "source_fact_id (leakage). Overlapping facts: "
            + ", ".join(sorted(fact_overlap))
        )


def require_development_only(
    samples: list[ValidationSample],
) -> None:
    if not samples:
        raise ValueError(
            "At least one development sample "
            "is required."
        )

    invalid = [
        sample.sample_id
        for sample in samples
        if sample.split
        != ValidationSplit.DEVELOPMENT
    ]

    if invalid:
        raise ValueError(
            "Threshold tuning and rule tuning "
            "are allowed on development data "
            "only. Held-out samples detected: "
            + ", ".join(invalid)
        )


def require_held_out_only(
    samples: list[ValidationSample],
) -> None:
    if not samples:
        raise ValueError(
            "At least one held-out sample "
            "is required."
        )

    invalid = [
        sample.sample_id
        for sample in samples
        if sample.split
        != ValidationSplit.HELD_OUT
    ]

    if invalid:
        raise ValueError(
            "Final evaluation must use "
            "held-out data only. Invalid "
            "samples: "
            + ", ".join(invalid)
        )
