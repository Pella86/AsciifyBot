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
import hashlib

import src.Asciify

# my imports
import src.telegram.Updater
import src.telegram.Bot
import src.telegram.TelegramObjects as tg_obj
import src.telegram.BotCommands

# =============================================================================
# Bot
# =============================================================================


class AsciifyBot(src.telegram.Bot.Bot):
    
    default_size = (25, 17)
    help_message = "Send a picture so that the bot will convert it in ascii art.\n/size widthxheight (in pixels) to change the default size."
    
    def __init__(self):
        super().__init__()
        
        self.bot_commands = src.telegram.BotCommands.BotCommandList()
        
        self.bot_commands.add_command(self, 
                                      "/size", 
                                      lambda message: self.change_size(message), 
                                      "This will change the output size, depending on screen size and font size telegram in general displays about 25 characters, so if you want a image to be contained in a message try to restrict it to 25 width.\n<code>/size widthxheight</code> (in pixels)\nexample: <code>/size 25x17</code>")
        
        
        self.bot_commands.add_command(self,
                                      "/start",
                                      lambda chat_id: self.start_message(chat_id),
                                      "")
        
        self.sizes_db = src.telegram.Updater.Database("./databases/size_database.pkl")
        
        
        
    
    def start_message(self, chat_id):
        # message sent when the command start is given
        
        text = "<b>Welcome to the Asciify bot</b>\n"
        text += self.help_message
        
        self.sendMessage(chat_id, text)
        
        self.sendPhoto(chat_id, "./example_pictures/Example_picture.png")


    def change_size(self, message):
        print("User requested change_size")
        
        if message.text == "/size":
            size = self.get_size(message.user.id)
            self.sendMessage(message.chat.id, f"Current size is {size[0]}x{size[1]}")
        else:
            try:
                text = message.text
                
                parts = text.split(" ")
                
                sizes_str = parts[1]
                
                size_parts = sizes_str.split("x")
                
                width = int(size_parts[0])
                height = int(size_parts[1])        
                
                user_id = message.user.id
                sizes = (width, height)
                
                for i, id_size in enumerate(self.sizes_db.data):
                    db_user_id, _ = id_size
                    if user_id == db_user_id:
                        self.sizes_db.data[i] = (user_id, sizes)
                        self.sizes_db.save()
                else:
                    self.sizes_db.data.append( (user_id, sizes) )  
                    self.sizes_db.save()
                        
                self.sendMessage(message.chat.id, f"Size set to {sizes[0]}x{sizes[1]}")
            
            except IndexError:
                print("change_size: Index Error")
                self.sendMessage(message.chat.id, self.bot_commands["/size"].help_message)
            
            except ValueError:
                print("change_size: ValueError")
                self.sendMessage(message.chat.id, self.bot_commands["/size"].help_message)
        
    def get_size(self, input_user_id):
        for user_id, sizes in self.sizes_db.data:
            if input_user_id == user_id:
                return sizes
        else:
            self.sizes_db.data.append( (input_user_id, self.default_size) )  
            self.sizes_db.save()            
            return self.default_size
        
        

    def handle_updates(self, new_updates):
        ''' This function manages the updates received from Telegram'''
        
        for update in new_updates:
            
             # manages callback queries
            
            # if "callback_query" in update:
            #     print("handle_updates: Received callback query...")
            #     pass
            
            if "message" in update:
                message = tg_obj.Message(update["message"])
                
                if message.text and message.chat.type == "private":
                    if self.bot_commands["/size"] == message.text:
                        self.bot_commands["/size"].fire([message])
                    
                    elif self.bot_commands["/start"] == message.text:
                        print("User started bot")
                        self.bot_commands["/start"].fire([message.chat.id])
                    
                    else:
                        self.sendMessage(message.chat.id, self.help_message)
               
                elif message.photos:
                    print("User requested ascii art")
                    # pick the smallest photo
                    file_id = message.photos.get_lowsest_res().file_id
                    
                    # get the picture
                    image_filename = self.get_image_filename(file_id)
                    
                    # get user preferred size
                    size = self.get_size(message.user.id)
                    
                    # do the magic
                    asciify = src.Asciify.Asciify(image_filename, size)
                    ascii_text = asciify.asciify()
                    
                    # send the text message
                    text = "<code>" + ascii_text + "</code>"
                    
                    if len(text) <= 4096:
                        self.sendMessage(message.chat.id, text)
                    else:
                        self.sendMessage(message.chat.id, "Output text too long for a telegram message, try reducing the size")
                    
                    # send the document
                    ids = file_id + "_" + f"{size[0]}x{size[1]}" + "_" + str(message.user.id)
                    unique_name = hashlib.md5(ids.encode()).hexdigest()
                    
                    filename ="./text_files/text_" + unique_name + ".txt"
                    with open(filename, "w") as f:
                        f.write(ascii_text)
                    
                    self.sendDocument(message.chat.id, filename)
                
                else:
                    self.sendMessage(message.chat.id, 
                                    self.help_message)
                    
                    
                    
                    
                
            
        
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

    # updates cycle
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


