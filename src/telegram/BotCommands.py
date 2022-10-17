# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 15:32:03 2022

@author: maurop
"""

# =============================================================================
# Bot commands
# =============================================================================

class BotCommand:
    
    def __init__(self, bot, command, function=None, help_message=""):
        self.bot = bot
        self.command = command
        self.function = function
        self.help_message = help_message
        
    def transform_message_text(self, text):
        if text == self.command:
            return self.command
        
        if text == self.command + "@" + self.bot.info.username:
            return self.command
        
    
    def fire(self, params):
        self.function(*params)
    
        
    def __eq__(self, text):
        
        text = text.lower()
        
        if text.startswith(self.command):
            return True
        
        if text.startswith(self.command + "@" + self.bot.info.username.lower()):
            return True
        
        return False

class BotCommandList:
    
    def __init__(self):
        self.commands = {}
    
    def __getitem__(self, key):
        return self.commands[key]
        
    def add_command(self, bot, command, function, help_message):
        self.commands[command] = BotCommand(bot, command, function, help_message)
        
    