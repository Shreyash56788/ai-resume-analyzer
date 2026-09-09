from pydantic import BaseModel


class JobRequirements(BaseModel):
    job_title: str
    required_skills: list[str]
    preferred_skills: list[str]


class SkillWeight(BaseModel):
    skill: str
    weight: int
    reason: str


class SkillWeights(BaseModel):
    skills: list[SkillWeight]


class SkillEvaluation(BaseModel):
    skill: str
    match: bool
    evidence_strength: str
    explanation: str


class SkillEvaluations(BaseModel):
    evaluations: list[SkillEvaluation]


class Suggestion(BaseModel):
    skill: str
    suggestion: str
    priority: str


class ImprovementSuggestions(BaseModel):
    suggestions: list[Suggestion]