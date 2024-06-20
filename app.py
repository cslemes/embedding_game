import streamlit as st
import numpy as np
from backend import (
    get_secret_word,
    get_neihgboors,
    get_distance_rank,
    write_charade,
    secret_word_list
) 

@st.experimental_dialog("Mostrar Vizinhos")
def show_neihgboors(neighboors):
    neighboors = neighboors.drop(columns="l2_distance")    
    st.dataframe(
    neighboors,
    column_config={
        "word": "Palavra",
        "distance": st.column_config.NumberColumn(
            "Distancia",
            format="%d ⬆️",
    ),
    },
    hide_index=True
    )

@st.experimental_dialog("Mostrar Dicas")
def show_guesses(guess):
    guess = guess.drop(columns="l2_distance")  
    st.dataframe(
    guess,
    column_config={
        "word": "Palavra",
        "distance": st.column_config.NumberColumn(
            "Distancia",
            format="%d ⬆️",           
            ),
    },      
    hide_index=True
    )           

@st.cache_data
def escolhendo_palavra(guessed_word):
    return get_neihgboors(guessed_word)

@st.cache_data
def cache_secret_wordlist():
    return secret_word_list()

def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )

st.set_page_config(page_icon="🕹️", layout="wide",
    page_title="Jogo de palavras")


# Initialize session state
# ----------------------
if 'secret_word' not in st.session_state:
    st.session_state.secret_word = get_secret_word(cache_secret_wordlist())
    
if 'attempts' not in st.session_state:
    st.session_state.attempts = []

if 'w_guessed_word' not in st.session_state: 
    st.session_state.w_guessed_word = []

if 'charade' not in st.session_state:
    st.session_state.charade = write_charade(st.session_state.secret_word)

# Declare functions
# -----------------

def submit():
    st.session_state.w_guessed_word = st.session_state.widget
    st.session_state.widget = ""

def submit_guessed_word(guessed_word):   
    guessed_word = guessed_word.lower().strip()
    df_neihgboors = escolhendo_palavra(st.session_state.secret_word)
    distance = get_distance_rank(guessed_word, df_neihgboors)        
    st.session_state.attempts.append((guessed_word, distance))    
    if distance > 1000:
        str_distance = "Longe demais 😒"
    else:
        str_distance = f"{distance} 🤔"
        
    st.markdown(
    f"""
    **Distancia:** {str_distance} **Tentativas:** {len(st.session_state.attempts)}

    """,
    unsafe_allow_html=True
    )
    if guessed_word.lower() == st.session_state.secret_word.lower():
        st.success(f"Parabens! Você descobriu a palavra: {st.session_state.secret_word}")
        st.balloons()
        if st.button("Vizinhos"):
            df_neihgboors = escolhendo_palavra(st.session_state.secret_word)
            show_neihgboors(df_neihgboors)    
    else:
        st.info("Tente de novo!")

def register_attempts():
    for attempt, distance in reversed(list(st.session_state.attempts)):
        st.error(f'{attempt} {distance}')


# ---------------------------   

# Start UI design

# ---------------------------
# Side Bar
with st.sidebar:   
    if st.button('Novo Jogo'):
        st.session_state.secret_word = get_secret_word(cache_secret_wordlist())
        st.session_state.attempts = []
        st.session_state.charade = write_charade(st.session_state.secret_word)
        st.session_state.attempts = []
        st.session_state.w_guessed_word = []        
        escolhendo_palavra(st.session_state.secret_word)

        print(st.session_state.secret_word)
    if prompt := st.button("Dicas"):
        df_neihgboors = escolhendo_palavra(st.session_state.secret_word)
        numero = np.random.randint(2, 50)
        guessed_word = df_neihgboors.loc[[numero]]['word'].values[0]
        st.session_state.w_guessed_word = guessed_word


    st.markdown(
    """    
    ### Como jogar 🎲 ###
    O jogo sorteia uma palavra e daí cria uma charada para você tentar adivinhar qual palavra é.
    Quanto mais longe da resposta certa maior a distância.	
    O Jogo calcula a distância entre as palavras. De acordo com seu contexto de uso gramatical.
    As palavras são sorteadas aleatoriamente de um arquivo de palavras.
    """
)    


## -------------------------------
## Body
icon("📝")
st.subheader("Advinhe a palavra secreta!", divider="rainbow", anchor=False)

escolhendo_palavra(st.session_state.secret_word)
# st.write(f"Palavra secreta gerada!")

st.markdown(st.session_state.charade)

st.text_input("Digite seu palpite: ", key="widget", on_change=submit)
guessed_word = st.session_state.w_guessed_word

if guessed_word:
    submit_guessed_word(guessed_word)

register_attempts()

print(st.session_state.secret_word)