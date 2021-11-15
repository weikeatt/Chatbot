from itertools import repeat
import pandas as pd
from datetime import datetime
from random import seed
from random import randint

# Get current time
now = datetime.now()
current_time = now.strftime("%H:%M:%S")

# Convert excel to dataframe
data = pd.read_excel(r'C:\Users\Acer\PycharmProjects\AI_ChatBot\original_food_list.xlsx')
df = pd.DataFrame(data)


# Ask user for food selection and quantity
def choose_food():
    counter = 0
    check = True
    global food
    global quantity
    while check:
        food = str.lower(input("\nWhat would you like to have?\n>> "))
        for item in df["item_name"]:
            # Compare input food with excel item_name
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
            # Ensure quantity entered is valid
            print("You've ordered " + str(quantity) + " set(s) of " + food)
            check_two = False
            break
        else:
            print("Invalid input. Please try again")


# Calculate total
def calculate():
    global total
    total = 0
    food_list = []
    # Add food selected into a list based on the value of quantity
    food_list.extend(repeat(food, quantity))
    for all_food in food_list:
        # Get food price from price column in excel
        food_index = df[df["item_name"].str.lower() == all_food.lower()].index.values
        # Save all the food price in total variable
        total += df.loc[food_index, 'price'].values


# Dine in or delivery
def eat_where():
    check = True
    while check:
        location = int(input("\nChoose an option:-\n1 - Dine in\n2 - Delivery\n>> "))
        # Find food index in item_name excel
        food_index = df[df["item_name"].str.lower() == food.lower()].index.values
        if location == 1:
            check = False
        if location == 2:
            # Check whether food is available for delivery
            if df.loc[food_index, 'delivery_service'].values == 'yes':
                address = input("Enter your location\n>> ")
                print("Address set to " + address)
                check = False
                break
            else:
                print("Sorry, this item does not have delivery service")
        else:
            print("Invalid input. Please try again")


# Add remarks for food
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


# Payment method
def payment():
    while True:
        # Convert variable to string to print
        print("\nThe total is RM" + str(float(total)))
        pay = int(input("How would you like to pay?\n1 - Cash\n2 - Card\n>> "))
        if pay == 1:
            print("Cash payment is selected")
            # Display current_time (Extra information)
            seed(1)
            print("Payment accepted and here's your order number " + str(randint(0, 100)) + "\nTime ordered = " + current_time)
            break
        elif pay == 2:
            print("Card payment is selected")
            seed(1)
            print("Payment accepted and here's your order number " + str(randint(0, 100)) + "\nTime ordered = " + current_time)
            break
        else:
            print("Invalid input. Please try again")

# choose_food()
# calculate()
# eat_where()
# remarks()
# payment()
