function scrollToUpload() {
    const uploadSection = document.getElementById("upload");
    if (uploadSection) {
        uploadSection.scrollIntoView({ behavior: "smooth" });
    }
}

window.currentProfile = null;
window.currentSkills = [];
window.currentCareerMatches = [];
window.currentMissingSkills = [];
window.interviewQuestions = [];
window.currentInterviewQuestionIndex = 0;
window.interviewAttempts = {};

async function uploadResume() {
    const fileInput = document.getElementById("resumeFile");
    const status = document.getElementById("uploadStatus");

    if (!fileInput || !status) {
        console.error("Resume input or status element is missing.");
        return;
    }

    if (!fileInput.files || fileInput.files.length === 0) {
        status.innerText = "Please select a resume first.";
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    status.innerText = "Analyzing your resume...";

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/upload-resume",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Resume analysis failed.");
        }

        window.currentProfile = data.profile || null;
        window.currentSkills = data.skills || [];
        window.currentCareerMatches = data.career_matches || [];
        window.currentMissingSkills = data.skill_gap?.missing_skills || [];

        status.innerText = "Resume uploaded successfully!";

        setText("dashboardScore", data.restart_score?.restart_score ?? "--");
        setText("skillsCount", window.currentSkills.length);
        setText("careerCount", window.currentCareerMatches.length);
        setText("matchCount", data.skill_gap?.match_score ?? "--");

        const progress = document.getElementById("scoreProgress");
        if (progress) {
            progress.style.width =
                `${data.restart_score?.restart_score ?? 0}%`;
        }

        showSkills(window.currentSkills);
        showCareerMatches(window.currentCareerMatches);
        showSkillGap(data.skill_gap);
        showSkillProgress(data.skill_progress);
        showProfile(data.profile);
        showReentryStatement(data.reentry_statement);
        showRestartScore(data.restart_score);
        showDashboard(data);

        const interviewData = data.interview_questions;
        window.interviewQuestions =
            interviewData?.questions || [];

        window.currentInterviewQuestionIndex = 0;
        window.interviewAttempts = {};

        setText(
            "currentInterviewQuestion",
            window.interviewQuestions.length
                ? window.interviewQuestions[0]
                : "Upload your resume to get interview questions."
        );

        setText("interviewFeedback", "");

        renderInterviewQuestions();
        window.updateInterviewSessionScore();

        const results = document.getElementById("results");
        if (results) {
            results.scrollIntoView({ behavior: "smooth" });
        }

        console.log("Resume Data:", data);

    } catch (error) {
        console.error("Resume upload error:", error);
        status.innerText = "Error: " + error.message;
    }
}

function setText(id, value) {
    const element = document.getElementById(id);
    if (element) element.innerText = value;
}

function showSkills(skills) {
    const element = document.getElementById("skillsResult");
    if (!element) return;

    element.innerHTML = skills.length
        ? `<ul>${skills.map(skill => `<li>${escapeHTML(skill)}</li>`).join("")}</ul>`
        : "No skills detected.";
}

function showCareerMatches(matches) {
    const element = document.getElementById("careerResult");
    if (!element) return;

    element.innerHTML = matches.length
        ? matches.map(match => `
            <div style="margin-bottom:15px;">
                <strong>${escapeHTML(match.role || "Career role")}</strong>
                <br>
                Match Score: ${Number(match.match_score || 0)}%
            </div>
        `).join("")
        : "No career matches found.";
}

function showSkillGap(skillGap) {
    const element = document.getElementById("skillGapResult");
    if (!element) return;

    if (!skillGap) {
        element.innerText = "Skill gap could not be calculated.";
        return;
    }

    const matched = skillGap.matched_skills || [];
    const missing = skillGap.missing_skills || [];

    element.innerHTML = `
        <strong>Matched Skills:</strong>
        <ul>${matched.map(skill => `<li>${escapeHTML(skill)}</li>`).join("")}</ul>
        <strong>Missing Skills:</strong>
        <ul>${missing.map(skill => `<li>${escapeHTML(skill)}</li>`).join("")}</ul>
        <strong>Overall Match:</strong> ${Number(skillGap.match_score || 0)}%
    `;
}

function showSkillProgress(items) {
    const element = document.getElementById("skillProgressResult");
    if (!element) return;

    if (!items || !items.length) {
        element.innerText = "Skill progress is not available.";
        return;
    }

    element.innerHTML = items.map(item => {
        const progress = Math.max(0, Math.min(100, Number(item.progress || 0)));

        return `
            <div style="margin-bottom:15px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
                    <strong>${escapeHTML(item.skill || "Skill")}</strong>
                    <span>${progress}%</span>
                </div>
                <div style="width:100%;height:10px;background:#eee;border-radius:10px;overflow:hidden;">
                    <div style="width:${progress}%;height:100%;background:#4CAF50;"></div>
                </div>
            </div>
        `;
    }).join("");
}

function showProfile(profile) {
    const element = document.getElementById("profileResult");
    if (!element) return;

    if (!profile) {
        element.innerText = "Profile analysis not available.";
        return;
    }

    element.innerHTML = `
        <p><strong>Education:</strong> ${escapeHTML(profile.education || "Not detected")}</p>
        <p><strong>Previous Role:</strong> ${escapeHTML(profile.previous_role || "Not detected")}</p>
        <p><strong>Experience:</strong> ${escapeHTML(profile.experience_years ?? "Not detected")} years</p>
        <p><strong>Career Break:</strong> ${escapeHTML(profile.career_break_years ?? "Not detected")} years</p>
        <p><strong>Break Reason:</strong> ${escapeHTML(profile.career_break_reason || "Not detected")}</p>
    `;
}

function showReentryStatement(statement) {
    setText(
        "reentryResult",
        statement || "Career re-entry statement not available."
    );
}

function showRestartScore(score) {
    const element = document.getElementById("restartScoreResult");
    if (!element) return;

    if (!score) {
        element.innerText = "Restart score not available.";
        return;
    }

    element.innerHTML = `
        <h4>Restart Score: ${Number(score.restart_score || 0)}/100</h4>
        <p><strong>Skill Score:</strong> ${Number(score.skill_score || 0)}</p>
        <p><strong>Experience Score:</strong> ${Number(score.experience_score || 0)}</p>
        <p><strong>Interview Score:</strong> ${Number(score.interview_score || 0)}</p>
    `;
}

function showDashboard(data) {
    const element = document.getElementById("dashboardResult");
    if (!element) return;

    const profile = data.profile || {};
    const topMatch = data.career_matches?.[0]?.role || "Not available";

    element.innerHTML = `
        <p><strong>Education:</strong> ${escapeHTML(profile.education || "Not detected")}</p>
        <p><strong>Previous Role:</strong> ${escapeHTML(profile.previous_role || "Not detected")}</p>
        <p><strong>Experience:</strong> ${escapeHTML(profile.experience_years ?? 0)} years</p>
        <p><strong>Career Break:</strong> ${escapeHTML(profile.career_break_years ?? 0)} years</p>
        <p><strong>Top Career Match:</strong> ${escapeHTML(topMatch)}</p>
        <p><strong>Skill Match:</strong> ${data.skill_gap?.match_score ?? "Not available"}%</p>
        <p><strong>Career Restart Score:</strong> ${data.restart_score?.restart_score ?? "--"}/100</p>
    `;
}

function escapeHTML(value) {
    return String(value ?? "").replace(/[&<>"']/g, character => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[character]);
}

async function evaluateInterviewAnswer(question, answer, targetRole) {
    const response = await fetch(
        "http://127.0.0.1:8000/interview/evaluate",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question,
                answer: answer,
                target_role: targetRole
            })
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Evaluation failed.");
    }

    return data;
}

function renderInterviewQuestions() {
    const result = document.getElementById("interviewResult");
    if (!result) return;

    const questions = window.interviewQuestions || [];
    const attempts = window.interviewAttempts || {};

    if (!questions.length) {
        result.innerText = "Upload your resume to get interview questions.";
        return;
    }

    result.innerHTML = "<ol>" + questions.map((question, index) => `
        <li style="margin-bottom:10px;">
            ${escapeHTML(question)}
            <br>
            ${attempts[index]
                ? `Attempted | Score: ${Number(attempts[index].score)}/10`
                : "Not attempted"}
        </li>
    `).join("") + "</ol>";
}

// FIX: Keep one global function so other functions can call it.
window.updateInterviewSessionScore = function () {
    const attempts = window.interviewAttempts || {};
    const questions = window.interviewQuestions || [];

    const scores = Object.values(attempts)
        .map(item => Number(item.score))
        .filter(score => Number.isFinite(score));

    const total = questions.length;
    const attempted = scores.length;

    const average = attempted
        ? scores.reduce((sum, score) => sum + score, 0) / attempted
        : 0;

    setText("questionsAttempted", `${attempted}/${total}`);

    setText(
        "averageInterviewScore",
        attempted ? `${average.toFixed(1)}/10` : "--"
    );

    setText(
        "interviewSessionScore",
        attempted
            ? `${scores.reduce((sum, score) => sum + score, 0)}/${attempted * 10}`
            : "--"
    );

    setText(
        "interviewPerformance",
        total > 0 && attempted === total
            ? `Interview completed! Average score: ${average.toFixed(1)}/10`
            : `You have attempted ${attempted} of ${total} questions.`
    );

    renderInterviewQuestions();
};

async function submitInterviewAnswer() {
    const index = window.currentInterviewQuestionIndex || 0;
    const questions = window.interviewQuestions || [];

    const answerBox = document.getElementById("interviewAnswer");
    const feedback = document.getElementById("interviewFeedback");

    if (!feedback || !answerBox) {
        console.error("Interview answer or feedback element is missing.");
        return;
    }

    if (!questions.length || !questions[index]) {
        feedback.innerText = "Please upload your resume first.";
        return;
    }

    const answer = answerBox.value.trim();

    if (!answer) {
        feedback.innerText = "Please write your answer first.";
        return;
    }

    feedback.innerText = "Evaluating your answer...";

    try {
        const targetRole =
            window.currentCareerMatches?.[0]?.role ||
            "Software Developer";

        const result = await evaluateInterviewAnswer(
            questions[index],
            answer,
            targetRole
        );

        window.interviewAttempts = window.interviewAttempts || {};

        window.interviewAttempts[index] = {
            score: Number(result.score ?? 0),
            feedback: result.feedback || "",
            suggestion: result.suggestion || ""
        };

        feedback.innerHTML = `
            <strong>Score: ${Number(result.score ?? 0)}/10</strong>
            <p>${escapeHTML(result.feedback || "No feedback provided.")}</p>
            <p>
                <strong>Suggestion:</strong>
                ${escapeHTML(result.suggestion || "Keep practising.")}
            </p>
        `;

        window.updateInterviewSessionScore();

    } catch (error) {
        console.error("Interview evaluation error:", error);
        feedback.innerText = "Evaluation failed: " + error.message;
    }
}

function nextInterviewQuestion() {
    const questions = window.interviewQuestions || [];
    const feedback = document.getElementById("interviewFeedback");

    if (!questions.length) {
        if (feedback) feedback.innerText = "Please upload your resume first.";
        return;
    }

    const nextIndex = (window.currentInterviewQuestionIndex || 0) + 1;

    if (nextIndex >= questions.length) {
        setText("currentInterviewQuestion", "You have reached the last question!");
        if (feedback) feedback.innerText = "Review your scores above.";
        return;
    }

    window.currentInterviewQuestionIndex = nextIndex;

    setText("currentInterviewQuestion", questions[nextIndex]);
    setText("interviewFeedback", "");

    const answerBox = document.getElementById("interviewAnswer");
    if (answerBox) answerBox.value = "";

    window.updateInterviewSessionScore();
}
// ===== INTERVIEW RESULT DISPLAY =====

function showInterviewFeedback(data) {
    const feedbackBox = document.getElementById("interviewFeedback");
    if (!feedbackBox) return;

    const score = Number(data.score ?? data.marks ?? 0);
    const feedback = data.feedback || data.evaluation || data.message || "Answer evaluated.";
    const strengths = data.strengths || [];
    const improvements = data.improvements || data.suggestions || [];

    feedbackBox.innerHTML = `
        <h3>Answer Evaluation</h3>
        <p><strong>Score:</strong> ${Number.isFinite(score) ? score : 0}/10</p>
        <p><strong>Feedback:</strong> ${escapeHTML(String(feedback))}</p>

        ${Array.isArray(strengths) && strengths.length
            ? `<p><strong>Strengths:</strong></p>
               <ul>${strengths.map(item => `<li>${escapeHTML(String(item))}</li>`).join("")}</ul>`
            : ""}

        ${Array.isArray(improvements) && improvements.length
            ? `<p><strong>Areas to Improve:</strong></p>
               <ul>${improvements.map(item => `<li>${escapeHTML(String(item))}</li>`).join("")}</ul>`
            : ""}
    `;
}


// ===== RESET INTERVIEW SESSION =====

function resetInterviewSession() {
    window.currentInterviewQuestionIndex = 0;
    window.interviewAttempts = {};

    const answerBox = document.getElementById("interviewAnswer");
    const feedbackBox = document.getElementById("interviewFeedback");

    if (answerBox) answerBox.value = "";
    if (feedbackBox) feedbackBox.innerHTML = "";

    renderInterviewQuestions();
    window.updateInterviewSessionScore();
}


// ===== SAFE BUTTON HANDLERS =====

window.renderInterviewQuestions = renderInterviewQuestions;
window.submitInterviewAnswer = submitInterviewAnswer;
window.nextInterviewQuestion = nextInterviewQuestion;
window.resetInterviewSession = resetInterviewSession;
window.showInterviewFeedback = showInterviewFeedback;


// ===== PAGE READY =====

document.addEventListener("DOMContentLoaded", function () {
    const uploadButton = document.getElementById("uploadButton");

    if (uploadButton) {
        uploadButton.addEventListener("click", function (event) {
            event.preventDefault();
            uploadResume();
        });
    }

    const answerButton = document.getElementById("submitInterviewButton");

    if (answerButton) {
        answerButton.addEventListener("click", function (event) {
            event.preventDefault();
            submitInterviewAnswer();
        });
    }

    const nextButton = document.getElementById("nextInterviewButton");

    if (nextButton) {
        nextButton.addEventListener("click", function (event) {
            event.preventDefault();
            nextInterviewQuestion();
        });
    }

    const resetButton = document.getElementById("resetInterviewButton");

    if (resetButton) {
        resetButton.addEventListener("click", function (event) {
            event.preventDefault();
            resetInterviewSession();
        });
    }
});
