from openai import OpenAI

from app.config import GROQ_API_KEY, GROQ_MODEL
from app.models import JobRequirements, SkillWeights
from app.skill_normalizer import normalize_skills


client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


def analyze_job(job_description):

   

    response = client.responses.parse(
        model=GROQ_MODEL,
        input=f"""
Analyze the following job description.

Job Description:
{job_description}

Extract:

1. Job title
2. Required technical skills
3. Preferred technical skills
4. Importance weights for every required skill

Rules:

- Extract only skills explicitly required or clearly stated
  in the job description.
- Do not invent skills.
- Keep required and preferred skills separate.
- Required skills must come from the Required Skills section
  when that section exists.
- Preferred skills must come from the Preferred Skills section
  when that section exists.
- Assign integer weights to required skills.
- The sum of all required skill weights must equal exactly 100.
- More important skills should receive higher weights.
- Give a short reason for every weight.
""",
        text_format=JobRequirements
    )

    requirements = response.output_parsed


   

    normalized_required_skills = normalize_skills(
        requirements.required_skills
    )


   

    normalized_preferred_skills = normalize_skills(
        requirements.preferred_skills
    )


   
    normalized_preferred_skills = [
        skill
        for skill in normalized_preferred_skills
        if skill not in normalized_required_skills
    ]


   

    weight_response = client.responses.parse(
        model=GROQ_MODEL,
        input=f"""
Create importance weights for these required skills.

Required Skills:
{normalized_required_skills}

Rules:

- Return every required skill exactly once.
- Use integer weights.
- The total weight must equal exactly 100.
- More important skills should receive higher weights.
- Give a short reason for every weight.
- Do not create additional skills.
""",
        text_format=SkillWeights
    )

    skill_weights = weight_response.output_parsed


   

    weight_map = {
        item.skill.lower(): item
        for item in skill_weights.skills
    }


 
    normalized_weights = []

    for skill in normalized_required_skills:

        item = weight_map.get(
            skill.lower()
        )

        if item is None:

            raise ValueError(
                f"Missing weight for required skill: {skill}"
            )

        normalized_weights.append(
            item
        )


   

    total_weight = sum(
        item.weight
        for item in normalized_weights
    )

    if total_weight != 100:

        normalized_weights[-1].weight += (
            100 - total_weight
        )


   

    requirements = JobRequirements(
        job_title=requirements.job_title,
        required_skills=normalized_required_skills,
        preferred_skills=normalized_preferred_skills
    )


    skill_weights = SkillWeights(
        skills=normalized_weights
    )


    

    return (
        requirements,
        skill_weights
    )