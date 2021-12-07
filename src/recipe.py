from bs4 import BeautifulSoup
import requests
import json
import unicodedata
from joblib import Parallel, delayed
import time

import sqlite3

# recipe level -> [ 0-star adjustment, 1-star adjustment, ... ]
LEVEL_DIFF = {
    # verified against app
    50: [ 0, 5, 20, 40, 60 ], # 50, 55, 70, 90, 110
    # unconfirmed from desynthesis results
    51: [ 69 ], # 120
    52: [ 73 ], # 125
    53: [ 77 ], # 130
    54: [ 79 ], # 133
    55: [ 81 ], # 136
    56: [ 83 ], # 139
    57: [ 85 ], # 142
    58: [ 87 ], # 145
    59: [ 89 ], # 148
    60: [ 90, 100, 120, 150, 190 ], # 150, 160, 180, 210, 250
    61: [ 199 ], # 260
    62: [ 203 ], # 265
    63: [ 207 ], # 270
    64: [ 209 ], # 273
    65: [ 211 ], # 276
    66: [ 213 ], # 279
    67: [ 215 ], # 282
    68: [ 217 ], # 285
    69: [ 219 ], # 288
    70: [ 220, 230, 250, 280, 310 ], # 290, 300, 320, 350, 380
    71: [ 319 ], # 390
    72: [ 323 ], # 395
    73: [ 327 ], # 400
    74: [ 329 ], # 403
    75: [ 331 ], # 406
    76: [ 333 ], # 409
    77: [ 335 ], # 412
    78: [ 337 ], # 415
    79: [ 339 ], # 418
    80: [ 350, 360, 370, 400, 430, 436 ], # 430, 440, 450, 480, 510, 516
    81: [ 436 ], # 517 # Yeah idfk how these numbers were acquired, are they even necessary?
    82: [ 438 ], # 520 # okay turns out they are kinda necessary
    83: [ 442 ], # 525 # find them by recipe itemlevel - level
    84: [ 446 ], # 530 # e.g.: 530 - 84 = 446
    85: [ 450 ], # 535 # thanks for wasting considerable amounts of my time by just not documenting shit properly :/
    86: [ 454 ], # 540
    87: [ 458 ], # 545
    88: [ 462 ], # 550
    89: [ 468 ], # 555
    90: [ 470, 480 ] # 560, 570
}

url = "https://na.finalfantasyxiv.com"
recipeListAlchemist = []
recipeListArmorer = []
recipeListBlacksmith = []
recipeListCarpenter = []
recipeListCulinarian = []
recipeListGoldsmith = []
recipeListLeatherworker = []
recipeListWeaver = []

def remove_control_characters(s):
    return ''.join(c for c in s if unicodedata.category(c)[0] != 'C')

def get(url):
    try:
        page = requests.get(url)
        if(page.status_code != 200):
            return get(url)
        return page
    except Exception:
        time.sleep(1)
        return get(url)

def getLinks(number):
    con = sqlite3.connect('../RecipeDB/link.db')
    cur = con.cursor()

    url = "https://na.finalfantasyxiv.com"
    page = get(url + "/lodestone/playguide/db/recipe?page="+str(number))
    soup = BeautifulSoup(page.content, 'html.parser')

    popups = soup.find_all(class_="db_popup db-table__txt--detail_link")

    for element in popups:
        cur.execute("REPLACE INTO links VALUES ('" + element.get('href') + "')")
    print("Page " + str(number))
    con.commit()
    con.close()

def getRecipe(row):
    con = sqlite3.connect('../RecipeDB/link.db')
    cur = con.cursor()

    page = get(url + row[0])
    soup = BeautifulSoup(page.content, 'html.parser')

    data = soup.find(class_="db-view__recipe__craftdata").find_all('li')

    job = soup.find(class_="db-view__item__text__job_name").get_text()
    baseLevel = int(soup.find(class_="db-view__item__text__level__num").get_text())
    difficulty = int(data[1].get_text().split()[1])
    durability = int(data[2].get_text().split()[1])
    id = row[0].split("/")[5]
    maxQuality = int(data[3].get_text().split()[2])
    name = remove_control_characters(soup.find(class_="db-view__item__text").find('h2').get_text())
    stars = int(len(soup.find_all(class_="ic_star--wh15")))
    level = 0
    suggestedCraftsmanship = 0
    suggestedControl = 0

    level_adjustment = 0
    if baseLevel in LEVEL_DIFF:
        try:
            level_adjustment = LEVEL_DIFF[baseLevel][stars]
        except IndexError:
            raise SystemExit

    level = baseLevel + level_adjustment

    conditions = soup.find(class_="db-view__recipe__crafting_conditions").find_all('dd')
    for element in conditions:
        element = element.get_text().split()
        if(element[0] == "Craftsmanship"):
            suggestedCraftsmanship = element[2]
        elif(element[0] == "Control"):
            suggestedControl = element[2]


    recipeDict = {"baseLevel": baseLevel,
        "difficulty": difficulty,
        "durability": durability,
        "id": id,
        "level": level,
        "maxQuality": maxQuality,
        "name": {"en": name},
        "stars": stars,
        "suggestedControl": suggestedControl,
        "suggestedCraftsmanship": suggestedCraftsmanship}

    if(job=="Alchemist"):
        recipeListAlchemist.append(recipeDict)
    elif(job=="Armorer"):
        recipeListArmorer.append(recipeDict)
    elif(job=="Blacksmith"):
        recipeListBlacksmith.append(recipeDict)
    elif(job=="Carpenter"):
        recipeListCarpenter.append(recipeDict)
    elif(job=="Culinarian"):
        recipeListCulinarian.append(recipeDict)
    elif(job=="Goldsmith"):
        recipeListGoldsmith.append(recipeDict)
    elif(job=="Leatherworker"):
        recipeListLeatherworker.append(recipeDict)
    elif(job=="Weaver"):
        recipeListWeaver.append(recipeDict)

    cur.execute("REPLACE INTO recipe VALUES (?,?,?,?,?,?,?,?,?,?,?)",(baseLevel,difficulty,durability,id,level,maxQuality,name,suggestedCraftsmanship,suggestedControl,job,stars))
    con.commit()
    con.close()

    print("Recipe:\t")
    print(recipeDict)

def getLinksfromDB():
    con = sqlite3.connect('../RecipeDB/link.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM links")
    return cur.fetchall()

def main(args):
    if(args.linksonly):
        Parallel(n_jobs=24)(delayed(getLinks)(i) for i in range(1,196))
        return 0
    elif(args.recipesonly):
        rows = getLinksfromDB()
        Parallel(n_jobs=24, require='sharedmem')(delayed(getRecipe)(row) for row in rows)
        return 0

    Parallel(n_jobs=24)(delayed(getLinks)(i) for i in range(1,196))
    rows = getLinksfromDB()
    Parallel(n_jobs=24, require='sharedmem')(delayed(getRecipe)(row) for row in rows)
    save()

def save():
    with open('../RecipeDB/Alchemist.json', 'w') as fout:
            fout.write(json.dumps(recipeListAlchemist, indent=4, sort_keys=True))

    with open('../RecipeDB/Armorer.json', 'w') as fout:
            fout.write(json.dumps(recipeListArmorer, indent=4, sort_keys=True))

    with open('../RecipeDB/Blacksmith.json', 'w') as fout:
            fout.write(json.dumps(recipeListBlacksmith, indent=4, sort_keys=True))

    with open('../RecipeDB/Carpenter.json', 'w') as fout:
            fout.write(json.dumps(recipeListCarpenter, indent=4, sort_keys=True))

    with open('../RecipeDB/Culinarian.json', 'w') as fout:
            fout.write(json.dumps(recipeListCulinarian, indent=4, sort_keys=True))

    with open('../RecipeDB/Goldsmith.json', 'w') as fout:
            fout.write(json.dumps(recipeListGoldsmith, indent=4, sort_keys=True))

    with open('../RecipeDB/Leatherworker.json', 'w') as fout:
            fout.write(json.dumps(recipeListLeatherworker, indent=4, sort_keys=True))

    with open('../RecipeDB/Weaver.json', 'w') as fout:
            fout.write(json.dumps(recipeListWeaver, indent=4, sort_keys=True))