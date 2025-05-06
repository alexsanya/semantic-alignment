📘 AI-Powered Bilingual Book Alignment with OpenAI & spaCy
Transform two editions of the same book (e.g., Russian and Spanish) into a bilingual reading experience using semantic embeddings and language models. This project aligns matching fragments from both versions using OpenAI embeddings and spaCy NLP.

📌 Overview
We aim to:

Segment the Russian edition into context-rich fragments

Embed and match them semantically with fragments from the Spanish edition

Build a parallel, bilingual text for immersive reading (and audiobook generation!)

🧰 Prerequisites
Python 3.11 (not 3.13+ due to spaCy compatibility)

spaCy, openai, googletrans, more-itertools, and numpy

bash
Copy
Edit
# Set up environment
pyenv virtualenv 3.11.8 bilingual-align
pyenv activate bilingual-align

# Install dependencies
pip install spacy openai googletrans==4.0.0-rc1 more-itertools numpy
python -m spacy download ru_core_news_lg
python -m spacy download es_dep_news_trf
Step 1: Split the Native Text into Chunks
python
Copy
Edit
import spacy
nlp_ru = spacy.load("ru_core_news_lg")

def split_into_chunks(text: str, max_chars: int = 300) -> list:
    doc = nlp_ru(text)
    sentences = [sent.text.strip() for sent in doc.sents]

    chunks = []
    current_chunk = ""
    for sent in sentences:
        if len(current_chunk) + len(sent) <= max_chars:
            current_chunk += (" " if current_chunk else "") + sent
        else:
            chunks.append(current_chunk)
            current_chunk = sent
    if current_chunk:
        chunks.append(current_chunk)

    return chunks
Load and Process File
python
Copy
Edit
from pathlib import Path

def load_text_from_file(filepath: str) -> str:
    return Path(filepath).read_text(encoding='utf-8')

text_ru = load_text_from_file("text_rus.txt")
chunks_ru = split_into_chunks(text_ru, max_chars=300)
Step 2: Break Long Spanish Sentences
Some Russian sentences may correspond to a single long sentence in Spanish. We'll split these to improve alignment.

python
Copy
Edit
from more_itertools import split_at

def break_long_sentences(doc):
    sublists = list(" ".join(line) for line in split_at([d.text for d in doc], lambda x: x == ","))
    return [chunk + ',' if i < len(sublists) - 1 else chunk for i, chunk in enumerate(sublists)]
Step 3: Translate & Embed Chunks
python
Copy
Edit
from googletrans import Translator
translator = Translator()

async def translate_russian_to_spanish(text: str) -> str:
    result = await translator.translate(text, src="ru", dest="es")
    return result.text
python
Copy
Edit
from openai import OpenAI
from typing import List
import numpy as np

client = OpenAI()

def get_embedding(text: str, model="text-embedding-3-small", **kwargs) -> List[float]:
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model, **kwargs)
    return response.data[0].embedding

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
Example Match & Score
python
Copy
Edit
# Evaluate semantic similarity between the first chunk in Russian and the first 3 chunks in Spanish
translated_ru = await translate_russian_to_spanish(chunks_ru[0])
es_snippet = " ".join(chunks_es[0:3])

similarity = cosine_similarity(get_embedding(translated_ru), get_embedding(es_snippet))
print(similarity)
Expected output:

python
Copy
Edit
0.8654  # High score indicates a strong semantic match
🔁 Alignment Strategy
Use a greedy pointer-based alignment algorithm:

Translate a Russian chunk into Spanish

Expand Spanish chunks one by one

Track the similarity score

Stop when the score starts decreasing

This helps find the best one-to-many match between the two texts.

🔜 Coming Next
A complete alignment script

Automatic generation of a bilingual book

Bonus: Convert it into a bilingual audiobook using Google Text-to-Speech!

📎 Resources
OpenAI Embeddings Guide

Semantic Search Example

spaCy

Cosine Similarity (Wikipedia)


