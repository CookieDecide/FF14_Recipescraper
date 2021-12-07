import db
import recipe

def main():
    db.createDB()
    recipe.main()


if __name__ == '__main__':
    main()