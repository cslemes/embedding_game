import numpy as np
import pandas as pd
from typing import Generator
import faiss
import pickle
from groq import Groq
import os
from dotenv import load_dotenv
from datetime import datetime


def load_index_file():
    index_file = 'glove_index.faiss'
    #index_file = join('data', 'glove_index.faiss')
    return faiss.read_index(index_file)


def load_word_to_index_file():
    word_to_index_file = 'word_to_index.pkl'
    #word_to_index_file = join('data', 'word_to_index.pkl')
    with open(word_to_index_file, 'rb') as f:
        return pickle.load(f)


def get_embedding(word):
    index = load_index_file()   
    words = load_word_to_index_file()    
    if word not in words:
        raise ValueError(f"Palavra '{word}' não encontrada.")   
    word_index = words.index(word)        
    embedding = index.reconstruct(word_index)    
    return embedding


def get_secret_word(df_secret_word):
    while True:    
        secret_word = df_secret_word.sample(n=1)['word'].values[0]
        if secret_word.isdigit(): 
            continue
        if len(secret_word) >= 3:
            break
    return secret_word.lower()


def secret_word_list():
    df_secret_word = pd.read_pickle('secret_words.pkl')
    return df_secret_word

import os
from datetime import date

def get_word_of_the_day(df_secret_word):
    word_pkl = 'word_of_the_day.pkl'
    if not os.path.exists(word_pkl):
        word_of_the_day = get_secret_word(df_secret_word)
        word_date = date.today().strftime('%d %m %Y')
        df = pd.DataFrame({'word': word_of_the_day, 'date': word_date}, index=[0])
        df.to_pickle(word_pkl)
    else:
        df = pd.read_pickle(word_pkl)
        today_date = date.today().strftime('%d %m %Y')
        if df['date'].values[0] == today_date:
            word_of_the_day = df['word'].values[0]
        else:
            word_of_the_day = get_secret_word(df_secret_word)
            df.loc[0, 'word'] = word_of_the_day
            df.loc[0, 'date'] = today_date
            df.to_pickle(word_pkl)
    return word_of_the_day


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
    
# Obtem a distancia pelo contador do pandas
def get_distance_rank(guessed_word, df_rank):
    rank_distance = df_rank[df_rank['word'] == guessed_word]
    if rank_distance.empty:
        return 9999
    else:
        return rank_distance.index.values[0]+1


def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


def write_charade(secret_word):
    load_dotenv()
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
    )
    prompt = f""" Você deve criar uma charada engraçada e criativa com a palavra secreta,
    Você não pode informar a palavra secreta na resposta.
    Palvra secreta: {secret_word} """

    chat_completion = client.chat.completions.create(
        messages = [{"role": "user", "content": prompt}],
        model="llama3-8b-8192",
        temperature=0,
        max_tokens=1024,
        stream=False,
    )
    return chat_completion.choices[0].message.content

