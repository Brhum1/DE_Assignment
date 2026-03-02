"""
    Multiple Inheritance in Python (this is task 1)

Definition:
تعتبر الوراثة المتعددة ميزة قوية في لغة بايثون
تسمح للكلاس الواحد أن يرث الخصائص والدوال من أكثر من كلاس أب في نفس الوقت.
هذا يعني أن الكلاس الابن يمكنه تجميع ميزات من مصادر مختلفة
"""
# مثال
class Camera:
    def take_photo(self):
        print("Taking a high-quality photo...")

class Phone:
    def make_call(self):
        print("Dialing a number...")

# الوراثة المتعددة هنا
class Smartphone(Camera, Phone):
    pass

# تجربة الكود
my_phone = Smartphone()
my_phone.take_photo()  # ورثها من Camera
my_phone.make_call()   # ورثها من Phone

"""=========================================================="""
"""
    Built-in Packages and Modules in Python (task 2)
    الحزم والموديلات المبنية داخلياً هي عبارة عن مكتبات برمجية تأتي محملة مسبقاً مع لغة بايثون عند تثبيتها
      الهدف منها هو توفير أدوات جاهزة للمبرمج للقيام بمهام معقدة مثل العمليات الحسابية أو التعامل مع الوقت دون الحاجة لكتابة الكود من الصفر 
"""
# مثال
import math
print(math.sqrt(16))  # دالة حساب الجذور التربيعية

import os 
os.system('cls' if os.name == 'nt' else 'clear') # هذا ينظف الشاشة في الكونسول من اي كتابة فيها سواء للويندوز او للينكس