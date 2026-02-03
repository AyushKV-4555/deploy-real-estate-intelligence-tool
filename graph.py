from langgraph.graph import StateGraph
from state import JobAgentState
from tools.search_tool import find_career_page
from tools.scraper import scrape_page
from tools.job_extractor import extract_jobs
from tools.filter_ai_jobs import filter_ai_roles
from memory import load_memory, save_memory
from tools.notify import notify_console


def build_graph():
    graph = StateGraph(JobAgentState)

    def discover_pages(state):
        state['career_pages'] = {}
        for c in state['companies']:
            state['career_pages'][c] = find_career_page(c)
        return state

    def scrape(state):
        state['scraped_pages'] = {}
        for c, url in state['career_pages'].items():
            if url:
                state['scraped_pages'][c] = scrape_page(url)
        return state
    
    def extract(state):
        state['extracted_jobs'] = {}

        for c, text in state['scraped_pages'].items():
            jobs = extract_jobs(text)

            # Ensure LLM returned a list
            if not isinstance(jobs, list):
                jobs = []

            state['extracted_jobs'][c] = jobs

            print(f"\n--- RAW EXTRACTED JOBS FOR {c} ---")
            for j in jobs:
                print(f"• {j.get('title')}")

        return state

    
    def filter_jobs(state):
        state['ai_jobs'] = {}
        for c, jobs in state['extracted_jobs'].items():
            state['ai_jobs'][c] = filter_ai_roles(jobs, state['roles'], c)

        return state


    def compare(state):
        memory = load_memory()
        state['new_jobs'] = {}
        for c, jobs in state['ai_jobs'].items():
            old = memory.get(c, [])
            diff = [j for j in jobs if j not in old]
            if diff:
                state['new_jobs'][c] = diff
            memory[c] = jobs
        save_memory(memory)
        return state


    def notify(state):
        if state['new_jobs']:
            notify_console(state['new_jobs'])
        else:
            notify_console({})
        return state

    
    graph.add_node("discover", discover_pages)
    graph.add_node("scrape", scrape)
    graph.add_node("extract", extract)
    graph.add_node("filter", filter_jobs)
    graph.add_node("compare", compare)
    graph.add_node("notify", notify)


    graph.set_entry_point("discover")
    graph.add_edge("discover", "scrape")
    graph.add_edge("scrape", "extract")
    graph.add_edge("extract", "filter")
    graph.add_edge("filter", "compare")
    graph.add_edge("compare", "notify")

    return graph.compile()