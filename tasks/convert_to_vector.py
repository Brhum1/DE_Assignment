def text_to_vector(text):
    words = text.lower().split()
    
    unique_words = sorted(list(set(words)))
    
    vector = []
    for word in unique_words:
        count = words.count(word)
        vector.append(count)
        
    return unique_words, vector

text_input = "python is great and python is easy"
labels, vec = text_to_vector(text_input)

print(f"words: {labels}")
print(f"Vector: {vec}")