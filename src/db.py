import sqlite3
import os

def createDB():
    if not os.path.exists('../RecipeDB'):
        os.mkdir('../RecipeDB')

    if not os.path.exists('../RecipeDB/recipe.db'):
        con = sqlite3.connect('../RecipeDB/recipe.db') 
        cur = con.cursor()
                
        cur.execute('''CREATE TABLE "recipe" (
                    "baseLevel"	INTEGER,
                    "difficulty"	INTEGER,
                    "durability"	INTEGER,
                    "level"	INTEGER,
                    "maxQuality"	INTEGER,
                    "name"	TEXT,
                    "suggestedCraftsmanship"	INTEGER,
                    "suggestedControl"	INTEGER,
                    "job"	TEXT,
                    "stars"	INTEGER,
                    "progressDivider"	INTEGER,
                    "progressModifier"	INTEGER,
                    "qualityDivider"	INTEGER,
                    "qualityModifier"	INTEGER,
                    PRIMARY KEY("job", "name"),
                    UNIQUE("job", "name")
                    );''')
                            
        con.commit()
        con.close()