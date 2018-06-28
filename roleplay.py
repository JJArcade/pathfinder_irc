import sys, os, re, sqlite3, textwrap
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from datetime import datetime
#import sopel.module

class roleplay:
    def __init__(self):
        dbPath = os.path.abspath("rp.db")
        self.conn = sqlite3.connect(dbPath)
        self.curr = self.conn.cursor()
        self.getCharacters()

    def getCharacters(self):
        #MAIN DATA
        self.curr.execute("SELECT * FROM char_main INNER JOIN abilities ON \
            abilities.char_id = char_main.char_id")
        self.chars = []
        data = self.curr.fetchall()
        headers = list(map(lambda x: x[0], self.curr.description))
        #store database data into a dictionary to be added to a list
        #of all characters in database
        for a in data:
            hold = {}
            for b in range(0,len(a)):
                hold[headers[b]] = a[b]
            self.chars.append(hold)

    def makeCharacterSheet(self, character):
        #location tuples
        locs = {"char_name": [(250,200),48],"alignment": [(822,192),14], \
            "gender": [(770,230),20],"level": [(), 10],"race": [(1234,137),48]\
            ,"class": [(1302,199),48],"xp": [(1550,196),20],"level": [(1555,231),20]}
        #add ability locations
        abilNames = ["strength","dexterity","constitution","intelligence","wisdom","charisma"]
        startX = 495
        startY = 357
        yDelta = 40
        xDelta = 100
        for a in abilNames:
            newSet = [(startX, startY), 24]
            locs[a] = newSet
            startY+=yDelta
        #get the character from the list
        selection = {}
        for a in self.chars:
            if a["char_name"]==character:
                selection = a
        #open blank character sheet
        sheetsFolder = Path("files/sheets")
        genFolder = Path("files/generated sheets")
        fontsPath = Path("files/Fonts/typw.ttf")
        sheet1Path = sheetsFolder / "Character Sheet_Page_1.jpg"
        sheet2Path = sheetsFolder / "Character Sheet_Page_2.jpg"
        sheet1 = Image.open(sheet1Path)
        #sheet2 = Image.open(sheet2Path)
        timeStamp = datetime.strftime(datetime.now(), "%d%b %H%M")
        d1 = ImageDraw.Draw(sheet1)
        for a in locs:
            col = (255,0,0)
            fnt = ImageFont.truetype(str(fontsPath), size=locs[a][1])
            inText = str(selection[a])
            if a == "alignment":
                offset = 0
                for line in inText.split():
                    d1.text((locs[a][0][0],locs[a][0][1]+offset), line, font=fnt, fill=col)
                    offset+=locs[a][1]
            else:
                d1.text(locs[a][0], inText, font=fnt, fill=col)
        genSheet1Path = genFolder / str(timeStamp+"-"+selection["char_name"]+"-sheet1.jpg")
        sheet1.save(genSheet1Path)

    def printCharInfo(self, character):
        #find char
        char = ""
        found = False
        for a in self.chars:
            found = bool(re.search(character,a["char_name"],re.IGNORECASE))
            if found:
                char = a
        if not found:
            return "No character found."
        #format
        outText = ""
        for a in char:
            if a != "char_id":
                outText+=a
                outText+=": "+str(char[a])
                outText+="\n"
        return outText

#test
#x = roleplay()
#x.makeCharacterSheet("Justin Case")
