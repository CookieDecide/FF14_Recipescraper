import sqlite3
import os

def createDB():
    if not os.path.exists('../RecipeDB'):
        os.mkdir('../RecipeDB')

    con = sqlite3.connect('../RecipeDB/link.db') 
    cur = con.cursor()

    cur.execute('''CREATE TABLE "links" (
                "link"	TEXT,
                PRIMARY KEY("link")
                );''')
            
    cur.execute('''CREATE TABLE "recipe" (
                "baseLevel"	INTEGER,
                "difficulty"	INTEGER,
                "durability"	INTEGER,
                "id"	TEXT,
                "level"	INTEGER,
                "maxQuality"	INTEGER,
                "name"	TEXT,
                "suggestedCraftsmanship"	INTEGER,
                "suggestedControl"	INTEGER,
                "job"	TEXT,
                "stars"	INTEGER,
                PRIMARY KEY("id")
                );''')
                        
    con.commit()
    con.close()