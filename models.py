from dataclasses import dataclass
from typing import Optional # for potentially missing values

@dataclass
class JobListing:
    """Class that will format raw data"""
    job_id: str
    company: str
    title: str
    location: str
    department: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None