from service.skill_gap import calculate_skill_gap
from service.career_match import match_careers
from service.upskilling import generate_roadmap
from service.resume_reentry import generate_reentry_statement
from service.interview_agent import generate_interview_questions
from service.restart_simulator import calculate_restart_score


def generate_career_plan(
    current_skills,
    target_role,
    required_skills,
    previous_role,
    career_break_years,
    career_break_reason
):
    # 1. Skill Gap
    skill_gap = calculate_skill_gap(
        current_skills,
        required_skills
    )

    # 2. Upskilling Roadmap
    roadmap = generate_roadmap(
        skill_gap["missing_skills"]
    )

    # 3. Resume Re-entry Statement
    reentry = generate_reentry_statement(
        previous_role,
        career_break_years,
        career_break_reason,
        current_skills,
        target_role
    )

    # 4. Interview Questions
    interview = generate_interview_questions(
        target_role,
        current_skills,
        career_break_years
    )

    # 5. Restart Score
    restart = calculate_restart_score(
        current_skills,
        required_skills,
        career_break_years,
        False
    )

    return {
        "target_role": target_role,
        "skill_gap": skill_gap,
        "upskilling_roadmap": roadmap,
        "resume_reentry": reentry,
        "interview_questions": interview,
        "restart_simulator": restart
    }