import requests
from bs4 import BeautifulSoup

def fetch_top_news():
    url = "https://news.ycombinator.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # التأكد من أن الموقع استجاب بنجاح
        soup = BeautifulSoup(response.text, 'html.parser')
        news_data = []
        
        articles = soup.find_all('tr', class_='athing')
        
        for article in articles:
            titleline = article.find('span', class_='titleline')
            if not titleline or not titleline.a:
                continue
                
            title = titleline.a.text
            link = titleline.a['href']
            
            next_row = article.find_next_sibling('tr')
            score_span = next_row.find('span', class_='score') if next_row else None
            
            if score_span:
                score_text = score_span.text.replace(' points', '').replace(' point', '')
                score = int(score_text)
            else:
                score = 0 
            
            news_data.append({
                "title": title,
                "url": link,
                "score": score
            })
            
        sorted_news = sorted(news_data, key=lambda x: x['score'], reverse=True)
        return sorted_news
        
    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
        return []


if __name__ == "__main__":
    print("Fetching data from Hacker News...\n")
    data = fetch_top_news()
    print(f"Successfully fetched {len(data)} items. Here are the top 5 rated news:")
    print("-" * 50)
    for i, news in enumerate(data[:5], 1): 
        print(f"{i}. {news['title']}")
        print(f"   Score: {news['score']} | Link: {news['url']}\n")