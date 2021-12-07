import sqlite3

def createDB():
    con = sqlite3.connect('link.db') 
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