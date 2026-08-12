from __future__ import annotations

import re


TEXT = {
    "en": {
        "platform_title": "AI Reliability Platform",
        "subtitle": (
            "Evaluate RAG reliability, diagnose failures, "
            "and track system health over time."
        ),
        "language": "Language",
        "connection": "Connection",
        "fastapi_url": "FastAPI URL",
        "check_api": "Check API Connection",
        "backend": "Backend: FastAPI + PostgreSQL",
        "dashboard": "Dashboard: Streamlit",
        "overview": "Overview",
        "run_check": "Run Health Check",
        "history": "History",
        "reliability_overview": "Reliability Overview",
        "total_checks": "Total Health Checks",
        "evaluated_checks": "Evaluated Checks",
        "average_score": "Average Health Score",
        "latest_score": "Latest Score",
        "critical_evaluations": "Critical Evaluations",
        "poor_warning": (
            "{count} evaluated health check(s) "
            "are POOR or CRITICAL."
        ),
        "health_score_history": "Health Score History",
        "no_scores": "No stored health scores yet.",
        "recent_checks": "Recent Health Checks",
        "created": "Created",
        "project": "Project",
        "score": "Score",
        "health": "Health",
        "evaluation": "Evaluation",
        "root_cause": "Root Cause",
        "no_checks": "No health checks found.",
        "run_new": "Run a New Health Check",
        "run_caption": (
            "Paste the RAG answer and retrieved context "
            "to evaluate the system."
        ),
        "project_id": "Project ID",
        "application_version": "Application Version",
        "question": "Question",
        "rag_answer": "RAG Answer",
        "retrieved_context": "Retrieved Context",
        "context_source": "Context Source",
        "reference_answer_optional": "Reference Answer (optional)",
        "prompt_optional": "Prompt (optional)",
        "model_configuration": "Model Configuration",
        "provider": "Provider",
        "model_name": "Model Name",
        "temperature": "Temperature",
        "run_button": "Run Reliability Check",
        "project_required": "Project ID is required.",
        "question_required": "Question is required.",
        "answer_required": "Answer is required.",
        "running": "Running reliability evaluation...",
        "completed": (
            "Health check completed and stored successfully."
        ),
        "history_title": "Health Check History",
        "select_check": "Select Health Check",
        "overall_health_score": "Overall Health Score",
        "health_status": "Health Status",
        "question_answer": "Question & Answer",
        "generated_answer": "Generated Answer",
        "reference_answer": "Reference Answer",
        "evaluation_metrics": "Evaluation Metrics",
        "correctness": "Correctness",
        "faithfulness": "Faithfulness",
        "context_precision": "Context Precision",
        "context_recall": "Context Recall",
        "answer_relevancy": "Answer Relevancy",
        "hallucination_risk": "Hallucination Risk",
        "evaluation_status": "Evaluation Status",
        "evaluation_explanation": "Evaluation Explanation",
        "original_explanation": (
            "Original technical explanation (English)"
        ),
        "no_evaluation": (
            "No evaluation metrics are stored "
            "for this health check."
        ),
        "no_diagnosis": (
            "No root cause diagnosis was generated."
        ),
        "category": "Category",
        "severity": "Severity",
        "confidence": "Confidence",
        "subcategory": "Subcategory",
        "recommendations": "Recommendations",
        "no_recommendations": "No recommendations generated.",
        "priority": "Priority",
        "expected_impact": "Expected Impact",
        "difficulty": "Difficulty",
        "affected_component": "Affected Component",
        "supporting_evidence": "Supporting Evidence",
        "retrieved_contexts": "Retrieved Contexts",
        "no_contexts": "No contexts were stored.",
        "context": "Context",
        "retrieval_score": "Retrieval Score",
        "connected": "Connected",
        "not_available": "N/A",
    },

    "ar": {
        "platform_title": "منصة موثوقية الذكاء الاصطناعي",
        "subtitle": (
            "قيّم موثوقية أنظمة RAG، وشخّص الأعطال، "
            "وتابع صحة النظام بمرور الوقت."
        ),
        "language": "اللغة",
        "connection": "الاتصال",
        "fastapi_url": "رابط FastAPI",
        "check_api": "التحقق من اتصال API",
        "backend": "الخلفية: FastAPI + PostgreSQL",
        "dashboard": "لوحة التحكم: Streamlit",
        "overview": "نظرة عامة",
        "run_check": "إجراء فحص",
        "history": "السجل",
        "reliability_overview": "نظرة عامة على الموثوقية",
        "total_checks": "إجمالي الفحوصات",
        "evaluated_checks": "الفحوصات المُقيّمة",
        "average_score": "متوسط درجة الصحة",
        "latest_score": "أحدث درجة",
        "critical_evaluations": "التقييمات الحرجة",
        "poor_warning": (
            "{count} من الفحوصات المُقيّمة "
            "حالته ضعيفة أو حرجة."
        ),
        "health_score_history": "سجل درجة الصحة",
        "no_scores": "لا توجد درجات صحة محفوظة حتى الآن.",
        "recent_checks": "أحدث الفحوصات",
        "created": "التاريخ",
        "project": "المشروع",
        "score": "الدرجة",
        "health": "حالة الصحة",
        "evaluation": "التقييم",
        "root_cause": "السبب الجذري",
        "no_checks": "لا توجد فحوصات مسجلة.",
        "run_new": "إجراء فحص موثوقية جديد",
        "run_caption": (
            "أدخل إجابة نظام RAG والسياق المسترجع "
            "لتقييم موثوقية النظام."
        ),
        "project_id": "معرّف المشروع",
        "application_version": "إصدار التطبيق",
        "question": "السؤال",
        "rag_answer": "إجابة RAG",
        "retrieved_context": "السياق المسترجع",
        "context_source": "مصدر السياق",
        "reference_answer_optional": "الإجابة المرجعية (اختياري)",
        "prompt_optional": "التوجيه Prompt (اختياري)",
        "model_configuration": "إعدادات النموذج",
        "provider": "المزوّد",
        "model_name": "اسم النموذج",
        "temperature": "درجة الحرارة",
        "run_button": "تشغيل فحص الموثوقية",
        "project_required": "معرّف المشروع مطلوب.",
        "question_required": "السؤال مطلوب.",
        "answer_required": "الإجابة مطلوبة.",
        "running": "جارٍ إجراء تقييم الموثوقية...",
        "completed": "اكتمل الفحص وتم حفظ النتيجة بنجاح.",
        "history_title": "سجل فحوصات الموثوقية",
        "select_check": "اختر فحصًا",
        "overall_health_score": "درجة الصحة العامة",
        "health_status": "حالة الصحة",
        "question_answer": "السؤال والإجابة",
        "generated_answer": "الإجابة المُولّدة",
        "reference_answer": "الإجابة المرجعية",
        "evaluation_metrics": "مقاييس التقييم",
        "correctness": "صحة الإجابة",
        "faithfulness": "الالتزام بالسياق المسترجع",
        "context_precision": "دقة السياق المسترجع",
        "context_recall": "تغطية السياق المسترجع",
        "answer_relevancy": "ارتباط الإجابة بالسؤال",
        "hallucination_risk": "مخاطر الهلوسة",
        "evaluation_status": "حالة التقييم",
        "evaluation_explanation": "تفسير نتيجة التقييم",
        "original_explanation": (
            "التفسير الفني الأصلي من المحرك (بالإنجليزية)"
        ),
        "no_evaluation": (
            "لا توجد مقاييس تقييم محفوظة لهذا الفحص."
        ),
        "no_diagnosis": "لم يتم اكتشاف سبب جذري محدد.",
        "category": "الفئة",
        "severity": "الشدة",
        "confidence": "درجة الثقة",
        "subcategory": "الفئة الفرعية",
        "recommendations": "التوصيات",
        "no_recommendations": "لا توجد توصيات.",
        "priority": "الأولوية",
        "expected_impact": "الأثر المتوقع",
        "difficulty": "مستوى الصعوبة",
        "affected_component": "المكوّن المتأثر",
        "supporting_evidence": "الدليل الداعم",
        "retrieved_contexts": "السياقات المسترجعة",
        "no_contexts": "لا توجد سياقات محفوظة.",
        "context": "السياق",
        "retrieval_score": "درجة الاسترجاع",
        "connected": "متصل",
        "not_available": "غير متوفر",
    },
}


VALUE_LABELS_AR = {
    "EXCELLENT": "ممتاز",
    "GOOD": "جيد",
    "HEALTHY": "سليم",
    "WARNING": "تحذير",
    "POOR": "ضعيف",
    "CRITICAL": "حرج",
    "COMPLETED": "مكتمل",

    "HIGH": "مرتفع",
    "MEDIUM": "متوسط",
    "LOW": "منخفض",

    "RETRIEVAL_FAILURE": "فشل الاسترجاع",
    "GENERATION_FAILURE": "فشل التوليد",
    "KNOWLEDGE_BASE_FAILURE": "قصور قاعدة المعرفة",
    "PROMPT_FAILURE": "مشكلة في التوجيه",

    "LOW_CONTEXT_PRECISION": "انخفاض دقة السياق",
    "UNSUPPORTED_CLAIM": "ادعاء غير مدعوم",
    "MISSING_INFORMATION": "معلومات مفقودة",
    "LOW_ANSWER_RELEVANCY": "انخفاض ارتباط الإجابة بالسؤال",

    "RETRIEVER": "نظام الاسترجاع",
    "GENERATION": "التوليد",
    "KNOWLEDGE_BASE": "قاعدة المعرفة",
    "PROMPT": "التوجيه",
}


RECOMMENDATION_ACTIONS_AR = {
    (
        "Review retrieval configuration and "
        "improve retrieved chunk relevance."
    ): (
        "راجع إعدادات الاسترجاع وحسّن مدى ارتباط "
        "المقاطع المسترجعة بالسؤال."
    ),

    (
        "Add or improve a reranking stage "
        "before sending context to the model."
    ): (
        "أضف مرحلة إعادة ترتيب (Reranking) أو حسّنها "
        "قبل إرسال السياق إلى النموذج."
    ),

    (
        "Tune Top-K, chunk size, and chunk "
        "overlap using evaluation results."
    ): (
        "اضبط Top-K وحجم المقطع والتداخل بين المقاطع "
        "بالاعتماد على نتائج التقييم."
    ),

    (
        "Strengthen grounding instructions "
        "so the model answers only from "
        "retrieved evidence."
    ): (
        "عزّز تعليمات الاستناد إلى الأدلة بحيث يجيب "
        "النموذج اعتمادًا على السياق المسترجع فقط."
    ),

    (
        "Require citations or explicit "
        "supporting evidence in generated "
        "answers."
    ): (
        "اطلب من النموذج إرفاق استشهادات أو أدلة "
        "داعمة واضحة في الإجابات المُولّدة."
    ),

    (
        "Add an abstention policy when "
        "available context does not support "
        "the answer."
    ): (
        "أضف سياسة امتناع عن الإجابة عندما لا يدعم "
        "السياق المتاح الإجابة."
    ),

    (
        "Add the missing information or "
        "documents to the knowledge base."
    ): (
        "أضف المعلومات أو المستندات المفقودة "
        "إلى قاعدة المعرفة."
    ),

    (
        "Review document freshness and "
        "replace outdated knowledge."
    ): (
        "راجع حداثة المستندات واستبدل المعرفة "
        "القديمة أو غير المحدثة."
    ),

    (
        "Re-index the knowledge base and "
        "verify document metadata."
    ): (
        "أعد فهرسة قاعدة المعرفة وتحقق من "
        "البيانات الوصفية للمستندات."
    ),

    (
        "Clarify the task and strengthen "
        "the prompt instructions."
    ): (
        "وضّح المهمة وعزّز تعليمات التوجيه."
    ),

    (
        "Remove conflicting instructions "
        "and explicitly define the expected "
        "response format."
    ): (
        "أزل التعليمات المتعارضة وحدد صيغة "
        "الاستجابة المطلوبة بشكل صريح."
    ),

    (
        "Add representative examples to "
        "improve response alignment."
    ): (
        "أضف أمثلة تمثيلية لتحسين توافق "
        "الإجابة مع المطلوب."
    ),
}


def tr(
    lang: str,
    key: str,
) -> str:
    return TEXT.get(
        lang,
        TEXT["en"],
    ).get(
        key,
        key,
    )


def localize_value(
    value: str | None,
    lang: str,
) -> str:
    if value is None:
        return tr(
            lang,
            "not_available",
        )

    if lang == "ar":
        return VALUE_LABELS_AR.get(
            value,
            value.replace(
                "_",
                " ",
            ),
        )

    return value.replace(
        "_",
        " ",
    ).title()


def localize_action(
    action: str,
    lang: str,
) -> str:
    if lang != "ar":
        return action

    return RECOMMENDATION_ACTIONS_AR.get(
        action,
        action,
    )


def _pct(
    value: float | None,
) -> str:
    if value is None:
        return "غير متوفر"

    return f"{value * 100:.1f}%"


def localize_evaluation_explanation(
    evaluation: dict | None,
    lang: str,
) -> str:
    if not evaluation:
        return ""

    original = evaluation.get(
        "explanation",
        "",
    )

    if lang != "ar":
        return original

    status = localize_value(
        evaluation.get("status"),
        "ar",
    )

    parts = [
        f"حالة التقييم: {status}.",
        (
            "بلغت صحة الإجابة "
            f"{_pct(evaluation.get('correctness_score'))}، "
            "والالتزام بالسياق المسترجع "
            f"{_pct(evaluation.get('faithfulness_score'))}."
        ),
        (
            "بلغت دقة السياق المسترجع "
            f"{_pct(evaluation.get('context_precision_score'))}، "
            "وتغطيته "
            f"{_pct(evaluation.get('context_recall_score'))}."
        ),
        (
            "بلغ ارتباط الإجابة بالسؤال "
            f"{_pct(evaluation.get('answer_relevancy_score'))}، "
            "ومخاطر الهلوسة "
            f"{_pct(evaluation.get('hallucination_risk'))}."
        ),
    ]

    duration_match = re.search(
        r"Unsupported duration values were found "
        r"in the answer: (\[[^\]]*\])\. "
        r"The evidence contains: (\[[^\]]*\])\.",
        original,
    )

    if duration_match:
        answer_values = duration_match.group(1)
        evidence_values = duration_match.group(2)

        parts.append(
            "تم اكتشاف تعارض رقمي في المدة: "
            f"الإجابة تحتوي على {answer_values}، "
            f"بينما الدليل يحتوي على {evidence_values}."
        )

    elif "numeric contradiction" in original.lower():
        parts.append(
            "تم اكتشاف تعارض رقمي بين الإجابة "
            "والدليل المتاح."
        )

    return " ".join(parts)


def localize_diagnosis_explanation(
    diagnosis: dict | None,
    evaluation: dict | None,
    lang: str,
) -> str:
    if not diagnosis:
        return ""

    original = diagnosis.get(
        "explanation",
        "",
    )

    if lang != "ar":
        return original

    evaluation = evaluation or {}

    category = diagnosis.get(
        "category"
    )

    precision = evaluation.get(
        "context_precision_score"
    )

    faithfulness = evaluation.get(
        "faithfulness_score"
    )

    recall = evaluation.get(
        "context_recall_score"
    )

    relevancy = evaluation.get(
        "answer_relevancy_score"
    )

    if category == "RETRIEVAL_FAILURE":
        return (
            "دقة السياق المسترجع منخفضة "
            f"({_pct(precision)}). يشير ذلك إلى أن نظام "
            "الاسترجاع يعيد مقاطع غير مرتبطة بالسؤال "
            "أو منخفضة الجودة."
        )

    if category == "GENERATION_FAILURE":
        return (
            "دقة السياق المسترجع جيدة "
            f"({_pct(precision)})، لكن الالتزام بالسياق "
            f"منخفض ({_pct(faithfulness)}). هذا يعني أن "
            "المعلومات المسترجعة كانت مناسبة، لكن النموذج "
            "ولّد إجابة غير مستندة إليها بشكل كافٍ."
        )

    if category == "KNOWLEDGE_BASE_FAILURE":
        return (
            "تغطية السياق المسترجع منخفضة "
            f"({_pct(recall)}) مع دقة سياق مقبولة "
            f"({_pct(precision)}). يشير ذلك إلى أن قاعدة "
            "المعرفة قد تفتقد جزءًا من المعلومات اللازمة "
            "للإجابة الكاملة عن السؤال."
        )

    if category == "PROMPT_FAILURE":
        return (
            "دقة السياق المسترجع جيدة "
            f"({_pct(precision)})، لكن ارتباط الإجابة "
            f"بالسؤال منخفض ({_pct(relevancy)}). يشير ذلك "
            "إلى مشكلة محتملة في وضوح التوجيه أو في "
            "استدلال النموذج."
        )

    return original