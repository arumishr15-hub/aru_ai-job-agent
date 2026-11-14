🌸 Aru AI Assistant
An AI-powered career companion for discovering jobs, understanding resume matches, and preparing personalized recruiter outreach.

Aru AI Assistant is a Python and Streamlit project built by a software developer exploring AI agents and practical AI-powered applications. It brings resume analysis, job discovery, AI writing assistance, and recruiter research into one soft-pink dashboard.
✨ Features
- Resume upload: Upload PDF or DOCX resumes and extract their text for analysis.
- Job discovery: Search public web results for opportunities by role, location, and preferred work arrangement using Tavily.
- Job description retrieval: Retrieve available text from a selected job posting for review.
- Resume match insights: Compare recognized skills in your resume and the selected job description.
- AI Resume Studio: Generate suggestions for tailoring resume wording to a job without inventing experience.
- Recruiter discovery: Search for publicly indexed LinkedIn profiles of potential recruiting contacts and display evidence-based relevance hints.
- LinkedIn message drafts: Use a local Ollama model to prepare concise, personalized recruiter messages that you can copy and review.
- Google Sign-In: Optional Google authentication using Streamlit's built-in OIDC support, once configured.
- Custom interface: A blush-and-magenta Streamlit theme, an About Me section, and a Ghibli-inspired portrait displayed on the right.
🛠 Tech stack
- Frontend: Streamlit
- Language: Python
- Local AI: Ollama with qwen3:4b
- Web search and content extraction: Tavily
- Document parsing: PyMuPDF (PDF) and python-docx (DOCX)
- Configuration: python-dotenv, Streamlit TOML configuration
- Authentication: Google OpenID Connect through Streamlit (optional)
