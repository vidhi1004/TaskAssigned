
# 🧠 Resume Parser & Job Matcher

A Django-based web application that allows candidates to upload resumes, parses key information using simple text processing, and matches them to jobs based on skills. Admins can manage jobs, view matched candidates, and trigger weekly job match emails using Celery & Redis.

---

## 🚀 Features

### 1. 👥 User Authentication
- Candidate sign-up and login with JWT-based authentication.
- Admin login with access to dashboard for job and candidate management.

### 2. 📄 Resume Upload & Parsing
- Upload resumes in `.pdf` or `.docx` formats.
- Extracts:
  - **Skills** (matched from a predefined list)
- Tools used:
  - `docx2txt` for `.docx`
  - `PyMuPDF` (fitz) for `.pdf`
- Saves extracted data in the candidate profile and performs skill-based job matching automatically.

### 3. 🧠 Job Matching Algorithm
- Compares candidate skills with each job’s `required_skills`.
- Calculates `match_percentage = (len(matching_skills) / len(required_skills)) * 100`.
- Stores matched jobs with match percentage in the database.
- Matching is triggered on:
  - Resume upload
  - New job creation

### 4. 🛠️ Admin Dashboard
- Built with Bootstrap.
- Admin functionalities include:
  - Create / delete / view jobs
  - Create new skills
  - View candidate profiles, parsed resumes, and matched jobs
- Admin authentication check before access.

### 5. 📋 Candidate Dashboard
- Profile section with:
  - Resume preview link
  - Extracted skills
  - List of matched jobs with percentages
- Resume re-upload supported with auto re-matching.

### 6. 📧 Weekly Job Match Emails (Celery Beat)
- Uses Celery + Redis to:
  - Periodically send matched job summaries to candidates.
  - Only sends if new matches are found.
  - Scheduled using Celery Beat.

### 7. 🔌 REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/api/register/`      | Register user           |
| POST   | `/api/login/`         | Login and get tokens    |
| POST   | `/api/verify/`        | Verify OTP              |
| POST   | `/api/resume/`        | Upload resume           |
| GET    | `/api/profile/`       | Get candidate profile   |
| GET    | `/api/job_view/`      | List all jobs           |
| GET    | `/api/job_match/`     | Get matched jobs for user |
| GET    | `/profile_all/`       | Admin: View all candidates |
| GET    | `/is_admin/`          | Admin check for frontend |
| GET    | `/api/skills/`        | List of available skills |
| POST   | `/api/skills_creation`| Create a new skill      |

---

## ⚙️ Tech Stack

- **Backend**: Django, Django REST Framework  
- **Authentication**: JWT (SimpleJWT)  
- **Frontend**: HTML, CSS, Bootstrap, JavaScript, Axios  
- **File Parsing**: PyMuPDF (fitz), docx2txt  
- **Database**: SQLite (default), compatible with PostgreSQL  
- **Async Tasks**: Celery + Redis  
- **Email**: Django email framework + Celery tasks  

---

## 💻 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/resume-job-matcher.git
cd resume-job-matcher
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python -m venv env
source env/bin/activate   # On Windows: env\Scripts\activate
pip install -r requirements.txt
```

### 3. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

---

## 📨 Celery + Redis Setup (For Weekly Email Summary)

### 1. Start Redis Server

```bash
redis-server
```

### 2. Start Celery Worker

```bash
celery -A yourprojectname worker --loglevel=info --pool=solo
```

### 3. Start Celery Beat Scheduler

```bash
celery -A yourprojectname beat --loglevel=info
```

---

## 👩‍💻 Author

**Assigned To**: Vidhi  
🎯 Internship Project – Resume Parser & Job Matcher

---

## 📄 License

This project is intended for learning and internship purposes. You may fork and extend it freely.

---

> “Match your resume with the right job.”
