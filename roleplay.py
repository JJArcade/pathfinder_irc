import sys, os
import sqlite3
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import datetime

class roleplay:
    def __init__(self):
        dbPath = os.path.abspath("rp.db")
        self.conn = sqlite3.connect(dbPath)
        self.curr = self.conn.cursor()
        self.getCharacters()

    def getCharacters(self):
        self.curr.execute("SELECT * FROM char_main")
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
        locs = {"char_name": [(250,200),48],"alignment": [(812,200),20], \
            "gender": [(770,230),20]}
        #get the character from the list
        selection = {}
        for a in self.chars:
            if a["char_name"]==character:
                selection = a
        #open blank character sheet
        sheetsFolder = Path("files/sheets")
        genFolder = Path("files/generated sheets")
        fontsPath = Path("files/Fonts/typw.ttf")
        print(fontsPath)
        sheet1Path = sheetsFolder / "Character Sheet_Page_1.jpg"
        sheet2Path = sheetsFolder / "Character Sheet_Page_2.jpg"
        sheet1 = Image.open(sheet1Path)
        #sheet2 = Image.open(sheet2Path)
        timeStamp = datetime.date.today().strftime("%d%b %H%M")
        d1 = ImageDraw.Draw(sheet1)
        for a in locs:
            col = (255,0,0)
            fnt = ImageFont.truetype(str(fontsPath), size=locs[a][1])
            d1.text(locs[a][0],selection[a],font=fnt,fill=col)
        genSheet1Path = genFolder / str(timeStamp+"-"+selection["char_name"]+"-sheet1.jpg")
        sheet1.save(genSheet1Path)

#test
x = roleplay()
x.makeCharacterSheet("Justin Case")
