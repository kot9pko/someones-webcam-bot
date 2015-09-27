#!/bin/env python3
# encoding: utf-8
# -*- coding: utf-8 -*-

import telegram
import json
import os
import subprocess
import threading
import time

updates = []
bot = None
keyboard = telegram.ReplyKeyboardMarkup([[telegram.Emoji.CAMERA.decode("utf-8")]], resize_keyboard=True)

def main():
    global bot
    
    token = '101605430:AAEQSLUU5UBktr_XzSEDWE_jv4pmgzz1q20'
    bot = telegram.Bot(token=token)
    capt = threading.Thread(name='updater', target=longpollListen)	# Listen for updates in another thread
    capt.setDaemon(False)
    capt.start()

def parser(u):      # Handle messages one by one
    global bot 		# bot's object
    global keyboard # keyboard object for reply_markup

    text = u.message.text
    chat_id = u.message.chat.id
    user = u.message.from_user
    resp = 'отвянь'
    print('parser')

    if text[0] == '/':                        # Slash means command

        if text == '/help':                  
            resp = 'Сделать снимок /snap'

        elif text == '/start':                
            resp = '''Get started!'''

        elif '/make_a_coffe' in text:         # Easter egg. Shows info about hosting machine
#            resp = subprocess.check_output('screenfetch -Nn', shell=True)					# don't work on Raspberry Pi
            print('your coffe')

    elif '/snap' or telegram.Emoji.CAMERA or telegram.Emoji.CAMERA.decode("utf-8") in text: # Make an image
        snap(chat_id)
        return

    else:
        resp = 'unknown command'

    bot.sendMessage(chat_id=chat_id, text=resp, reply_markup=keyboard)

def snap(chat_id):		# Make an image and send it
	global keyboard
	subprocess.call(['fswebcam', './snapshot.jpg'])
	#time.sleep(5)
	with open('./snapshot.jpg', 'rb') as input_photo:
		bot.sendPhoto(chat_id, input_photo, reply_markup=keyboard)


def longpollListen():   # Updates
    global updates
    global bot
    global threads

    LAST_UPDATE_ID = 0

    print('Connecting...')    
    for i in range(10):
        print('Attempt #' + str(i+1))
        try:
            LAST_UPDATE_ID = bot.getUpdates()[-1].update_id  # Get lastest update
        except telegram.error.TelegramError or IndexError as err:
            print(err)
            continue
        break
    
        print(LAST_UPDATE_ID)

    while True:                             # Always listening
        try:
            fresh = bot.getUpdates(offset=LAST_UPDATE_ID)   # get fresh list od updates
        except tg.error.TelegramError as err:
            print('Error while updating messages: ' + str(err))
            continue        
        for u in fresh:                     # Handle each message
            chat_id = u.message.chat.id
            text = u.message.text
            user = u.message.from_user
    
            

            update_id = u.update_id

            if LAST_UPDATE_ID < update_id:  # If newer than the initial LAST_UPDATE_ID
                updates = fresh             # ...make it global
                print(user.first_name + ": " + text)   # for debug
                parser(u)                   # parse a command
        LAST_UPDATE_ID = update_id          # refresh update id
                    
if __name__ == "__main__":
    main()
