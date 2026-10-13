def generate_reentry_statement(profile):
    role = profile.get("previous_role", "")
    break_years = profile.get("career_break_years", "")
    reason = profile.get("career_break_reason", "")

    if not break_years:
        return "No career break detected."

    if reason:
        return (
            f"Took a {break_years}-year career break due to {reason.lower()} "
            f"and am now ready to resume my professional career"
            + (f" in {role.lower()}." if role else ".")
        )

    return (
        f"Took a {break_years}-year career break and am now ready "
        f"to resume my professional career"
        + (f" in {role.lower()}." if role else ".")
    )