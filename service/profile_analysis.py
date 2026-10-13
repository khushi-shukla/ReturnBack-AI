import re


def extract_profile(text):
    text_lower = text.lower()

    profile = {
        "education": "",
        "previous_role": "",
        "experience_years": "",
        "career_break_years": "",
        "career_break_reason": ""
    }

    # Education
    education_patterns = [
        r"(b\.?tech|bachelor of technology)",
        r"(b\.?e\.?|bachelor of engineering)",
        r"(m\.?tech|master of technology)",
        r"(bca|bachelor of computer applications)",
        r"(mca|master of computer applications)",
        r"(mba|master of business administration)"
    ]

    for pattern in education_patterns:
        match = re.search(pattern, text_lower)
        if match:
            profile["education"] = match.group(0)
            break

    # Experience
    experience_match = re.search(
        r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)\s*(?:of)?\s*experience",
        text_lower
    )

    if experience_match:
        profile["experience_years"] = experience_match.group(1)

    # Previous role
    role_patterns = [
        "software engineer",
        "software developer",
        "web developer",
        "data analyst",
        "data scientist",
        "business analyst",
        "python developer",
        "java developer",
        "machine learning engineer",
        "project manager",
        "teacher",
        "developer"
    ]

    for role in role_patterns:
        if role in text_lower:
            profile["previous_role"] = role.title()
            break

    # Career break
    break_match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\s*(?:career\s*)?(?:break|gap)",
        text_lower
    )

    if break_match:
        profile["career_break_years"] = break_match.group(1)

    # Career break reason
    reasons = [
        "parenting",
        "childcare",
        "family",
        "maternity",
        "health",
        "personal reasons",
        "relocation",
        "marriage"
    ]

    for reason in reasons:
        if reason in text_lower:
            profile["career_break_reason"] = reason.title()
            break

    return profile