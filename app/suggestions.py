from openai import OpenAI

from app.config import GROQ_API_KEY , GROQ_MODEL
from app.models import ImprovementSuggestions

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


def generate_suggestions(missing_skills):

    if not missing_skills:
        return ImprovementSuggestions(
            suggestions=[]
        )

    missing_text = "\n".join(
        f"- {skill}"
        for skill in missing_skills
    )

    response = client.responses.parse(
        model=GROQ_MODEL,
        input=f"""
Create practical improvement suggestions for the candidate.

Missing Skills:
{missing_text}

Rules:
- Give exactly one suggestion for each missing skill.
- Keep suggestions practical and specific.
- Focus on what the candidate should learn or build.
- Do not claim the candidate already knows the missing skill.
- Set priority as High, Medium, or Low.
""",
        text_format=ImprovementSuggestions
    )

    return response.output_parsed