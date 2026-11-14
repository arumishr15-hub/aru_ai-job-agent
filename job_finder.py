
import os

from dotenv import load_dotenv
from tavily import TavilyClient


load_dotenv()


def get_client():
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise ValueError("TAVILY_API_KEY missing from .env")

    return TavilyClient(api_key=api_key)


def search_jobs(role: str, location: str, work_mode: str) -> list:
    """Search the web for job postings."""

    client = get_client()

    query = (
        f"{role} jobs hiring "
        f"{location} {work_mode} "
        "apply careers job description"
    )

    response = client.search(
        query=query,
        search_depth="basic",
        max_results=8,
    )

    jobs = []

    for item in response.get("results", []):
        title = item.get("title", "")
        url = item.get("url", "")

        if not title or not url:
            continue

        jobs.append({
            "title": title,
            "url": url,
            "summary": item.get("content", ""),
        })

    return jobs


def fetch_job_description(url: str) -> str:
    """Retrieve text from the selected job posting."""

    client = get_client()

    response = client.extract(urls=[url])

    results = response.get("results", [])

    if not results:
        raise ValueError(
            "Could not extract this job page. "
            "Try another posting."
        )

    content = results[0].get("raw_content", "")

    if not content or len(content.strip()) < 100:
        raise ValueError(
            "The full job description was not available."
        )

    return content.strip()
