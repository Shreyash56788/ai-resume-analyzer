SKILL_ALIASES = {
    "generative ai and llms": [
        "Generative AI",
        "LLM"
    ],
    "generative ai": [
        "Generative AI"
    ],
    "genai": [
        "Generative AI"
    ],
    "large language models": [
        "LLM"
    ],
    "large language model": [
        "LLM"
    ],
    "llms": [
        "LLM"
    ],
    "llm": [
        "LLM"
    ],
    "retrieval-augmented generation": [
        "RAG"
    ],
    "retrieval augmented generation": [
        "RAG"
    ],
    "rag": [
        "RAG"
    ],
    "agentic ai": [
        "Agentic AI"
    ],
    "ai agents": [
        "Agentic AI"
    ],
    "langchain": [
        "LangChain"
    ],
    "fast api": [
        "FastAPI"
    ],
    "fastapi": [
        "FastAPI"
    ],
    "amazon web services": [
        "AWS"
    ],
    "aws": [
        "AWS"
    ],
    "structured query language": [
        "SQL"
    ],
    "sql": [
        "SQL"
    ]
}


def normalize_skill(skill):

    normalized = skill.strip().lower()

    # RAG variations
    if (
        normalized == "rag"
        or normalized.startswith("rag ")
        or normalized.startswith("rag(")
        or normalized.startswith("rag (")
    ):
        return ["RAG"]

    if (
        "retrieval-augmented generation"
        in normalized
        or
        "retrieval augmented generation"
        in normalized
    ):
        return ["RAG"]

    # Known aliases
    if normalized in SKILL_ALIASES:
        return SKILL_ALIASES[normalized]

    return [skill.strip()]


def normalize_skills(skills):

    normalized_skills = []

    for skill in skills:

        canonical_skills = normalize_skill(skill)

        for canonical_skill in canonical_skills:

            if canonical_skill not in normalized_skills:

                normalized_skills.append(
                    canonical_skill
                )

    return normalized_skills