import requests
from models import JobListing


def fetch_anthropic_jobs():
    url = "https://boards-api.greenhouse.io/v1/boards/anthropic/jobs"

    # fetch the raw JSON
    r = requests.get(url)
    data = r.json()  # .json() converts the text to a dictionary; for efficient parsing

    # return only the jobs in the dictionary
    return data['jobs']


def parse_anthropic_jobs(raw_jobs):
    clean_list = []
    for item in raw_jobs:
        # map data keys to JobListing fields; will trigger __post_init__ for remote logic
        job = JobListing(
            job_id=str(item['id']),
            company="Anthropic",
            title=item['title'],
            location_raw=item['location']['name'],
            department=item.get('departments', {})[
                0].get('name', 'AI Research')
        )
        clean_list.append(job)
    return clean_list


if __name__ == "__main__":
    print("--- Starting Test ---")

    # test the fetch function
    try:
        raw_data = fetch_anthropic_jobs()
        print(f"Success: Found {len(raw_data)} raw jobs")

        # test the parse function
        cleaned_jobs = parse_anthropic_jobs(raw_data)
        print(f"Success: Parsed {len(cleaned_jobs)} JobListing objects")

        # look at a sample
        if cleaned_jobs:
            sample = cleaned_jobs[0]
            print(f"\nSample Job Details:")
            print(f"Title: {sample.title}")
            print(f"Location: {sample.location_raw}")
            print(f"Is Remote: {getattr(sample, 'is_remote', 'N/A')}")

    except Exception as e:
        print(f"Test Failed: {e}")
