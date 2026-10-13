def generate_roadmap(missing_skills):
    missing_skills = [
        skill.strip()
        for skill in missing_skills
        if skill.strip()
    ]

    roadmap = []

    for skill in missing_skills:
        roadmap.append({
            "skill": skill,
            "duration": "2 weeks",
            "goal": f"Learn and practice {skill}",
            "activities": [
                f"Learn basic concepts of {skill}",
                f"Practice {skill} with small exercises",
                f"Build a mini project using {skill}"
            ]
        })

    return roadmap