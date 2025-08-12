import json
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Embedding, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load the intents file
with open('intents.json') as file:
    data = json.load(file)

# Prepare training data
training_sentences = []
training_labels = []
responses = {}

for intent in data['intents']:
    for pattern in intent['patterns']:
        training_sentences.append(pattern)
        training_labels.append(intent['tag'])
    responses[intent['tag']] = intent['responses']

# Encode labels using LabelEncoder
lbl_encoder = LabelEncoder()
lbl_encoder.fit(training_labels)
training_labels_encoded = lbl_encoder.transform(training_labels)
num_classes = len(lbl_encoder.classes_)

print(f"Classes found: {lbl_encoder.classes_}")
print(f"Number of classes: {num_classes}")

# Convert encoded labels to categorical (one-hot)
training_labels_categorical = tf.keras.utils.to_categorical(training_labels_encoded, num_classes=num_classes)

# Tokenize sentences
vocab_size = 1000
embedding_dim = 16
max_len = 20
oov_token = "<OOV>"

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token)
tokenizer.fit_on_texts(training_sentences)
sequences = tokenizer.texts_to_sequences(training_sentences)
padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)

# Build the model
model = Sequential()
model.add(Embedding(vocab_size, embedding_dim, input_length=max_len))
model.add(GlobalAveragePooling1D())
model.add(Dense(24, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

print("Training model...")
model.fit(padded_sequences, training_labels_categorical, epochs=200, verbose=1)

# Save the model and tokenizer and label encoder
model.save('chatbot_model/chatbot_model.h5')

import pickle

with open('chatbot_model/tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('chatbot_model/label_encoder.pickle', 'wb') as ecn_file:
    pickle.dump(lbl_encoder, ecn_file, protocol=pickle.HIGHEST_PROTOCOL)

print("Training complete ✅")
