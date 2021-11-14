import pickle
import numpy as np
import json
import time
import random
import pandas as pd


import takeOrder as to

import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

from keras.models import load_model
model = load_model('chatbot_model.h5')

intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                bag[i] = 1
                if show_details:
                    print("Found in bag: %s" % word)
    return np.array(bag)


def predict_class(sentence):
    p = bag_of_words(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result


def print_menu():
    data = pd.read_excel(r'C:\Users\Acer\PycharmProjects\AI_ChatBot\original_food_list.xlsx')
    while True:
        stalls = str.lower(input("Please choose a stall\n>>"))
        df = pd.DataFrame(data)
        if stalls == "malay":
            df.set_index("stall_name", inplace=True)
            df.head()
            print(df.loc["Malay"])
            break
        elif stalls == "mamak":
            df.set_index("stall_name", inplace=True)
            df.head()
            print(df.loc["Mamak"])
            break
        elif stalls == "beverage":
            df.set_index("stall_name", inplace=True)
            df.head()
            print(df.loc["Beverage"])
            break
        elif stalls == "japanese":
            df.set_index("stall_name", inplace=True)
            df.head()
            print(df.loc["Japanese"])
            break
        elif stalls == "korean":
            df.set_index("stall_name", inplace=True)
            df.head()
            print(df.loc["Korean"])
            break
        else:
            print("\nSorry, I don't understand. Please try again")


print("\nChatbot initialized\n")
username = input("What's your name?\n>>")
print("Good day " + username + "! Please choose the options below:-")

while True:
    print("\n1 - Menu and order\n2 - Connect to agent\n3 - Exit program")
    message = input(">> ")
    if message == '1':
        print("Menu")
        print("Stalls available:-")
        print("Malay | Mamak | Beverage | Japanese | Korean")
        print_menu()
        to.choose_food()
        to.calculate()
        to.eat_where()
        to.remarks()
        to.payment()
        time.sleep(3)
    elif message == '2':
        print("\nConnecting to agent...\nI am Alexa. How can I help?")
        while True:
            message = input(">> ")
            ints = predict_class(message)
            res = getResponse(ints, intents)
            print(res)
    elif message == '3':
        print("Thank you and have a nice day!")
        time.sleep(3)
        exit()
    else:
        print("Invalid input. Please try again")


