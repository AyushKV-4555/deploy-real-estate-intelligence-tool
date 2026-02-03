from typing import TypedDict, List, Dict


class JobAgentState(TypedDict):
    companies: List[str]
    roles: List[str]
    max_experience_years: int
    career_pages: Dict[str, str]
    scraped_pages: Dict[str, str]
    extracted_jobs: Dict[str, List[str]]
    ai_jobs: Dict[str, List[str]]
    previous_jobs: Dict[str, List[str]]
    new_jobs: Dict[str, List[str]]