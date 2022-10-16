# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 09:57:19 2022

@author: maurop
"""

# =============================================================================
# Imports
# =============================================================================

import json
import time
import traceback

import src.Asciify

# my imports
import src.telegram.Updater
import src.telegram.Bot
import src.telegram.TelegramObjects as tg_obj

# =============================================================================
# Bot
# =============================================================================


class AsciifyBot(src.telegram.Bot.Bot):
    
    def __init__(self):
        super().__init__()

# =============================================================================
# update handler
# =============================================================================

    def handle_updates(self, new_updates):
        ''' This function manages the updates received from Telegram'''
        
        for update in new_updates:
            
             # manages callback queries
             
            print(update)
            
            if "callback_query" in update:
                print("handle_updates: Received callback query...")
                pass
            
            if "message" in update:
                message = tg_obj.Message(update["message"])
               
                if message.photos:
                    file_id = message.photos[0].file_id
                    print(file_id)
                    image_filename = self.get_image_filename(file_id)
                    
                    
                    asciify = src.Asciify.Asciify(image_filename, (25,17))
                  
                    
                    text = "<code>" + asciify.asciify() + "</code>"
                    
                    print(text)
                    bot.sendMessage(message.chat.id, text)
                    
                    
                    
                    
                
            
        
        # # messages
        # if "message" in update and "text" in update["message"]:
        #     pass
        
        
        
        
               
           

# =============================================================================
# main
# =============================================================================
        
if __name__ == "__main__":
    
    # main updater
    
    updater = src.telegram.Updater.Update()
    
    # bot
    bot = AsciifyBot()

    

    while True:
        time.sleep(0.1)
        
        new_updates = updater.getUpdates()

        try:
            bot.handle_updates(new_updates)
      
        except KeyError as e:
            print("key:", e)
            print(traceback.format_exc())
            
            print("message parsing error")
            print(json.dumps(new_updates, indent=4))


