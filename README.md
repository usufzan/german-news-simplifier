# German News Simplifier

This Python script simplifies German news articles for A2-level language learners using a local LLM via Ollama. It fetches an article from a URL, cleans it, and then uses a custom prompt to generate a simplified version, a glossary, and a comprehension question.

## Prerequisites

* Python 3.x
* [Ollama](https://ollama.com/) installed and running.
* An Ollama model downloaded, e.g., `ollama pull gemma`

## Setup

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/usufzan/german-news-simplifier.git](https://github.com/usufzan/german-news-simplifier.git)
    cd german-news-simplifier
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # For Mac/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

## How to Use

1.  Make sure your local Ollama instance is running.
2.  Open `simplify_article.py` and change the `ARTICLE_URL` variable to the news article you want to simplify.
3.  If you use a different model, update the `OLLAMA_MODEL` variable.
4.  Run the script from your terminal:
    ```sh
    python simplify_article.py
    ```

The simplified output will be printed directly to your console.
