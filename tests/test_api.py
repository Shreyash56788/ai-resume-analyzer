from fastapi.testclient import TestClient

from app.api import app


client = TestClient(app)


def test_reject_non_pdf_resume():

    response = client.post(
        "/analyze",
        files={
            "resume": (
                "resume.txt",
                b"This is not a PDF resume.",
                "text/plain"
            )
        },
        data={
            "job_description": "Looking for a Python developer."
        }
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "Only PDF resumes are supported."
    )


def test_reject_empty_job_description():

    response = client.post(
        "/analyze",
        files={
            "resume": (
                "resume.pdf",
                b"fake pdf content",
                "application/pdf"
            )
        },
        data={
            "job_description": ""
        }
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "Job description cannot be empty."
    )


def test_reject_empty_resume():

    response = client.post(
        "/analyze",
        files={
            "resume": (
                "resume.pdf",
                b"",
                "application/pdf"
            )
        },
        data={
            "job_description": "Looking for a Python developer."
        }
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "Uploaded resume is empty."
    )