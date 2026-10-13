
import pandas as pd
from service.career_match import match_careers
from service.skill_extraction import extract_skills

df = pd.read_csv("data/cleaned_resumes.csv")

top1_hits = 0
top3_hits = 0
valid = 0
skipped = 0

for _, row in df.iterrows():
    actual = str(row["category"]).strip().lower()
    skills = extract_skills(str(row["resume"]))

    if not skills:
        skipped += 1
        continue

    results = match_careers(skills)
    roles = [
        str(item["role"]).strip().lower()
        for item in results
    ]

    valid += 1
    if roles and roles[0] == actual:
        top1_hits += 1
    if actual in roles:
        top3_hits += 1

print("Total resumes:", len(df))
print("Resumes evaluated:", valid)
print("Resumes skipped (no skills found):", skipped)

if valid:
    print(f"Top-1 category hit rate: {top1_hits / valid * 100:.2f}%")
    print(f"Top-3 category hit rate: {top3_hits / valid * 100:.2f}%")
else:
    print("No resumes could be evaluated.")
