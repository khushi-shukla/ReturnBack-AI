def generate_interview_questions(
    target_role,
    current_skills,
    career_break_years,
    profile=None
):
    profile = profile or {}

    questions = []

    # 1. Profile-based introduction
    education = profile.get("education", "")
    previous_role = profile.get("previous_role", "")
    experience = profile.get("experience_years", "")

    if previous_role:
        questions.append(
            f"Tell me about your experience as a {previous_role} "
            f"and how it relates to {target_role}."
        )
    else:
        questions.append(
            f"Tell me about yourself and why you are interested in {target_role}."
        )

    # 2. Career restart motivation
    questions.append(
        f"Why do you want to restart your career as a {target_role}?"
    )

    # 3. Career break specific questions
    try:
        break_years = float(career_break_years or 0)
    except (ValueError, TypeError):
        break_years = 0

    if break_years > 0:
        questions.append(
            f"Can you explain your {break_years:g}-year career break?"
        )

        questions.append(
            "What did you learn or develop during your career break?"
        )

        questions.append(
            "Why do you feel ready to return to the workforce now?"
        )

    # 4. Experience-based question
    if experience:
        questions.append(
            f"How does your {experience} years of experience "
            f"prepare you for this role?"
        )

    # 5. Skill-based technical questions
    for skill in current_skills[:5]:
        questions.append(
            f"How have you used {skill} in a practical project or situation?"
        )

    # 6. Role-specific question
    questions.append(
        f"What are the most important skills for a {target_role}, "
        f"and which ones are you currently improving?"
    )

    # 7. Workplace readiness
    questions.extend([
        "What are your strengths?",
        "What is one skill you are currently improving?",
        "How do you handle challenges at work?",
        "How will you manage work and personal responsibilities?",
        f"Why should we select you for the {target_role} role?"
    ])

    return {
        "target_role": target_role,
        "profile_used": {
            "education": education,
            "previous_role": previous_role,
            "experience_years": experience,
            "career_break_years": break_years
        },
        "total_questions": len(questions),
        "questions": questions
    }