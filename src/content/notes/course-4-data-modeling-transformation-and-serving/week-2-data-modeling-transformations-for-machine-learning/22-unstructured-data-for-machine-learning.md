---
title: "2.2 Unstructured Data for Machine Learning"
course: "Course 4: Data Modeling, Transformation, and Serving"
courseSlug: "course-4-data-modeling-transformation-and-serving"
courseOrder: 4
week: "Week 2: Data Modeling & Transformations for Machine Learning"
weekSlug: "week-2-data-modeling-transformations-for-machine-learning"
weekOrder: 2
order: 2
notionId: "1f7969a7-aa01-8017-917c-eb29354e53f7"
---


## 2.2.1 Image Data for Machine Learning

**Modeling and Processing Unstructured Data for Machine Learning**

Unstructured data -- images, text, audio -- requires specialized preprocessing before it can be fed into ML models. This section covers the techniques for images and text.

**Modeling Image Data for ML Algorithms**

Traditional ML algorithms expect tabular input, but treating images as flat tabular data loses spatial information and creates extremely large feature vectors (a 1000x1000 image becomes a vector of 1 million values), which is computationally expensive and can degrade model performance.

The preferred alternative is a **Convolutional Neural Network (CNN)**. Each layer identifies progressively more complex features -- early layers detect generic patterns while deeper layers capture complex structures. In practice, ML teams start with **pre-trained CNN models** and fine-tune them on their specific task and data.

**Preparing images for deep learning models** typically involves augmentations:
- Resizing
- Scaling features
- Flipping, rotating, cropping
- Adjusting brightness

Example Code for Augmenting Images with Tensorflow

```python
import tensorflow as tf
import matplotlib.pyplot as plt
import tensorflow_datasets as tfds


**load the dataset**
dataset = tfds.load('cats_vs_dogs', split='train', as_supervised=True)

def resize_normalize(image, label, image_size=150):

**resize the image**
  image = tf.image.resize(image, [image_size, image_size])

**normalize the image**
  image = (image / 255.0)
  return image, label

def augment(image, label):
  image = tf.image.random_flip_left_right(image)
  image = tf.image.rot90(image)
  image = tf.image.random_contrast(image, lower=0.2, upper=0.8)
  image = tf.image.random_brightness(image, max_delta=0.5)
  return image, label

image, label = next(iter(dataset))
image, label = resize_normalize(image)
image, label = augment(image)

```


## 2.2.2 Text Preprocessing and Classification

**Preprocessing Text for Analysis and Text Classification**

NLP tasks span a wide range -- sentiment analysis, article classification, chatbots, spam detection, customer segmentation, and product recommendations. Despite advances in language models, text preprocessing remains important: raw text contains typos, inconsistencies, and irrelevant characters; training LLMs is expensive; and text features often need to be combined with categorical or numeric features.

**Preprocessing Text Workflow**

1. **Cleaning** -- Remove punctuation, extra spaces, and meaningless characters
2. **Normalization** -- Convert text to a consistent format: lowercase, expand contractions, convert numbers/symbols to words
3. **Tokenization** -- Split text into individual tokens (words, subwords, or short sentences). The simplest method converts each word into a token.
4. **Removal of Stop Words** -- Filter out common words like "is," "are," "the," "for," "a." Libraries: spaCy, NLTK, Gensim, TextBlob.
5. **Lemmatization** -- Replace each word with its base form or lemma (e.g. "getting"/"got" becomes "get")

```python
import pandas as pd
import re
import unicodedata
import spacy
import numpy as np


**A dictionary expanding common contractions**

**See: github.com/dipanjanS/practical-machine-learning-with-python**
CONTRACTION_MAP = {
    "ain't": "is not",
    "aren't": "are not",
    "can't": "cannot",
    "cz": "because",
    "could've": "could have",
    "couldn't": "could not",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "gonna": "going to",
    "hadn't": "had not",
    "hasn't": "has not",
    "haven't": "have not",
    "isn't": "is not",
    "it's": "it is",
    "let's": "let us",
    "mustn't": "must not",
    "shan't": "shall not",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "that's": "that is",
    "there's": "there is",
    "they'd": "they would",
    "they'll": "they will",
    "they're": "they are",
    "they've": "they have",
    "wanna": "want to",
    "wasn't": "was not",
    "we'd": "we would",
    "we'll": "we will",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what's": "what is",
    "won't": "will not",
    "would've": "would have",
    "wouldn't": "would not",
    "you'd": "you would",
    "you'll": "you will",
    "you're": "you are",
    "you've": "you have"
}

def remove_special_char(text, special_characters = ['~','@', '#', '$', '%','^', '&', '*'], numeric = False):
    """
    This function cleans text from any special characters.
    """
    pattern = '[' + special_characters[0]
    for char in special_characters:
        pattern = pattern + '|' + char
    if (numeric):
        pattern = pattern + '|'+ '0-9'
    pattern = pattern + ']'
    filtered_text = re.sub(pattern, r'', text)
    return filtered_text

def remove_accents(text):
    """
    This function removes accent from text
    """
    filtered_text = unicodedata.normalize(
        'NFKD', text).encode('ascii', 'ignore').decode('utf8')
    return filtered_text

def expand_contractions(text):
    """
    This function expands the contractions in text
    """
    text = " ".join([CONTRACTION_MAP[word] if word in CONTRACTION_MAP else word for word in text.split()])
    return text

def remove_stopwords_punctuation(text, lang_model, lemmatizing=False, stop_words=False):
    """
    This function uses spacy to remove stop_words and punctuation marks.
    It can also replace words with their lemma.
    """
    doc_text = lang_model(text)

    if lemmatizing:
        st= " ".join([token.lemma_ for token in doc_text if not(token.is_punct)])
    else:
        st= " ".join([token.text for token in doc_text if not(token.is_punct)])
    return st

def preprocess_text(text, nlp, special_characters = ['~','@', '#', '$', '%', '^', '&', '*'], numeric = False, lemmatizing=False):
    """
    This function pre-processes the text.
    """
    text =  remove_special_char(text, special_characters, numeric)
    text = text.lower().strip()
    text =  remove_accents(text)
    text = expand_contractions(text)
    filtered_text =  remove_stopwords_punctuation(text, nlp, lemmatizing)
    return filtered_text

```


## 2.2.3 Text Vectorization and Embeddings

**Text Vectorization and Embedding**

After preprocessing, text must be converted into numerical representations. The approach depends on the scale and complexity of the task.

**Traditional Vectorization**

Traditional methods assign numbers to words based on their frequency within documents and across the corpus. A **corpus** is a collection of documents (e.g. all customer reviews), and the **vocabulary** is the set of all unique preprocessed words.

**Bag of Words**

Bag of Words creates binary vectors whose length matches the number of documents in the corpus. A `1` at a given index indicates the word appears in that document. The limitation: high-frequency words get more weight, but they may carry little meaning, while rare words that are more significant to the task get underweighted.
![](/data-engineering-specialization-website/images/6b312fd4-79e8-4792-900a-5b09e27ead0b.png)

**TF-IDF**

**TF-IDF** (Term Frequency-Inverse Document Frequency) accounts for both the weight and rarity of each word. **TF** is the number of times a term appears in a document divided by the document length. **IDF** measures how common or rare that word is across the entire corpus. It is easily computed with scikit-learn.
![](/data-engineering-specialization-website/images/3944827b-0dd0-4b55-8107-353869e2587d.png)

These methods work well for smaller datasets where key words have significance to the task (e.g. sentiment analysis), but they produce high-dimensional sparse vectors and ignore word proximity.

**Word Embeddings**

A word embedding is a dense vector that captures semantic meaning. Models like **word2vec** and **GloVe** learn embeddings from word co-occurrences. However, word embeddings ignore position within a sentence. **Sentence embeddings** solve this by capturing the semantic meaning of entire sentences in lower-dimensional vectors than TF-IDF produces.

Pre-trained NLP models for embeddings:
- **Open Source**: SentenceTransformers (sbert.net)
- **Closed Source**: OpenAI, Anthropic, Google

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


**load a pre-trained sentence transformer model**
embedder = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
	"this is a wonderful price for the amount you get",
	"great product big amount",
	"I bought this for my son",
	]


**encode sentences**
embeddings = embedder.encode(sentences)

print(embeddings.shape) # (3, 384)

sim = cosine_similarity(embeddings, embeddings)[0, 1:] # similarity to first sentence

print(sim) # array([0.5106675, 0.13981295])

```

Embeddings can be used as features for ML algorithms, or for clustering and similarity search.

Example: Vectorizing Text with Scikit-Learn

```python
from sklearn.feature_extraction.text import CountVectorizer

reviews = ["this wonderful price amount you get",
         "great product big amount",
         "I buy this my son his hair thin"]


**bag of words**
vectorizer_bag_words = CountVectorizer(token_pattern='(?u)\\b\\w+\\b')


**fit-transform**
vectorizer_bag_words.fit(reviews)
reviews_bag_words = vectorizer_bag_words.transform(reviews)

print(vectorizer_bag_words.get_feature_names_out())

print(reviews_bag_words.todense())

```

```python
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer_tfidf = TfidfVectorizer(token_pattern='(?u)\\b\\w+\\b')
vectorizer_tfidf.fit(reviews)
reviews_tfidf = vectorizer_tfidf.transform(reviews)

print(vectorizer_tfidf.get_feature_names_out())

print(reviews_tfidf.todense())
```
