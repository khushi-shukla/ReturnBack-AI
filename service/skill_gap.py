def calculate_skill_gap(current_skills, required_skills):
    current = {skill.lower().strip() for skill in current_skills}
    required = {skill.lower().strip() for skill in required_skills}

    matched_skills = sorted(current.intersection(required))
    missing_skills = sorted(required - current)

    if required:
        match_score = round((len(matched_skills) / len(required)) * 100, 2)
    else:
        match_score = 0

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_score": match_score
    }