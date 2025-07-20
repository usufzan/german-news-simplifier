# German News Simplifier
# Copyright (C) 2025 usufzan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>.

import requests
import json
import sys
from readability import Document
from markdownify import markdownify as md

# The URL of the German news article you want to simplify.
ARTICLE_URL = 'https://www.dw.com/de/frantz-fanon-algeriens-befreiungsheld-w%C3%A4re-100-jahre-alt/a-73309704' #Please insert the link you'd like to get simplified here

# The name of the model you have downloaded in Ollama.
# Run `ollama list` in your terminal to see available models.
OLLAMA_MODEL = 'gemma:latest'

# The API endpoint for your local Ollama instance. This is the default and usually does not need to be changed.
OLLAMA_API_ENDPOINT = 'http://localhost:11434/api/chat'

# The filename of the prompt that defines the LLM's role and task.
PROMPT_FILENAME = 'prompt_a2_tutor.md' 


def load_prompt_from_file(filename):

    print(f"   -> Loading system prompt from '{filename}'...")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"\nError: Prompt file not found at '{filename}'")
        print("Please make sure the prompt file is in the same directory as the script.")
        sys.exit(1) 
    except Exception as e:
        print(f"\nAn unexpected error occurred while reading the prompt file: {e}")
        sys.exit(1)

def fetch_and_parse_article(url):

    print(f"1. Fetching article from: {url}")

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    print("2. Extracting clean article content...")
    
    doc = Document(response.text)
    article_title = doc.title()
    clean_html = doc.summary()
    
    print(f"   -> Successfully extracted article: '{article_title}'")
    
    print("3. Converting clean HTML to Markdown...")
    
    markdown_content = md(clean_html, heading_style="ATX")
    return f"# {article_title}\n\n{markdown_content}"
    print("# {article_title}\n\n{markdown_content}")

def get_simplified_text_from_ollama(system_prompt, article_text):

    print("\n4. Sending article to Ollama with the detailed prompt...")


    ollama_payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": article_text}
        ],
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_ENDPOINT, json=ollama_payload)
        response.raise_for_status()
        print("5. Received response from Ollama.")
        response_data = response.json()

        return response_data.get('message', {}).get('content', 'Error: Could not find content in Ollama response.')

    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to Ollama. Is Ollama running?"
    except requests.exceptions.RequestException as e:
        return f"Error: A request to Ollama failed. Details: {e}"


if __name__ == "__main__":
    try:
        system_prompt = load_prompt_from_file(PROMPT_FILENAME)
        
        markdown_article = fetch_and_parse_article(ARTICLE_URL)
        
        simplified_version = get_simplified_text_from_ollama(system_prompt, markdown_article)

        print("\n" + "="*50)
        print("   Final Output Based on Your Custom Prompt")
        print("="*50 + "\n")
        print(simplified_version)

    except requests.exceptions.RequestException as e:
        print(f"\nError: Could not fetch the URL. Please check the link and your connection.")
        print(f"   Details: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")