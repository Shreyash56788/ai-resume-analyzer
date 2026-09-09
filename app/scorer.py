from app.models import SkillEvaluation, SkillWeights


EVIDENCE_SCORES = {
    "Strong": 100,
    "Moderate": 70,
    "Weak": 40,
    "None": 0
}


def calculate_match_score(
    results: list[SkillEvaluation],
    skill_weights: SkillWeights
):

    weighted_score = 0

    for result in results:

        # A skill that is not matched must contribute 0 points.
        if not result.match:
            continue

        for skill_weight in skill_weights.skills:

            if (
                result.skill.lower()
                == skill_weight.skill.lower()
            ):

                evidence_score = EVIDENCE_SCORES.get(
                    result.evidence_strength,
                    0
                )

                contribution = (
                    skill_weight.weight
                    * evidence_score
                    / 100
                )

                weighted_score += contribution

                break

    return round(weighted_score, 2)