# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 12:06:09 2022

@author: maurop
"""

import copy

import src.TelegramObjects as tg_obj 

import src.CallbackQueryDataManager

import math

class PagesBase:
    ''' This class is a tool that should manage the page changes of a list
    when a message has a list that is too long to be represented'''
    
    def __init__(self, bot, title):
        self.current_page = 0
        self.title = title
        self.id = id(self)
        self.bot = bot        

    def add_elements(self, elements, elements_per_page):
        ''' this function creates the elements, in general lines and calculates
        the total number of pages in the system'''
        self.elements = elements
        self.elements_per_page = elements_per_page
        self.tot_pages = math.ceil(len(elements) / self.elements_per_page)
        self.current_page = 0  
        
    def get_page_elements(self, page_num):
        start_index = page_num * self.elements_per_page
        end_index = page_num * self.elements_per_page + self.elements_per_page
        page_elements = self.elements[start_index : end_index]        
        return page_elements
    
    def create_page_change_keyboard(self, keyboard, user_id):

        cb_data = src.CallbackQueryDataManager.CallbackQueryDataManager()
        
        cb_data.add_value("command", "page_change", "str")
        cb_data.add_value("pages_id", self.id, "int")
        cb_data.add_value("user_id", user_id, "int")
        
        cb_data_bw = copy.deepcopy(cb_data)
        cb_data_bw.add_value("direction", "back", "str")
        
        
        button_back = tg_obj.InlineKeyboardButton("<", callback_data=cb_data_bw.encode())
        
        cb_data_fw = copy.deepcopy(cb_data)
        cb_data_fw.add_value("direction", "forward", "str")
        button_forward = tg_obj.InlineKeyboardButton(">", callback_data=cb_data_fw.encode())


        last_row = len(keyboard.inline_keyboard)
        
        keyboard.add_button(last_row,button_back)
        keyboard.add_button(last_row, button_forward)    
        
        return keyboard
    
    def send_message(self, chat_id, user_id):
        print("sending page message...")
        message_text, keyboard = self.page_message(user_id)
        print("Pages: send_message:", message_text)
        if keyboard:
            resp = self.bot.sendMessageKeyboard(chat_id, message_text, keyboard)  
            print(resp)
        else:
            self.bot.sendMessage(chat_id, message_text)


    
    
    def update_page(self, chat_id, message_id, user_id):
        
        text, keyboard = self.page_message(user_id)
        if keyboard:
            self.bot.editMessageText(chat_id, message_id, text, keyboard)
        else:
            print("Pages: update_page: update without keyboard not implemented yet")
            
        
        
    
    def change_page(self, cb_query):
        print("changing page...")
        
        cb_manager = src.CallbackQueryDataManager.CallbackQueryDataManager()
        cb_manager.decode(cb_query.data)
        
        if cb_manager["user_id"] != cb_query.user.id:
            self.bot.answerCallbackQuery(cb_query.id, "You are not the user controlling these pages")
            return

        direction = cb_manager["direction"]
        user_id = cb_manager["user_id"]
        
        
        def answer_message(cb_query, user_id):
            message_text, keyboard = self.page_message(user_id)
            message_id = cb_query.message.message_id
            chat_id = cb_query.message.chat.id
            
            self.bot.editMessageText(chat_id, message_id, message_text, keyboard)
            self.bot.answerCallbackQuery(cb_query.id, f"page: {self.current_page + 1}")          
    
        if direction == "back":
            if self.current_page > 0:                
                self.current_page -= 1
                answer_message(cb_query, user_id)
                
            else:
                self.bot.answerCallbackQuery(cb_query.id, "already on first page")
        
        else:
            if self.current_page < self.tot_pages - 1:
                self.current_page += 1
                answer_message(cb_query, user_id)
            
            else:
                self.bot.answerCallbackQuery(cb_query.id, "already on last page")   
        
class PagesKeyboard(PagesBase):
    
    def __init__(self, bot, title):
        super().__init__(bot, title)
           
    
    def create_page(self, page_num):
        page_elements = self.get_page_elements(page_num)
        
        element_keyboard = tg_obj.InlineKeyboardMarkup()
        for i, button_row in enumerate(page_elements):
            for button in button_row:
                element_keyboard.add_button(i, button)
                
        return element_keyboard   
    
    def page_message(self, user_id):
        message_text = self.title + "\n"
        message_text += f"page: {self.current_page + 1}|{int(self.tot_pages) if self.tot_pages else 1}"
        
        keyboard = self.create_page(self.current_page)
        
        if self.tot_pages > 1:
            keyboard = self.create_page_change_keyboard(keyboard, user_id)
        
        return message_text, keyboard  
    
 
 
                    
        

class Pages(PagesBase):


    def __init__(self, bot, title, og_keyboard=None):
        super().__init__(bot, title)
        self.og_keyboard = og_keyboard
        
    def add_keyboard(self, keyboard):
        self.og_keyboard = keyboard
    
    def get_page(self, page_num):
        page_elements = self.get_page_elements(page_num)
        
        s = ""
        for element in page_elements:
            s += str(element) + "\n"
        
        return s
    
    def page_message(self, user_id):
        message_text = self.title + "\n"
        message_text += self.get_page(self.current_page)
        message_text += f"page: {self.current_page + 1}|{int(self.tot_pages) if self.tot_pages else 1}"

        keyboard = copy.deepcopy(self.og_keyboard) if self.og_keyboard else None
        
        if self.tot_pages > 1:
            
            if keyboard is None:
                keyboard = tg_obj.InlineKeyboardMarkup()
            
            keyboard = self.create_page_change_keyboard(keyboard, user_id)
        
        return message_text, keyboard