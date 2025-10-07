import os
from urllib.parse import quote
import argparse
from france_ioi.Account import Account
from france_ioi.Task import TaskCategory
from france_ioi.Solvers.CourseTaskSolver import solve_course_task
from france_ioi.Solvers.ValidationChallengeDiscoveryApplicationTaskSolver import solve_validation_challenge_discovery_application_task

def main():
    parser = argparse.ArgumentParser(
        prog='france-ioi-bot',
        description='A bot that tries to complete all tasks on the France-IOI platform.',
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
                answerExists = os.path.isfile(f'./answers/{level.title}/{chapter.title}/{task.title}.py')
                finishedState = 'FINISHED' if task.isFinished else 'NOT FINISHED'
                solvableState = 'SOLVABLE' if answerExists else 'UNSOLVABLE'
                print(f"\t\t- [{finishedState} - {solvableState}] {task.title} ({task.category})")
                if not task.isFinished:
                    if task.category == TaskCategory.COURSE:
                        print(f"\t\t:: Attempting to solve course task...")
                        print(f"\t\t:: > {'Success!' if solve_course_task(account, task) else 'Failed!'}")
                    elif task.category == TaskCategory.VALIDATION or task.category == TaskCategory.CHALLENGE or task.category == TaskCategory.DISCOVERY or task.category == TaskCategory.APPLICATION:
                        print(f"\t\t:: Attempting to solve validation/challenge/discovery/application task...")
                        print(f"\t\t:: > {'Success!' if solve_validation_challenge_discovery_application_task(account, task) else 'Failed!'}")
                    else:
                        print(f"\t\t:: ! Unknown task category {task.category}, cannot solve!")

if __name__ == "__main__":
    main()
