import requests
import json
import math
from joblib import Parallel, delayed
import time

import sqlite3

recipeListAlchemist = []
recipeListArmorer = []
recipeListBlacksmith = []
recipeListCarpenter = []
recipeListCulinarian = []
recipeListGoldsmith = []
recipeListLeatherworker = []
recipeListWeaver = []

def get(url):
    try:
        page = requests.get(url)
        if(page.status_code != 200):
            return get(url)
        return page
    except Exception:
        time.sleep(1)
        return get(url)

def getRecipe(pageNum):
    url = "https://xivapi.com/Recipe?page=" + str(pageNum) + "&columns=Name,ClassJob.NameEnglish,DurabilityFactor,QualityFactor,DifficultyFactor,RequiredControl,RequiredCraftsmanship,RecipeLevelTable"

    pageData = get(url).json()

    for recipe in pageData["Results"]:
        if(recipe["RecipeLevelTable"] == None or recipe["Name"] == None):
            continue
        job = recipe["ClassJob"]["NameEnglish"]
        baseLevel = recipe["RecipeLevelTable"]["ClassJobLevel"]
        difficulty = math.floor(recipe["RecipeLevelTable"]["Difficulty"] * recipe["DifficultyFactor"] / 100)
        durability = math.floor(recipe["RecipeLevelTable"]["Durability"] * recipe["DurabilityFactor"] / 100)
        maxQuality = math.floor(recipe["RecipeLevelTable"]["Quality"] * recipe["QualityFactor"] / 100)
        name = recipe["Name"]
        stars = recipe["RecipeLevelTable"]["Stars"]
        level = recipe["RecipeLevelTable"]["ID"]
        suggestedCraftsmanship = recipe["RecipeLevelTable"]["SuggestedCraftsmanship"]
        suggestedControl = recipe["RecipeLevelTable"]["SuggestedControl"]
        progressDivider = recipe["RecipeLevelTable"]["ProgressDivider"]
        progressModifier = recipe["RecipeLevelTable"]["ProgressModifier"]
        qualityDivider = recipe["RecipeLevelTable"]["QualityDivider"]
        qualityModifier = recipe["RecipeLevelTable"]["QualityModifier"]

        recipeDict = {
            "name": {"en": name},
            "job": job, 
            "baseLevel": baseLevel,
            "level": level,
            "difficulty": difficulty,
            "durability": durability,
            "maxQuality": maxQuality,
            "suggestedCraftsmanship": suggestedCraftsmanship,
            "suggestedControl": suggestedControl,
            "progressDivider": progressDivider,
            "progressModifier": progressModifier,
            "qualityDivider": qualityDivider,
            "qualityModifier": qualityModifier,
            "stars": stars}

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

        #print("Recipe:\t")
        #print(recipeDict)

def getPageNum():
    recipe_url = 'https://xivapi.com/Recipe'
    r = get(recipe_url)
    recipe_data = r.json()
    return recipe_data['Pagination']['PageTotal']

def main():
    pages = getPageNum()

    Parallel(n_jobs=24, require='sharedmem')(delayed(getRecipe)(i) for i in range(1, pages + 1))

    save()
    saveDB([recipeListAlchemist, recipeListArmorer, recipeListBlacksmith, recipeListCarpenter, recipeListCulinarian, recipeListGoldsmith, recipeListLeatherworker, recipeListWeaver])

def saveDB(lists):
    con = sqlite3.connect('../RecipeDB/recipe.db')
    cur = con.cursor()
    for list in lists:
        for recipe in list:
            cur.execute("REPLACE INTO recipe VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(recipe["baseLevel"],recipe["difficulty"],recipe["durability"],recipe["level"],recipe["maxQuality"],recipe["name"]["en"],recipe["suggestedCraftsmanship"],recipe["suggestedControl"],recipe["job"],recipe["stars"],recipe["progressDivider"],recipe["progressModifier"],recipe["qualityDivider"],recipe["qualityModifier"]))
    con.commit()
    con.close()

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