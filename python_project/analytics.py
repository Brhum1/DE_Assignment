def get_top_student(students):
    return max(students, key=lambda s: s.calculate_average()) if students else None

def rank_students(students):
    return sorted(students, key=lambda s: s.calculate_average(), reverse=True)

def get_grade_distribution(students):
    dist = {"A": 0, "B": 0, "C": 0, "F": 0}
    for s in students:
        dist[s.get_grade_category()] += 1
    return dist