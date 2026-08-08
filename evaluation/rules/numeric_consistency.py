import re
from dataclasses import dataclass


NUMBER_WORDS = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "ten": "10",
    "eleven": "11",
    "twelve": "12",
    "thirteen": "13",
    "fourteen": "14",
    "fifteen": "15",
    "sixteen": "16",
    "seventeen": "17",
    "eighteen": "18",
    "nineteen": "19",
    "twenty": "20",
    "thirty": "30",
    "forty": "40",
    "fifty": "50",
    "sixty": "60",
}

SPECIAL_ARABIC_DURATIONS = {
    "أسبوعين": "2 أسبوع",
    "اسبوعين": "2 اسبوع",
    "أسبوعان": "2 أسبوع",
    "اسبوعان": "2 اسبوع",
    "يومين": "2 يوم",
    "يومان": "2 يوم",
    "شهرين": "2 شهر",
    "شهران": "2 شهر",
    "سنتين": "2 سنة",
    "سنتان": "2 سنة",
}

UNIT_TO_DAYS = {
    "day": 1,
    "days": 1,
    "يوم": 1,
    "أيام": 1,
    "ايام": 1,

    "week": 7,
    "weeks": 7,
    "أسبوع": 7,
    "اسبوع": 7,
    "أسابيع": 7,
    "اسابيع": 7,

    "month": 30,
    "months": 30,
    "شهر": 30,
    "أشهر": 30,
    "اشهر": 30,

    "year": 365,
    "years": 365,
    "سنة": 365,
    "سنوات": 365,
}

ARABIC_DIACRITICS_PATTERN = re.compile(
    r"[\u0617-\u061A\u064B-\u0652]"
)

ARABIC_DIGIT_TRANSLATION = str.maketrans(
    "٠١٢٣٤٥٦٧٨٩٫",
    "0123456789.",
)

DURATION_TOLERANCE_DAYS = 0.01


@dataclass(frozen=True)
class NumericConsistencyResult:
    contradiction: bool
    answer_values_in_days: list[float]
    evidence_values_in_days: list[float]
    unsupported_answer_values: list[float]
    explanation: str


def normalize_text(text: str) -> str:
    normalized = text.lower()
    normalized = normalized.translate(
        ARABIC_DIGIT_TRANSLATION
    )
    normalized = ARABIC_DIACRITICS_PATTERN.sub(
        "",
        normalized,
    )

    for phrase, replacement in SPECIAL_ARABIC_DURATIONS.items():
        normalized = normalized.replace(
            phrase,
            replacement,
        )

    for word, number in NUMBER_WORDS.items():
        normalized = re.sub(
            rf"\b{re.escape(word)}\b",
            number,
            normalized,
        )

    return normalized


def extract_durations_in_days(
    text: str,
) -> list[float]:
    normalized = normalize_text(text)

    unit_pattern = "|".join(
        sorted(
            (
                re.escape(unit)
                for unit in UNIT_TO_DAYS
            ),
            key=len,
            reverse=True,
        )
    )

    duration_pattern = re.compile(
        rf"(\d+(?:\.\d+)?)\s*({unit_pattern})"
    )

    durations: list[float] = []

    for value, unit in duration_pattern.findall(normalized):
        duration_in_days = (
            float(value)
            * UNIT_TO_DAYS[unit]
        )

        durations.append(duration_in_days)

    return durations


def values_match(
    first_value: float,
    second_value: float,
) -> bool:
    return (
        abs(first_value - second_value)
        <= DURATION_TOLERANCE_DAYS
    )


def check_duration_consistency(
    answer: str,
    evidence: str,
) -> NumericConsistencyResult:
    answer_values = extract_durations_in_days(answer)
    evidence_values = extract_durations_in_days(evidence)

    if not answer_values or not evidence_values:
        return NumericConsistencyResult(
            contradiction=False,
            answer_values_in_days=answer_values,
            evidence_values_in_days=evidence_values,
            unsupported_answer_values=[],
            explanation="No comparable durations were found.",
        )

    unsupported_answer_values = [
        answer_value
        for answer_value in answer_values
        if not any(
            values_match(
                answer_value,
                evidence_value,
            )
            for evidence_value in evidence_values
        )
    ]

    if unsupported_answer_values:
        return NumericConsistencyResult(
            contradiction=True,
            answer_values_in_days=answer_values,
            evidence_values_in_days=evidence_values,
            unsupported_answer_values=unsupported_answer_values,
            explanation=(
                "Unsupported duration values were found "
                f"in the answer: {unsupported_answer_values}. "
                f"The evidence contains: {evidence_values}."
            ),
        )

    return NumericConsistencyResult(
        contradiction=False,
        answer_values_in_days=answer_values,
        evidence_values_in_days=evidence_values,
        unsupported_answer_values=[],
        explanation=(
            "All duration values in the answer "
            "are supported by the evidence."
        ),
    )
