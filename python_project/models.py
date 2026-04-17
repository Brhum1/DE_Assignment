class Student:
    def __init__(self, student_id, name, grades):
        self.__student_id = student_id
        self.name = name
        self.grades = grades 

    @property
    def student_id(self):
        return self.__student_id

    def calculate_average(self):
        try:
            return sum(self.grades) / len(self.grades) if self.grades else 0
        except Exception:
            return 0

    def get_grade_category(self):
        try:
            avg = self.calculate_average()
            if avg >= 90: 
                return "Excellent"
            elif avg >= 80: 
                return "Very Good"
            elif avg >= 65: 
                return "Good"
            elif avg >= 50:
                return "Pass"
            else: 
                return "Fail"
        except Exception:
            return "N/A"

class Classroom:
    def __init__(self):
        self.students = []

    def generate_next_id(self):
        try:
            if not self.students:
                return "1"
            
            ids = [int(s.student_id) for s in self.students if s.student_id.isdigit()]
            if not ids:
                return str(len(self.students) + 1)
                
            return str(max(ids) + 1) 
        except Exception:
            return str(len(self.students) + 1)

    def add_student(self, student):
        self.students.append(student)

    def remove_student(self, student_id):
        self.students = [s for s in self.students if s.student_id != student_id]

    def search_student(self, student_id):
        for s in self.students:
            if s.student_id == student_id:
                return s
        return None
    
    def calculate_classroom_average(self):
        try:
            if not self.students:
                return 0.0
            
            total_averages = sum(s.calculate_average() for s in self.students)

            return total_averages / len(self.students)
        except Exception:
            return 0.0