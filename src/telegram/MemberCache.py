# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 21:17:01 2022

@author: maurop
"""

# =============================================================================
# Imports
# =============================================================================

import datetime
import threading

import src.telegram.TelegramObjects as tg_obj
from src.telegram.Requests import tg_requests

# =============================================================================
# Chat Member List
# =============================================================================


class ChatMemberList:
    
    def __init__(self, user_list):
        self.members_status = {}
        self.update_time = datetime.timedelta(minutes=5)
       
        t = threading.Thread(target=lambda user_list: self.initialize_status(user_list), args=[user_list])
        t.start()
    
    def initialize_status(self, user_list):
        
        key_list = []
        for user in user_list:
            key = (user.group_id, user.user.id)
            key_list.append(key)
        
        for key in key_list:
            status = self.get_status_api(key[0], key[1])
            date = datetime.datetime.now()
            self.members_status[key] = MemberStatus(status, date)
        
    
    def update_users(self, key_list):

        for key in key_list:
            
            status = self.get_status_api(key[0], key[1])
            date = datetime.datetime.now()
            
            self.members_status[key] = MemberStatus(status, date)
        
    
    def get_list(self, user_list):
        
        update_users = []
        # key (group_id, user_id) value: True/False
        status_dict = {}
        
        for user in user_list:
            key = (user.group_id, user.user.id)
            
            if key in self.members_status:
                status_dict[key] = self.members_status[key].status
                
                if datetime.datetime.now() - self.members_status[key].date > self.update_time:
                    update_users.append(key)
                
            else:
                # assign a default value
                status_dict[key] = self.default_value()
                update_users.append(key)
                
        
        target = lambda key_list : self.update_users(key_list)
        args = tuple([update_users])
        
        thread = threading.Thread(target=target, args=args)
        thread.start()
        
        return status_dict
    

class IsGroupMemberList(ChatMemberList):
    
    def __init__(self, user_list):
        super().__init__(user_list)
        
    
    def get_status_api(self, group_id, user_id):
        chat_member_res = tg_requests.getChatMemeber(group_id, user_id)
        
        if chat_member_res:
            chat_member = tg_obj.ChatMember(chat_member_res.json()["result"])
            
            
            if chat_member.status == "left" or chat_member.status == "kicked":
                left = False
            else:
                left = True
    
            return left
        else:
            return False       
        
    def default_value(self):
        return False
        
        

        

# =============================================================================
# Chat Member Base
# =============================================================================

class MemberStatus:
    ''' Class that stores the status and the date '''
    
    def __init__(self, status, date):
        self.status = status
        self.date = date

class ChatMemberCache:
    ''' Class that will store for x minutes the results of the chat member
    so that not so many requests are sent'''
    
    def __init__(self):
        # stores the information of the status and of the member / group
        # self.member_status[(group_id, user_id)] = MemberStatus()
        self.member_status = {}
        self.update_time = datetime.timedelta(minutes=5)

    def update_member_status(self, group_id, user_id):
        ''' This function updates the member status by calling the API
        self.get_status_api is defined in the derived classes'''
    
        status =  self.get_status_api(group_id, user_id)
        date = datetime.datetime.today()
        member_status = MemberStatus(status, date)
        
        self.member_status[(group_id, user_id)] = member_status     
        
    def __getitem__(self, group_user_id):
        ''' This getter will check if the group/user pair is already present
        and if is recent enough
        self.get_status_api is a virtual function that will be present in the
        derivate classes'''
        
        group_id, user_id = group_user_id
        

        # if the status is already present in the cache
        if (group_id, user_id) in self.member_status:
            mstatus = self.member_status[(group_id, user_id)]
            
            diff = datetime.datetime.today() - mstatus.date
            
            # check if the request is too old
            if diff < self.update_time:
                return mstatus.status
            
            else:
                # start a thread for the update
                target = lambda gid, uid : self.update_member_status(gid, uid)
                args = (group_id, user_id)
                
                t = threading.Thread(target=target, args=args)
                t.start()
                
                return mstatus.status
        else:
            # add member to the cache
            status =  self.get_status_api(group_id, user_id)
            date = datetime.datetime.today()
            member_status = MemberStatus(status, date)
            
            self.member_status[(group_id, user_id)] = member_status 
            return status   
        

# =============================================================================
# Is Group Member        
# =============================================================================
        
class IsGroupMember(ChatMemberCache):
    
    def __init__(self):
        super().__init__()
        
    
    def get_status_api(self, group_id, user_id):
        chat_member_res = tg_requests.getChatMemeber(group_id, user_id)
        
        if chat_member_res:
            chat_member = tg_obj.ChatMember(chat_member_res.json()["result"])
            
            
            if chat_member.status == "left" or chat_member.status == "kicked":
                left = False
            else:
                left = True
    
            return left
        else:
            return False

# =============================================================================
# Check if it has ban permissions
# =============================================================================
    
class CanBanMember(ChatMemberCache):
    
    def __init__(self):
        super().__init__()
        
    def get_status_api(self, group_id, user_id):
        chat_member_res = tg_requests.getChatMemeber(group_id, user_id)
        if chat_member_res:
            chat_member = tg_obj.ChatMember(chat_member_res.json()["result"])
        
            can_ban = False
            if chat_member.status == "creator":
                can_ban = True
                
            if chat_member.status == "administrator":
                if chat_member.can_restrict_members == True:
                    can_ban = True 
            return can_ban  
        else:
            return False
        