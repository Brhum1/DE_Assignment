from fastapi import FastAPI
from scraper import fetch_top_news # نستدعي دالتك التي جربتها للتو!

# تهيئة التطبيق
app = FastAPI(
    title="Hacker News API",
    description="An API that serves the top stories from Hacker News.",
    version="1.0"
)

# نقطة الوصول الرئيسية للترحيب
@app.get("/")
def read_root():
    return {"message": "Welcome to Hacker news API! Visit /api/news to get the data."}

# نقطة الوصول الخاصة بالبيانات (الـ Endpoint المطلوب في التكليف)
@app.get("/api/news")
def get_news():
    print("Received a request for news. Fetching data...")
    # نقوم بتشغيل سكربت الاستخراج الخاص بك
    data = fetch_top_news()
    
    # نعيد البيانات منسقة كـ JSON
    return {
        "status": "success",
        "total_articles": len(data),
        "data": data
    }
