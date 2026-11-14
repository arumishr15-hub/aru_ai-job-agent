
import json
import os
import re
from urllib.parse import urlparse

from dotenv import load_dotenv
from ollama import chat
from tavily import TavilyClient


# Load the Tavily API key from .env
load_dotenv()


# ==========================================
# 1. EXTRACT JOB DETAILS USING OLLAMA
# ==========================================

def extract_job_details(jd: str) -> dict:
    """Extract company and job title from a JD."""

    response = chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract the hiring company and job title "
                    "from the provided job description. "
                    "Return only JSON with keys company "
                    "and job_title. Use empty strings "
                    "when unknown. Never invent details."
                ),
            },
            {
                "role": "user",
                "content": jd[:3000],
            },
        ],
        format="json",
        think=False,
        options={
            "temperature": 0,
            "num_predict": 100,
        },
    )

    data = json.loads(
        response.message.content or "{}"
    )

    return {
        "company": str(
            data.get("company") or ""
        ).strip(),
        "job_title": str(
            data.get("job_title") or ""
        ).strip(),
    }


# ==========================================
# 2. DETECT RECRUITING SPECIALIZATION
# ==========================================

def get_specialty(job_title: str) -> str:
    """Choose recruiter keywords based on the job."""

    title = job_title.lower()

    if any(term in title for term in [
        "data scientist",
        "data analyst",
        "machine learning",
        "artificial intelligence",
        "ai engineer",
    ]):
        return "technical recruiter"

    if any(term in title for term in [
        "software",
        "developer",
        "backend",
        "frontend",
        "full stack",
        "java",
        "python",
        "engineer",
    ]):
        return "technical recruiter"

    if "product manager" in title:
        return "product recruiter"

    if any(term in title for term in [
        "designer",
        "ux",
        "ui design",
    ]):
        return "design recruiter"

    return "talent acquisition"


# ==========================================
# 3. CLEAN RECRUITER NAMES
# ==========================================

def clean_recruiter_name(title: str) -> str:
    """Extract a readable name from a search title."""

    name = title.split(" - ")[0]
    name = name.split(" | ")[0]

    name = name.replace(" | LinkedIn", "")

    return name.strip()


# ==========================================
# 4. EVALUATE PUBLIC SEARCH EVIDENCE
# ==========================================

def evaluate_recruiter(
    title: str,
    description: str,
    company: str,
    job_title: str,
) -> dict:
    """Estimate relevance using public search text."""

    text = f"{title} {description}".lower()

    points = 0
    evidence = []

    company_pattern = (
        r"(?<!\w)"
        + re.escape(company.lower())
        + r"(?!\w)"
    )

    # Company match
    if re.search(company_pattern, text):
        points += 3
        evidence.append(
            "Hiring company mentioned in search result"
        )

    # Recruiting role match
    recruiter_terms = [
        "recruiter",
        "recruiting",
        "talent acquisition",
        "talent partner",
        "sourcer",
        "staffing",
    ]

    if any(term in text for term in recruiter_terms):
        points += 2
        evidence.append(
            "Recruiting experience mentioned"
        )

    # Specialization match
    specialty = get_specialty(job_title)

    specialty_keywords = {
        "technical recruiter": [
            "technical recruiter",
            "technical recruiting",
            "engineering recruiter",
            "engineering recruiting",
            "software engineering",
            "tech talent",
        ],
        "product recruiter": [
            "product recruiter",
            "product recruiting",
            "product talent",
        ],
        "design recruiter": [
            "design recruiter",
            "design recruiting",
            "ux recruiting",
        ],
        "talent acquisition": [
            "talent acquisition",
            "recruiter",
        ],
    }

    terms = specialty_keywords.get(
        specialty,
        [],
    )

    if any(term in text for term in terms):
        points += 3
        evidence.append(
            "Relevant recruiting specialization mentioned"
        )

    if points >= 8:
        relevance = "Stronger lead"
    elif points >= 5:
        relevance = "Possible lead"
    else:
        relevance = "Limited evidence"

    return {
        "relevance": relevance,
        "points": points,
        "evidence": evidence,
        "verified_for_job": False,
    }


# ==========================================
# 5. FIND NAMED RECRUITERS USING TAVILY
# ==========================================

def find_recruiters(
    company: str,
    job_title: str,
) -> list:
    """Find, deduplicate, and rank recruiter profiles."""

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise ValueError(
            "TAVILY_API_KEY missing from .env"
        )

    client = TavilyClient(api_key=api_key)

    specialty = get_specialty(job_title)

    # Broad searches preserve more named profiles.
    # Specialized search helps identify relevant leads.
    queries = [
        (
            f'site:linkedin.com/in/ "{company}" '
            f'recruiter'
        ),
        (
            f'site:linkedin.com/in/ "{company}" '
            f'"talent acquisition"'
        ),
        (
            f'site:linkedin.com/in/ "{company}" '
            f'"{specialty}"'
        ),
    ]

    recruiters_by_url = {}

    for query in queries:

        response = client.search(
            query=query,
            search_depth="basic",
            max_results=8,
        )

        for item in response.get("results", []):

            url = item.get("url", "")

            parsed = urlparse(url)

            hostname = (
                parsed.hostname or ""
            ).lower()

            # Keep only LinkedIn person profiles.
            if hostname not in [
                "linkedin.com",
                "www.linkedin.com",
            ]:
                continue

            if not parsed.path.startswith("/in/"):
                continue

            profile_path = parsed.path.rstrip("/")

            clean_url = (
                "https://www.linkedin.com"
                + profile_path
            )

            title = item.get("title", "")
            description = item.get("content", "")

            name = clean_recruiter_name(title)

            # Skip results without a readable title.
            if not name:
                continue

            evaluation = evaluate_recruiter(
                title,
                description,
                company,
                job_title,
            )

            recruiter = {
                "name": name,
                "role": title,
                "description": description,
                "url": clean_url,
                **evaluation,
            }

            previous = recruiters_by_url.get(
                clean_url
            )

            # Keep the more informative result
            # if multiple searches find one person.
            if (
                previous is None
                or recruiter["points"] > previous["points"]
            ):
                recruiters_by_url[
                    clean_url
                ] = recruiter

    recruiters = list(
        recruiters_by_url.values()
    )

    # Higher relevance first
    recruiters.sort(
        key=lambda recruiter: recruiter["points"],
        reverse=True,
    )

    return recruiters[:8]
