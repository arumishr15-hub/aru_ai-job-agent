
import re

# Skills our application can recognize
SKILLS = [
    "python",
    "java",
    "sql",
    "docker",
    "aws",
    "react",
    "machine learning",
    "rest api",
    "git",
    "spring boot",
    "fastapi",
    "streamlit"
]


def extract_skills(text: str) -> set[str]:
    """Extract known technical skills from text."""

    found_skills = set()

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text, flags=re.IGNORECASE):
            found_skills.add(skill)

    return found_skills


def analyze_match(resume: str, job_description: str) -> dict:
    """Compare resume skills with job requirements."""

    resume_skills = extract_skills(resume)
    job_skills = extract_skills(job_description)

    matching = resume_skills & job_skills
    missing = job_skills - resume_skills

    score = (
        len(matching) / len(job_skills) * 100
        if job_skills else 0
    )

    return {
        "score": round(score, 1),
        "matching": sorted(matching),
        "missing": sorted(missing),
    }
