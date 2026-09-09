from app.models import SkillEvaluation, SkillEvaluations


def test_multiple_skill_evaluations():

    evaluations = SkillEvaluations(
        evaluations=[
            SkillEvaluation(
                skill="Python",
                match=True,
                evidence_strength="Strong",
                explanation="Strong Python experience."
            ),
            SkillEvaluation(
                skill="Docker",
                match=False,
                evidence_strength="None",
                explanation="No Docker evidence."
            ),
            SkillEvaluation(
                skill="AWS",
                match=False,
                evidence_strength="None",
                explanation="No AWS evidence."
            )
        ]
    )

    assert len(evaluations.evaluations) == 3

    assert evaluations.evaluations[0].skill == "Python"
    assert evaluations.evaluations[0].match is True

    assert evaluations.evaluations[1].skill == "Docker"
    assert evaluations.evaluations[1].match is False

    assert evaluations.evaluations[2].skill == "AWS"
    assert evaluations.evaluations[2].match is False

    print("\n========== EVALUATOR STRUCTURE TEST ==========")

    for evaluation in evaluations.evaluations:

        print(
            f"{evaluation.skill}: "
            f"{evaluation.evidence_strength} "
            f"→ "
            f"{'Matched' if evaluation.match else 'Not Matched'}"
        )

    print("==============================================")
    print("\n🎉 Evaluator structure test passed!")


if __name__ == "__main__":

    test_multiple_skill_evaluations()