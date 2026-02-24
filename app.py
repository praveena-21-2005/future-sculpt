import streamlit as st
import os
from resume_parser import extract_resume_text
from groq_utils import call_groq, safe_json_loads

st.set_page_config(page_title="VidyaGuide AI", layout="wide")

st.title("🚀 VidyaGuide AI Agent")
st.markdown("### Career Planning & Resume Mentor")

# Sidebar Navigation
option = st.sidebar.radio(
    "Choose Feature",
    ["Resume Analysis", "Skill Gap Analysis", "Career Chat"]
)

# -------------------------------
# 1️⃣ Resume Analysis
# -------------------------------
if option == "Resume Analysis":

    st.header("📄 Resume Analysis")

    uploaded_file = st.file_uploader(
        "Upload your resume (PDF or DOCX)",
        type=["pdf", "docx"]
    )

    target_role = st.text_input("Target Job Role (Optional)")

    if uploaded_file:
        resume_text = extract_resume_text(uploaded_file)

        if st.button("Analyze Resume"):

            with st.spinner("Analyzing resume..."):

                system_prompt = """You are a professional HR expert and ATS evaluator."""

                user_prompt = f"""
                Analyze the following resume.

                Target Role: {target_role}

                Resume:
                {resume_text}

                Return STRICT JSON format:
                {{
                    "score": number,
                    "strengths": [],
                    "weaknesses": [],
                    "missing_skills": [],
                    "ats_tips": [],
                    "recommended_roles": []
                }}
                """

                result = call_groq(system_prompt, user_prompt)
                data = safe_json_loads(result)

                if data:
                    st.success(f"Resume Score: {data.get('score', 0)}/100")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("✅ Strengths")
                        for item in data.get("strengths", []):
                            st.write("- ", item)

                        st.subheader("⚠ Weaknesses")
                        for item in data.get("weaknesses", []):
                            st.write("- ", item)

                    with col2:
                        st.subheader("❌ Missing Skills")
                        for item in data.get("missing_skills", []):
                            st.write("- ", item)

                        st.subheader("📌 ATS Tips")
                        for item in data.get("ats_tips", []):
                            st.write("- ", item)

                    st.subheader("🎯 Recommended Roles")
                    for role in data.get("recommended_roles", []):
                        st.write("- ", role)

                else:
                    st.error("Failed to parse AI response. Showing raw output:")
                    st.write(result)

# -------------------------------
# 2️⃣ Skill Gap Analysis
# -------------------------------
elif option == "Skill Gap Analysis":

    st.header("🧩 Skill Gap Analysis")

    current_skills = st.text_area("Enter your current skills (comma separated)")
    target_role = st.text_input("Target Role")

    if st.button("Analyze Skill Gap"):

        with st.spinner("Analyzing skills..."):

            system_prompt = "You are a career coach specializing in skill gap analysis."

            user_prompt = f"""
            Current Skills: {current_skills}
            Target Role: {target_role}

            Provide:
            - Skill match percentage
            - Missing skills
            - 6 month learning roadmap
            """

            result = call_groq(system_prompt, user_prompt)
            st.markdown(result)

# -------------------------------
# 3️⃣ AI Career Chat
# -------------------------------
elif option == "Career Chat":

    st.header("💬 AI Career Mentor")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.chat_input("Ask about career guidance...")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):

                system_prompt = "You are an expert career mentor."

                result = call_groq(system_prompt, user_input)

                st.markdown(result)

        st.session_state.messages.append(
            {"role": "assistant", "content": result}
        )