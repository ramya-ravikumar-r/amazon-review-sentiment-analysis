import streamlit as st
from utils import load_pdf, chunk_text
from vector_store import compute_ats_score
from skill_extractor import extract_skills_from_text, compare_skills


st.set_page_config(page_title="GenAI Resume Analyzer")

st.title("GenAI Resume Analyzer")

# ---------------- UI INPUT ---------------- #

resume_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
jd_text = st.text_area("Paste Job Description")

analyze_btn = st.button("Analyze Resume")


# ---------------- PROCESSING ---------------- #

if analyze_btn:

    if not resume_file or not jd_text:
        st.warning("Please upload resume and paste job description")

    else:

        # Save uploaded resume
        with open("temp_resume.pdf", "wb") as f:
            f.write(resume_file.read())

        with st.spinner("Analyzing Resume..."):

            # Extract Resume Text
            resume_text = load_pdf("temp_resume.pdf")

            # Chunk Resume
            resume_chunks = chunk_text(resume_text)

            # -------- Semantic ATS Score -------- #
            semantic_score = compute_ats_score(resume_chunks, jd_text)

            # -------- JD Driven Skill Extraction -------- #
            resume_skills = extract_skills_from_text(resume_text)
            jd_skills = extract_skills_from_text(jd_text)

            matched_skills, missing_skills = compare_skills(resume_skills, jd_skills)

            # -------- Skill Match Score -------- #
            skill_score = (len(matched_skills) / len(jd_skills)) * 100 if jd_skills else 0

            # -------- Final ATS Score -------- #
            final_score = (0.7 * semantic_score) + (0.3 * skill_score)

        # ---------------- OUTPUT ---------------- #

        st.success("Resume processed successfully!")

        # Final ATS Score
        st.subheader("Final ATS Match Score")
        st.metric(label="Resume Match", value=f"{final_score:.2f}%")

        # Score Interpretation
        if final_score >= 75:
            st.success("Strong Match – Resume aligns well with Job Description")
        elif final_score >= 50:
            st.warning("Moderate Match – Resume can be improved")
        else:
            st.error("Low Match – Resume needs significant improvement")

        # ---------------- SKILL OUTPUT ---------------- #

        st.subheader("Matched Skills")
        st.write(", ".join(matched_skills) if matched_skills else "No matched skills found")

        st.subheader("Missing Skills")
        st.write(", ".join(missing_skills) if missing_skills else "No missing skills")
