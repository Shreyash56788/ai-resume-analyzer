from app.models import (
    JobRequirements,
    SkillWeights,
    SkillWeight,
    SkillEvaluation,
    SkillEvaluations,
    ImprovementSuggestions,
    Suggestion
)


SKILL_LIBRARY = [
    "Python",
    "Machine Learning",
    "Deep Learning",
    "Generative AI",
    "LLM",
    "RAG",
    "Agentic AI",
    "LangChain",
    "Docker",
    "AWS",
    "FastAPI",
    "SQL",
    "Git",
    "GitHub",
    "MLOps",
    "OpenAI API",
    "Groq API",
    "FAISS",
    "Pinecone",
    "ChromaDB"
]


def detect_skills(text):

    text_lower = text.lower()

    detected_skills = []

    for skill in SKILL_LIBRARY:

        if skill.lower() in text_lower:

            detected_skills.append(skill)

    return detected_skills


def extract_section(
    job_description,
    section_name,
    next_sections
):

    text_lower = job_description.lower()

    start_marker = section_name.lower()

    start_index = text_lower.find(
        start_marker
    )

    if start_index == -1:

        return ""

    start_index += len(
        start_marker
    )

    end_index = len(
        job_description
    )

    for section in next_sections:

        section_index = text_lower.find(
            section.lower(),
            start_index
        )

        if (
            section_index != -1
            and section_index < end_index
        ):

            end_index = section_index

    return job_description[
        start_index:end_index
    ]


def create_demo_job_analysis(
    job_description
):

    required_section = extract_section(
        job_description,
        "Required Skills:",
        [
            "Responsibilities:",
            "Preferred Skills:",
            "The ideal candidate"
        ]
    )

    preferred_section = extract_section(
        job_description,
        "Preferred Skills:",
        [
            "The ideal candidate"
        ]
    )

    required_skills = detect_skills(
        required_section
    )

    preferred_skills = detect_skills(
        preferred_section
    )

    if not required_skills:

        required_skills = detect_skills(
            job_description
        )

    preferred_skills = [
        skill
        for skill in preferred_skills
        if skill not in required_skills
    ]

    if not required_skills:

        required_skills = [
            "Python",
            "Machine Learning"
        ]

    weight_value = (
        100 // len(required_skills)
    )

    remainder = 100 - (
        weight_value
        * len(required_skills)
    )

    skill_weights = []

    for index, skill in enumerate(
        required_skills
    ):

        weight = weight_value

        if index == 0:

            weight += remainder

        skill_weights.append(
            SkillWeight(
                skill=skill,
                weight=weight,
                reason="Demo mode skill weighting."
            )
        )

    requirements = JobRequirements(
        job_title="AI/ML Engineer",
        required_skills=required_skills,
        preferred_skills=preferred_skills
    )

    return (
        requirements,
        SkillWeights(
            skills=skill_weights
        )
    )


def create_demo_skill_evaluations(
    required_skills
):

    resume_skills = {
        "python": (
            "Strong Python experience detected."
        ),
        "machine learning": (
            "Machine Learning experience detected."
        ),
        "deep learning": (
            "Deep Learning experience detected."
        ),
        "llm": (
            "LLM experience detected."
        )
    }

    evaluations = []

    for skill in required_skills:

        skill_lower = skill.lower()

        if skill_lower in resume_skills:

            evidence_strength = "Strong"

            if skill_lower == "deep learning":

                evidence_strength = "Moderate"

            evaluations.append(
                SkillEvaluation(
                    skill=skill,
                    match=True,
                    evidence_strength=evidence_strength,
                    explanation=resume_skills[
                        skill_lower
                    ]
                )
            )

        else:

            evaluations.append(
                SkillEvaluation(
                    skill=skill,
                    match=False,
                    evidence_strength="None",
                    explanation=(
                        "Demo mode: no evidence "
                        "detected."
                    )
                )
            )

    return SkillEvaluations(
        evaluations=evaluations
    )


def create_demo_suggestions(
    missing_skills
):

    suggestions = []

    for skill in missing_skills:

        suggestions.append(
            Suggestion(
                skill=skill,
                priority="High",
                suggestion=(
                    f"Learn {skill} and build a "
                    f"practical project demonstrating "
                    f"hands-on experience."
                )
            )
        )

    return ImprovementSuggestions(
        suggestions=suggestions
    )