from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load embedding model once
model = SentenceTransformer('all-MiniLM-L6-v2')


def generate_resume_embeddings(resume_chunks):
    return model.encode(resume_chunks)


def generate_jd_embedding(jd_text):
    return model.encode([jd_text])


def compute_ats_score(resume_chunks, jd_text):

    resume_embeddings = generate_resume_embeddings(resume_chunks)
    jd_embedding = generate_jd_embedding(jd_text)

    similarity_scores = cosine_similarity(resume_embeddings, jd_embedding)

    ats_score = similarity_scores.mean()

    return round(float(ats_score) * 100, 2)
