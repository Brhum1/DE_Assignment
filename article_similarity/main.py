import csv
import numpy as np
import re
import pickle

def read_articles(file_path):
    articles = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            articles.append(row)
    return articles

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.split()

def build_vocabulary(all_cleaned_contents):
    vocabulary = set()
    for content in all_cleaned_contents:
        vocabulary.update(content)
    return sorted(list(vocabulary))

def build_vectors(all_cleaned_contents, vocabulary):
    vectors = []
    word_to_index = {word: i for i, word in enumerate(vocabulary)}
    
    for content in all_cleaned_contents:
        vector = np.zeros(len(vocabulary))
        content_set = set(content)
        for word in content_set:
            if word in word_to_index:
                vector[word_to_index[word]] = 1
        vectors.append(vector)
    
    return np.array(vectors)

def calculate_similarity_matrix(vectors):
    dot_product = np.dot(vectors, vectors.T)
    norms = np.linalg.norm(vectors, axis=1)
    
    norms[norms == 0] = 1e-10 
    
    similarity_matrix = dot_product / np.outer(norms, norms)
    return similarity_matrix

def get_top_3_similar(article_id, articles, similarity_matrix):
    try:
        idx = next(i for i, a in enumerate(articles) if a['id'] == str(article_id))
    except StopIteration:
        return "Article ID not found."
    
    scores = similarity_matrix[idx]
    
    related_indices = np.argsort(scores)[::-1]
    related_indices = [i for i in related_indices if i != idx][:3]
    
    return [articles[i]['title'] for i in related_indices]

# --- MAIN EXECUTION  ---

articles_data = read_articles('articles.csv')

cleaned_contents = [clean_text(a['content']) for a in articles_data]
global_vocab = build_vocabulary(cleaned_contents)
article_vectors = build_vectors(cleaned_contents, global_vocab)

sim_matrix = calculate_similarity_matrix(article_vectors)

with open('similarities.pkl', 'wb') as f:
    pickle.dump(sim_matrix, f)

print("--- Similarity Analysis Results ---")
target_id = 1
top_3 = get_top_3_similar(target_id, articles_data, sim_matrix)

print(f"Top 3 articles similar to '{articles_data[0]['title']}':")
for i, title in enumerate(top_3, 1):
    print(f"{i}. {title}")