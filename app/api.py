import os
import hashlib
import openai

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form,
    HTTPException
)

from app.config import DEMO_MODE
from app.resume_processor import load_and_split_resume
from app.embeddings import create_embeddings

from app.retriever import (
    create_faiss_index,
    save_faiss_index,
    load_faiss_index,
    save_chunks,
    load_chunks
)

from app.job_analyzer import analyze_job
from app.evaluator import evaluate_skills
from app.suggestions import generate_suggestions
from app.scorer import calculate_match_score

from app.job_cache import (
    load_job_analysis,
    save_job_analysis
)

from app.demo_analyzer import (
    create_demo_job_analysis,
    create_demo_skill_evaluations,
    create_demo_suggestions
)

from app.performance import PerformanceTimer
from app.logger import logger


app = FastAPI(
    title="AI Resume Analyzer",
    version="1.0.0"
)


UPLOAD_DIR = "uploads"
STORAGE_DIR = "storage"


os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

os.makedirs(
    STORAGE_DIR,
    exist_ok=True
)


@app.get("/")
def home():

    return {
        "message": "AI Resume Analyzer API is running"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "AI Resume Analyzer API"
    }


@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form("")
):

    timer = PerformanceTimer()

    try:

        if (
            not resume.filename
            or not resume.filename.lower().endswith(".pdf")
        ):

            raise HTTPException(
                status_code=400,
                detail="Only PDF resumes are supported."
            )

        if not job_description.strip():

            raise HTTPException(
                status_code=400,
                detail="Job description cannot be empty."
            )

        logger.info(
            "Starting resume analysis."
        )

        resume_bytes = await resume.read()

        if not resume_bytes:

            raise HTTPException(
                status_code=400,
                detail="Uploaded resume is empty."
            )

        resume_hash = hashlib.sha256(
            resume_bytes
        ).hexdigest()[:16]

        # Save resume
        resume_path = os.path.join(
            UPLOAD_DIR,
            f"{resume_hash}.pdf"
        )

        with open(
            resume_path,
            "wb"
        ) as file:

            file.write(
                resume_bytes
            )

        timer.checkpoint(
            "resume_upload"
        )

        storage_path = os.path.join(
            STORAGE_DIR,
            resume_hash
        )

        os.makedirs(
            storage_path,
            exist_ok=True
        )

        index_path = os.path.join(
            storage_path,
            "resume.index"
        )

        chunks_path = os.path.join(
            storage_path,
            "chunks.pkl"
        )

        if (
            os.path.exists(index_path)
            and os.path.exists(chunks_path)
        ):

            logger.info(
                "Cached resume index found."
            )

            index = load_faiss_index(
                index_path
            )

            chunks = load_chunks(
                chunks_path
            )

        else:

            logger.info(
                "No cached index found. Processing resume."
            )

            chunks = load_and_split_resume(
                resume_path
            )

            timer.checkpoint(
                "resume_processing"
            )

            texts = [
                chunk.page_content
                for chunk in chunks
            ]

            logger.info(
                "Creating embeddings for resume chunks."
            )

            embeddings = create_embeddings(
                texts
            )

            timer.checkpoint(
                "embedding_creation"
            )

            index = create_faiss_index(
                embeddings
            )

            logger.info(
                "FAISS index created successfully."
            )

            save_faiss_index(
                index,
                index_path
            )

            save_chunks(
                chunks,
                chunks_path
            )

            logger.info(
                "FAISS index and resume chunks saved to storage."
            )

        timer.checkpoint(
            "resume_index_ready"
        )

        logger.info(
            f"Demo mode: {DEMO_MODE}"
        )

        if DEMO_MODE:

            logger.info(
                "Running analysis in Demo Mode."
            )

            (
                requirements,
                skill_weights
            ) = create_demo_job_analysis(
                job_description
            )

            timer.checkpoint(
                "job_analysis"
            )

            evaluation_response = (
                create_demo_skill_evaluations(
                    requirements.required_skills
                )
            )

            evaluations = (
                evaluation_response.evaluations
            )

            timer.checkpoint(
                "skill_evaluation"
            )

            missing_skills = [
                evaluation.skill
                for evaluation in evaluations
                if not evaluation.match
            ]

            suggestions_response = (
                create_demo_suggestions(
                    missing_skills
                )
            )

            timer.checkpoint(
                "suggestions"
            )

            match_score = calculate_match_score(
                evaluations,
                skill_weights
            )

        else:

            logger.info(
                "Checking job description cache."
            )

            cached_job = load_job_analysis(
                job_description
            )

            if cached_job is not None:

                logger.info(
                    "Cached job analysis found."
                )

                requirements = (
                    cached_job["requirements"]
                )

                skill_weights = (
                    cached_job["skill_weights"]
                )

            else:

                logger.info(
                    "No cached job analysis found. "
                    "Calling job analysis LLM."
                )

                requirements, skill_weights = (
                    analyze_job(
                        job_description
                    )
                )

                save_job_analysis(
                    job_description,
                    requirements,
                    skill_weights
                )

                logger.info(
                    "Job analysis saved to cache."
                )

            timer.checkpoint(
                "job_analysis"
            )

            logger.info(
                "Evaluating required skills."
            )

            evaluations = evaluate_skills(
                chunks,
                index,
                requirements.required_skills
            )

            timer.checkpoint(
                "skill_evaluation"
            )

            missing_skills = [
                evaluation.skill
                for evaluation in evaluations
                if not evaluation.match
            ]

            logger.info(
                "Generating improvement suggestions."
            )

            suggestions_response = (
                generate_suggestions(
                    missing_skills
                )
            )

            timer.checkpoint(
                "suggestions"
            )

            match_score = calculate_match_score(
                evaluations,
                skill_weights
            )

        timer.checkpoint(
            "scoring"
        )

        matched_skills = [
            evaluation.skill
            for evaluation in evaluations
            if evaluation.match
        ]

        performance = {
            "total_time_seconds": (
                timer.get_total_time()
            ),
            "checkpoints": (
                timer.get_checkpoints()
            )
        }

        logger.info(
            f"Resume analysis completed. "
            f"Match score: {match_score}"
        )

        return {
            "job_title": requirements.job_title,

            "match_score": match_score,

            "required_skills": (
                requirements.required_skills
            ),

            "preferred_skills": (
                requirements.preferred_skills
            ),

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "skill_analysis": [
                evaluation.model_dump()
                for evaluation in evaluations
            ],

            "suggestions": [
                suggestion.model_dump()
                for suggestion
                in suggestions_response.suggestions
            ],

            "performance": performance,

            "demo_mode": DEMO_MODE
        }

    except HTTPException:
        raise

    except openai.RateLimitError as e:

        logger.exception(
            "Groq rate limit error."
        )

        raise HTTPException(
            status_code=429,
            detail=f"Groq rate limit error: {e}"
        )

    except openai.AuthenticationError as e:

        logger.exception(
            "Groq authentication error."
        )

        raise HTTPException(
            status_code=401,
            detail=f"Groq authentication error: {e}"
        )

    except openai.APIConnectionError as e:

        logger.exception(
            "Groq connection error."
        )

        raise HTTPException(
            status_code=502,
            detail=f"Groq connection error: {e}"
        )

    except openai.APIStatusError as e:

        logger.exception(
            "Groq API status error."
        )

        raise HTTPException(
            status_code=502,
            detail=f"Groq API error: {e}"
        )

    except Exception as e:

        logger.exception(
            "Unexpected error during resume analysis."
        )

        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {e}"
        )