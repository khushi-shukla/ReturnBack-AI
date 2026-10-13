def generate_reentry_statement(
    previous_role,
    career_break_years,
    career_break_reason,
    current_skills,
    target_role
):
    skills = ", ".join(current_skills)

    statement = (
        f"I previously worked as a {previous_role}. "
        f"I took a {career_break_years}-year career break due to "
        f"{career_break_reason}. "
        f"During my return-to-work preparation, I have developed "
        f"skills in {skills}. "
        f"I am now looking to restart my career as a {target_role} "
        f"and contribute my previous experience along with my updated skills."
    )

    return {
        "previous_role": previous_role,
        "career_break_years": career_break_years,
        "career_break_reason": career_break_reason,
        "target_role": target_role,
        "reentry_statement": statement
    }