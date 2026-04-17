import requests
from bs4 import BeautifulSoup

def fetch_top_news():
    url = "https://news.ycombinator.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        # 1. إرسال الطلب لجلب الصفحة (مرحلة الـ Data Ingestion)
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # التأكد من أن الموقع استجاب بنجاح
        
        # 2. تحويل كود الصفحة إلى كائن BeautifulSoup يسهل البحث فيه
        soup = BeautifulSoup(response.text, 'html.parser')
        news_data = []
        
        # 3. البحث عن الأخبار:
        # موقع Hacker News يضع كل خبر داخل وسم <tr> يحمل الكلاس 'athing'
        articles = soup.find_all('tr', class_='athing')
        
        for article in articles:
            # استخراج العنوان والرابط
            titleline = article.find('span', class_='titleline')
            if not titleline or not titleline.a:
                continue
                
            title = titleline.a.text
            link = titleline.a['href']
            
            # 4. استخراج النقاط (التقييم):
            # موقعهم مصمم بحيث تكون النقاط في السطر <tr> الذي يلي سطر العنوان مباشرة
            next_row = article.find_next_sibling('tr')
            score_span = next_row.find('span', class_='score') if next_row else None
            
            # 5. تنظيف البيانات (Data Cleaning):
            # النص يأتي هكذا "150 points"، نريد تحويله للرقم 150 فقط لسهولة ترتيبه لاحقاً
            if score_span:
                score_text = score_span.text.replace(' points', '').replace(' point', '')
                score = int(score_text)
            else:
                score = 0 # بعض الأخبار الجديدة أو الإعلانات لا تحتوي على تقييم
            
            # تجميع البيانات في قاموس (Dictionary) وإضافتها للقائمة
            news_data.append({
                "title": title,
                "url": link,
                "score": score
            })
            
        # 6. ترتيب البيانات (Data Manipulation):
        # ترتيب الأخبار من الأعلى تقييماً إلى الأقل
        sorted_news = sorted(news_data, key=lambda x: x['score'], reverse=True)
        return sorted_news
        
    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
        return []

# هذا الجزء يعمل فقط إذا قمنا بتشغيل هذا الملف مباشرة للتجربة
if __name__ == "__main__":
    print("Fetching data from Hacker News...\n")
    data = fetch_top_news()
    print(f"Successfully fetched {len(data)} items. Here are the top 5 rated news:")
    print("-" * 50)
    for i, news in enumerate(data[:5], 1): 
        print(f"{i}. {news['title']}")
        print(f"   Score: {news['score']} | Link: {news['url']}\n")