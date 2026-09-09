from app.models import SkillEvaluation, SkillWeights, SkillWeight
from app.scorer import calculate_match_score


def test_offline_resume_evaluation():

    results = [
        SkillEvaluation(
            skill="Python",
            match=True,
            evidence_strength="Strong",
            explanation="Strong Python project experience."
        ),
        SkillEvaluation(
            skill="Machine Learning",
            match=True,
            evidence_strength="Strong",
            explanation="Machine Learning projects are present."
        ),
        SkillEvaluation(
            skill="Deep Learning",
            match=True,
            evidence_strength="Moderate",
            explanation="Deep Learning experience is mentioned."
        ),
        SkillEvaluation(
            skill="LLM",
            match=True,
            evidence_strength="Strong",
            explanation="LLM projects are present."
        ),
        SkillEvaluation(
            skill="Docker",
            match=False,
            evidence_strength="None",
            explanation="No Docker experience found."
        ),
        SkillEvaluation(
            skill="AWS",
            match=False,
            evidence_strength="None",
            explanation="No AWS experience found."
        )
    ]

    weights = SkillWeights(
        skills=[
            SkillWeight(
                skill="Python",
                weight=25,
                reason="Core programming skill."
            ),
            SkillWeight(
                skill="Machine Learning",
                weight=20,
                reason="Core AI skill."
            ),
            SkillWeight(
                skill="Deep Learning",
                weight=15,
                reason="Important AI skill."
            ),
            SkillWeight(
                skill="LLM",
                weight=20,
                reason="Important Generative AI skill."
            ),
            SkillWeight(
                skill="Docker",
                weight=10,
                reason="Deployment skill."
            ),
            SkillWeight(
                skill="AWS",
                weight=10,
                reason="Cloud deployment skill."
            )
        ]
    )

    score = calculate_match_score(
        results,
        weights
    )

    matched_skills = [
        result.skill
        for result in results
        if result.match
    ]

    missing_skills = [
        result.skill
        for result in results
        if not result.match
    ]

    print("\n========== OFFLINE EVALUATION ==========")

    print(f"\nMatch Score: {score}/100")

    print("\nMatched Skills:")
    for skill in matched_skills:
        print(f"  ✅ {skill}")

    print("\nMissing Skills:")
    for skill in missing_skills:
        print(f"  ❌ {skill}")

    print("\n========================================")

    assert score == 75.5
    assert len(matched_skills) == 4
    assert len(missing_skills) == 2

    assert "Python" in matched_skills
    assert "Machine Learning" in matched_skills
    assert "Deep Learning" in matched_skills
    assert "LLM" in matched_skills

    assert "Docker" in missing_skills
    assert "AWS" in missing_skills


if __name__ == "__main__":

    test_offline_resume_evaluation()

    print("\n🎉 Offline evaluation test passed!")