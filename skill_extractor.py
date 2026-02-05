import re

TECH_KEYWORDS = [
    "python","sql","tableau","power","bi","excel","aws","azure","gcp",
    "pandas","numpy","matplotlib","seaborn","nlp","machine","learning",
    "etl","spark","hadoop","looker","git","tensorflow","pytorch"
]

def extract_skills_from_text(text):

    text = text.lower()

    found_skills = []

    for keyword in TECH_KEYWORDS:
        if keyword in text:
            found_skills.append(keyword)

    return list(set(found_skills))


def compare_skills(resume_skills, jd_skills):

    matched = list(set(resume_skills) & set(jd_skills))
    missing = list(set(jd_skills) - set(resume_skills))

    return matched, missing
