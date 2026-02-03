from graph import build_graph

if __name__ == "__main__":
    agent = build_graph()

    agent.invoke({
        "companies": [
            "Observe.AI",
            "Snowflake",
            "Confluent"
        ],
        "roles": [
            "AI Engineer",
            "ML Engineer",
            "Data Analyst",
            "Data Scientist"
        ],
        "max_experience_years": 3,
        "career_pages": {},
        "scraped_pages": {},
        "extracted_jobs": {},
        "ai_jobs": {},
        "previous_jobs": {},
        "new_jobs": {}
    })

