# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 08:48:42 2022

@author: maurop
"""


import pathlib
import pickle
import json

import src.telegram.Requests

# =============================================================================
# Database
# =============================================================================


class Database:
    
    ''' Class to store stuff in files'''
    
    
    def __init__(self, filename):
        # filename
        self.filename = filename

        # data
        self.data = []
        self.initialize()
    
    
    def initialize(self):
        if pathlib.Path(self.filename).exists():
            with open(self.filename, "rb") as f:
                self.data = pickle.load(f)
            name = pathlib.Path(self.filename).name
            print(f"Database {name} initialized, retrived {len(self.data)} elements")
    
    def save(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self.data, f)
            
    
    def __getitem__(self, i):
        return self.data[i]
        

# =============================================================================
# Updater
# =============================================================================

class Update:
    
    update_filename = "./databases/update_database.pkl"
    # update_log_filename = "./logs/message_log.txt"
    
    def __init__(self):
        
        # a database with the numbers
        self.database = Database(self.update_filename)
        
        # current index
        self.index = 0
        
        # if not pathlib.Path(self.update_log_filename).exists():
        #     with open(self.update_log_filename, "w") as f:
        #         f.write("header\n")
                
    
    
    def getUpdates(self):
        
        response_length = 100
        
        # crawl through the requests
        while response_length == 100:
            
            # request the updates from the api
            params = {"offset": self.index}
            r = src.telegram.Requests.tg_requests.getUpdates(params)   
            rjson = r.json()     
            
            
            # set the offset
            if len(rjson["result"]) > 0:
                self.index = rjson["result"][0]["update_id"] 
            
            # if the response is 100, it means that there might be more 
            # pending responses
            response_length = len(rjson["result"]) 
            
            if response_length == 100:
                self.index += 100
                
        
        # store the messages
        
        new_messages = []
        
        
        
        for message in rjson["result"]:
            
            update_id = message["update_id"]
    
            if update_id not in self.database.data:
                self.index += 1 
                
                new_messages.append(message)
                
                # add the ids to the file
                self.database.data.append(update_id)
                self.database.save()
                
                # # log the messages for further use 
                # with open(self.update_log_filename, "a") as f:
                #     f.write(json.dumps(message) + "\n")
        
        return new_messages