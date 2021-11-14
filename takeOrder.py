from itertools import repeat
import pandas as pd
from datetime import datetime
now = datetime.now()
current_time = now.strftime("%H:%M:%S")

data = pd.read_excel(r'C:\Users\Acer\PycharmProjects\AI_ChatBot\food_list.xlsx')
df = pd.DataFrame(data)


def choose_food():
    counter = 0
    check = True
    global food
    global quantity
    while check:
        food = str.lower(input("\nWhat would you like to have?\n>> "))
        for item in df["item_name"]:
            if food.lower() == item.lower():
                print(food.capitalize() + " is available")
                counter = 1
                check = False
        if counter == 0:
            print("Sorry, item not found. Please try again")

    check_two = True
    while True:
        quantity = int(input("\nHow many set(s) would you like?[Numerical input only]\n>> "))
        if quantity > 0:
            print("You've ordered " + str(quantity) + " set(s) of " + food)
            check_two = False
            break
        else:
            print("Invalid input. Please try again")

def calculate():
    global total
    total = 0
    food_list = []
    food_list.extend(repeat(food, quantity))
    for all_food in food_list:
        food_index = df[df["item_name"] == all_food.lower()].index.values
        total += df.loc[food_index, 'price'].values


def eat_where():
    check = True
    while check:
        location = int(input("\nChoose an option:-\n1 - Dine in\n2 - Delivery\n>> "))
        food_index = df[df["item_name"] == food.lower()].index.values
        if location == 1:
            check = False
        if location == 2:
            if df.loc[food_index, 'delivery_service'].values == 'yes':
                address = input("Enter your location\n>> ")
                print("Address set to " + address)
                check = False
                break
            else:
                print("Sorry, this item does not have delivery service")


def remarks():
    while True:
        remarks = int(input("\nDo you have any remarks?\n1 - Yes\n2 - No\n>> "))
        if remarks == 1:
            remarks_true = input("Please enter your remarks\n>> ")
            print(remarks_true + " is noted.")
            break
        elif remarks == 2:
            print("No remarks added")
            break
        else:
            print("Invalid input. Please try again")


def payment():
    while True:
        print("\nThe total is RM" + str(float(total)))
        pay = int(input("How would you like to pay?\n1 - Cash\n2 - Card\n>> "))
        if pay == 1:
            print("Cash payment is selected")
            print("Payment accepted and here's your order number - 1234\nTime ordered = " + current_time)
            break
        elif pay == 2:
            print("Card payment is selected")
            print("Payment accepted and here's your order number - 5678\nTime ordered = " + current_time)
            break
        else:
            print("Invalid input. Please try again")


# choose_food()
# calculate()
# eat_where()
# remarks()
# payment()

