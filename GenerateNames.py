from PIL import Image, ImageDraw, ImageSequence, ImageFont
from collections import defaultdict
import random
import copy
from os import  path
from io import BytesIO


class Generate():
    def __init__(self, names_dict):
        self.name_dict = names_dict
        self.final_dict = defaultdict(list)
        Generate.generateGroups(self)
        
    def generateGroups(self):
        while True:
            try:
                matches = Generate.random(self, [names for names in self.name_dict.keys()])
                break
            except:
                continue
        for name, info in self.name_dict.items():
            for orname, matched in matches:
                if matched == name:
                    gif_file = Generate.generateGifs(self, info[0], name)
                    self.final_dict[orname].append(name)
                    self.final_dict[orname].append(gif_file)
                    self.final_dict[orname].append(info[1])
            
            
    def generateGifs(self, url, name):
                                   
        im = Image.open('Gifs\\original.gif')
        
        pfp = Image.open(BytesIO(url)).resize((64,64))
            
        frames = [f.copy() for f in ImageSequence.Iterator(im)]
            
        for i, frame in enumerate(frames):
            frame = frame.convert("RGBA")
            d = ImageDraw.Draw(frame)
            d.text((120,190), "You received:", font=ImageFont.truetype('font\\MinecraftTen-VGORe.ttf', 40), fill='black')
            d.text((120,230), "%s"%(str(name).strip('#0123456789')), font=ImageFont.truetype('font\\MinecraftTen-VGORe.ttf', 40), fill='gray')
            del d
            frame.paste(pfp, (220, 275))
            frames[i] = frame
    
        frames[0].save('Gifs\\%s.gif'%(str(name).strip('#0123456789')), save_all=True, append_images=frames[1:])
        return 'Gifs\\%s.gif'%(str(name).strip('#0123456789'))
            
            
    def random(self, my_list):
        file_data = open('SantaInfo.txt', 'a')
        file_data.write('=============NewList=============\n')
        choose = copy.copy(my_list)
        result = []
        for i in my_list:
            names = copy.copy(my_list)
            names.pop(names.index(i))
            chosen = random.choice(list(set(choose)&set(names)))
            result.append((i,chosen))
            choose.pop(choose.index(chosen))
            
        for name, matched in result:
            file_data.write(str(name) + ' ' + str(matched) + '\n')
        
        file_data.close()
        return result
    
    def __iter__(self):
        for name, items in self.final_dict.items():
            matched, url, message = items
            yield name, matched, url, message
            
