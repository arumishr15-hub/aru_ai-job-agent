
import hashlib
from pathlib import Path

import streamlit as st

from resume_loader import load_resume
from job_finder import search_jobs, fetch_job_description
from resume_analyzer import analyze_match
from ai_assistant import improve_resume, create_recruiter_message
from recruiter_finder import extract_job_details, find_recruiters


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Aru AI Assistant",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ==========================================
# 2. FIND GHIBLI PORTRAIT
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"


def find_portrait():
    """Find Aru's Ghibli picture."""

    for filename in [
        "aru_bg.png",
        "aru_bg.jpg",
        "aru_bg.jpeg",
    ]:

        image_path = ASSETS_DIR / filename

        if image_path.is_file():
            return image_path

    return None


portrait_path = find_portrait()


# ==========================================
# 3. MAGENTA PINK THEME
# ==========================================

st.markdown(
    """
    <style>

    /* MAIN APP */

    .stApp {
        background-color: #FFF9FC !important;
        color: #392B40 !important;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .stApp h1,
    .stApp h2,
    .stApp h3 {
        color: #392B40 !important;
    }

    .stApp p,
    .stApp label {
        color: #493B50;
    }


    /* STANDARD BUTTONS */

    div.stButton > button {
        background-color: #F7D1E4 !important;
        color: #4A2340 !important;
        border: 1px solid #C85A91 !important;
        border-radius: 14px !important;
        font-weight: 600 !important;
    }

    div.stButton > button:hover {
        background-color: #E8A9C5 !important;
        color: #4A2340 !important;
        border-color: #A04A79 !important;
    }


    /* PRIMARY BUTTONS */

    div.stButton > button[kind="primary"] {
        background-color: #C85A91 !important;
        color: #FFFFFF !important;
        border-color: #C85A91 !important;
    }

    div.stButton > button[kind="primary"]:hover {
        background-color: #A04A79 !important;
        color: #FFFFFF !important;
    }


    /* LINKEDIN BUTTONS */

    div[data-testid="stLinkButton"] a {
        background-color: #C85A91 !important;
        color: #FFFFFF !important;
        border: 1px solid #C85A91 !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        text-decoration: none !important;
    }

    div[data-testid="stLinkButton"] a:hover {
        background-color: #A04A79 !important;
        color: #FFFFFF !important;
    }


    /* TEXT INPUTS */

    div[data-baseweb="input"] > div {
        background-color: #F7D1E4 !important;
        border: 1px solid #C85A91 !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="input"] input {
        background-color: transparent !important;
        color: #4A2340 !important;
        -webkit-text-fill-color: #4A2340 !important;
    }

    div[data-baseweb="input"] input::placeholder {
        color: #986B86 !important;
        -webkit-text-fill-color: #986B86 !important;
    }


    /* TEXT AREAS */

    div[data-baseweb="textarea"] > div {
        background-color: #F7D1E4 !important;
        border: 1px solid #C85A91 !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="textarea"] textarea {
        background-color: transparent !important;
        color: #4A2340 !important;
        -webkit-text-fill-color: #4A2340 !important;
    }


    /* DROPDOWNS */

    div[data-baseweb="select"] > div {
        background-color: #F7D1E4 !important;
        color: #4A2340 !important;
        border: 1px solid #C85A91 !important;
        border-radius: 12px !important;
    }


    /* GHIBLI PORTRAIT */

    div[data-testid="stImage"] img {
        border-radius: 22px !important;
        border: 3px solid #F1C7DD !important;
        box-shadow: 0 8px 24px rgba(160, 74, 121, 0.15);
    }


    /* METRICS */

    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid #EDD8E4 !important;
        border-radius: 16px !important;
        padding: 18px !important;
    }


    /* TABS */

    button[data-baseweb="tab"] {
        color: #6D3155 !important;
        font-weight: 600 !important;
    }


    /* ABOUT ME EXPANDER */

    div[data-testid="stExpander"] {
        background-color: #FFF0F7 !important;
        border: 1px solid #EDD8E4 !important;
        border-radius: 18px !important;
    }

    div[data-testid="stExpander"] details {
        background-color: transparent !important;
    }

    div[data-testid="stExpander"] summary {
        color: #A04A79 !important;
        font-weight: 600 !important;
    }


    /* PINK FILE UPLOADER */

    div[data-testid="stFileUploader"] {
        background-color: #FFF9FC !important;
        border: 1px solid #EDD8E4 !important;
        border-radius: 18px !important;
        padding: 12px !important;
    }

    /* Main upload area */

    [data-testid="stFileUploaderDropzone"] {
        background: #FBEAF3 !important;
        background-color: #FBEAF3 !important;
        border: 2px dashed #DDA9C5 !important;
        border-radius: 14px !important;
        color: #493B50 !important;
    }

    /* Remove dark internal backgrounds */

    [data-testid="stFileUploaderDropzone"] section,
    [data-testid="stFileUploaderDropzone"] > div,
    [data-testid="stFileUploaderDropzone"] section > div {
        background-color: transparent !important;
        background: transparent !important;
    }

    /* Upload text */

    [data-testid="stFileUploaderDropzone"] p,
    [data-testid="stFileUploaderDropzone"] span,
    [data-testid="stFileUploaderDropzone"] small {
        color: #493B50 !important;
        -webkit-text-fill-color: #493B50 !important;
    }

    /* Upload icon */

    [data-testid="stFileUploaderDropzone"] svg {
        color: #A04A79 !important;
        stroke: #A04A79 !important;
    }

    /* Upload button */

    [data-testid="stFileUploaderDropzone"] button {
        background-color: #C85A91 !important;
        color: #FFFFFF !important;
        border: 1px solid #C85A91 !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
    }

    [data-testid="stFileUploaderDropzone"] button *,
    [data-testid="stFileUploaderDropzone"] button span {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    [data-testid="stFileUploaderDropzone"] button:hover {
        background-color: #A04A79 !important;
        border-color: #A04A79 !important;
    }

    /* Uploaded file */

    [data-testid="stFileUploaderFile"] {
        background-color: #FBEAF3 !important;
        border-radius: 12px !important;
    }


    /* DIVIDERS */

    hr {
        border-color: #EDD8E4 !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# GOOGLE SIGN-IN
# ==========================================

def show_login_screen():
    """Welcome screen for visitors who are not signed in."""

    left_col, right_col = st.columns([3, 2], gap="large")

    with left_col:
        st.title("🌸 Welcome to Aru AI Assistant")

        st.subheader("Your AI-powered career companion ✨")

        st.write(
            "Discover jobs, improve your resume, "
            "and connect with potential recruiters."
        )

        st.markdown("**Your career, in bloom. 🌷**")

        if st.button(
            "🔐 Continue with Google",
            type="primary",
            use_container_width=True,
        ):
            st.login()

    with right_col:
        if portrait_path is not None:
            st.image(
                str(portrait_path),
                use_container_width=True,
            )


# Require login before showing the dashboard.
if not st.user.is_logged_in:
    show_login_screen()
    st.stop()


# ==========================================
# SIGNED-IN USER
# ==========================================

welcome_col, logout_col = st.columns([4, 1])

with welcome_col:
    user_name = st.user.get("name", "there")
    st.write(f"🌷 Welcome, **{user_name}**!")

with logout_col:
    if st.button("Sign Out", use_container_width=True):
        st.logout()

st.divider()



# ==========================================
# 4. SESSION STATE
# ==========================================

if "page" not in st.session_state:
    st.session_state["page"] = "resume"

if "resume_text" not in st.session_state:
    st.session_state["resume_text"] = ""

if "resume_name" not in st.session_state:
    st.session_state["resume_name"] = ""

if "resume_signature" not in st.session_state:
    st.session_state["resume_signature"] = None


def clear_job_analysis():
    """Remove results related to the previous job."""

    keys = [
        "jd",
        "job_url",
        "job_details",
        "recruiters",
        "suggestions",
        "recruiter_messages",
        "match_result",
    ]

    for key in keys:
        st.session_state.pop(key, None)


def change_page(page_name):
    """Switch between dashboard pages."""

    st.session_state["page"] = page_name


# ==========================================
# 5. HEADER WITH GHIBLI PORTRAIT
# ==========================================

left_col, right_col = st.columns(
    [3, 2],
    gap="large",
)

with left_col:

    st.title("🌸 Aru AI Assistant")

    st.markdown(
        "### Your personal AI career companion ✨"
    )

    st.write(
        "Discover opportunities, improve your resume, "
        "and connect with potential recruiters."
    )

    st.markdown(
        "**Your career, in bloom. 🌷**"
    )


with right_col:

    if portrait_path is not None:

        st.image(
            str(portrait_path),
            caption="Aru's little corner 🌸",
            use_container_width=True,
        )

    else:

        st.info(
            "Place your Ghibli picture in "
            "assets/aru_bg.png to display it here."
        )


# ==========================================
# 6. ABOUT ME SECTION
# ==========================================

with st.expander(
    "🌷 About Me · Meet the Developer",
    expanded=True,
):

    st.markdown(
        """
**Software Developer | AI Enthusiast | App Builder**

Hi, I'm Arundhati! 👋

I'm a Software Developer with a growing passion
for Artificial Intelligence and building applications
that solve real-world problems.

I love turning ideas into working software,
exploring new technologies, and learning by building.

My journey started with software development,
and now I'm expanding into AI — experimenting with
LLMs, intelligent agents, and AI-powered applications.

**Aru AI Assistant is one of my passion projects** —
combining software engineering with my enthusiasm
for AI to make job searching smarter, simpler,
and more personalized.

✨ *Always learning. Always building.*
"""
    )


st.divider()


# ==========================================
# 7. CAREER WORKSPACE NAVIGATION
# ==========================================

st.subheader("Your Career Workspace")

col1, col2, col3 = st.columns(3)

with col1:

    st.button(
        "📄 My Resume",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state["page"] == "resume"
            else "secondary"
        ),
        on_click=change_page,
        args=("resume",),
    )

with col2:

    st.button(
        "🔎 Discover Jobs",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state["page"] == "jobs"
            else "secondary"
        ),
        on_click=change_page,
        args=("jobs",),
    )

with col3:

    st.button(
        "💌 Recruiter Connect",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state["page"] == "recruiters"
            else "secondary"
        ),
        on_click=change_page,
        args=("recruiters",),
    )


st.divider()

page = st.session_state["page"]


# ==========================================
# 8. PAGE ONE - MY RESUME
# ==========================================

if page == "resume":

    st.header("01 · My Resume")

    st.write(
        "Upload your resume to use it for job matching "
        "and personalized suggestions."
    )

    uploaded_file = st.file_uploader(
        "Choose your PDF or Word resume",
        type=["pdf", "docx"],
    )

    if uploaded_file is not None:

        try:

            file_bytes = uploaded_file.getvalue()

            signature = hashlib.sha256(
                file_bytes
            ).hexdigest()

            if (
                signature
                != st.session_state["resume_signature"]
            ):

                resume_text = load_resume(uploaded_file)

                if resume_text and resume_text.strip():

                    st.session_state[
                        "resume_text"
                    ] = resume_text

                    st.session_state[
                        "resume_name"
                    ] = uploaded_file.name

                    st.session_state[
                        "resume_signature"
                    ] = signature

                    clear_job_analysis()

                else:

                    st.error(
                        "No readable text was found in your resume."
                    )

        except Exception as error:

            st.error(
                f"Resume upload error: {error}"
            )

    if st.session_state["resume_text"]:

        st.success(
            "Your resume is ready! 🌷"
        )

        st.write(
            "**Uploaded resume:**",
            st.session_state["resume_name"],
        )

        with st.expander(
            "Preview Extracted Resume"
        ):

            st.text_area(
                "Resume text",
                value=st.session_state["resume_text"],
                height=300,
                disabled=True,
            )

        st.button(
            "✨ Continue to Job Discovery",
            type="primary",
            use_container_width=True,
            on_click=change_page,
            args=("jobs",),
        )

    else:

        st.info(
            "Upload your resume to begin."
        )


# ==========================================
# 9. PAGE TWO - DISCOVER JOBS
# ==========================================

elif page == "jobs":

    st.header("02 · Discover Opportunities")

    st.write(
        "Find job opportunities based on your "
        "career goals and preferences."
    )

    if st.session_state["resume_text"]:

        st.success(
            "Your resume is loaded and ready."
        )

    else:

        st.warning(
            "Upload your resume to enable job matching."
        )

    role = st.text_input(
        "Desired Job Title",
        placeholder="Gen AI Engineer",
    )

    location = st.text_input(
        "Preferred Location",
        placeholder="Boston, MA",
    )

    work_mode = st.selectbox(
        "Work Preference",
        [
            "Any",
            "Remote",
            "Hybrid",
            "On-site",
        ],
    )

    if st.button(
        "🔎 Find Matching Jobs",
        type="primary",
        use_container_width=True,
    ):

        if not role.strip() or not location.strip():

            st.warning(
                "Please enter a job title and location."
            )

        else:

            try:

                with st.spinner(
                    "Searching for job opportunities..."
                ):

                    jobs = search_jobs(
                        role,
                        location,
                        work_mode,
                    )

                st.session_state["jobs"] = jobs

                clear_job_analysis()

                st.session_state.pop(
                    "selected_job_index",
                    None,
                )

            except Exception as error:

                st.error(
                    f"Job search error: {error}"
                )


    # --------------------------------------
    # DISPLAY JOB RESULTS
    # --------------------------------------

    jobs = st.session_state.get(
        "jobs",
        [],
    )

    if jobs:

        st.subheader(
            "✨ Opportunities Found"
        )

        st.caption(
            f"{len(jobs)} search results. "
            "Verify each original posting is still active."
        )

        selected_index = st.selectbox(
            "Select a job",
            options=list(range(len(jobs))),
            format_func=lambda i: jobs[i]["title"],
            key="selected_job_index",
            on_change=clear_job_analysis,
        )

        selected_job = jobs[selected_index]

        with st.container(border=True):

            st.subheader(
                selected_job["title"]
            )

            st.write(
                selected_job["summary"]
            )

            st.link_button(
                "View Original Job Posting",
                selected_job["url"],
            )

            if st.button(
                "Fetch Job Description",
                type="primary",
            ):

                try:

                    with st.spinner(
                        "Fetching job description..."
                    ):

                        jd = fetch_job_description(
                            selected_job["url"]
                        )

                    clear_job_analysis()

                    if jd and jd.strip():

                        st.session_state["jd"] = jd

                        st.session_state[
                            "job_url"
                        ] = selected_job["url"]

                        st.success(
                            "Job description retrieved! 🌸"
                        )

                    else:

                        st.warning(
                            "No readable job description returned."
                        )

                except Exception as error:

                    st.error(
                        f"Could not fetch JD: {error}"
                    )

    elif "jobs" in st.session_state:

        st.info(
            "No jobs found. Try different keywords."
        )


    # --------------------------------------
    # JOB MATCH AND RESUME STUDIO
    # --------------------------------------

    jd = st.session_state.get(
        "jd",
        "",
    )

    resume = st.session_state["resume_text"]

    if jd:

        st.divider()

        st.header(
            "03 · Your Job Match"
        )

        with st.expander(
            "View Job Description"
        ):

            st.text_area(
                "Retrieved job page text",
                value=jd[:12000],
                height=250,
                disabled=True,
            )

        st.caption(
            "Review the retrieved text. "
            "Some job pages contain unrelated content."
        )

        if not resume:

            st.warning(
                "Upload your resume to analyze this job."
            )

        else:

            tab1, tab2 = st.tabs([
                "💗 Match Insights",
                "✨ Resume Studio",
            ])


            # --------------------------
            # TAB 1 - RESUME MATCH
            # --------------------------

            with tab1:

                st.subheader(
                    "Resume Match Analysis"
                )

                if st.button(
                    "Analyze Resume Match"
                ):

                    try:

                        result = analyze_match(
                            resume,
                            jd,
                        )

                        st.session_state[
                            "match_result"
                        ] = result

                    except Exception as error:

                        st.error(
                            f"Analysis error: {error}"
                        )

                if "match_result" in st.session_state:

                    result = st.session_state[
                        "match_result"
                    ]

                    st.metric(
                        "Skill Keyword Match",
                        f"{result['score']}%",
                    )

                    st.caption(
                        "This measures recognized keyword coverage, "
                        "not an official ATS score."
                    )

                    st.subheader(
                        "Matching Skills"
                    )

                    if result["matching"]:

                        for skill in result["matching"]:
                            st.success(skill)

                    else:

                        st.info(
                            "No matching skills detected."
                        )

                    st.subheader(
                        "Missing Skills"
                    )

                    if result["missing"]:

                        for skill in result["missing"]:
                            st.warning(skill)

                    else:

                        st.success(
                            "No missing recognized skills!"
                        )


            # --------------------------
            # TAB 2 - AI RESUME STUDIO
            # --------------------------

            with tab2:

                st.subheader(
                    "AI Resume Studio ✨"
                )

                st.write(
                    "Generate truthful, job-specific "
                    "resume improvement suggestions."
                )

                if st.button(
                    "Generate Resume Suggestions",
                    type="primary",
                ):

                    try:

                        with st.spinner(
                            "Aru AI is analyzing your resume..."
                        ):

                            suggestions = improve_resume(
                                resume,
                                jd[:12000],
                            )

                        st.session_state[
                            "suggestions"
                        ] = suggestions

                    except Exception as error:

                        st.error(
                            f"AI analysis error: {error}"
                        )

                if "suggestions" in st.session_state:

                    st.markdown(
                        st.session_state["suggestions"]
                    )

                    st.download_button(
                        "Download Resume Suggestions",
                        data=st.session_state[
                            "suggestions"
                        ],
                        file_name="resume_suggestions.md",
                        mime="text/markdown",
                    )

                    st.info(
                        "Never add skills or experience "
                        "you do not actually have."
                    )

        st.button(
            "💌 Continue to Recruiter Connect",
            use_container_width=True,
            on_click=change_page,
            args=("recruiters",),
        )


# ==========================================
# 10. PAGE THREE - RECRUITER CONNECT
# ==========================================

elif page == "recruiters":

    st.header(
        "03 · Recruiter Connect 💌"
    )

    st.write(
        "Discover potential recruiting contacts "
        "and prepare personalized LinkedIn messages."
    )

    resume = st.session_state["resume_text"]

    jd = st.session_state.get(
        "jd",
        "",
    )

    if not jd:

        st.warning(
            "Select a job and fetch its "
            "description before searching for recruiters."
        )

        st.button(
            "🔎 Go to Job Discovery",
            type="primary",
            on_click=change_page,
            args=("jobs",),
        )

    else:

        st.success(
            "Your selected job description is ready!"
        )

        if st.button(
            "Find Potential Recruiters",
            type="primary",
        ):

            try:

                with st.spinner(
                    "Identifying company and job title..."
                ):

                    details = extract_job_details(
                        jd[:3000]
                    )

                st.session_state[
                    "job_details"
                ] = details

                st.session_state[
                    "recruiters"
                ] = []

                st.session_state[
                    "recruiter_messages"
                ] = {}

                if details.get("company"):

                    with st.spinner(
                        "Searching for relevant recruiters..."
                    ):

                        recruiters = find_recruiters(
                            details["company"],
                            details.get("job_title", ""),
                        )

                    st.session_state[
                        "recruiters"
                    ] = recruiters

                else:

                    st.warning(
                        "Could not identify the hiring company."
                    )

            except Exception as error:

                st.error(
                    f"Recruiter search error: {error}"
                )


        # ----------------------------------
        # IDENTIFIED JOB DETAILS
        # ----------------------------------

        details = st.session_state.get(
            "job_details",
            {},
        )

        if details:

            st.subheader(
                "Identified Job"
            )

            st.write(
                "**Company:**",
                details.get("company", ""),
            )

            st.write(
                "**Job Title:**",
                details.get("job_title", ""),
            )


        # ----------------------------------
        # POTENTIAL RECRUITER RESULTS
        # ----------------------------------

        recruiters = st.session_state.get(
            "recruiters",
            [],
        )

        if recruiters:

            st.subheader(
                "Potential LinkedIn Recruiters"
            )

            st.caption(
                "These are public web search results, "
                "not verified hiring contacts "
                "for the exact job posting."
            )

            for index, recruiter in enumerate(
                recruiters
            ):

                with st.container(border=True):

                    # Recruiter's name
                    st.subheader(
                        recruiter.get(
                            "name",
                            "Potential recruiter",
                        )
                    )

                    # Profile title
                    role_text = recruiter.get(
                        "role",
                        "",
                    )

                    if role_text:

                        st.caption(role_text)

                    # Search result details
                    st.write(
                        recruiter.get(
                            "description",
                            "",
                        )
                    )

                    # Relevance
                    st.write(
                        "**Relevance:**",
                        recruiter.get(
                            "relevance",
                            "Not evaluated",
                        ),
                    )

                    evidence = recruiter.get(
                        "evidence",
                        [],
                    )

                    if evidence:

                        with st.expander(
                            "Why was this recruiter suggested?"
                        ):

                            for reason in evidence:

                                st.write(
                                    "✓", reason
                                )

                    st.caption(
                        "Not confirmed as the recruiter "
                        "assigned to this particular vacancy."
                    )

                    # LinkedIn profile
                    st.link_button(
                        "View LinkedIn Profile",
                        recruiter["url"],
                    )

                    # Recruiter name verification
                    verified_name = st.text_input(
                        "Verified Recruiter Name",
                        key=f"verified_name_{index}",
                        placeholder="Enter the recruiter's name",
                    )


                    # --------------------------
                    # CREATE LINKEDIN MESSAGE
                    # --------------------------

                    if st.button(
                        "💌 Generate Personalized Message",
                        key=f"message_button_{index}",
                    ):

                        if not resume:

                            st.warning(
                                "Please upload your resume first."
                            )

                        elif not verified_name.strip():

                            st.warning(
                                "Verify the recruiter and "
                                "enter their name."
                            )

                        else:

                            try:

                                with st.spinner(
                                    "Generating your LinkedIn message..."
                                ):

                                    message = (
                                        create_recruiter_message(
                                            resume,
                                            details.get(
                                                "job_title",
                                                "",
                                            ),
                                            details.get(
                                                "company",
                                                "",
                                            ),
                                            verified_name,
                                        )
                                    )

                                if (
                                    "recruiter_messages"
                                    not in st.session_state
                                ):

                                    st.session_state[
                                        "recruiter_messages"
                                    ] = {}

                                st.session_state[
                                    "recruiter_messages"
                                ][index] = message

                            except Exception as error:

                                st.error(
                                    f"Message generation error: {error}"
                                )


                    # --------------------------
                    # DISPLAY GENERATED MESSAGE
                    # --------------------------

                    messages = st.session_state.get(
                        "recruiter_messages",
                        {},
                    )

                    if index in messages:

                        st.success(
                            "Your personalized message is ready! 💌"
                        )

                        st.write(
                            "Copy the message using the "
                            "copy icon in the top-right corner."
                        )

                        st.code(
                            messages[index],
                            language=None,
                        )

                        st.link_button(
                            "💌 Open Recruiter's LinkedIn Profile",
                            recruiter["url"],
                            use_container_width=True,
                        )

                        st.info(
                            "Review your message, copy it, "
                            "open LinkedIn, and send it manually."
                        )

        elif "recruiters" in st.session_state:

            st.info(
                "No potential recruiter profiles "
                "were found for this search."
            )


# ==========================================
# 11. FOOTER
# ==========================================

st.divider()

st.caption(
    "🌸 Aru AI Assistant ✦ "
    "Made with curiosity, creativity, and a love for AI."
)
