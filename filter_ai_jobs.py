from tools.strict_matcher import is_strict_ai_role
from tools.experience_filter import is_fresher_role

def filter_ai_roles(jobs, roles, company):
    filtered = []

    for job in jobs:
        title = job.get("title", "")
        description = job.get("description", "")
        full_text = f"{title} {description}"

        # 1️⃣ Strict AI title check
        if not is_strict_ai_role(title):
            continue

        # 2️⃣ Strict experience check (≤ 3 years)
        if not is_fresher_role(full_text):
            continue

        filtered.append({
            "company": company,
            "title": title,
            "date_posted": job.get("date_posted", "Unknown"),
            "experience": "≤ 3 years"
        })

    return filtered
