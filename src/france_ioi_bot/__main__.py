import os
from urllib.parse import quote
import requests
import argparse
from france_ioi.Account import *

def main():
    parser = argparse.ArgumentParser(
        prog='france-ioi-bot',
        description='A bot that tries to complete all challenges on the France-IOI platform.',
        epilog='')

    parser.add_argument("-t", "--token", help="The required PHPSESSID token", required=True)
    args = parser.parse_args()

    account = Account(args.token)
    if not account.hasSuccessfullyInitialized:
        print("Authentication failed!")
        exit(1)

    print(f"Logged in user @{account.username}!")
    print("Enumerating all chapters and their tasks...")

    levels = account.queryLevels()
    if levels is None:
        print("Failed to query levels!")
        exit(1)

    for level in levels:
        print(f"- {level.title} (Locked: {level.locked})")
        for chapter in level.chapters:
            print(f"\t- {chapter.title} ({chapter.link})")
            for task in chapter.tasks:
                print(f"\t\t- [{'X' if task.isFinished else ' '} - {'SVE' if os.path.exists(f'{level.title}/{chapter.title}/{task.title}') else 'NSV'}] {task.title} ({task.category})")

if __name__ == "__main__":
    main()
