import pandas as pd
import re


# Load skill vocabulary
skills_df = pd.read_csv("data/mvp_skill_vocabulary.csv")

skills = (
    skills_df["skill"]
    .dropna()
    .astype(str)
    .str.lower()
    .str.strip()
    .unique()
)


def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skill in skills:
        skill = skill.strip()

        if not skill:
            continue

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(set(found_skills))