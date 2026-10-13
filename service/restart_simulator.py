def calculate_restart_score(
    current_skills,
    required_skills,
    career_break_years,
    interview_ready=False
):
    current = {
        skill.lower().strip()
        for skill in current_skills
        if skill and skill.strip()
    }

    required = {
        skill.lower().strip()
        for skill in required_skills
        if skill and skill.strip()
    }

    # Skill readiness: 60 points
    if required:
        matched_skills = current.intersection(required)

        skill_score = (
            len(matched_skills) / len(required)
        ) * 60
    else:
        matched_skills = set()
        skill_score = 0

    # Career break readiness: 20 points
    try:
        break_years = float(career_break_years or 0)
    except (ValueError, TypeError):
        break_years = 0

    if break_years == 0:
        experience_score = 20
    elif break_years <= 2:
        experience_score = 16
    elif break_years <= 5:
        experience_score = 12
    else:
        experience_score = 8

    # Interview readiness: 20 points
    interview_score = 20 if interview_ready else 0

    total_score = round(
        skill_score +
        experience_score +
        interview_score,
        2
    )

    return {
        "restart_score": total_score,
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(required - current),
        "skill_score": round(skill_score, 2),
        "experience_score": experience_score,
        "interview_score": interview_score,
        "max_score": 100
    }