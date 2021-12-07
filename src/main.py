import db
import recipe
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-l",
        "--linksonly",
        help="Only pull links of all available recipes.",
        action="store_true"
    )
    group.add_argument(
        "-r",
        "--recipesonly",
        help="Only pull recipes of all saved links.",
        action="store_true"
    )
    return parser.parse_args()

def main():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    
    args = parse_args()
    db.createDB()
    recipe.main(args)


if __name__ == '__main__':
    main()