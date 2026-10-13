
def career_chatbot(message, profile=None, skills=None, career_matches=None):
    message = message.lower().strip()

    if not message:
        return "Please type a message so I can help you."

    profile = profile or {}
    skills = skills or []
    career_matches = career_matches or []

    # Startup and business guidance
    if any(word in message for word in [
        "startup", "start my company", "own company",
        "business idea", "entrepreneur", "founder"
    ]):
        return (
            "Here is your startup roadmap:\n\n"
            "1. Identify a real problem people face.\n"
            "2. Choose an idea based on your skills and interests.\n"
            "3. Research customers and competitors.\n"
            "4. Build a small MVP (Minimum Viable Product).\n"
            "5. Test it with real users and collect feedback.\n"
            "6. Calculate costs, pricing and expected revenue.\n"
            "7. Improve your product and grow gradually.\n\n"
            "Start small and validate your idea before investing heavily."
        )

    # Business plan and budget
    if any(word in message for word in [
        "business plan", "budget", "business cost",
        "profit", "pricing", "revenue"
    ]):
        return (
            "A simple business plan should include:\n\n"
            "1. Business idea and problem solved.\n"
            "2. Target customers.\n"
            "3. Competitor research.\n"
            "4. Startup costs and monthly expenses.\n"
            "5. Product pricing and expected sales.\n"
            "6. Marketing and customer acquisition.\n"
            "7. Revenue goals and risks.\n\n"
            "Your actual budget depends on your business type. "
            "Estimate costs before making financial commitments."
        )

    # Funding
    if any(word in message for word in [
        "funding", "investor", "investment", "loan", "raise money"
    ]):
        return (
            "To explore startup funding:\n\n"
            "1. Validate your idea with potential customers.\n"
            "2. Prepare a business plan and cost estimate.\n"
            "3. Build a prototype if possible.\n"
            "4. Explore bootstrapping, incubators, grants "
            "and suitable investor opportunities.\n"
            "5. Compare repayment terms and risks before taking a loan.\n\n"
            "Funding is not guaranteed. Verify eligibility and terms "
            "before applying."
        )

    # Marketing and customers
    if any(word in message for word in [
        "marketing", "customers", "customer", "promote",
        "sales", "social media"
    ]):
        return (
            "To find your first customers:\n\n"
            "1. Define exactly who needs your product.\n"
            "2. Speak with potential customers.\n"
            "3. Create a simple website or social media page.\n"
            "4. Demonstrate your product and its benefits.\n"
            "5. Ask for feedback and referrals.\n"
            "6. Track which marketing activities bring genuine customers.\n\n"
            "Start with a small experiment before spending heavily on ads."
        )

    # Career and job guidance
    if any(word in message for word in [
        "career", "job", "role", "profession"
    ]):
        if career_matches:
            roles = [
                item["role"]
                for item in career_matches[:3]
                if item.get("role")
            ]
            if roles:
                return (
                    "Based on your analyzed profile, possible career roles are: "
                    + ", ".join(roles)
                    + ". Compare their requirements and choose one to explore."
                )

        return (
            "Upload your resume for personalized career suggestions. "
            "You can also tell me your education, interests and target role."
        )

    # Personalized skills and learning roadmap
    if any(word in message for word in [
        "skill", "skills", "learn", "course", "roadmap", "what should i study"
    ]):
        if skills:
            return (
                "Your detected skills include: "
                + ", ".join(skills[:10])
                + ".\n\nChoose a target role, check its required skills, "
                "learn the missing skills in order, practise with projects "
                "and add your work to your portfolio."
            )

        return (
            "Upload your resume so I can use your detected skills "
            "to guide your learning. You can also tell me your target career."
        )

    # Business career options
    if any(word in message for word in [
        "freelance", "freelancing", "self employed", "side hustle"
    ]):
        return (
            "To explore freelancing:\n\n"
            "1. Choose a service you can deliver.\n"
            "2. Build two or three portfolio projects.\n"
            "3. Define your target clients and pricing.\n"
            "4. Create a professional portfolio.\n"
            "5. Start with small projects and request honest feedback.\n\n"
            "Examples include web development, design, writing and data analysis."
        )

    # Resume guidance
    if any(word in message for word in ["resume", "cv"]):
        return (
            "Improve your resume with clear skills, relevant projects, "
            "education and measurable achievements. Keep the layout readable "
            "and tailor it to each role. Explain a career break honestly "
            "and focus on your readiness to return."
        )

    # Interview coaching
    if any(word in message for word in [
        "interview", "interviewing", "interview questions"
    ]):
        return (
            "Interview preparation plan:\n\n"
            "1. Practise your introduction.\n"
            "2. Review the skills listed on your resume.\n"
            "3. Prepare examples of projects and achievements.\n"
            "4. Practise common technical and behavioural questions.\n"
            "5. Prepare a clear explanation of your career journey.\n"
            "6. Ask the interviewer thoughtful questions."
        )

    # Career break and return to work
    if any(word in message for word in [
        "career break", "career gap", "employment gap", "return to work"
    ]):
        years = profile.get("career_break_years")

        return (
            f"Your detected career break is {years} years. "
            if years not in (None, "")
            else "A career break does not define your ability. "
        ) + (
            "Refresh relevant skills, build a recent project, update your "
            "resume and practise explaining your return positively. "
            "Focus on what you can contribute now."
        )

    # Women career re-entry support
    if any(word in message for word in [
        "women", "woman", "work from home", "returnship",
        "confidence", "restart my career"
    ]):
        return (
            "For restarting your career, consider returnship programmes, "
            "remote roles where suitable, internships and skill-refresh courses. "
            "Update your resume, build a recent project and practise interviews. "
            "Choose opportunities that fit your skills, schedule and goals. "
            "Verify job offers and never pay an employer to secure a job."
        )

    # Profile guidance
    if any(word in message for word in [
        "profile", "experience", "education"
    ]):
        if profile:
            return (
                f"Education: {profile.get('education') or 'Not detected'}\n"
                f"Experience: {profile.get('experience_years') or '0'} years\n"
                f"Career break: {profile.get('career_break_years') or '0'} years"
            )

        return "Upload your resume first so I can analyze your profile."

    # Greeting
    if any(word in message.split() for word in ["hi", "hello", "hey"]):
        return (
            "Hi! Welcome to ReturnBack AI. I can help with career planning, "
            "skills, resumes, interviews, startup ideas, business plans, "
            "funding basics and career re-entry. What would you like help with?"
        )

    # Default response
    return (
        "I can help with career guidance, skill development, resumes, "
        "interviews, startup planning, business budgets, funding basics, "
        "marketing and career re-entry.\n\n"
        "Try asking: 'How do I start a business?' or "
        "'How can I restart my career?'"
    )
