from app.models import (
    SkillEvaluation,
    SkillWeights,
    SkillWeight
)

from app.scorer import calculate_match_score


def test_strong_match():

    results = [
        SkillEvaluation(
            skill="Python",
            match=True,
            evidence_strength="Strong",
            explanation="Strong Python project experience."
        ),
        SkillEvaluation(
            skill="Docker",
            match=True,
            evidence_strength="Strong",
            explanation="Docker used in projects."
        )
    ]

    weights = SkillWeights(
        skills=[
            SkillWeight(
                skill="Python",
                weight=60,
                reason="Core programming skill."
            ),
            SkillWeight(
                skill="Docker",
                weight=40,
                reason="Required deployment skill."
            )
        ]
    )

    score = calculate_match_score(
        results,
        weights
    )

    assert score == 100


def test_partial_match():

    results = [
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
        )
    ]

    weights = SkillWeights(
        skills=[
            SkillWeight(
                skill="Python",
                weight=60,
                reason="Core skill."
            ),
            SkillWeight(
                skill="Docker",
                weight=40,
                reason="Deployment skill."
            )
        ]
    )

    score = calculate_match_score(
        results,
        weights
    )

    assert score == 60


def test_moderate_evidence():

    results = [
        SkillEvaluation(
            skill="Python",
            match=True,
            evidence_strength="Moderate",
            explanation="Python mentioned with limited detail."
        )
    ]

    weights = SkillWeights(
        skills=[
            SkillWeight(
                skill="Python",
                weight=100,
                reason="Core skill."
            )
        ]
    )

    score = calculate_match_score(
        results,
        weights
    )

    assert score == 70


def test_unmatched_skill_with_strong_evidence():

    results = [
        SkillEvaluation(
            skill="Docker",
            match=False,
            evidence_strength="Strong",
            explanation="Intentional inconsistent test case."
        )
    ]

    weights = SkillWeights(
        skills=[
            SkillWeight(
                skill="Docker",
                weight=100,
                reason="Test skill."
            )
        ]
    )

    score = calculate_match_score(
        results,
        weights
    )

    assert score == 0


if __name__ == "__main__":

    test_strong_match()
    print("✅ Strong match test passed")

    test_partial_match()
    print("✅ Partial match test passed")

    test_moderate_evidence()
    print("✅ Moderate evidence test passed")

    test_unmatched_skill_with_strong_evidence()
    print("✅ Unmatched skill safety test passed")

    print("\n🎉 All scoring tests passed!")