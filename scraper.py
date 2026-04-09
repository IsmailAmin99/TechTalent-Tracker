import requests
import time
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
        # check to see if 'departments' exists & isn't empty
        # if dept exists grab the name, otherwise list as general
        depts = item.get('departments', [])

        if depts and len(depts) > 0:
            dept_name = depts[0].get('name', 'General')
        else:
            dept_name = 'General'

        # map data keys to JobListing fields; will trigger __post_init__ for remote logic
        job = JobListing(
            job_id=str(item['id']),
            company="Anthropic",
            title=item.get('title', 'Unknown Title'),
            location_raw=item.get('location', {}).get('name', 'Remote'),
            department=dept_name
        )
        clean_list.append(job)
    return clean_list

# fetch function to get job details


def fetch_job_details(job_id):
    """Grabs the individual job API to get salary and full content"""
    # ?content=true to get the description from Greenhouse
    url = f"https://boards-api.greenhouse.io/v1/boards/anthropic/jobs/{job_id}?content=true"

    try:
        r = requests.get(url)
        # convert job text to a dictionary
        item = r.json()

        # access pay ranges list from the Network tab
        pay_info = item.get('pay_ranges', [{}])[0]

        # store info into a dictionary to handle sparse data (missing data)
        # .get() the script will return None instead of crashing --> keeps automation robust
        return {
            "salary_min": pay_info.get('min'),
            "salary_max": pay_info.get('max'),
            "description": item.get('content')
        }
    except Exception as e:
        print(f"Error minin details for {job_id}: {e}")
        return {}


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

            # test the mining
            print("\n--- Mining Detailed Data (First 3 Jobs) ---")
            for i in range(3):
                target_job = cleaned_jobs[i]
                # bridge the general list & the mined data
                details = fetch_job_details(target_job.job_id)

                # update obj with data
                target_job.salary_min = details.get('salary_min')
                target_job.salary_max = details.get('salary_max')

                print(f"Fetched: {target_job.title}")
                print(
                    f"Salary Range: {target_job.salary_min} - {target_job.salary_max}")

                time.sleep(1)  # 1-sec pause between scrape

    except Exception as e:
        print(f"Test Failed: {e}")
