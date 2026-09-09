from app.job_cache import (
    create_job_hash,
    save_job_analysis,
    load_job_analysis
)

from app.models import (
    JobRequirements,
    SkillWeights,
    SkillWeight
)


def test_job_cache():

    job_description = """
    We are looking for an AI Engineer.

    Required Skills:
    - Python
    - Machine Learning
    - Docker
    - AWS
    """

    requirements = JobRequirements(
        job_title="AI Engineer",
        required_skills=[
            "Python",
            "Machine Learning",
            "Docker",
            "AWS"
        ],
        preferred_skills=[]
    )

    skill_weights = SkillWeights(
        skills=[
            SkillWeight(
                skill="Python",
                weight=40,
                reason="Core programming skill."
            ),
            SkillWeight(
                skill="Machine Learning",
                weight=30,
                reason="Core AI skill."
            ),
            SkillWeight(
                skill="Docker",
                weight=15,
                reason="Deployment skill."
            ),
            SkillWeight(
                skill="AWS",
                weight=15,
                reason="Cloud skill."
            )
        ]
    )

    job_hash = create_job_hash(
        job_description
    )

    print("\n========== JOB CACHE TEST ==========")

    print(
        f"Generated job hash: {job_hash}"
    )

    save_job_analysis(
        job_description,
        requirements,
        skill_weights
    )

    cached_data = load_job_analysis(
        job_description
    )

    assert cached_data is not None

    assert (
        cached_data["requirements"].job_title
        == "AI Engineer"
    )

    assert (
        cached_data["requirements"].required_skills
        == [
            "Python",
            "Machine Learning",
            "Docker",
            "AWS"
        ]
    )

    assert (
        len(
            cached_data["skill_weights"].skills
        )
        == 4
    )

    print(
        "Cache saved successfully: ✅"
    )

    print(
        "Cache loaded successfully: ✅"
    )

    print(
        "Job title:",
        cached_data["requirements"].job_title
    )

    print(
        "Required skills:",
        cached_data["requirements"].required_skills
    )

    print(
        "==================================="
    )

    print(
        "\n🎉 Job cache test passed!"
    )


if __name__ == "__main__":

    test_job_cache()