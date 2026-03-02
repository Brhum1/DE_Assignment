import csv
import os

class FileHandler:
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def load_from_csv(file_path):
        students_data = []
        try:
            if not os.path.exists(file_path):
                return []
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        grades = [float(g.strip()) for g in row['grades'].split(',')]
                        students_data.append({'id': row['id'], 'name': row['name'], 'grades': grades})
                    except (ValueError, KeyError):
                        continue # تخطي السطر التالف والاستمرار
        except Exception as e:
            print(f" ERROR: {e}")
        return students_data
    
    @staticmethod
    def save_to_csv(file_path, students):
        """حفظ قائمة الطلاب إلى ملف CSV"""
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                fieldnames = ['id', 'name', 'grades']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for s in students:
                    grades_str = ",".join(map(str, s.grades))
                    writer.writerow({
                        'id': s.student_id,
                        'name': s.name,
                        'grades': grades_str
                    })
        except Exception as e:
            print(f"ERROR while saving: {e}")

    @staticmethod
    def validate_input(prompt, type_func):
        while True:
            try:
                user_input = input(prompt).strip()
                if not user_input:
                    raise ValueError("Empty input")
                return type_func(user_input)
            except ValueError:
                print(" Unvalid input, please enter a correct value")