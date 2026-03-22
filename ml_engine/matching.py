from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_similarity(student_skills, teacher_skills):

    if not student_skills or not teacher_skills:
        return 0.0

    student_text = " ".join(student_skills)
    teacher_text = " ".join(teacher_skills)

    corpus = [student_text, teacher_text]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    similarity_score = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )

    return float(similarity_score[0][0])