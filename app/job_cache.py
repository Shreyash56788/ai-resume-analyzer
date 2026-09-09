import os
import hashlib
import pickle


CACHE_DIR = "storage/job_cache"


def create_job_hash(job_description):

    normalized_job = job_description.strip().lower()

    return hashlib.sha256(
        normalized_job.encode("utf-8")
    ).hexdigest()[:16]


def get_cache_path(job_description):

    job_hash = create_job_hash(
        job_description
    )

    os.makedirs(
        CACHE_DIR,
        exist_ok=True
    )

    return os.path.join(
        CACHE_DIR,
        f"{job_hash}.pkl"
    )


def save_job_analysis(
    job_description,
    requirements,
    skill_weights
):

    cache_path = get_cache_path(
        job_description
    )

    data = {
        "requirements": requirements,
        "skill_weights": skill_weights
    }

    with open(
        cache_path,
        "wb"
    ) as file:

        pickle.dump(
            data,
            file
        )


def load_job_analysis(job_description):

    cache_path = get_cache_path(
        job_description
    )

    if not os.path.exists(cache_path):

        return None

    with open(
        cache_path,
        "rb"
    ) as file:

        return pickle.load(
            file
        )