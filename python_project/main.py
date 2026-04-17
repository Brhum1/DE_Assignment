# -	Interactive CLI menu
# -	Uses all modules
# -	Proper error handling
# -	Clean user interaction

from models import Student, Classroom
from utils import FileHandler
from analytics import get_top_student

def main_menu():
    room = Classroom()
    # تحميل البيانات عند البدء مع حماية كاملة [cite: 37, 43]
    initial_data = FileHandler.load_from_csv('data.csv')
    for item in initial_data:
        room.add_student(Student(item['id'], item['name'], item['grades']))

    while True:
        try:
            FileHandler.clear_screen()
            print("====================================")
            print("=== STUDENT PERFORMANCE ANALYZER ===")
            print("====================================")
            print("1.  Add New Student")
            print("2.  Search Student")
            print("3.  Remove Student")
            print("4.  View All Students")
            print("5.  View Top Performer")
            print("0.  Exit")
            print("------------------------------------")
            
            choice = input("Select an option: ")

            if choice == '1':
                FileHandler.clear_screen()
                print("=== Add new Student ===")

                new_id = room.generate_next_id()
                print(f"Student ID: {new_id}")
                name = FileHandler.validate_input("Enter Name: ", str)
                g_raw = FileHandler.validate_input("Enter Grades (e.g. 80,90): ", str)
                
                try:
                    grades = [float(g.strip()) for g in g_raw.split(',')]
                    new_student = Student(new_id, name, grades)
                    room.add_student(new_student)
                    
                    FileHandler.save_to_csv('data.csv', room.students)
                    
                    print("\n Student added and saved to data.csv")
                except Exception as e:
                    print(f"Error adding grades: {e}")
                
                input("Press Enter to continue...")

            elif choice == '2':
                FileHandler.clear_screen()
                print("=== Search for a Student ===")
                search_id = FileHandler.validate_input("Enter ID to search: ", str)
                student = room.search_student(search_id)
                if student:
                    print("\ Student Found:")
                    print("-" * 30)
                    print(f"ID:      {student.student_id}")
                    print(f"Name:    {student.name}")
                    print(f"Grades:  {student.grades}")
                    print(f"Average: {student.calculate_average():.2f}")
                    print(f"Status:  {student.get_grade_category()}")
                    print("-" * 50)
                else:
                    print(f"\nNo student found with ID: {search_id}")
                
                input("\nPress Enter to return to menu...")

            elif choice == '3':
                FileHandler.clear_screen()
                print("=== Remove a Student ===")
                id = FileHandler.validate_input("Enter ID to remove: ", str)
                FileHandler.save_to_csv('data.csv', room.students)
                student_to_remove = room.search_student(id)

                if student_to_remove:
                    student = student_to_remove.name
                    room.remove_student(id)
                    
                    FileHandler.save_to_csv('data.csv', room.students)
                    
                    print(f"\nStudent with ID: {id}, name: {student} has been removed and file updated.")
                else:
                    print(f"\n No student found with ID {id}.")
                
                input("\nPress Enter to return to menu...")

            elif choice == '4':
                FileHandler.clear_screen()
                print("=== View All Students ===")
                if not room.students:
                    print("No students found.")
                else:
                    print(f"{'ID':<10} | {'Name':<15} | {'Avg':<8} | {'Grade'}")
                    print("-" * 45)
                    for s in room.students:
                        print(f"{s.student_id:<10} | {s.name:<15} | {s.calculate_average():<8.2f} | {s.get_grade_category()}")

                    avg_class = room.calculate_classroom_average()
                    print(f"\nCurrent Class Performance: {avg_class:.2f}%")  
                input("\nPress Enter to return to menu...")

            elif choice == '5':
                FileHandler.clear_screen()
                print("=== View Top Performer ===")
                top = get_top_student(room.students)
                if top:
                    print(f"\n Top Student: {top.name} with Average: {top.calculate_average():.2f}")
                else:
                    print("\n No data available to analyze.")
                input("\nPress Enter to return...")

            elif choice == '0':
                print("Exiting... Goodbye!")
                break
            
            else:
                print(" Invalid choice. Please try again.")
                import time; time.sleep(1)

        except Exception as e:
            print(f"\n error occurred: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main_menu()