# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 15:32:34 2022

@author: maurop
"""
from src.telegram.Requests import tg_requests, tg_get_file

import src.telegram.TelegramObjects as tg_obj

import src.telegram.MemberCache


# =============================================================================
# Bot class
# ============================================================================= 

class Bot:
    '''Bot class: simple telegram requests manage'''
    
    telegram_api = tg_requests
    

    def __init__(self):
        '''Initialize the bot and use get me as a logging tool'''
        r = self.telegram_api.getMe()
        rjson = r.json()
  
        self.info = tg_obj.User(rjson["result"])
        print("Bot:", self.info)
        
        self.can_ban = src.telegram.MemberCache.CanBanMember()

    def sendMessage(self, chat_id, text, parse_mode="HTML"):
        '''Send a general text message '''
        params= {"chat_id":chat_id,
                 "text":text,
                 "parse_mode":parse_mode}
        
        print("sending message...")
                
        return self.telegram_api.sendMessage(params)  
        
    def sendMessageKeyboard(self, chat_id, text, keyboard):
        '''Send a text message with a reply keyboard markup'''
        params= {"chat_id":chat_id,
                 "text":text,
                 "parse_mode":"HTML",
                 "reply_markup":keyboard.to_json()}
        return self.telegram_api.sendMessage(params)
        
    def answerCallbackQuery(self, callback_id, text):
        '''Answer a callback query so that the stupid clock symbol goes away
        from the button'''
        self.telegram_api.answerCallbackQuery(callback_id, text=text)
        
    
    def editMessageText(self, chat_id, message_id, text, keyboard):
        '''Edit a message'''
        return self.telegram_api.editMessageText(text, chat_id=chat_id, message_id=message_id, reply_markup=keyboard.to_json())

    def answerInlineQuery(self, query_id, query_list):
        return self.telegram_api.answerInlineQuery(query_id, query_list)
        
        
    def user_can_ban(self, group_id, user):
        return self.can_ban[(group_id, user.id)]
    
    def kick(self, group_id, admin_user, banned_user):
        print("Bot: kick user function...")

        can_ban = self.user_can_ban(group_id, admin_user)
                    
        if can_ban:
            print("kicking....")
            resp = self.telegram_api.banChatMemeber(group_id, banned_user.id)
            
            
            if resp and resp.status_code == 200:
                resp = self.telegram_api.unbanChatMember(group_id, banned_user.id)
                
                print("unban resp")
                print(resp)
                print(resp.json())
                
                print(banned_user, "successfully kicked")
                return True
            
            else:

                print("ERROR: kick function")
                if resp:
                    print(resp.json())
                
                return False
        else:          
            print(admin_user, "doesnt have the permission to ban")
            return False
        
    # def get_file(self, file_id):
    #     tg_get_file.get_file(file_id)
        
    def get_image_filename(self, file_id):
        return tg_get_file.get_image_filename(file_id)
        

    def kick_user_reply(self, admin_user, group_id, banned_user):
        print("kick user function...")
        
        can_ban = self.user_can_ban(group_id, admin_user)

        if can_ban:
            print("kicking....")
            resp = self.telegram_api.banChatMemeber(group_id, banned_user.id)

            if resp and resp.status_code == 200:
                self.telegram_api.unbanChatMember(group_id, banned_user.id)
            
                self.sendMessage(group_id, f"user {banned_user} kicked by {admin_user}") 
            else:
                self.sendMessage(group_id, f"Something went wrong in banning {banned_user}")
                print("ERROR: kick function")
                if resp:
                    print(resp.json())
        else:          
            self.sendMessage(group_id, "you dont have the permissions to ban")