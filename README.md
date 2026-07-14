# AI Study Planner

A Django-based study planner with a rule-based AI recommendation engine
that generates a daily study schedule from your subjects, tasks, exam
dates, and completion history.

## ✅ What's fully built (working code)

- **Accounts**: custom user model (email login), registration, login,
  logout, forgot/reset password (Django's built-in token flow), profile
  editing with photo upload.
- **Dashboard**: stat cards (subjects, completed/pending tasks, today's
  hours, weekly progress, completion %), Chart.js charts (study hours
  trend, weekly performance, subject-wise progress).
- **Subjects**: full CRUD (name, difficulty, priority, credits, target
  score) with per-subject completion tracking.
- **Tasks**: full CRUD (title, subject, date, start/end time, estimated
  hours, status, notes), search + status filter, pagination.
- **Exams**: full CRUD, automatically boosts AI urgency scoring as the
  exam date approaches.
- **Goals**: full CRUD with completed/remaining/percentage tracking.
- **AI Study Planner** (`planner/ai_engine.py`): rule-based scoring
  engine (priority + difficulty + exam urgency + completion rate) that
  allocates your available daily hours into a real time-blocked
  schedule with breaks and a closing revision block. Fully explainable
  — every slot has a `reason`.
- **AI Recommendation Engine**: weak-subject detection, high-priority
  subject list, revision schedule, daily motivational quote, study tip,
  recommended daily hours — all shown on the dashboard and plan page.
- **Search**: global search across subjects and tasks.
- **Admin panel**: all models registered with list/search/filter config.
- **UI**: responsive sidebar/navbar/footer layout, dark mode (persisted
  in localStorage), gradient theme, hover effects, progress bars, JS
  form validation.

## 🚧 Not yet built (clearly out of scope for this pass)

To avoid handing you a huge pile of unverified code, these modules from
the original spec are **not implemented yet**:

- Notes module (add note / upload PDF / upload image / delete)
- Reminder module (daily/exam/assignment reminders + email sending)
- Interactive calendar view (FullCalendar.js integration)
- PDF report generation (study report / progress report)
- Pomodoro timer, achievements/badges, streaks, leaderboard
- Email notifications (SMTP is wired up in settings, but nothing sends yet)

Each of these fits cleanly into the existing app structure (e.g. Notes
would be a `notes` app following the same model/form/view/template
pattern as `goals`). Happy to build any of these next — just say which.

## 📁 Folder Structure

```
ai_study_planner/
├── manage.py
├── requirements.txt
├── .env.example
├── ai_study_planner/        # project settings, root urls, wsgi/asgi
├── accounts/                 # custom User model, auth views
├── core/                     # home/about/contact/dashboard/search
├── subjects/                 # Subject CRUD
├── tasks/                    # Task CRUD
├── exams/                    # Exam CRUD
├── goals/                    # Goal CRUD
├── planner/                  # AI recommendation engine + daily plan
├── templates/                # base.html, shared partials
├── static/css, static/js     # stylesheet + vanilla JS
└── media/                    # user uploads (profile pictures etc.)
```

## ⚙️ Setup

### 1. Create a virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure PostgreSQL
Using `psql` or pgAdmin, create the database:
```sql
CREATE DATABASE ai_study_planner;
```
Copy `.env.example` to `.env` (or just export the variables) and fill in
your actual DB credentials. `settings.py` reads them via
`os.environ.get(...)`, so either export the vars in your shell or use a
tool like `python-decouple` / `django-environ` to load the `.env` file
— the simplest option is:
```bash
export $(cat .env | xargs)   # macOS/Linux
```

### 3. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create an admin user
```bash
python manage.py createsuperuser
```

### 5. Run the dev server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/`.

## 🧠 How the AI engine works

See `planner/ai_engine.py`. In short:

1. **Score each subject** using: priority weight + difficulty weight +
   exam-urgency boost (bigger the closer the exam) + weak-subject boost
   (based on task completion rate) + ambitious-target-score nudge.
2. **Allocate today's available hours** (from `StudyPreference`)
   proportionally to each subject's score, with a floor (20 min) and
   ceiling (150 min) per subject so no subject is starved or hogs the day.
3. **Lay out real clock times** starting at the user's preferred start
   time, inserting a break every `long_session_minutes` of continuous
   study, and closing with a 30-minute revision block on the
   top-scoring subject.
4. Persist the result as `GeneratedPlanSlot` rows so the plan doesn't
   get recomputed (and potentially change) on every page refresh —
   "Regenerate Plan" recomputes it on demand.

This is intentionally rule-based and fully explainable (`reason` field
on every slot). To upgrade to ML later: replace `compute_subject_scores()`
with a call to a trained model that predicts an urgency score per
subject — `generate_daily_plan()` doesn't need to change.

## Note on this environment

This project was written directly to files without being run, migrated,
or tested here (no internet access / no Django installed in this sandbox
to install it). Run the setup steps above locally to actually launch it,
and check the Django/PostgreSQL logs for anything environment-specific
(exact Postgres version, OS package names, etc.) that might need minor
tweaks.
