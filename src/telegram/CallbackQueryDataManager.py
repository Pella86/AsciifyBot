# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 12:42:07 2022

@author: maurop
"""

# =============================================================================
# Key Manager
# =============================================================================

import struct


class CallbackQueryManagerError(Exception):
    pass


class KeyManager:
    
    def __init__(self):
        ''' This class keeps track of the callback queries data in dictionaries
        so they can be encoded and decoded'''
        
        # this is the "type" manager, remembers the key and the type of the key
        self.fmt_manager = {}
        
        # this converts a key to an integer depending on the counter
        self.key_shortener = {}
        self.key_expander = {}
        self.key_shortener_counter = 0
        
        # this converts a string type to an integer
        self.str_shortener = {}
        self.str_expander = {}
        self.str_shortener_counter = 0     
    
    def add_key(self, key):
        if key not in self.key_shortener:
            self.key_shortener[key] = self.key_shortener_counter
            self.key_expander[self.key_shortener_counter] = key
            self.key_shortener_counter += 1
            
            # since the keys are encoded as single unsigned bytes if they are 
            # above 255 the idx will repeat
            if self.key_shortener_counter > 255:
                raise CallbackQueryManagerError("Too many keys, counter above 255")
    
    def add_str(self, value):
        if value not in self.str_shortener:
            self.str_shortener[value] = self.str_shortener_counter
            self.str_expander[self.str_shortener_counter] = value
            self.str_shortener_counter += 1        

            # since the str values are encoded as single unsigned bytes if they  
            # are above 255 the idx will repeat            
            if self.str_shortener_counter > 255:
                raise CallbackQueryManagerError("Too many str values, counter above 255")

# =============================================================================
# CallbackQueryDataManager
# =============================================================================

class CallbackQueryDataManager:
    
    sep = "|"
    key_sep = ":"
    
    key_manager = KeyManager()
    
    # these structures manage the byte packing
    skey_struct = struct.Struct("B")
    sstr_struct = struct.Struct("B")
    sint_struct = struct.Struct("q") # int are 64-bit integers
    
    def __init__(self):
        ''' This class manages a callbackquery data, converts strings to
        integers so that they will use up less bytes, 
        todo: use bytes instead of strings
        
        example:
        # bot:anti_lurking|command:kick_user|user_id:1235678|group_id:123423
        # 0:0|1:2|3:1235678|4:123423
        '''
        
        
        self.data = {}

    
    def __getitem__(self, key):
        return self.data[key]
    
    def get(self, key):
        ''' returns None if the key is not there'''
        return self.data.get(key)
    
    def add_value(self, key, value, fmt):
        ''' Thi function adds a keyword + value to the callback data'''
        
        # add the key
        self.key_manager.add_key(key)
        
        # add the data, if is a string check in the key manager
        if fmt == "str":
            self.key_manager.add_str(value)
            
        self.data[key] = value
        
        # store the format information
        self.key_manager.fmt_manager[key] = fmt
        
    
    def encode(self):
        ''' This function encodes the self.data dictionary in a callback_data
        string'''
        
        # creates the callback in a byte like object
        callback_data = bytearray()
        
        for key, value in self.data.items():

            # shortens the key
            skey = self.key_manager.key_shortener[key]
            skey_byte = self.skey_struct.pack(skey)
            callback_data.extend(skey_byte)
            
            # shortens the value
            if self.key_manager.fmt_manager[key] == "str":
                # first convert the string in the integer from the database
                # of the key manager
                short_value = self.key_manager.str_shortener[value]
                
                # pack the int in a bytelike format
                str_bytes = self.sstr_struct.pack(short_value)
                
                # add it to the callback_data
                callback_data.extend(str_bytes)
            
            elif self.key_manager.fmt_manager[key] == "int":
                # packs the integer in a 64-bit unsigned integer
                int_bytes = self.sint_struct.pack(value)
                callback_data.extend(int_bytes)
       
            else:
                 raise CallbackQueryManagerError(f"Error: CallbackQueryDataManager encode: the format for the key {key} is not present")
            
        # decode the bytes in a raw string (dont print it, it contains special
        # characters)
        decoded_data = "".join(map(chr, callback_data))

        if len(decoded_data) > 64:
            print(self.data)
            print(callback_data)
            print("decoded_data len", len(decoded_data))
            raise CallbackQueryManagerError("Error: CallbackQueryDataManager: callback_data too long")
            
        return decoded_data
        

    
    def decode(self, callback_data):
        ''' This function decodes the incoming callback_data string'''
        
        # convert the string in an array of integers
        callback_data = list(map(ord, callback_data))
        
        # transform the array of integers in a byte array
        callback_data = bytearray(callback_data)
        
        byte_idx = 0

        while byte_idx < len(callback_data):
            
            
            # read the key
            skey = callback_data[byte_idx]
            byte_idx += 1

            # expand the key to access the database
            key = self.key_manager.key_expander[skey]
            
            # the database knows which format the value is stored in
            if self.key_manager.fmt_manager[key] == "str":
                
                # for strings the value is just a single byte
                value = callback_data[byte_idx]
                byte_idx += 1

                self.data[key] = self.key_manager.str_expander[value]
            
            elif self.key_manager.fmt_manager[key] == "int":
                
                # for integers is a 64-bit integer (8 bytes)
                ivalue_byte = callback_data[byte_idx : byte_idx + 8]
                byte_idx += 8
                
                value = self.sint_struct.unpack(ivalue_byte)[0]
                
                self.data[key] = int(value)
            else:
                raise CallbackQueryManagerError(f"Error: CallbackQueryDataManager decode: the format for the key {key} is not present")                
            

    def __str__(self):
        s = ""
        for key, value in self.data.items():
            s += key + self.key_sep + str(value) + self.sep
        s = s[:-1]
        return s