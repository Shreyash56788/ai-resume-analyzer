from openai import OpenAI
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from app.config import GROQ_API_KEY, GROQ_MODEL
from app.models import SkillEvaluation, SkillEvaluations


client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


EVALUATION_MODEL = GROQ_MODEL
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)

RETRIEVAL_K = 2
SIMILARITY_THRESHOLD = 0.25

VALID_EVIDENCE_STRENGTHS = {
    "Strong",
    "Moderate",
    "Weak",
    "None"
}


EVALUATION_SCHEMA = {
    "type": "object",
    "properties": {
        "evaluations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "skill": {
                        "type": "string"
                    },
                    "match": {
                        "type": "boolean"
                    },
                    "evidence_strength": {
                        "type": "string",
                        "enum": [
                            "Strong",
                            "Moderate",
                            "Weak",
                            "None"
                        ]
                    },
                    "explanation": {
                        "type": "string"
                    }
                },
                "required": [
                    "skill",
                    "match",
                    "evidence_strength",
                    "explanation"
                ],
                "additionalProperties": False
            }
        }
    },
    "required": [
        "evaluations"
    ],
    "additionalProperties": False
}


def validate_evaluations(
    evaluations,
    required_skills
):

    required_skill_map = {
        skill.lower(): skill
        for skill in required_skills
    }

    evaluation_map = {}

    for evaluation in evaluations:

        skill_key = evaluation.skill.strip().lower()

        if skill_key not in required_skill_map:
            continue

        if skill_key in evaluation_map:
            continue

        evidence_strength = (
            evaluation.evidence_strength
        )

        if evidence_strength not in VALID_EVIDENCE_STRENGTHS:
            evidence_strength = "None"

        if not evaluation.match:
            evidence_strength = "None"

        evaluation_map[skill_key] = SkillEvaluation(
            skill=required_skill_map[skill_key],
            match=evaluation.match,
            evidence_strength=evidence_strength,
            explanation=evaluation.explanation.strip()
        )

    validated_results = []

    for skill in required_skills:

        evaluation = evaluation_map.get(
            skill.lower()
        )

        if evaluation is None:

            validated_results.append(
                SkillEvaluation(
                    skill=skill,
                    match=False,
                    evidence_strength="None",
                    explanation=(
                        "No valid evaluation was returned "
                        "for this skill."
                    )
                )
            )

        else:

            validated_results.append(
                evaluation
            )

    return validated_results


def evaluate_skills(
    chunks,
    index,
    required_skills
):

    skill_embeddings = embedding_model.encode(
        required_skills,
        convert_to_numpy=True
    )

    skill_contexts = []

    for skill, embedding in zip(
        required_skills,
        skill_embeddings
    ):

        skill_embedding = np.array(
            [embedding],
            dtype="float32"
        )

        faiss.normalize_L2(
            skill_embedding
        )

        scores, indices = index.search(
            skill_embedding,
            k=RETRIEVAL_K
        )

        relevant_chunks = []

        for score, index_position in zip(
            scores[0],
            indices[0]
        ):

            if index_position == -1:
                continue

            if score < SIMILARITY_THRESHOLD:
                continue

            relevant_chunks.append(
                chunks[index_position].page_content
            )

        if relevant_chunks:

            context = "\n\n".join(
                relevant_chunks
            )

        else:

            context = (
                "No sufficiently relevant "
                "resume evidence found."
            )

        skill_contexts.append(
            f"""
Required Skill:
{skill}

Resume Evidence:
{context}
"""
        )

    all_context = "\n\n".join(
        skill_contexts
    )

    prompt = f"""
You are a strict resume evaluator.

Evaluate EVERY required skill listed below.

{all_context}

Evaluation Rules:

1. Use ONLY the provided resume evidence.

2. Do NOT use outside knowledge.

3. Do NOT infer that the candidate knows a skill simply
because another related skill appears.

4. The candidate must have explicit or strongly demonstrated
evidence of the required skill.

5. Examples:

Python experience can support Python.

Machine Learning experience can support Machine Learning.

Docker experience can support Docker.

AWS experience can support AWS.

But:

Python alone does NOT prove Docker.

Machine Learning alone does NOT prove Deep Learning.

LLM experience does NOT automatically prove RAG.

AI experience does NOT automatically prove Agentic AI.

6. Project experience, implementation, deployment, work
experience, certifications, or clearly stated technical
experience can be considered evidence.

7. If the evidence is ambiguous, choose match=false.

8. If no sufficiently relevant evidence is provided:

match=false

evidence_strength="None"

9. evidence_strength must be exactly one of:

Strong
Moderate
Weak
None

10. Strong means the resume clearly demonstrates the skill
through specific projects, implementation, deployment,
work experience, or substantial technical usage.

11. Moderate means the skill is explicitly mentioned or
demonstrated but hands-on evidence is limited.

12. Weak means there is only indirect or very limited evidence.

13. None means there is no evidence demonstrating the skill.

14. Do not award a match based only on semantic similarity.

15. Evaluate every required skill exactly once.

16. Keep explanations short and reference only the provided
resume evidence.

17. Do not create skills that are not in the required skills.

18. Return skills in the same order as the required skills.

19. If match=false, evidence_strength MUST be "None".

20. Do not return null values.

21. Return exactly one evaluation for every required skill.
"""

    response = client.chat.completions.create(
        model=EVALUATION_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict resume evaluation "
                    "system. Return only the requested "
                    "structured JSON."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "skill_evaluations",
                "strict": True,
                "schema": EVALUATION_SCHEMA
            }
        },
        temperature=0
    )

    raw_content = (
        response.choices[0]
        .message
        .content
    )

    parsed_data = json.loads(
        raw_content
    )

    parsed_output = SkillEvaluations.model_validate(
        parsed_data
    )

    validated_results = validate_evaluations(
        parsed_output.evaluations,
        required_skills
    )

    return validated_results