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

Unstructured data - images, text, audio - requires specialized preprocessing before it can be fed into ML models.

---

**Why Not Tabular?**

Traditional ML algorithms expect tabular input, but treating images as flat tabular data loses spatial information and creates extremely large feature vectors (a 1000x1000 image becomes a vector of 1 million values). This is computationally expensive and degrades model performance.

---

**Convolutional Neural Networks (CNNs)**

The preferred approach is a **CNN** where each layer identifies progressively more complex features - early layers detect edges and textures, deeper layers capture complex structures. In practice, ML teams start with **pre-trained CNN models** and fine-tune them on their specific task and data.

---

**Image Augmentation**

Preparing images for deep learning typically involves augmentations to increase training data diversity:

| Augmentation            | Purpose                                             |
| ----------------------- | --------------------------------------------------- |
| Resizing                | Standardize dimensions for batch processing         |
| Scaling (normalization) | Scale pixel values to [0, 1] for faster convergence |
| Flipping / Rotating     | Teach invariance to orientation                     |
| Cropping                | Focus on relevant regions                           |
| Brightness / Contrast   | Teach robustness to lighting conditions             |

```python
import tensorflow as tf
import tensorflow_datasets as tfds

# Load dataset
dataset = tfds.load("cats_vs_dogs", split="train", as_supervised=True)

def resize_normalize(image, label, image_size=150):
    """Resize to fixed dimensions and normalize pixel values to [0, 1]."""
    image = tf.image.resize(image, [image_size, image_size])
    image = image / 255.0
    return image, label

def augment(image, label):
    """Apply random augmentations for training data diversity."""
    image = tf.image.random_flip_left_right(image)
    image = tf.image.rot90(image)
    image = tf.image.random_contrast(image, lower=0.2, upper=0.8)
    image = tf.image.random_brightness(image, max_delta=0.5)
    return image, label

# Apply preprocessing pipeline
image, label = next(iter(dataset))
image, label = resize_normalize(image, label)
image, label = augment(image, label)
```

## 2.2.2 Text Preprocessing and Classification

NLP tasks span sentiment analysis, article classification, chatbots, spam detection, customer segmentation, and product recommendations. Despite advances in language models, text preprocessing remains important: raw text contains typos and irrelevant characters, training LLMs is expensive, and text features often need to be combined with categorical or numeric features.

---

**Preprocessing Pipeline**

| Step                     | Action                                               | Example                                      |
| ------------------------ | ---------------------------------------------------- | -------------------------------------------- |
| **1. Cleaning**          | Remove punctuation, extra spaces, special characters | `"Hello!! World"` → `"Hello World"`          |
| **2. Normalization**     | Lowercase, expand contractions, convert symbols      | `"I can't"` → `"i cannot"`                   |
| **3. Tokenization**      | Split into individual tokens (words, subwords)       | `"i cannot go"` → `["i", "cannot", "go"]`    |
| **4. Stop word removal** | Filter common words with little meaning              | `["i", "cannot", "go"]` → `["cannot", "go"]` |
| **5. Lemmatization**     | Replace words with their base form (lemma)           | `"getting"` → `"get"`, `"got"` → `"get"`     |

```python
import re
import unicodedata
import spacy

# Common contractions dictionary
CONTRACTION_MAP = {
    "can't": "cannot", "don't": "do not", "it's": "it is",
    "won't": "will not", "they're": "they are",
    # ... (full map omitted for brevity)
}

def preprocess_text(text, nlp, special_chars=None, lemmatize=False):
    """Full text preprocessing pipeline."""
    if special_chars is None:
        special_chars = ["~", "@", "#", "$", "%", "^", "&", "*"]

    # Remove special characters
    pattern = "[" + "|".join(re.escape(c) for c in special_chars) + "]"
    text = re.sub(pattern, "", text)

    # Normalize: lowercase, strip whitespace, remove accents
    text = text.lower().strip()
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf8")

    # Expand contractions
    text = " ".join(
        CONTRACTION_MAP.get(word, word) for word in text.split()
    )

    # Tokenize, remove punctuation, optionally lemmatize
    doc = nlp(text)
    if lemmatize:
        tokens = [token.lemma_ for token in doc if not token.is_punct]
    else:
        tokens = [token.text for token in doc if not token.is_punct]

    return " ".join(tokens)
```

## 2.2.3 Text Vectorization and Embeddings

After preprocessing, text must be converted into numerical representations for ML algorithms.

---

**Traditional Vectorization**

| Method           | How it Works                                                                     | Limitations                                                                |
| ---------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **Bag of Words** | Binary vector - `1` if word appears in document, `0` otherwise                   | High-frequency words dominate; rare but meaningful words are underweighted |
| **TF-IDF**       | TF (term frequency in document) × IDF (inverse document frequency across corpus) | High-dimensional sparse vectors, ignores word proximity and context        |

Both work well for smaller datasets where key words are significant to the task (e.g., sentiment analysis).

```python
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

reviews = [
    "this wonderful price amount you get",
    "great product big amount",
    "I buy this my son his hair thin"
]

# Bag of Words
bow_vectorizer = CountVectorizer(token_pattern=r"(?u)\b\w+\b")
bow_vectorizer.fit(reviews)
bow_vectors = bow_vectorizer.transform(reviews)
print(bow_vectorizer.get_feature_names_out())
print(bow_vectors.todense())

# TF-IDF
tfidf_vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
tfidf_vectorizer.fit(reviews)
tfidf_vectors = tfidf_vectorizer.transform(reviews)
print(tfidf_vectors.todense())
```

---

**Word and Sentence Embeddings**

A **word embedding** is a dense vector that captures semantic meaning, learned from word co-occurrences (e.g., `word2vec`, `GloVe`). However, word embeddings ignore position within a sentence.

**Sentence embeddings** capture the semantic meaning of entire sentences in lower-dimensional vectors. Pre-trained models:

| Source            | Models                             |
| ----------------- | ---------------------------------- |
| **Open source**   | SentenceTransformers (`sbert.net`) |
| **Closed source** | OpenAI, Anthropic, Google          |

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load pre-trained model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "this is a wonderful price for the amount you get",
    "great product big amount",
    "I bought this for my son",
]

# Encode sentences into 384-dimensional vectors
embeddings = embedder.encode(sentences)
print(embeddings.shape)  # (3, 384)

# Compute cosine similarity to first sentence
sim = cosine_similarity(embeddings, embeddings)[0, 1:]
print(sim)  # [0.51, 0.14] - first pair is more similar
```

Embeddings can be used as features for downstream ML algorithms, or directly for clustering and similarity search.
