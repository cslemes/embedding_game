# %%
import numpy as np
import pandas as pd
from typing import Generator
import faiss
import pickle
from groq import Groq
import os
from dotenv import load_dotenv
from os.path import join

# %%
def load_index_file():
    index_file = 'glove_index.faiss'
    #index_file = join('data', 'glove_index.faiss')
    return faiss.read_index(index_file)


def load_word_to_index_file():
    word_to_index_file = 'word_to_index.pkl'
    #word_to_index_file = join('data', 'word_to_index.pkl')
    with open(word_to_index_file, 'rb') as f:
        return pickle.load(f)


# %%
def get_embedding(word):
    index = load_index_file()   
    words = load_word_to_index_file()    
    if word not in words:
        raise ValueError(f"Palavra '{word}' não encontrada.")   
    word_index = words.index(word)        
    embedding = index.reconstruct(word_index)    
    return embedding

# %%

# %%
def get_secret_word(df_secret_word):
    while True:    
        secret_word = df_secret_word.sample(n=1)['word'].values[0]
        if secret_word.isdigit(): 
            continue
        if len(secret_word) >= 3:
            break
    return secret_word.lower()

# %%
# Obtem as top k palavras vizinhas
def get_neihgboors(secret_word):
    index = load_index_file()
    words = load_word_to_index_file()
    k = 1000
    embedding=get_embedding(secret_word)    
    query_vector = np.array(embedding).reshape(1, -1)
    distances, indices = index.search(query_vector, k)
    result_words = [words[idx] for idx in indices[0]]
    result_distances = distances[0]
    result_rank = [i for i in range(1, k+1)]
    results_df = pd.DataFrame({            
        'word': result_words,
        'distance': result_rank,
        'l2_distance': result_distances
    })
    return results_df
    
# %%
# Obtem a distancia pelo contador do pandas
def get_distance_rank(guessed_word, df_rank):
    rank_distance = df_rank[df_rank['word'] == guessed_word]
    if rank_distance.empty:
        return 9999
    else:
        return rank_distance.index.values[0]+1
# %%  
# %% 
def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


# %%
def write_charade(secret_word):
    load_dotenv()
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
    )
    prompt = f"crie uma charada com a palavra {secret_word}, não fale a palavra na charada"

    chat_completion = client.chat.completions.create(
        messages = [{"role": "user", "content": prompt}],
        model="llama3-8b-8192",
        temperature=1.0,
        max_tokens=1024,
        stream=False,
    )
    return chat_completion.choices[0].message.content

def secret_word_list():
    df_secret_word = pd.read_pickle('secret_words.pkl')
    return df_secret_word