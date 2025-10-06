from france_ioi.Account import *

def main():
    phpSessId: str = input("Please enter your PHPSESSID token: ") # TODO: Use argparse to get this from command line arguments instead of input()
    account = Account(phpSessId)
    if not account.hasSuccessfullyInitialized:
        print("Authentication failed!")
        exit(1)

    print(f"Logged in user @{account.username}!")
    print(f"Enumerating all chapters and their tasks...")

    levels = account.queryLevels()
    if levels is None:
        print("Failed to query levels!")
        exit(1)

    for level in levels:
        print(f"- {level.title} (Locked: {level.locked})")
        for chapter in level.chapters:
            print(f"\t- {chapter.title} ({chapter.link})")
            for task in chapter.tasks:
                print(f"\t\t- [{'X' if task.isFinished else ' '}] {task.title} ({task.link})")

if __name__ == "__main__":
    main()
