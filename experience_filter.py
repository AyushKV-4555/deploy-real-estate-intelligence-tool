import re

MAX_EXPERIENCE_YEARS = 3

def extract_experience(text: str):
    """
    Extract experience range or value from text.
    Returns (min_years, max_years) or None
    """

    if not text:
        return None

    text = text.lower()

    # Match patterns like:
    # 0-2 years, 1–3 years, 2 to 4 years
    range_match = re.search(
        r"(\d+)\s*(?:-|–|to)\s*(\d+)\s*years?", text
    )
    if range_match:
        return int(range_match.group(1)), int(range_match.group(2))

    # Match patterns like:
    # 0+ years, 2+ years
    plus_match = re.search(
        r"(\d+)\s*\+\s*years?", text
    )
    if plus_match:
        years = int(plus_match.group(1))
        return years, years + 10

    # Match patterns like:
    # minimum 2 years, at least 1 year
    min_match = re.search(
        r"(minimum|at least)\s*(\d+)\s*years?", text
    )
    if min_match:
        years = int(min_match.group(2))
        return years, years

    # Match single number:
    # 1 year, 2 years
    single_match = re.search(
        r"(\d+)\s*years?", text
    )
    if single_match:
        years = int(single_match.group(1))
        return years, years

    return None


def is_fresher_role(job_text: str) -> bool:
    exp = extract_experience(job_text)

    # STRICT MODE:
    # If experience not mentioned → reject
    if exp is None:
        return False

    min_years, max_years = exp

    return min_years <= MAX_EXPERIENCE_YEARS and max_years <= MAX_EXPERIENCE_YEARS
