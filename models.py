from dataclasses import dataclass
from typing import Optional  # for potentially missing values
from datetime import datetime  # for grabbing metadata for automation


@dataclass
class JobListing:
    """Class that will format raw data"""
    # core identification
    job_id: str
    company: str
    title: str

    # location data
    location_raw: str
    is_remote: bool = False  # for "separates remote locations into their own category"

    # filtering for trends
    department: str

    # financial data: job postings sometimes don't show the min/max for salary --> Optional
    salary_min: Optional[int] = None
    salry_max: Optional[int] = None
    currency: str = "USD"

    # metadata: checking for any new job postings each week
    date_scraped: datetime = datetime.now()
    url: str = ""
