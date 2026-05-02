import os
import subprocess

import psutil
from dotenv import load_dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import json
import telebot
from datetime import datetime

load_dotenv()

bot = telebot.TeleBot(os.getenv("TELE_API_KEY"))
TelegramUsers = [int(os.getenv("BASE_TELE_USER_ID"))]

#Get today's date in integer format
def today_date():
    # Creating a datetime object so we can test.
    a = datetime.now()
    # Converting a to string in the desired format (YYYYMMDD) using strftime
    # and then to int.
    a = str(a.strftime('%d/%m/%y'))
    return a

#Checks if User is Authorized or not
def UserCheck(message):
    if message.from_user.id in TelegramUsers:    
        return True
    else:
        bot.reply_to(message, "Unauthorized User")
        print(message.from_user.id)
        return False

def cpu_usage():
    try:
        CPULOARD= psutil.cpu_percent()
    except Exception as e:
        print(f"Error occurred: {e}")
        CPULOARD = "Error retrieving CPU usage."
    return CPULOARD

def measure_temp():
    try:
        temp = os.popen("vcgencmd measure_temp").readline()                    
        return (temp.replace("temp=","").replace("'C","").replace("\n",""))
    except Exception as e:
        print(f"Error occurred: {e}")
        return "Error retrieving temperature."

def get_ip_address():
    try:
        arg = 'hostname'  # Linux command to retrieve device's name
        # Runs 'arg' in a hidden terminal.
        p = subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE)
        data = p.communicate()  # Get data from 'p terminal'.
        # Parse out device name
        name_lines = data[0].splitlines()
        name_line = name_lines[0].split()
        name = name_line[0]
        device = '%s' % (name.decode())

        arg = 'hostname -I'  # Linux command to retrieve ip addresses
        # Runs 'arg' in a hidden terminal.
        p = subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE)
        data = p.communicate()  # Get data from 'p terminal'.
        # Parse out ip address of device
        ip_lines = data[0].splitlines()
        split_line = ip_lines[0].split()
        ipaddr = split_line[0]
        my_ip = '%s' % (ipaddr.decode())
    except Exception as e:
        print(f"Error occurred: {e}")
        my_ip = "Error retrieving IP address."
    return my_ip

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    if UserCheck(message) == True:
            bot.send_message(message.chat.id, "Welcome {}\nUser: {}  ".format(message.from_user.first_name,message.from_user.id))
            bot.reply_to(message, "/start & /help to start and get commands\n/add to add record")
    else:
        pass

# Get IP address of device and send to user
@bot.message_handler(commands=['ip'])
def get_ip(message):
    if UserCheck(message) == True:
        my_ip = get_ip_address()
        bot.send_message(message.chat.id, my_ip)
    else:
        pass

# Get temperature of device and send to user
@bot.message_handler(commands=['temp'])
def get_temp(message):
    if UserCheck(message) == True:
        my_temp = measure_temp()
        bot.send_message(message.chat.id, my_temp)
    else:
        pass

# Get CPU usage of device and send to user
@bot.message_handler(commands=['cpu'])
def get_cpu(message):
    if UserCheck(message) == True:
        my_cpu = cpu_usage()
        bot.send_message(message.chat.id, f"CPU Usage: {my_cpu}%")
    else:
        pass

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, "out of first loop")

print("I'm listening...")
bot.infinity_polling()