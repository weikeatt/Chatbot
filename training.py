import numpy as np
import random
import json
import pickle

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD

import nltk
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

intents_file = open('intents.json').read()
intents = json.loads(intents_file)

# Preprocess data
words = []
classes = []
documents = []
ignore_letters = ['!', '?', ',', '.', 's', '<', '>', '%']
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Tokenize each words
        word = nltk.word_tokenize(pattern)
        words.extend(word)
        # Add documents in the corpus
        documents.append((word, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# print(documents)

# lemmatize, lowercase each word and remove duplicates
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_letters]
# Sort words and classes
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# Create training data using neural network
training = []
output_empty = [0] * len(classes)
for doc in documents:
    bag = []
    # List of tokenized words for the pattern
    word_patterns = doc[0]
    # Create a base word to represent a related word
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

# Shuffle the features and turn into numpy array
random.shuffle(training)
training = np.array(training)

# Create training data
train_x = list(training[:, 0])
train_y = list(training[:, 1])
print("Training data created")


# 3 layers of neural network
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Use Stochastic Gradient Descent with Nesterov accelerated gradient
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Fitting and saving the learning model
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('chatbot_model.h5', hist)
print("Model created")
