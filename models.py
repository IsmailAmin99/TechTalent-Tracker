from dataclasses import dataclass, field
from typing import Optional  # for potentially missing values
from datetime import datetime  # for grabbing metadata for automation


@dataclass
class JobListing:
    """
    This class will format raw job posting data
    """
    # core identification
    job_id: str  # for database
    company: str
    title: str

    # location data
    location_raw: str
    # for "separates remote locations into their own category; betetr for visualization"
    is_remote: bool = False

    # filtering for trends --> allows filtering out non-tech roles
    department: str

    # financial data: job postings sometimes don't show the min/max for salary --> Optional
    salary_min: Optional[int] = None
    salry_max: Optional[int] = None
    currency: str = "USD"

    # metadata: checking for any new job postings over time automatically
    # default_factory: runs the funct when a new obj is created; dynamic
    date_scraped: datetime = field(default_factory=datetime.now)
    url: str = ""

    # logic for checking if a location is remote
    def __post_init__(self):
        """
        This function runs automatically after each JobListing obj is created
            - checks if a job is remote 
        """
        if "remote" in self.location_raw.lower():
            self.is_remote = True
