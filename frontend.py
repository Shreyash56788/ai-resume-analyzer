import streamlit as st
import requests


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


st.title("📄 AI Resume Analyzer")

st.write(
    "Upload your resume and compare it with a job description "
    "using AI-powered skill analysis."
)


resume = st.file_uploader(
    "📎 Upload Resume",
    type=["pdf"]
)


job_description = st.text_area(
    "💼 Job Description",
    height=250,
    placeholder="Paste the job description here..."
)


if st.button(
    "🚀 Analyze Resume",
    use_container_width=True
):

    if resume is None:

        st.error(
            "❌ Please upload a resume PDF."
        )

    elif not job_description.strip():

        st.error(
            "❌ Please enter a job description."
        )

    else:

        with st.spinner(
            "🤖 AI is analyzing your resume..."
        ):

            try:

                response = requests.post(
                    "http://backend:8001/analyze",
                    files={
                        "resume": (
                            resume.name,
                            resume.getvalue(),
                            "application/pdf"
                        )
                    },
                    data={
                        "job_description": job_description
                    },
                    timeout=300
                )

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Could not connect to the backend. "
                    "Please make sure the backend service is running."
                )

                st.stop()

            except requests.exceptions.Timeout:

                st.error(
                    "⏳ The analysis request timed out. "
                    "Please try again later."
                )

                st.stop()

            except requests.exceptions.RequestException as e:

                st.error(
                    "❌ A network error occurred."
                )

                st.code(
                    str(e)
                )

                st.stop()


        if response.status_code == 200:

            result = response.json()

            st.success(
                "✅ Resume analysis completed!"
            )

            st.divider()

            st.subheader(
                "💼 Job Information"
            )

            st.write(
                f"**Position:** {result['job_title']}"
            )

            st.divider()

            st.subheader(
                "📊 Resume Match Score"
            )

            score = result["match_score"]

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Overall Match",
                    f"{score}/100"
                )

            with col2:

                st.metric(
                    "Matched Skills",
                    len(result["matched_skills"])
                )

            with col3:

                st.metric(
                    "Missing Skills",
                    len(result["missing_skills"])
                )

            st.progress(
                min(score / 100, 1.0),
                text=f"Resume Match: {score}/100"
            )

            if score >= 80:

                st.success(
                    "🌟 Excellent match for this role."
                )

            elif score >= 60:

                st.info(
                    "👍 Good match, but there are some areas to improve."
                )

            elif score >= 40:

                st.warning(
                    "⚠️ Moderate match. Consider improving the missing skills."
                )

            else:

                st.error(
                    "🚨 Low match. Significant skill gaps were detected."
                )

            st.divider()

            col1, col2 = st.columns(2)

            with col1:

                st.subheader(
                    "✅ Matched Skills"
                )

                if result["matched_skills"]:

                    for skill in result["matched_skills"]:

                        st.success(
                            f"✓ {skill}"
                        )

                else:

                    st.info(
                        "No required skills were matched."
                    )

            with col2:

                st.subheader(
                    "❌ Missing Skills"
                )

                if result["missing_skills"]:

                    for skill in result["missing_skills"]:

                        st.error(
                            f"✗ {skill}"
                        )

                else:

                    st.success(
                        "🎉 No required skills are missing!"
                    )

            st.divider()

            st.subheader(
                "🧠 Detailed Skill Analysis"
            )

            for skill in result["skill_analysis"]:

                evidence = skill["evidence_strength"]

                match = skill["match"]

                status = (
                    "✅ Matched"
                    if match
                    else "❌ Not Matched"
                )

                with st.expander(
                    f"{skill['skill']} — {status}"
                ):

                    col1, col2 = st.columns(2)

                    with col1:

                        st.write(
                            f"**Match:** "
                            f"{'Yes' if match else 'No'}"
                        )

                    with col2:

                        st.write(
                            f"**Evidence:** {evidence}"
                        )

                    st.write(
                        f"**Explanation:** "
                        f"{skill['explanation']}"
                    )

            st.divider()

            st.subheader(
                "💡 Improvement Suggestions"
            )

            suggestions = result["suggestions"]

            if suggestions:

                for suggestion in suggestions:

                    priority = suggestion["priority"]

                    if priority == "High":

                        priority_label = "🔴 High Priority"

                    elif priority == "Medium":

                        priority_label = "🟡 Medium Priority"

                    else:

                        priority_label = "🟢 Low Priority"

                    with st.expander(
                        f"🎯 {suggestion['skill']} — {priority_label}"
                    ):

                        st.write(
                            f"**Priority:** {priority}"
                        )

                        st.write(
                            f"**What to do:** "
                            f"{suggestion['suggestion']}"
                        )

            else:

                st.success(
                    "🎉 No improvement suggestions! "
                    "Your resume covers all required skills."
                )


        elif response.status_code == 429:

            st.error(
                "💳Groq API quota exceeded."
            )

            st.warning(
                "Your Groq API credits or usage limit "
                "has been reached. Please check your Groq "
                "API billing and usage before running the "
                "analysis again."
            )


        elif response.status_code == 401:

            st.error(
                "🔐 Groq API authentication failed."
            )

            st.warning(
                "Please check that your Groq API key "
                "is valid."
            )


        elif response.status_code == 503:

            st.error(
                "🌐 Groq API is currently unavailable."
            )

            st.warning(
                "The backend could not connect to Groq. "
                "Please try again later."
            )


        elif response.status_code == 502:

            st.error(
                "⚠️ Groq API returned an error."
            )

            st.warning(
                "The AI service returned an unexpected "
                "response. Please try again later."
            )


        elif response.status_code == 400:

            st.error(
                "❌ Invalid request."
            )

            try:

                error_data = response.json()

                st.warning(
                    error_data.get(
                        "detail",
                        "Please check your uploaded resume "
                        "and job description."
                    )
                )

            except Exception:

                st.warning(
                    "Please check your uploaded resume "
                    "and job description."
                )


        else:

            st.error(
                f"❌ Server error: {response.status_code}"
            )

            try:

                error_data = response.json()

                st.warning(
                    error_data.get(
                        "detail",
                        "An unexpected server error occurred."
                    )
                )

            except Exception:

                st.code(
                    response.text
                )