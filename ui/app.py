import streamlit as st

from backend.app.services.course_loader import load_all_courses


# -----------------------------
# Helpers
# -----------------------------

def format_duration(seconds: int | None) -> str:
    if not seconds or seconds <= 0:
        return "—"
    h, rem = divmod(seconds, 3600)
    m, _ = divmod(rem, 60)
    return f"{h}h {m}m" if h else f"{m}m"


def course_stats(course):
    lessons = [
        lesson
        for section in course.sections
        for lesson in section.lessons
    ]

    total_lessons = len(lessons)
    total_seconds = sum(l.duration_seconds or 0 for l in lessons)

    missing_video = sum(1 for l in lessons if not l.video_url)
    missing_transcript = sum(1 for l in lessons if not l.transcript_path)

    return {
        "sections": len(course.sections),
        "lessons": total_lessons,
        "duration": format_duration(total_seconds),
        "missing_video_pct": round(missing_video / total_lessons * 100, 1) if total_lessons else 0,
        "missing_transcript_pct": round(missing_transcript / total_lessons * 100, 1) if total_lessons else 0,
    }


# -----------------------------
# Streamlit App
# -----------------------------

st.set_page_config(
    page_title="Wellness Atlas Academy",
    layout="wide",
)

st.title("Wellness Atlas Academy")

courses = load_all_courses()

if not courses:
    st.warning("No courses found in courses/processed/")
    st.stop()

# --- Sidebar: Course Selector ---
course_titles = [course.title for course in courses]
selected_course_title = st.sidebar.selectbox(
    "Select a course",
    course_titles
)

selected_course = next(
    c for c in courses if c.title == selected_course_title
)

# -----------------------------
# Course Overview (Option A)
# -----------------------------

st.header(selected_course.title)

stats = course_stats(selected_course)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Sections", stats["sections"])
c2.metric("Lessons", stats["lessons"])
c3.metric("Total Duration", stats["duration"])
c4.metric("Lessons w/o Video", f"{stats['missing_video_pct']}%")
c5.metric("Lessons w/o Transcript", f"{stats['missing_transcript_pct']}%")

st.divider()

# -----------------------------
# Sections & Lessons
# -----------------------------

for section in selected_course.sections:
    section_seconds = sum(
        lesson.duration_seconds or 0 for lesson in section.lessons
    )

    with st.expander(
        f"{section.title} · {len(section.lessons)} lessons · {format_duration(section_seconds)}",
        expanded=False,
    ):
        for lesson in section.lessons:
            cols = st.columns([5, 2, 2])

            # Lesson Title
            cols[0].markdown(f"**{lesson.title}**")

            # Duration
            cols[1].caption(format_duration(lesson.duration_seconds))

            # Status
            status = []
            if not lesson.video_url:
                status.append("video missing")
            if not lesson.transcript_path:
                status.append("transcript missing")

            cols[2].caption(" | ".join(status) if status else "complete")
