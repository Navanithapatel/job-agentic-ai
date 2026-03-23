from flask import Flask, render_template, request, redirect, url_for
import os
import re

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ---------------- MATCH FUNCTION ----------------
def match_score(resume_text, job_desc):
    resume_words = set(re.findall(r'\b\w+\b', resume_text.lower()))
    job_words = set(re.findall(r'\b\w+\b', job_desc.lower()))

    if not job_words:
        return 0

    match = resume_words.intersection(job_words)
    score = (len(match) / len(job_words)) * 100
    return round(score, 2)

# ---------------- SKILL EXTRACTION ----------------
def extract_skills(text):
    skills_list = [
        "python", "java", "c", "c++", "machine learning",
        "data science", "sql", "html", "css", "javascript",
        "react", "node", "flask", "django", "ai"
    ]

    found_skills = []
    text = text.lower()

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return found_skills

# ---------------- JOB SUGGESTION ----------------
def suggest_jobs(skills):
    job_roles = []

    if "python" in skills:
        job_roles.append(("Python Developer", "https://www.naukri.com/python-developer-jobs"))

    if "machine learning" in skills or "ai" in skills:
        job_roles.append(("ML Engineer Intern", "https://www.indeed.com/jobs?q=machine+learning+intern"))

    if "data science" in skills:
        job_roles.append(("Data Analyst", "https://www.linkedin.com/jobs/data-analyst-jobs"))

    if "html" in skills or "css" in skills or "javascript" in skills:
        job_roles.append(("Frontend Developer", "https://www.naukri.com/frontend-developer-jobs"))

    if "java" in skills:
        job_roles.append(("Java Developer", "https://www.indeed.com/jobs?q=java+developer"))

    return job_roles

@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    with open('users.txt', 'a') as f:
        f.write(f"{username},{password}\n")

    return redirect(url_for('login'))

@app.route('/login_user', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']

    with open('users.txt', 'r') as f:
        users = f.readlines()

    for user in users:
        u, p = user.strip().split(',')
        if u == username and p == password:
            return redirect(url_for('home'))

    return "Invalid Credentials ❌"

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    job_desc = request.form['job_desc']
    file = request.files['resume']

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            resume_text = f.read()

        score = match_score(resume_text, job_desc)

        skills = extract_skills(resume_text)
        jobs = suggest_jobs(skills)

        return render_template(
            'home.html',
            score=score,
            skills=skills,
            jobs=jobs
        )

    return render_template('home.html', score=0)


if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)