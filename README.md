# embedding_game
# Word Guessing Game with Streamlit

Welcome to the Word Guessing Game implemented with Streamlit! This interactive game allows users to guess a secret word based on clues provided. The game uses embeddings and distance metrics to help users narrow down their guesses.

## Features

- **Random Secret Word**: A secret word is randomly selected from a pre-defined list of words.
- **Clue Generation**: Each secret word comes with a charade-like clue to assist in guessing.
- **Distance Calculation**: Utilizes word embeddings and the L2 distance metric to determine how close a guessed word is to the secret word.
- **Hint System**: Provides hints by showing neighboring words based on their similarity to the secret word.
- **Persistent State**: Keeps track of user attempts and allows restarting the game with a new secret word.

## Technologies Used

- **Streamlit**: Front-end framework for building interactive web applications with Python.
- **numpy**: Library for numerical computing.
- **pandas**: Data manipulation and analysis library.
- **FAISS**: Library for efficient similarity search and clustering of dense vectors.
- **NLTK**: Natural Language Toolkit for natural language processing tasks.

## How to Run

1. Clone the repository:

```
git clone <repository_url>
cd <repository_name>
```

2. Install dependencies:


```
pip install -r requirements.txt
```


3. Run the Streamlit app:

```
streamlit run game_app.py
```



4. Access the game in your browser at `http://localhost:8501`.

## Screenshots

Include screenshots or GIFs of the game interface and key features in action.

## Contributing

Contributions are welcome! Please follow the guidelines in `CONTRIBUTING.md`.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Acknowledgments

- Mention any acknowledgments of libraries, tools, or people whose work has been instrumental in this project.
