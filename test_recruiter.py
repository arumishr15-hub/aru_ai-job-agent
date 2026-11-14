
from recruiter_finder import find_recruiters


company = "Microsoft"
job_title = "Software Engineer"

results = find_recruiters(company, job_title)

print(f"Found {len(results)} potential profiles")

for recruiter in results:
    print("\nName:", recruiter["name"])
    print("LinkedIn:", recruiter["url"])
