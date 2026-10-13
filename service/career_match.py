import pandas as pd


def match_careers(current_skills):
    df = pd.read_csv("data/role_skill_profiles.csv")

    current = {skill.lower().strip() for skill in current_skills}

    results = []

    for _, row in df.iterrows():
        role = str(row["Category"])

        required = {
            skill.lower().strip()
            for skill in str(row["required_skills"]).split(",")
            if skill.strip()
        }

        matched = sorted(current.intersection(required))
        missing = sorted(required - current)

        if required:
            score = round((len(matched) / len(required)) * 100, 2)
        else:
            score = 0

        results.append({
            "role": role,
            "match_score": score,
            "matched_skills": matched,
            "missing_skills": missing
        })

    results.sort(key=lambda x: x["match_score"], reverse=True)

    return results[:3]