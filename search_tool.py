from ddgs import DDGS


def find_career_page(company: str) -> str:
    query = f"{company} careers jobs"
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=1))
        if results:
            return results[0]['href']
    return ""