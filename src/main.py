import db
import recipe
import os

def main():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    
    db.createDB()
    recipe.main()


if __name__ == '__main__':
    main()