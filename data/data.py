# %%
import numpy as np
import faiss
import pickle

# %%
# Função para carregar vetores GloVe
def load_glove_model(file_path, expected_dim=50):
    glove_model = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.replace(',', '.').split()
            word = parts[0]
            try:
                vector = np.array(parts[1:], dtype=np.float32)
                if vector.shape[0] == expected_dim:
                    glove_model[word] = vector
                else:
                    print(f"Skipping line with wrong dimension: {line}")
            except ValueError:
                print(f"Skipping line with error: {line}")
    return glove_model

# Caminho para o arquivo GloVe 
glove_file = '../corpus/glove_s50.txt'

# Carrega o modelo GloVe
glove_model = load_glove_model(glove_file)

words = list(glove_model.keys())
vectors = np.array(list(glove_model.values()))
# %%
dimension = vectors.shape[1]  
index = faiss.IndexFlatL2(dimension) 

# %%
index.add(vectors)
# %%
# Save the FAISS index to a file
index_file = 'glove_index.faiss'
faiss.write_index(index, index_file)
print(f"FAISS index saved to {index_file}")

# %%
word_to_index_file = 'word_to_index.pkl'
with open(word_to_index_file, 'wb') as f:
    pickle.dump(words, f)
print(f"Word-to-index mapping saved to {word_to_index_file}")

