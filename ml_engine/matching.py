# Simple text similarity without sklearn (temporary replacement)
def compute_similarity(student_skills, teacher_skills):

    if not student_skills or not teacher_skills:
        return 0.0

    # Convert to sets for simple Jaccard similarity
    student_set = set(skill.lower() for skill in student_skills)
    teacher_set = set(skill.lower() for skill in teacher_skills)

    # Calculate Jaccard similarity
    intersection = len(student_set & teacher_set)
    union = len(student_set | teacher_set)

    if union == 0:
        return 0.0

    return float(intersection) / union