import pymysql
import requests
import webbrowser
from PIL import Image 
from io import BytesIO
import os
import getpass
from random import randint
#from kivy.app import App

# If we want this to be multi-player we will have to use the socket module and perhaps a simple login/username system
# First We'll need the logic
# https://cataas.com/#/ has random cat pics
# The pics will have their location put into a sql database along with the rating (1-10)
# 10 buttons on the bottom for score
# 1 button below for Show favorite cats random fave (maybe an algorithm that goes from the top score down to the bottom)
# 1 button next to it for new cat


passw = getpass.getpass("Enter your sql password: ")

# This if the number prefix for the amount of images you can save
image_number = []
for i in range(200):
    i += 1
    image_number.append(i)

# Get sql pass and connect to db
def check_if_database_exists():
    #passw = getpass.getpass("Enter your sql password: ")
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password=passw
    )
    mycursor = connection.cursor()
    mycursor.execute("SHOW DATABASES")
    
    for x in mycursor.fetchall():
        if x[0] == "cats":
            # instead of break here we'll just open the database and make the cursor
            break
    else: 
        print("You do not have a cat database yet\n")
        print("Creating database")
        create_database(mycursor)

# Creates the database
def insert_pics_to_database(rating, location): 
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password=passw,
        database='cats'
    )
    mycursor = connection.cursor()
    mycursor.execute("INSERT INTO ratings (rating,location) VALUES(%s,%s)", (str(rating), location))
    print(str(mycursor.rowcount) + ": Cat records updated!")
    connection.commit()
    
# Function to setup your database
def create_database(mycursor):
    mycursor.execute("CREATE DATABASE IF NOT EXISTS cats")
    mycursor.execute("USE cats")
    mycursor.execute("CREATE TABLE IF NOT EXISTS ratings (rating VARCHAR(255), location VARCHAR(255), id INT AUTO_INCREMENT PRIMARY KEY)")
    print("cats database and ratings table created!")
# Checks if you have a cats database or not

check_if_database_exists()

def generate_cat_image_file(resp_cont, rating):
    # Open database here
    # Function for saving cat pictures to ./cats
    for x in range(len(image_number)):
        # This checks to make sure it's not overwritting cat pictures
        if not os.path.exists(r".\\cats\\" + "cat_" + str(image_number[x]) + ".jpg"):
            # Save image
            with open(r".//cats//cat_" + str(image_number[x]) + ".jpg", "wb") as f:
                f.write(resp_cont) 
                location = r".//cats//cat_" + str(image_number[x]) + ".jpg"
                insert_pics_to_database(rating, location)
                break

          #"""
            #Create a function for this one 
            #mycursor.execute("INSERT INTO CUSTOMERS (rating,location) VALUES(%s,%s)", (str(rating), location))
            #print(mycursor.rowcount + ": Cat records updated!")
            #break
          #"""

    # Let's you know if your number is out of range
    else:
        print("You can't exceed 200 cat pics!")

# This function shows all cats rated 8, 9, and 10
def show_favorite_cats():
    # Change this later to do something more specific the user wants to do
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password=passw,
        database='cats'
    )
    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM ratings WHERE rating IN ('8', '9', '10') LIMIT 10")
    result = mycursor.fetchall()
    cat = randint(0, len(result)) - 1
    print(result)
    cat_image_location = result[cat][1]
    cat_image = cat_image_location
    with open(cat_image, "rb") as file: 
        cat_image_bytes = file.read()
    return BytesIO(cat_image_bytes)

def clear_database_table_and_images():
    # Clears table and files in cats directory
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password=passw,
        database='cats'
    )
    mycursor = connection.cursor()
    mycursor.execute("DROP DATABASE IF EXISTS cats")
    folder_path = r".\cats"

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)    

# API request
def call_api():
    response = requests.get("https://cataas.com/cat")
    check_if_database_exists()

    if response.status_code == 200:
        
        # Let's not save the image first, let's pull up the image and ask the user to rank it
        print("Connection successful")
        image = response.content
        # print("Here is an image of the first cat rate it from 1-10")
        
        # Displays image on screen with PIL
        #cat_pic = Image.open(BytesIO(image))
        #cat_pic.show()

        # Takes your rating of the cat and stores it as a varaible
        #rating = input()

    # Checks the rating you've provided
    #if int(rating) == 8 or int(rating) == 9 or int(rating) == 10:
        # Should probably take this out and just send your rating and cat image to be stored
        #choice = input("Would you like to save this cat image? ")
        #if choice in ("y", "yes", 'yeah', 'sure'):
        #generate_cat_image_file(response.content, rating)

    #else:
    #    print("No worries, next image incoming!\n")    

        return BytesIO(image), response.content 
        
    else:
        print("Connection Failed")


