# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 08:44:46 2022

@author: maurop
"""

import datetime
import requests
import time
import pathlib
import os
import pickle

import src.telegram.TelegramObjects as tg_obj


class TelegramRequestError(Exception):
    pass

# =============================================================================
# Requests
# =============================================================================

class Requests:
    ''' The class Requests ensures that the limit of 30 requests per second is
    not surpassed. '''
    
    messages_second = 30
    
    def __init__(self):
        # stores the time when a request was done
        self.requests_stack = []
 
    
    def clean_stack(self):
        # remove the requests times that are past 1 second ago
        delete_indexes = []
        for i, date in enumerate(self.requests_stack):
            if datetime.datetime.now() - date > datetime.timedelta(seconds=1):
                delete_indexes.append(i)

        delete_indexes.reverse()

        for i in delete_indexes:
            del self.requests_stack[i]        
    
    
    def request(self, reqfunc, url, params, files=None):

        self.clean_stack()
        
        self.requests_stack.append(datetime.datetime.now())
        
        while len(self.requests_stack) > self.messages_second:
            print("Requests: limit reached")
            print("waiting...")
            time.sleep(1)
        
        if files:
            response = reqfunc(url, params, files=files)
        else:
            response = reqfunc(url, params)
        
        if response is None:
            print(params)
            print(url)
            print("This should be None", response)
            
            raise TelegramRequestError("response is none")
            
        
        if response.status_code != 200:
            print("Error: response")
            print(params)
            print(url)
            print(response.json())
            
            raise TelegramRequestError("status code not 200")
            
        return response            

    
    def get(self, url, params = {}): 
        response = self.request(requests.get, url, params)
        return response
        
    
    def post(self, url, params={}, files=None):
        response = self.request(requests.post, url, params, files)
        return response


# =============================================================================
# Telegram Requests
# =============================================================================

class BaseTelegramRequests:
    
    ''' Base class for the requests, manages the token'''
    
    request = Requests()
    
    def __init__(self):
        self.token = self.read_token()
        
        self.api_url = "https://api.telegram.org/bot" + self.token + "/"   

        
    def read_token(self):
        with open("./bot_token/bot_token.txt") as f:
            lines = f.readlines()
            
        
        for line in lines:
            
            if line:
                parts = line.split("=")
                
                token = parts[1].strip()
    
        return token
    
# =============================================================================
# Get/Send File
# =============================================================================

class PhotoCache:
    
    ''' This class manages a file cache '''
    
    def __init__(self, photo_folder, database_path):
        self.database_path = pathlib.Path(database_path)
        
        # folder where the files will be stored
        self.photo_folder = pathlib.Path(photo_folder)
        
        # id filename 
        self.database = {}
        
        # create the folder
        if not self.photo_folder.is_dir():
            print("creating photo folder...")
            os.mkdir(self.photo_folder)        

        # load the database file if present
        if self.database_path.is_file():
            print("loading photo database from file...")
            with open(self.database_path, "rb") as f:
                self.database = pickle.load(f)
                
    def __getitem__(self, file_id):
        return self.database[file_id]
    
    def __setitem__(self, file_id, filename):
        self.database[file_id] = filename
        
    def save(self):
        with open(self.database_path, "wb") as f:
            pickle.dump(self.database, f)
        
class GetFile(BaseTelegramRequests):
    
    ''' GetFile Request: contains a cache saved in ./pictures
    the cache is based on the unique id of the picture'''
    
    def __init__(self):
        super().__init__()
        
        self.api_file_url = "https://api.telegram.org/file/bot" + self.token + "/"          
        
        self.id_filename_db = PhotoCache("./download_pictures", "./download_pictures/database.pkl")
        
        
    def get_image_filename(self, file_id):
        ''' this function will return the filename in the cache if present
        if not will create a new picture'''
        
        try:
            return self.id_filename_db[file_id]
        except KeyError:
            return self.get_file(file_id)

    def get_file(self, file_id):
        ''' this function will request a file from telegram and download it
        '''
        
        # first request to see if the file exist
        api_url = self.api_url + "getFile"
        params = {"file_id" : file_id}
        
        resp = self.request.get(api_url, params)
        
        # the response should return a File object which contains
        # information on the file
        file = tg_obj.File(resp.json()["result"])
        
        if file.file_path:
            # construct the file request
            
            url = self.api_file_url + file.file_path
            resp_file = self.request.get(url)
            
            # constructs the filename from the file path
            # store files and ids in a folder
            given_filename = pathlib.Path(pathlib.Path(file.file_path).name)
            filename = self.id_filename_db.photo_folder / given_filename

            if file.file_size == len(resp_file.content):
                
                # store in the database the file
                self.id_filename_db[file.file_id] = filename
                
                # updates the database
                self.id_filename_db.save()
                
                # writes the file to the pc
                with open(filename, "wb") as f:
                    f.write(resp_file.content)
                
                # returns the local location of the file
                return self.id_filename_db[file_id]
            else:
                raise TelegramRequestError("GetFile: get_file: File size different than the one stated by telegram")

        else:
            raise TelegramRequestError("GetFile: get_file: no file path given")


class SendFile(BaseTelegramRequests):
    
    '''This class manages sending a file from disk, if the file was already sent
    uses the telgram returned file_id'''
    
    def __init__(self):
        super().__init__()
        
        self.uploaded_files_db = PhotoCache("./databases", "./databases/uploaded_files.pkl")
    
    
    def sendFile(self, url, params, filename, doc_type):
        # try to see if filename > file_id exist which means the picture was
        # already sent
        try:
            file_id = self.uploaded_files_db[filename]
            
            params[doc_type] = file_id
            
            self.request.post(url, params)
        
        # if the file was never sent then it means there is no id
        # so it will be loaded from disk
        except KeyError:
            with open(filename, "rb") as f:
                
                files = {}
                files[doc_type] = f
                
                resp = self.request.post(url, params, files=files)
                
                # the sendDocument or sendPhoto method respond with a message
                # containint the file ids
                message = tg_obj.Message(resp.json()["result"])
                
                # get the file_id from the telegram response
                if doc_type == "photo":
                    # there might be a problem since photos are always in multiples
                    photo = message.photos.get_highest_res()
                    file_id = photo.file_id   
                
                elif doc_type == "document":
                    document = message.document
                    file_id = document.file_id
                
                else:
                    raise Exception("Send File: file type not supported")
                
                self.uploaded_files_db[filename] = file_id
                self.uploaded_files_db.save()                
        
        
    
    def sendDocument(self, chat_id, filename, caption = "", parse_mode = "HTML"):
        url = self.api_url + "sendDocument"
        
        params ={"chat_id" : chat_id,
                 "caption" : caption,
                 "parse_mode" : parse_mode
                 }
        
        
        self.sendFile(url, params, filename, "document")
        
    
    def sendPhoto(self, chat_id, filename, caption = "", parse_mode = "HTML"):
        url = self.api_url + "sendPhoto"
        
        params ={"chat_id" : chat_id,
                 "caption" : caption,
                 "parse_mode" : parse_mode
                 }
        
        
        self.sendFile(url, params, filename, "photo")        
        
            
            
# =============================================================================
# Telegram requests
# =============================================================================

class TelegramRequests(BaseTelegramRequests):
    ''' Main class that manages the queries to the API'''
    
    def __init__(self):
        super().__init__()
        
    
    def getMe(self):
        url = self.api_url + "getMe"
        return self.request.get(url)
    
    
    def getUpdates(self, params):
        url = self.api_url + "getUpdates"
        return self.request.get(url, params)
    
    def sendMessage(self, params):
        url = self.api_url + "sendMessage"
        return self.request.post(url, params)
    
    def editMessageText(self, text, chat_id=None, message_id=None, inline_message_id=None, parse_mode="HTML", entities=None, disable_web_page_preview=None, reply_markup=None):
        url = self.api_url + "editMessageText"
        params = {"text":text}
        
        if chat_id:
            params["chat_id"] = chat_id
        
        if message_id:
            params["message_id"] = message_id
        
        if inline_message_id:
            params["inline_message_id"] = inline_message_id
            
        params["parse_mode"] = parse_mode
            
        if entities:
            params["entities"] = entities
            
        if disable_web_page_preview:
            params["disable_web_page_preview"] = disable_web_page_preview
            
        if reply_markup:
            params["reply_markup"] = reply_markup
        
        
        return self.request.post(url, params)

    
    def answerInlineQuery(self, query_id, query_list):
        url = self.api_url + "answerInlineQuery"
        params = {"inline_query_id" : query_id,
                  "results": query_list}
        return self.request.post(url, params)
    
    def getChatMemeber(self, chat_id, user_id):
        url = self.api_url + "getChatMember"
        params = {"chat_id" : chat_id,
                  "user_id": user_id}
        return self.request.get(url, params)        

    def banChatMemeber(self, chat_id, user_id, until_date=None, revoke_messages=None):
        url = self.api_url + "banChatMember"
        params = {"chat_id" : chat_id,
                  "user_id": user_id
            }
        
        if until_date:
            params["until_date"] = until_date  
            
        
        if revoke_messages:
            params["revoke_messages"] = revoke_messages
        
        
        return self.request.post(url, params)
    
    def unbanChatMember(self, chat_id, user_id, only_if_banned=None):
        url = self.api_url + "unbanChatMember"
        params = {"chat_id" : chat_id,
                  "user_id": user_id
            }
        
        if only_if_banned:
            params["only_if_banned"] = only_if_banned
            
        return self.request.post(url, params)
    
    def getChatMember(self, chat_id, user_id):
        url = self.api_url + "getChatMember"
        params = {"chat_id" : chat_id,
                  "user_id": user_id
            }
    
        return self.request.get(url, params)  

    def answerCallbackQuery(self, callback_query_id, text=None, show_alert=None, url=None):
        api_url = self.api_url + "answerCallbackQuery"
        
        
        params = {"callback_query_id" : callback_query_id
            }
        
        if text:
            params["text"] = text
        
        if show_alert:
            params["show_alert"] = show_alert
            
        if url:
            params["url"] = url
    
        return self.request.post(api_url, params)          
        


# these are instanciated here to make sure requests is instanciated once
# yet they could be wrapped in a class and be class variables
tg_requests = TelegramRequests()
tg_get_file = GetFile()
tg_send_file = SendFile()
