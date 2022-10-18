# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 11:00:56 2022

@author: maurop
"""

from PIL import Image, ImageFont, ImageDraw, ImageOps
import copy

def normalize(iterable):
    max_i = max(iterable)
    min_i = min(iterable)
    
    if (max_i - min_i) == 0:
        return [0 for value in iterable]
    else: 
        return [(value - min_i) / (max_i - min_i) for value in iterable]


class CharacterRanges:
    
    ''' This classes manages different unicode characters.
    Stores the code points of some of the important tables as start and end
    indexes.
    '''
    
    def __init__(self):
        
        # unicode tables
        self.char_sets = {}
        self.char_sets["ascii_chars"] = (32, 126)
        self.char_sets["latin_1"] = (0xC0, 0x24F)
        self.char_sets["cyrillic"] = (0x400, 0x4FF)
        self.char_sets["general_punctuation"] = (0x2030, 0x205E)
        self.char_sets["arrows"] = (0x2030, 0x205E)
        self.char_sets["mathematical_operators"] = (0x2200, 0x22FF)
        self.char_sets["box_drawing"] = (0x2500, 0x257F)
        self.char_sets["block_elements"] = (0x2591, 0x259F)
        self.char_sets["geometric_shapes"] = (0x25A0, 0x25FF)
        
        # put characters all in a list that can be accessed through self.idx
        self.chars = []
        self.idx = {}
        chars_idx = 0
        for k in self.char_sets.keys():
            start = self.char_sets[k][0]
            end = self.char_sets[k][1]
            
            idx_start = chars_idx
            for i in range(start, end):
                self.chars.append(chr(i))
                chars_idx += 1
            
            idx_end = chars_idx
            
            self.idx[k] = (idx_start, idx_end)



class CharColor:
    
    ''' this class calculates the "luminance" of a caracter and sets them in 
    an array, so that they can be retrived by comparing them to a pixel'''
    
    char_signs = CharacterRanges()
    
    def __init__(self):
        
        # load the a monospace font
        font = ImageFont.truetype("consola.ttf", 32)
   
        characters = []
        values = []
        
        image_size = (32, 32)        
        
        # for each character calcuale the similitude
        for char in self.char_signs.chars:
            
            # draw the character on a small picture
            img = Image.new("RGB",image_size, color=(255, 255, 255))
            imdraw = ImageDraw.Draw(img)
            imdraw.text((0,0), char, font=font, fill=(0, 0, 0))
            
            # calculate how many white pixels has
            white_px = 0
            for i in list(img.getdata()):
                if i == (255, 255, 255):
                    white_px += 1
                    

            characters.append(char)
            values.append(white_px / image_size[0]**2)
            
        # normalize values from 0 to 1
        norm_values = normalize(values)
        
        # save them in this structure
        self.char_color = list(zip(norm_values, characters))   
        
    
    def get_ascii(self):
        # get the character corresponding to the ascii table
        idx_start, idx_end = self.char_signs.idx["ascii_chars"]
        return self.char_color[idx_start : idx_end]
    
    def remove_char(self, char_list, char):
        for i, vchar in enumerate(char_list):
            v, ichar = vchar
            if ichar == char:
                del char_list[i]
                return
        
    def get_telegram(self):
        
        char_color = copy.deepcopy(self.get_ascii())
        
        # remove characters that cause problems with telegram parsing
        self.remove_char(char_color, "<")
        self.remove_char(char_color, ">")
        #self.remove_char(char_color, "`")
        return char_color
    
    def get_char(self, color_value):
        
        char_color = self.get_telegram()
        
        min_v = abs(color_value - char_color[0][0])
        char_v  = char_color[0][1]
        
        # find the character that is most similar to the color
        for value, char in char_color[1:]:
            test_v = abs(color_value - value)            
            if test_v < min_v:
                min_v = test_v
                char_v = char
        
        return char_v      

# =============================================================================
# Asciify class
# =============================================================================
    
class Asciify:
    
    ''' This class takes a picture file name and transform said picture into 
    ascii art'''
    
    char_color = CharColor() 
    
    
    def __init__(self, file_name, size):
        self.size = size
        
        # load the image
        img = Image.open(file_name)

        # covert to gray scale
        grey_img = ImageOps.grayscale(img)

        #rescale image
        resized_img = grey_img.resize(self.size)

        # pixels table
        raw_pixels = resized_img.getdata() 
        
        self.pixels = normalize(raw_pixels)

    
    
    def asciify(self):
        
        text = ""
        for i in range(self.size[1]):
            for j in range(self.size[0]):
                # get the pixel
                idx = i*self.size[0] + j
                px_value = self.pixels[idx]
                
                # find the character
                closest_char = self.char_color.get_char(px_value)
                
                # add the character to the text
                text += closest_char
                
            text += "\n"
        return text   
    
    
if __name__ == "__main__":
    asciify = Asciify("../test_image.jpg", (25,17))
    print(asciify.asciify())