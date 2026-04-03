# Recruiter Intelligence Platform – Case Study

## Deliverables
- pipeline.py – Python script
- allset_jobs.csv – Normalized output
- part-1-notes.md – Part 1 details
- Part-2.md – Design notes (talent schema, enrichment, matching, hiring intent)
- Part-3.md – RAG assistant design
- images/ – Diagrams

## How to Run Locally

1. Install Python 3.8+ 
2. Install dependencies (only pandas required):

## Schema of allset_jobs.csv
- id – int
- title – string
- company – string
- city – string or None
- region – string or None
- country – string or None
- remote_status – enum: remote, hybrid, onsite, None
- employment_contract – enum: permanent, contract, None
- employment_time – enum: full_time, part_time, None
- salary_min – float or None
- salary_max – float or None
- salary_currency – string or None
- salary_period – enum: year, month, hour, None
- date_posted – date (YYYY-MM-DD) or None
- skills – string or None (comma‑separated)
- industry – string or None
- seniority – enum: senior, mid, junior, None
- description – string
- source – enum: reed, naukri, dice
