def notify_console(new_jobs: dict):
    print("\n================ NEW AI JOB OPENINGS ================\n")

    if not new_jobs:
        print("No new AI-related job openings found today.\n")
        return

    for company, jobs in new_jobs.items():
        print(f"🏢 {company}")
        for job in jobs:
            print(f"   🔹 {job}")
        print()

    print("====================================================\n")
