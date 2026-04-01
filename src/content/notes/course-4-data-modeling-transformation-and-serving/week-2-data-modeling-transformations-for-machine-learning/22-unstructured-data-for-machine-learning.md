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

## Modeling and Processing Unstructured Data for Machine Learning

### Modeling Image Data for ML Algorithms

- Traditional ML Algorithms:
- Expect data to be in tabular form
- Problem with treating images as tabular data:
  - Loss of spatial information that can be extracted from the relative location of pixels
  - Flattenning 1000 pixels by 1000 pixels - vector of size 1 million - very intensive on compute and memory and can affect the performance of the ML algorithm
- Alternative Approach
- Convolutional Neural Network
  - Each layer tries to identify more image features to help with the ML task
    - First layers: generic features
    - Deeper layers: complex patterns and features
  - In practice, ML teams start with pre-trained CNN models and fine tune them on specific task and data
- Preparing images for Deep Learning models:
- Augmentations:
  - Resizing
  - Scaling features
  - Flipping, Rotating, Cropping
  - Adjusting Brightness

Example Code for Augmenting Images with Tensorflow

```python
import tensorflow as tf
import matplotlib.pyplot as plt
import tensorflow_datasets as tfds

# load the dataset
dataset = tfds.load('cats_vs_dogs', split='train', as_supervised=True)

def resize_normalize(image, label, image_size=150):
  # resize the image
  image = tf.image.resize(image, [image_size, image_size])
  # normalize the image
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

### Preprocessing Text for Analysis and Text Classification

- Some examples of NLP Tasks:
- sentiment analysis of product reviews
- classification of news articles
- chatbots and virtual assistants
- span detection
- customer segmentation
- product recommendations
- Why we still need to preprocess textual data
- Might contain typos, inconsistencies and repetitions
- Not all words or characters are relevant to the NLP task
- Training LLMs is expensive and time consuming
- We might want to combine text features with other types of features such as categorical, numeric.

Preprocessing Text Workflow

1. Cleaning
1. Removing punctuation, extra spaces, characters that add no meaning
2. Normalization
1. Converting text to consistent format: transforming to lower case, converting numbers or symbols to characters, expanding contractions
3. Tokenization
1. Split each review into individual tokens (words, subwords or short sentences)
2. The easiest tokenization method converts each word into a token
4. Removal of Stop Words
1. "is", "are", "the", "for", "a"
2. some libraries that do this: spaCy, NLTK, Gensim, TextBlob
5. Lemmatization
1. Replacing each word with its base form or lemma (e.g. getting/got to get)

```python
import pandas as pd
import re
import unicodedata
import spacy
import numpy as np

# A dictionary expanding common contractions
# See: github.com/dipanjanS/practical-machine-learning-with-python
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

### Text Vectorization and Embedding

The next stage after pre-preocessing hte text data is converting words, sub-words, characters, or even sentences into tokens (depending on the scale).

**Traditional Vectorization**

- Bag of Words
- TF-IDF (Term Frequency Inverse Document Frequency)

These methods assign a number to a word based on the frequency of its occurrence in a document/corpus

- Several or many documents in a corpus
- A document can be a customer review, and the corpus the collection of all reviews
- The vocabulary consists of all unique pre-processed words

**Bag of Words**

- Binary vectors, the length of the number of documents in the corpus
- 1 in the index corresponding to the document if the word exists in it
- Problem with this method: more weight is given based on frequency, however high frequency words might have little meaning, whereas low frequency words can be more significant to the task.
![](/data-engineering-specialization-website/images/6b312fd4-79e8-4792-900a-5b09e27ead0b.png)

**TF-IDF**

- Account for the weight and rarity of each word
- TF: the number of times the term occurred in a document divided by the length of that document
- IDF: how common or rare that word is in the entire corpus
- Easily computed with scikit-learn
![](/data-engineering-specialization-website/images/3944827b-0dd0-4b55-8107-353869e2587d.png)

These tokenization methods are useful for smaller datasets and when "key" words have significance to the task (e.g. sentiment analysis)

Problems:

- High dimensional vector with very sparse values
- No meaning to nearby words

**Word Embeddings**

- Vector that captures the semantic meaning of the word
- word2vec, GLOVE
- Trained to learn the embeddings of wrods from their occurrences
- Word embeddings do not take into account the position of words in a sentence
- To solve this - use sentence embeddings
- Takes into account the semantic meaning of the sentence
- Lower dimension than the vector generated by TF-IDF
- Pre-Trained NLP models:
  - Open Source:
    - SentenceTransformers (sbert.net)
  - Closed Source:
    - OpenAI, Anthropic, Google

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# load a pre-trained sentence transformer model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
	"this is a wonderful price for the amount you get",
	"great product big amount",
	"I bought this for my son",
	]

# encode sentences
embeddings = embedder.encode(sentences)

print(embeddings.shape) # (3, 384)

sim = cosine_similarity(embeddings, embeddings)[0, 1:] # similarity to first sentence

print(sim) # array([0.5106675, 0.13981295])

```

What we can do with these embeddings:

- Features to train an ML algorithm
- Clustering, or similarity search

Example: Vectorizing Text with Scikit-Learn

```python
from sklearn.feature_extraction.text import CountVectorizer

reviews = ["this wonderful price amount you get",
         "great product big amount",
         "I buy this my son his hair thin"]

# bag of words
vectorizer_bag_words = CountVectorizer(token_pattern='(?u)\\b\\w+\\b')

# fit-transform
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
