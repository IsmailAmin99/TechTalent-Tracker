# TechTalent-Tracker

A tech-market intelligence pipeline designed to track hiring trends using automated web scraping, optimized data structures & regression-based salary prediction.

## My Vision

### What do I with this project?

- I want to look at hiring trends for companies that are mainly concentraed of software engineers, DS, etc.
- where is the data?: Greenhouse API for Databricks, Reddit, Duolingo, Nextdoor, Coinbase, Robinhood, Affirm, GitHub, Anthropic, Medium, Block
- what am i doing to the data?: filtering for "Data Scientist", "Data Analyst", "Engineer" titles, & extractiing 'Location' and 'Salary'. As well as tracking how often these companies are posting job opportunities to see a trend.
- where does it go?: a database; SQL

---

## Development Phases

### 1. Create a Data Model

- goal: define what each "job" will look like in the system for naming consistency
- process: create a DataClass that will store all fields I'm looking for (name,  job title, location, etc.)
  - location: be sure to include logic on handling remote locations for later modeling

### 2. Implement the Scarper

- goal: fill the data model with data
- process: script that fetches data for a single company & turn it into JobListing obj
  - Greenhouse offers API --> **requests** for web scraping (simple and inexpsensive comapred to Selenium)

#### Finding the API URL

- go to a comapany's job listing site, inspect it and find the general URL format through the Network tab (filter by Fetch and copy their URLs)
  - find the slug: unqiue name the comapny uses
  - can be found by going to their career page and looking at the last word of their URL
- process:
  - fetch function that will get us the raw data from the site
