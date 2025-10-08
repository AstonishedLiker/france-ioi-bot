import time
import argparse
from france_ioi.Account import Account
from france_ioi.Task import Task, TaskCategory
from france_ioi.Solvers.CourseTaskSolver import solve_course_task
from france_ioi.Solvers.ProgramBasedTaskSolver import solve_program_based_task

def main():
    parser = argparse.ArgumentParser(
        prog='france-ioi-bot',
        description='A bot that tries to complete all the tasks on the France-IOI platform.',
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

    tasks = []
    solvedTasks = 0
    def handle_task(task: Task) -> bool:
        nonlocal solvedTasks # else we can't modify it in this nested function
        if task.category == TaskCategory.COURSE:
            success, answerAvailable = solve_course_task(account, task)
        else:
            success, answerAvailable = solve_program_based_task(account, task)
        if success:
            solvedTasks += 1
        return answerAvailable

    for level in levels:
        for chapter in level.chapters:
            for task in chapter.tasks:
                if not task.isFinished:
                    tasks.append(task)

    print(f" > Solving {len(tasks)} unfinished task(s)...")
    for task in tasks:
        if handle_task(task): # If answer was available (and sent)
            time.sleep(5)

    print(f":: Successfully solved {solvedTasks} task(s)!")

if __name__ == "__main__":
    main()
