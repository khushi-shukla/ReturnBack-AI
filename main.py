import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from service.rp import extract_resume_text
from service.skill_extraction import extract_skills
from service.upskilling import generate_roadmap
from service.skill_gap import calculate_skill_gap
from service.career_match import match_careers
from service.chatbot import career_chatbot
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from service.profile_analysis import extract_profile
from service.career_reentry import generate_reentry_statement
from service.interview_agent import generate_interview_questions
from service.restart_simulator import calculate_restart_score
from database import create_tables
from database import get_connection
app = FastAPI(title="ReturnBack AI")
create_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return {
        "message": "ReturnBack AI Backend is Running!"
    }
@app.get("/health")
def health():
    return {
        "status": "OK"
    }
@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    allowed_extensions = {
        ".pdf",
        ".docx",
        ".jpg",
        ".jpeg",
        ".png"
    }

    filename = file.filename or ""
    extension = os.path.splitext(filename)[1].lower()

    # File validation
    if not filename:
        raise HTTPException(
            status_code=400,
            detail="Please upload a resume file."
        )

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload PDF, DOCX, JPG, JPEG or PNG."
        )

    try:
        # Save uploaded file
        os.makedirs("uploads", exist_ok=True)

        file_path = os.path.join("uploads", filename)

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Extract resume text
        text = extract_resume_text(file_path)

        if not text or not text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the resume. Please upload a clear resume."
            )

        # Extract skills and profile
        skills = extract_skills(text)
        profile = extract_profile(text)

        # Career matches
        career_matches = match_careers(skills)

        # Target role
        target_role = (
            career_matches[0]["role"]
            if career_matches
            else "Software Developer"
        )

        # Interview questions
        interview_questions = generate_interview_questions(
            target_role,
            skills,
            profile.get("career_break_years", "0"),
            profile
        )

        # Career re-entry statement
        reentry_statement = generate_reentry_statement(profile)

        # Required skills
        required_skills = [
            "python",
            "sql",
            "excel",
            "power bi",
            "statistics"
        ]

        # Skill gap
        skill_gap = calculate_skill_gap(
            skills,
            required_skills
        )

        # Skill Progress Tracker
        skill_progress = []

        for skill in required_skills:

            if skill.lower() in [s.lower() for s in skills]:
                progress = 100
            else:
                progress = 0

            skill_progress.append({
                "skill": skill,
                "progress": progress
            })
        # Safe career break value
        try:
            break_years = float(
                profile.get("career_break_years") or 0
            )
        except (ValueError, TypeError):
            break_years = 0
        # Restart Simulator
        restart_score = calculate_restart_score(
            skills,
            required_skills,
            break_years,
            False
        )
        # Save profile to database
        connection = get_connection()
        try:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO profiles (
                    filename,
                    education,
                    previous_role,
                    experience_years,
                    career_break_years,
                    career_break_reason,
                    restart_score
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                filename,
                profile.get("education", ""),
                profile.get("previous_role", ""),
                profile.get("experience_years", ""),
                profile.get("career_break_years", ""),
                profile.get("career_break_reason", ""),
                restart_score.get("restart_score", 0)
            ))

            connection.commit()

        finally:
            connection.close()

        # Final response
        return {
            "filename": filename,
            "message": "Resume uploaded successfully!",
            "extracted_text": text,
            "skills": skills,
            "profile": profile,
            "career_matches": career_matches,
            "skill_gap": skill_gap,
            "skill_progress": skill_progress,
            "restart_score": restart_score,
            "reentry_statement": reentry_statement,
            "interview_questions": interview_questions
        }

    except HTTPException:
        raise

    except Exception as e:

        print("Resume processing error:", e)

        raise HTTPException(
            status_code=500,
            detail="Something went wrong while processing the resume. Please try again."
        )
@app.get("/profile-history")
def profile_history():

    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                filename,
                education,
                previous_role,
                experience_years,
                career_break_years,
                career_break_reason,
                restart_score
            FROM profiles
            ORDER BY id DESC
        """)
        rows = cursor.fetchall()
        history = []
        for row in rows:
            history.append({
                "id": row[0],
                "filename": row[1],
                "education": row[2],
                "previous_role": row[3],
                "experience_years": row[4],
                "career_break_years": row[5],
                "career_break_reason": row[6],
                "restart_score": row[7]
            })
        return {
            "history": history
        }
    except Exception as e:

        print("Profile history error:", e)

        raise HTTPException(
            status_code=500,
            detail="Unable to load profile history. Please try again."
        )
    finally:

        if connection:
            connection.close()
@app.post("/upskill")
def create_upskill_roadmap(missing_skills: list[str]):
    print("Received missing skills:", missing_skills)
    try:
        roadmap = generate_roadmap(missing_skills)
        print("Generated roadmap:", roadmap)

        return {"roadmap": roadmap}
    except Exception as e:
        print("Roadmap generation error:", repr(e))
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
class ChatRequest(BaseModel):
    message: str
    profile: dict = {}
    skills: list = []
    career_matches: list = []
@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    try:
        answer = career_chatbot(
            request.message,
            profile=request.profile,
            skills=request.skills,
            career_matches=request.career_matches
        )
        return {"response": answer}
    except Exception as e:
        print("Chatbot error:", repr(e))
        raise HTTPException(
            status_code=500,
            detail="Unable to generate a response."
        )
class InterviewQuestionsRequest(BaseModel):
    target_role: str = "Software Developer"
    current_skills: list[str] = []
    career_break_years: float = 0
    profile: dict = {}
@app.post("/interview/questions")
def get_interview_questions(request: InterviewQuestionsRequest):
    try:
        result = generate_interview_questions(
            request.target_role,
            request.current_skills,
            request.career_break_years,
            request.profile
        )
        return result
    except Exception as e:
        print("Interview questions error:", repr(e))
        raise HTTPException(
            status_code=500,
            detail="Unable to generate interview questions."
        )
class InterviewEvaluationRequest(BaseModel):
    question: str
    answer: str
    target_role: str = "Software Developer"
@app.post("/interview/evaluate")
def evaluate_interview_answer(request: InterviewEvaluationRequest):
    answer = request.answer.strip()

    if not answer:
        raise HTTPException(
            status_code=400,
            detail="Please write your answer first."
        )

    # Basic rule-based evaluation
    words = answer.split()
    word_count = len(words)

    score = 2
    if word_count >= 20:
        score += 2
    if word_count >= 50:
        score += 2

    keywords = [
        "because", "example", "experience",
        "project", "skill", "learn", "result",
        "problem", "solution", "team"
    ]

    matched_keywords = sum(
        1 for word in keywords
        if word in answer.lower()
    )
    score += min(matched_keywords, 4)
    score = min(score, 10)

    if word_count < 20:
        feedback = "Your answer is too short. Explain your point in more detail."
        suggestion = "Write 3–5 sentences and include a relevant example."
    elif matched_keywords < 2:
        feedback = "Good start, but your answer needs more specific details."
        suggestion = "Include the situation, your action, and the result."
    else:
        feedback = "Your answer includes useful details. Keep it clear and structured."
        suggestion = "Add a specific example related to the target role."

    return {
        "score": score,
        "feedback": feedback,
        "suggestion": suggestion
    }