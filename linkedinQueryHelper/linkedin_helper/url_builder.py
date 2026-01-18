"""LinkedIn URL building logic."""

from urllib.parse import urlencode
from typing import List, Dict
from .constants import (
    WORKPLACE_TYPE_MAP,
    DATE_POSTED_MAP,
    EXPERIENCE_LEVEL_MAP,
    JOB_TYPE_MAP,
    RECRUITMENT_TERMS_PT,
    REMOTE_WORK_TERMS_PT,
)


def apply_exclusions(tech: str, exclude_keywords: List[str]) -> str:
    """
    Append excluded keywords to tech string using LinkedIn's negative operator (-).

    Args:
        tech: Technology search string
        exclude_keywords: List of keywords to exclude

    Returns:
        Technology string with negative keywords appended
    """
    if not exclude_keywords:
        return tech

    exclusions = " ".join(f"-{kw}" for kw in exclude_keywords if kw.strip())
    return f"{tech} {exclusions}".strip()


def build_job_search_url(
    tech: str, page_number: int, exclude_keywords: List[str], filters: Dict
) -> str:
    """
    Build LinkedIn job search URL with filters.

    Args:
        tech: Technology/keyword to search
        page_number: Page number (1-indexed)
        exclude_keywords: Keywords to exclude from search
        filters: Dict with keys: easyApply, workplaceType, datePosted

    Returns:
        Complete LinkedIn job search URL
    """
    params = {}

    # Keywords - append excluded terms with minus sign
    final_keywords = apply_exclusions(tech, exclude_keywords)
    params["keywords"] = final_keywords

    # Pagination - LinkedIn uses skip (0, 25, 50, ...)
    skip = (page_number - 1) * 25
    if skip > 0:
        params["start"] = str(skip)

    # Easy Apply filter
    if filters.get("easyApply"):
        params["f_AL"] = "true"

    # Workplace Type - multiple selection
    workplace_types = filters.get("workplaceType", [])
    if workplace_types:
        values = ",".join(WORKPLACE_TYPE_MAP[wt] for wt in workplace_types)
        params["f_WT"] = values

    # Date Posted filter
    date_posted = filters.get("datePosted", "any")
    if date_posted != "any":
        params["f_TPR"] = DATE_POSTED_MAP[date_posted]

    # Experience Level (Senioridade) - multiple selection
    experience_levels = filters.get("experienceLevel", [])
    if experience_levels:
        values = ",".join(EXPERIENCE_LEVEL_MAP[level] for level in experience_levels)
        params["f_E"] = values

    # Job Type (Tipo de Contrato) - multiple selection
    job_types = filters.get("jobType", [])
    if job_types:
        values = ",".join(JOB_TYPE_MAP[jt] for jt in job_types)
        params["f_JT"] = values

    # Jobs In Your Network - flag booleana
    if filters.get("inYourNetwork"):
        params["f_JIYN"] = "true"

    return f"https://www.linkedin.com/jobs/search/?{urlencode(params)}"


def enrich_query_with_recruitment_terms(tech: str) -> str:
    """
    Enrich query with recruitment and remote work terms for content search.

    Args:
        tech: Base technology search term

    Returns:
        Enriched query string
    """
    if not tech or tech.strip() == "":
        return tech

    recruitment_terms = " OR ".join(RECRUITMENT_TERMS_PT)
    remote_terms = " OR ".join(f'"{term}"' for term in REMOTE_WORK_TERMS_PT)

    return f"{tech.strip()} ({recruitment_terms}) ({remote_terms})"


def build_content_search_url(
    tech: str, page_number: int, exclude_keywords: List[str]
) -> str:
    """
    Build LinkedIn content/post search URL.

    Args:
        tech: Technology/keyword to search
        page_number: Page number (1-indexed)
        exclude_keywords: Keywords to exclude from search

    Returns:
        Complete LinkedIn content search URL
    """
    # Apply exclusions first
    tech_with_exclusions = apply_exclusions(tech, exclude_keywords)

    # Enrich with recruitment terms
    # Note: We pass the whole string including exclusions.
    # The enrich function wraps the original tech in a way that might separate it from exclusions
    # but let's look at enrich_query_with_recruitment_terms implementation again.
    # It does: f"{tech.strip()} ({recruitment_terms}) ({remote_terms})"
    # If tech has exclusions: "React -junior (recruitment) (remote)"
    # This works for LinkedIn.
    enriched_query = enrich_query_with_recruitment_terms(tech_with_exclusions)

    # Build URL
    params = {
        "keywords": enriched_query,
    }

    # Pagination
    skip = (page_number - 1) * 25
    if skip > 0:
        params["start"] = str(skip)

    return f"https://www.linkedin.com/search/results/CONTENT/?{urlencode(params)}"
